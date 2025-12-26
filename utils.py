"""
Utility functions for Rural Connectivity Mapper 2026

This module provides utility functions for speed testing, geocoding, validation,
report generation, and data management.
"""

import json
import csv
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Any
import platform

try:
    import speedtest
except ImportError:
    speedtest = None

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
except ImportError:
    Nominatim = None

try:
    import pandas as pd
except ImportError:
    pd = None

from models import AccessPoint


# Constants
DATA_FILE = "data/pontos.json"
REPORTS_DIR = "data/relatorios"
BACKUP_DIR = "data/backups"


def measure_speed(debug: bool = False) -> Dict[str, float]:
    """
    Measure internet speed using speedtest-cli.
    
    Args:
        debug: Enable debug output
        
    Returns:
        dict: Dictionary with download, upload, latency, and stability metrics
        
    Raises:
        RuntimeError: If speedtest-cli is not available or test fails
    """
    if speedtest is None:
        raise RuntimeError("speedtest-cli library not installed. Install with: pip install speedtest-cli")
    
    try:
        if debug:
            print("Initializing speed test...")
        
        st = speedtest.Speedtest()
        
        if debug:
            print("Getting best server...")
        st.get_best_server()
        
        if debug:
            print("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        if debug:
            print("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Get latency from server results
        latency = st.results.ping
        
        # Estimate stability (simplified - in production, would need multiple tests)
        stability = 95.0  # Default high stability
        
        if debug:
            print(f"Download: {download_speed:.2f} Mbps")
            print(f"Upload: {upload_speed:.2f} Mbps")
            print(f"Latency: {latency:.2f} ms")
        
        return {
            "download": round(download_speed, 2),
            "upload": round(upload_speed, 2),
            "latency": round(latency, 2),
            "stability": stability
        }
    
    except Exception as e:
        raise RuntimeError(f"Speed test failed: {str(e)}")


def geocode_address(address: str, debug: bool = False) -> Optional[Dict[str, float]]:
    """
    Geocode an address to get latitude and longitude.
    
    Args:
        address: Address string to geocode
        debug: Enable debug output
        
    Returns:
        dict: Dictionary with 'lat' and 'lon' keys, or None if geocoding fails
    """
    if Nominatim is None:
        if debug:
            print("Warning: geopy library not installed. Cannot geocode address.")
        return None
    
    try:
        geolocator = Nominatim(user_agent="rural_connectivity_mapper_2026")
        
        if debug:
            print(f"Geocoding address: {address}")
        
        location = geolocator.geocode(address, timeout=10)
        
        if location:
            if debug:
                print(f"Found location: ({location.latitude}, {location.longitude})")
            return {
                "lat": location.latitude,
                "lon": location.longitude
            }
        else:
            if debug:
                print(f"Could not geocode address: {address}")
            return None
    
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        if debug:
            print(f"Geocoding error: {str(e)}")
        return None
    except Exception as e:
        if debug:
            print(f"Unexpected geocoding error: {str(e)}")
        return None


def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate latitude and longitude coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        bool: True if coordinates are valid
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180


def validate_access_point(ap: AccessPoint) -> List[str]:
    """
    Validate an AccessPoint object and return any errors.
    
    Args:
        ap: AccessPoint instance to validate
        
    Returns:
        list: List of validation error messages (empty if valid)
    """
    errors = []
    
    if not validate_coordinates(ap.lat, ap.lon):
        errors.append(f"Invalid coordinates: ({ap.lat}, {ap.lon})")
    
    if ap.download < 0:
        errors.append(f"Invalid download speed: {ap.download}")
    
    if ap.upload < 0:
        errors.append(f"Invalid upload speed: {ap.upload}")
    
    if ap.latency < 0:
        errors.append(f"Invalid latency: {ap.latency}")
    
    if not (0 <= ap.stability <= 100):
        errors.append(f"Invalid stability: {ap.stability} (must be 0-100)")
    
    return errors


def load_data(filepath: str = DATA_FILE, debug: bool = False) -> List[AccessPoint]:
    """
    Load access points from JSON file.
    
    Args:
        filepath: Path to JSON file
        debug: Enable debug output
        
    Returns:
        list: List of AccessPoint instances
    """
    if not os.path.exists(filepath):
        if debug:
            print(f"Data file not found: {filepath}. Starting with empty list.")
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        access_points = [AccessPoint.from_dict(item) for item in data]
        
        if debug:
            print(f"Loaded {len(access_points)} access points from {filepath}")
        
        return access_points
    
    except json.JSONDecodeError as e:
        if debug:
            print(f"Error parsing JSON file: {e}")
        return []
    except Exception as e:
        if debug:
            print(f"Error loading data: {e}")
        return []


def save_data(access_points: List[AccessPoint], filepath: str = DATA_FILE, debug: bool = False) -> bool:
    """
    Save access points to JSON file.
    
    Args:
        access_points: List of AccessPoint instances
        filepath: Path to JSON file
        debug: Enable debug output
        
    Returns:
        bool: True if successful
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        data = [ap.to_dict() for ap in access_points]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        if debug:
            print(f"Saved {len(access_points)} access points to {filepath}")
        
        return True
    
    except Exception as e:
        if debug:
            print(f"Error saving data: {e}")
        return False


def backup_data(filepath: str = DATA_FILE, debug: bool = False) -> Optional[str]:
    """
    Create a backup of the data file.
    
    Args:
        filepath: Path to file to backup
        debug: Enable debug output
        
    Returns:
        str: Path to backup file, or None if backup failed
    """
    if not os.path.exists(filepath):
        if debug:
            print(f"File not found: {filepath}. Nothing to backup.")
        return None
    
    try:
        # Create backup directory
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(filepath)
        backup_path = os.path.join(BACKUP_DIR, f"{filename}_{timestamp}.bak")
        
        # Copy file
        shutil.copy2(filepath, backup_path)
        
        if debug:
            print(f"Backup created: {backup_path}")
        
        return backup_path
    
    except Exception as e:
        if debug:
            print(f"Error creating backup: {e}")
        return None


def import_csv(filepath: str, debug: bool = False) -> List[AccessPoint]:
    """
    Import access points from CSV file.
    
    Expected CSV columns: lat, lon, provider, address, download, upload, latency, stability, tags
    
    Args:
        filepath: Path to CSV file
        debug: Enable debug output
        
    Returns:
        list: List of AccessPoint instances
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    
    access_points = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Parse tags if present
                    tags = []
                    if 'tags' in row and row['tags']:
                        tags = [tag.strip() for tag in row['tags'].split(',')]
                    
                    ap = AccessPoint(
                        lat=float(row.get('lat', 0)),
                        lon=float(row.get('lon', 0)),
                        provider=row.get('provider', 'Unknown'),
                        address=row.get('address', ''),
                        download=float(row.get('download', 0)),
                        upload=float(row.get('upload', 0)),
                        latency=float(row.get('latency', 0)),
                        stability=float(row.get('stability', 100)),
                        tags=tags
                    )
                    
                    # Validate
                    errors = validate_access_point(ap)
                    if errors:
                        if debug:
                            print(f"Validation errors for row: {errors}")
                    else:
                        access_points.append(ap)
                
                except (ValueError, KeyError) as e:
                    if debug:
                        print(f"Error parsing row: {e}")
        
        if debug:
            print(f"Imported {len(access_points)} access points from {filepath}")
        
        return access_points
    
    except Exception as e:
        raise RuntimeError(f"Error importing CSV: {e}")


def export_csv(access_points: List[AccessPoint], filepath: str, debug: bool = False) -> bool:
    """
    Export access points to CSV file.
    
    Args:
        access_points: List of AccessPoint instances
        filepath: Path to CSV file
        debug: Enable debug output
        
    Returns:
        bool: True if successful
    """
    try:
        # Ensure directory exists
        dirname = os.path.dirname(filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['lat', 'lon', 'provider', 'address', 'download', 'upload', 
                         'latency', 'stability', 'timestamp', 'tags', 'quality_score']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for ap in access_points:
                row = ap.to_dict()
                row['tags'] = ', '.join(row['tags']) if row['tags'] else ''
                writer.writerow(row)
        
        if debug:
            print(f"Exported {len(access_points)} access points to {filepath}")
        
        return True
    
    except Exception as e:
        if debug:
            print(f"Error exporting CSV: {e}")
        return False


def generate_report_txt(access_points: List[AccessPoint], filepath: str, debug: bool = False) -> bool:
    """
    Generate a text report of access points.
    
    Args:
        access_points: List of AccessPoint instances
        filepath: Path to output file
        debug: Enable debug output
        
    Returns:
        bool: True if successful
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RURAL CONNECTIVITY MAPPER 2026 - RELATÓRIO\n")
            f.write("=" * 80 + "\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de pontos: {len(access_points)}\n")
            f.write("=" * 80 + "\n\n")
            
            if not access_points:
                f.write("Nenhum ponto de acesso encontrado.\n")
            else:
                # Statistics
                avg_download = sum(ap.download for ap in access_points) / len(access_points)
                avg_upload = sum(ap.upload for ap in access_points) / len(access_points)
                avg_latency = sum(ap.latency for ap in access_points) / len(access_points)
                avg_quality = sum(ap.quality_score for ap in access_points) / len(access_points)
                
                f.write("ESTATÍSTICAS GERAIS\n")
                f.write("-" * 80 + "\n")
                f.write(f"Download médio: {avg_download:.2f} Mbps\n")
                f.write(f"Upload médio: {avg_upload:.2f} Mbps\n")
                f.write(f"Latência média: {avg_latency:.2f} ms\n")
                f.write(f"Quality Score médio: {avg_quality:.4f}\n")
                f.write("\n")
                
                # Provider breakdown
                providers = {}
                for ap in access_points:
                    providers[ap.provider] = providers.get(ap.provider, 0) + 1
                
                f.write("PROVEDORES\n")
                f.write("-" * 80 + "\n")
                for provider, count in sorted(providers.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{provider}: {count} pontos\n")
                f.write("\n")
                
                # Individual points
                f.write("PONTOS DE ACESSO\n")
                f.write("-" * 80 + "\n")
                for i, ap in enumerate(access_points, 1):
                    f.write(f"\n{i}. {ap.provider}\n")
                    f.write(f"   Localização: ({ap.lat}, {ap.lon})\n")
                    if ap.address:
                        f.write(f"   Endereço: {ap.address}\n")
                    f.write(f"   Download: {ap.download} Mbps | Upload: {ap.upload} Mbps\n")
                    f.write(f"   Latência: {ap.latency} ms | Estabilidade: {ap.stability}%\n")
                    f.write(f"   Quality Score: {ap.quality_score}\n")
                    if ap.tags:
                        f.write(f"   Tags: {', '.join(ap.tags)}\n")
                    f.write(f"   Timestamp: {ap.timestamp}\n")
        
        if debug:
            print(f"Text report generated: {filepath}")
        
        return True
    
    except Exception as e:
        if debug:
            print(f"Error generating text report: {e}")
        return False


def generate_report_json(access_points: List[AccessPoint], filepath: str, debug: bool = False) -> bool:
    """
    Generate a JSON report of access points.
    
    Args:
        access_points: List of AccessPoint instances
        filepath: Path to output file
        debug: Enable debug output
        
    Returns:
        bool: True if successful
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_points": len(access_points),
            "statistics": {},
            "access_points": [ap.to_dict() for ap in access_points]
        }
        
        if access_points:
            report["statistics"] = {
                "avg_download": round(sum(ap.download for ap in access_points) / len(access_points), 2),
                "avg_upload": round(sum(ap.upload for ap in access_points) / len(access_points), 2),
                "avg_latency": round(sum(ap.latency for ap in access_points) / len(access_points), 2),
                "avg_quality_score": round(sum(ap.quality_score for ap in access_points) / len(access_points), 4),
            }
            
            # Provider breakdown
            providers = {}
            for ap in access_points:
                providers[ap.provider] = providers.get(ap.provider, 0) + 1
            report["statistics"]["providers"] = providers
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        if debug:
            print(f"JSON report generated: {filepath}")
        
        return True
    
    except Exception as e:
        if debug:
            print(f"Error generating JSON report: {e}")
        return False


def generate_report_html(access_points: List[AccessPoint], filepath: str, debug: bool = False) -> bool:
    """
    Generate an HTML report of access points.
    
    Args:
        access_points: List of AccessPoint instances
        filepath: Path to output file
        debug: Enable debug output
        
    Returns:
        bool: True if successful
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rural Connectivity Mapper 2026 - Relatório</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .quality-high {
            color: green;
            font-weight: bold;
        }
        .quality-medium {
            color: orange;
            font-weight: bold;
        }
        .quality-low {
            color: red;
            font-weight: bold;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛰️ Rural Connectivity Mapper 2026</h1>
        <p><strong>Relatório gerado em:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p><strong>Total de pontos:</strong> """ + str(len(access_points)) + """</p>
"""
        
        if access_points:
            avg_download = sum(ap.download for ap in access_points) / len(access_points)
            avg_upload = sum(ap.upload for ap in access_points) / len(access_points)
            avg_latency = sum(ap.latency for ap in access_points) / len(access_points)
            avg_quality = sum(ap.quality_score for ap in access_points) / len(access_points)
            
            html += """
        <h2>Estatísticas Gerais</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Download Médio</div>
                <div class="stat-value">""" + f"{avg_download:.2f}" + """ Mbps</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Upload Médio</div>
                <div class="stat-value">""" + f"{avg_upload:.2f}" + """ Mbps</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Latência Média</div>
                <div class="stat-value">""" + f"{avg_latency:.2f}" + """ ms</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Quality Score Médio</div>
                <div class="stat-value">""" + f"{avg_quality:.4f}" + """</div>
            </div>
        </div>
        
        <h2>Pontos de Acesso</h2>
        <table>
            <thead>
                <tr>
                    <th>Provedor</th>
                    <th>Localização</th>
                    <th>Download (Mbps)</th>
                    <th>Upload (Mbps)</th>
                    <th>Latência (ms)</th>
                    <th>Estabilidade (%)</th>
                    <th>Quality Score</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for ap in access_points:
                # Determine quality class
                quality_class = "quality-low"
                if ap.quality_score > 1.0:
                    quality_class = "quality-high"
                elif ap.quality_score > 0.5:
                    quality_class = "quality-medium"
                
                html += f"""
                <tr>
                    <td>{ap.provider}</td>
                    <td>({ap.lat:.4f}, {ap.lon:.4f})</td>
                    <td>{ap.download}</td>
                    <td>{ap.upload}</td>
                    <td>{ap.latency}</td>
                    <td>{ap.stability}</td>
                    <td class="{quality_class}">{ap.quality_score}</td>
                </tr>
"""
            
            html += """
            </tbody>
        </table>
"""
        else:
            html += """
        <p>Nenhum ponto de acesso encontrado.</p>
"""
        
        html += """
        <div class="footer">
            <p>Rural Connectivity Mapper 2026 - Powered by SpaceX Starlink Technology</p>
            <p>Focusing on rural Brazil connectivity expansion for 2026</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        if debug:
            print(f"HTML report generated: {filepath}")
        
        return True
    
    except Exception as e:
        if debug:
            print(f"Error generating HTML report: {e}")
        return False


def is_platform_supported() -> bool:
    """
    Check if the current platform is supported.
    
    Returns:
        bool: True if platform is supported
    """
    supported_platforms = ['Linux', 'Darwin', 'Windows']
    return platform.system() in supported_platforms


def get_provider_stats(access_points: List[AccessPoint]) -> Dict[str, Dict[str, Any]]:
    """
    Calculate statistics grouped by provider.
    
    Args:
        access_points: List of AccessPoint instances
        
    Returns:
        dict: Statistics for each provider
    """
    providers = {}
    
    for ap in access_points:
        if ap.provider not in providers:
            providers[ap.provider] = {
                'count': 0,
                'total_download': 0,
                'total_upload': 0,
                'total_latency': 0,
                'total_quality': 0
            }
        
        stats = providers[ap.provider]
        stats['count'] += 1
        stats['total_download'] += ap.download
        stats['total_upload'] += ap.upload
        stats['total_latency'] += ap.latency
        stats['total_quality'] += ap.quality_score
    
    # Calculate averages
    for provider, stats in providers.items():
        count = stats['count']
        stats['avg_download'] = round(stats['total_download'] / count, 2)
        stats['avg_upload'] = round(stats['total_upload'] / count, 2)
        stats['avg_latency'] = round(stats['total_latency'] / count, 2)
        stats['avg_quality'] = round(stats['total_quality'] / count, 4)
    
    return providers
