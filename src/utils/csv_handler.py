"""CSV import/export utilities."""

import csv
from pathlib import Path
from typing import List
from datetime import datetime
import logging

from src.models.connectivity_point import ConnectivityPoint
from src.models.speed_test import SpeedTest

logger = logging.getLogger(__name__)


def export_to_csv(points: List[ConnectivityPoint], filepath: str) -> None:
    """
    Export connectivity points to CSV file.
    
    Args:
        points: List of ConnectivityPoint objects
        filepath: Output CSV file path
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'point_id', 'latitude', 'longitude', 'address', 'provider', 
            'tags', 'timestamp'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for point in points:
            writer.writerow({
                'point_id': point.point_id,
                'latitude': point.latitude,
                'longitude': point.longitude,
                'address': point.address or '',
                'provider': point.provider or '',
                'tags': ','.join(point.tags) if point.tags else '',
                'timestamp': point.timestamp.isoformat()
            })
    
    logger.info(f"Exported {len(points)} points to {filepath}")


def import_from_csv(filepath: str) -> List[ConnectivityPoint]:
    """
    Import connectivity points from CSV file.
    
    Args:
        filepath: Input CSV file path
    
    Returns:
        List of ConnectivityPoint objects
    """
    points = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                tags = [tag.strip() for tag in row.get('tags', '').split(',') if tag.strip()]
                
                point = ConnectivityPoint(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    address=row.get('address') or None,
                    provider=row.get('provider') or None,
                    tags=tags,
                    timestamp=datetime.fromisoformat(row['timestamp']) if row.get('timestamp') else None,
                    point_id=row.get('point_id') or None
                )
                points.append(point)
            except Exception as e:
                logger.error(f"Error importing row: {e}")
                continue
    
    logger.info(f"Imported {len(points)} points from {filepath}")
    return points
