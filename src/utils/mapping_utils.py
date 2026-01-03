"""Mapping utilities for interactive map generation."""

import logging
from typing import List, Dict
from pathlib import Path
from datetime import datetime

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

logger = logging.getLogger(__name__)


def get_starlink_coverage_zones():
    """Get Starlink coverage zones for Brazil.
    
    Returns simulated Starlink coverage data based on known deployment patterns.
    In production, this could be replaced with actual API calls to Starlink's
    availability service or public coverage maps.
    
    Returns:
        List of coverage zone dictionaries with coordinates and coverage quality
    """
    # Starlink coverage zones for Brazil (2026 expansion roadmap)
    # Based on major urban centers and rural expansion areas
    coverage_zones = [
        # High coverage - Major urban areas
        {
            'name': 'Southeast Region (SP/RJ)',
            'center': [-23.0, -46.0],
            'radius': 300000,  # 300km radius
            'coverage': 'excellent',
            'color': '#00FF00',
            'opacity': 0.15
        },
        {
            'name': 'Brasília & Central-West',
            'center': [-15.7801, -47.9292],
            'radius': 250000,
            'coverage': 'excellent',
            'color': '#00FF00',
            'opacity': 0.15
        },
        # Good coverage - Northeast coastal areas
        {
            'name': 'Salvador & Bahia Coast',
            'center': [-12.9714, -38.5014],
            'radius': 200000,
            'coverage': 'good',
            'color': '#90EE90',
            'opacity': 0.12
        },
        {
            'name': 'Fortaleza & Ceará',
            'center': [-3.7172, -38.5433],
            'radius': 200000,
            'coverage': 'good',
            'color': '#90EE90',
            'opacity': 0.12
        },
        {
            'name': 'Recife & Pernambuco',
            'center': [-8.0476, -34.8770],
            'radius': 180000,
            'coverage': 'good',
            'color': '#90EE90',
            'opacity': 0.12
        },
        # Moderate coverage - Rural expansion zones
        {
            'name': 'Amazon Region',
            'center': [-3.1190, -60.0217],
            'radius': 400000,
            'coverage': 'moderate',
            'color': '#FFFF00',
            'opacity': 0.10
        },
        {
            'name': 'South Region (PR/SC/RS)',
            'center': [-25.5, -50.0],
            'radius': 280000,
            'coverage': 'good',
            'color': '#90EE90',
            'opacity': 0.12
        },
        {
            'name': 'Mato Grosso Agricultural',
            'center': [-12.5, -55.5],
            'radius': 300000,
            'coverage': 'moderate',
            'color': '#FFFF00',
            'opacity': 0.10
        },
    ]
    
    return coverage_zones


def generate_map(data: List[Dict], output_path: str = None, include_starlink_coverage: bool = True) -> str:
    """Generate interactive Folium map from connectivity data.
    
    Args:
        data: List of connectivity point dictionaries
        output_path: Optional output file path for HTML map
        include_starlink_coverage: Whether to include Starlink coverage overlay layer (default: True)
        
    Returns:
        str: Path to generated HTML map file
        
    Raises:
        ImportError: If folium is not installed
    """
    if not FOLIUM_AVAILABLE:
        raise ImportError("folium is required for map generation. Install with: pip install folium")
    
    try:
        if output_path is None:
            output_path = f"connectivity_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if not data:
            logger.warning("No data provided for map generation")
            # Create empty map centered on Brazil
            m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
            
            # Add Starlink coverage layer even without data points
            if include_starlink_coverage:
                starlink_layer = folium.FeatureGroup(name='Starlink Coverage Zones', show=True)
                coverage_zones = get_starlink_coverage_zones()
                
                for zone in coverage_zones:
                    folium.Circle(
                        location=zone['center'],
                        radius=zone['radius'],
                        color=zone['color'],
                        fill=True,
                        fillColor=zone['color'],
                        fillOpacity=zone['opacity'],
                        opacity=0.3,
                        popup=folium.Popup(
                            f"<b>{zone['name']}</b><br>"
                            f"Coverage: {zone['coverage'].title()}<br>"
                            f"Radius: ~{zone['radius']//1000} km",
                            max_width=200
                        ),
                        tooltip=f"{zone['name']} - {zone['coverage'].title()} coverage"
                    ).add_to(starlink_layer)
                
                starlink_layer.add_to(m)
                folium.LayerControl(position='topright', collapsed=False).add_to(m)
            
            m.save(str(path))
            return str(path)
        
        # Calculate center of map from data points
        latitudes = [point.get('latitude', 0) for point in data]
        longitudes = [point.get('longitude', 0) for point in data]
        center_lat = sum(latitudes) / len(latitudes)
        center_lon = sum(longitudes) / len(longitudes)
        
        # Create base map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        
        # Add Starlink coverage layer (optional, toggleable)
        if include_starlink_coverage:
            # Create a feature group for Starlink coverage
            starlink_layer = folium.FeatureGroup(name='Starlink Coverage Zones', show=True)
            
            coverage_zones = get_starlink_coverage_zones()
            
            for zone in coverage_zones:
                # Add circle for coverage area
                folium.Circle(
                    location=zone['center'],
                    radius=zone['radius'],
                    color=zone['color'],
                    fill=True,
                    fillColor=zone['color'],
                    fillOpacity=zone['opacity'],
                    opacity=0.3,
                    popup=folium.Popup(
                        f"<b>{zone['name']}</b><br>"
                        f"Coverage: {zone['coverage'].title()}<br>"
                        f"Radius: ~{zone['radius']//1000} km",
                        max_width=200
                    ),
                    tooltip=f"{zone['name']} - {zone['coverage'].title()} coverage"
                ).add_to(starlink_layer)
            
            starlink_layer.add_to(m)
        
        # Create a feature group for connectivity points
        points_layer = folium.FeatureGroup(name='Connectivity Points', show=True)
        
        # Add markers for each connectivity point
        for point in data:
            lat = point.get('latitude')
            lon = point.get('longitude')
            
            if lat is None or lon is None:
                continue
            
            # Get quality score for color coding
            qs = point.get('quality_score', {})
            overall_score = qs.get('overall_score', 0)
            rating = qs.get('rating', 'Unknown')
            
            # Determine marker color based on quality score
            if overall_score >= 80:
                color = 'green'
            elif overall_score >= 60:
                color = 'blue'
            elif overall_score >= 40:
                color = 'orange'
            else:
                color = 'red'
            
            # Build popup content
            provider = point.get('provider', 'Unknown')
            st = point.get('speed_test', {})
            download = st.get('download', 'N/A')
            upload = st.get('upload', 'N/A')
            latency = st.get('latency', 'N/A')
            
            popup_html = f"""
            <div style="font-family: Arial; min-width: 200px;">
                <h4 style="margin: 0 0 10px 0; color: {color};">{provider}</h4>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td><b>Location:</b></td>
                        <td>{lat:.4f}, {lon:.4f}</td>
                    </tr>
                    <tr>
                        <td><b>Download:</b></td>
                        <td>{download} Mbps</td>
                    </tr>
                    <tr>
                        <td><b>Upload:</b></td>
                        <td>{upload} Mbps</td>
                    </tr>
                    <tr>
                        <td><b>Latency:</b></td>
                        <td>{latency} ms</td>
                    </tr>
                    <tr>
                        <td><b>Quality:</b></td>
                        <td>{overall_score:.1f}/100 ({rating})</td>
                    </tr>
                </table>
            </div>
            """
            
            # Add marker to map
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{provider} - {rating}",
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(points_layer)
        
        # Add points layer to map
        points_layer.add_to(m)
        
        # Add layer control to toggle layers on/off
        if include_starlink_coverage:
            folium.LayerControl(position='topright', collapsed=False).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: auto; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p style="margin: 0; font-weight: bold;">Quality Rating</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:green"></i> Excellent (80+)</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:blue"></i> Good (60-79)</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:orange"></i> Fair (40-59)</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:red"></i> Poor (&lt;40)</p>
        '''
        
        if include_starlink_coverage:
            legend_html += '''
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0 0 0; font-weight: bold;">Starlink Coverage</p>
        <p style="margin: 5px 0;"><span style="color:#00FF00">●</span> Excellent</p>
        <p style="margin: 5px 0;"><span style="color:#90EE90">●</span> Good</p>
        <p style="margin: 5px 0;"><span style="color:#FFFF00">●</span> Moderate</p>
            '''
        
        legend_html += '</div>'
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save map
        m.save(str(path))
        
        logger.info(f"Interactive map generated with {len(data)} points: {path}")
        return str(path)
    
    except Exception as e:
        logger.error(f"Error generating map: {e}")
        raise
