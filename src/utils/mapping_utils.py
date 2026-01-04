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

from .starlink_coverage_utils import (
    get_starlink_coverage_zones,
    get_starlink_signal_points,
    get_coverage_color,
    get_coverage_rating
)

logger = logging.getLogger(__name__)


def generate_map(data: List[Dict], output_path: str = None) -> str:
    """Generate interactive Folium map from connectivity data.
    
    Args:
        data: List of connectivity point dictionaries
        output_path: Optional output file path for HTML map
        
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
            m.save(str(path))
            return str(path)
        
        # Calculate center of map from data points
        latitudes = [point.get('latitude', 0) for point in data]
        longitudes = [point.get('longitude', 0) for point in data]
        center_lat = sum(latitudes) / len(latitudes)
        center_lon = sum(longitudes) / len(longitudes)
        
        # Create base map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        
        # Add Starlink coverage zones
        logger.info("Adding Starlink coverage zones to map...")
        coverage_zones = get_starlink_coverage_zones()
        coverage_group = folium.FeatureGroup(name='Starlink Coverage Zones', show=True)
        
        for zone in coverage_zones:
            folium.Polygon(
                locations=zone['coordinates'],
                popup=f"<b>{zone['name']}</b><br>{zone['description']}<br>Signal: {zone['signal_strength'].title()}",
                tooltip=f"{zone['name']} - {zone['signal_strength'].title()}",
                color=zone['color'],
                fill=True,
                fillColor=zone['color'],
                fillOpacity=zone['opacity'],
                weight=2
            ).add_to(coverage_group)
        
        coverage_group.add_to(m)
        
        # Add Starlink signal strength points
        signal_points = get_starlink_signal_points()
        signal_group = folium.FeatureGroup(name='Starlink Signal Points', show=False)
        
        for point in signal_points:
            signal_color = get_coverage_color(point['signal_strength'])
            signal_rating = get_coverage_rating(point['signal_strength'])
            
            signal_popup_html = f"""
            <div style="font-family: Arial; min-width: 180px;">
                <h4 style="margin: 0 0 10px 0; color: {signal_color};">Starlink Signal</h4>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td><b>Strength:</b></td>
                        <td>{point['signal_strength']}/100</td>
                    </tr>
                    <tr>
                        <td><b>Rating:</b></td>
                        <td>{signal_rating}</td>
                    </tr>
                    <tr>
                        <td><b>Type:</b></td>
                        <td>{point['coverage_type'].title()}</td>
                    </tr>
                </table>
            </div>
            """
            
            folium.CircleMarker(
                location=[point['latitude'], point['longitude']],
                radius=8,
                popup=folium.Popup(signal_popup_html, max_width=250),
                tooltip=f"Signal: {point['signal_strength']}/100 ({signal_rating})",
                color=signal_color,
                fillColor=signal_color,
                fillOpacity=0.6,
                weight=2
            ).add_to(signal_group)
        
        signal_group.add_to(m)
        
        # Add connectivity data markers group
        connectivity_group = folium.FeatureGroup(name='Speedtest Data Points', show=True)
        
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
            ).add_to(connectivity_group)
        
        connectivity_group.add_to(m)
        
        # Add layer control to toggle different layers
        folium.LayerControl(position='topright', collapsed=False).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 220px; height: auto; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:12px; padding: 10px">
        <p style="margin: 0 0 8px 0; font-weight: bold; font-size: 14px;">Map Legend</p>
        
        <p style="margin: 8px 0 4px 0; font-weight: bold;">Connectivity Quality</p>
        <p style="margin: 3px 0;"><i class="fa fa-circle" style="color:green"></i> Excellent (80+)</p>
        <p style="margin: 3px 0;"><i class="fa fa-circle" style="color:blue"></i> Good (60-79)</p>
        <p style="margin: 3px 0;"><i class="fa fa-circle" style="color:orange"></i> Fair (40-59)</p>
        <p style="margin: 3px 0;"><i class="fa fa-circle" style="color:red"></i> Poor (&lt;40)</p>
        
        <p style="margin: 8px 0 4px 0; font-weight: bold;">Starlink Coverage</p>
        <p style="margin: 3px 0;"><span style="color:#00ff00">█</span> Excellent Signal</p>
        <p style="margin: 3px 0;"><span style="color:#ffff00">█</span> Good Signal</p>
        <p style="margin: 3px 0;"><span style="color:#ffa500">█</span> Fair Signal</p>
        
        <p style="margin: 8px 0 0 0; font-size: 10px; font-style: italic;">
        Use layer control (top right) to toggle layers
        </p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save map
        m.save(str(path))
        
        logger.info(f"Interactive map generated with {len(data)} points: {path}")
        return str(path)
    
    except Exception as e:
        logger.error(f"Error generating map: {e}")
        raise
