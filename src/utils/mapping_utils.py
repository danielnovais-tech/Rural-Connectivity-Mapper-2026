"""Mapping utilities for interactive map generation."""

import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from .config_utils import get_map_center, get_zoom_level, get_default_country

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

logger = logging.getLogger(__name__)


def generate_map(
    data: List[Dict], 
    output_path: str = None,
    country_code: Optional[str] = None
) -> str:
    """Generate interactive Folium map from connectivity data.
    
    Args:
        data: List of connectivity point dictionaries
        output_path: Optional output file path for HTML map
        country_code: ISO country code for map center (default: uses default country)
        
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
        
        # Determine map center and zoom
        if country_code is None:
            country_code = get_default_country()
        
        if not data:
            logger.warning("No data provided for map generation")
            # Create empty map centered on specified country
            center = get_map_center(country_code)
            zoom = get_zoom_level(country_code)
            m = folium.Map(location=center, zoom_start=zoom)
            m.save(str(path))
            return str(path)
        
        # Calculate center of map from data points
        latitudes = [point.get('latitude', 0) for point in data]
        longitudes = [point.get('longitude', 0) for point in data]
        center_lat = sum(latitudes) / len(latitudes)
        center_lon = sum(longitudes) / len(longitudes)
        
        # Create base map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        
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
            ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 180px; height: 140px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p style="margin: 0; font-weight: bold;">Quality Rating</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:green"></i> Excellent (80+)</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:blue"></i> Good (60-79)</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:orange"></i> Fair (40-59)</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:red"></i> Poor (&lt;40)</p>
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
