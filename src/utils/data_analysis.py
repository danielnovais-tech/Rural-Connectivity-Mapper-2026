"""Data analysis utilities for temporal and provider comparisons."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from src.models.connectivity_point import ConnectivityPoint

logger = logging.getLogger(__name__)


def analyze_temporal_trends(
    points: List[ConnectivityPoint],
    time_window: timedelta = timedelta(days=30)
) -> Dict[str, Any]:
    """
    Analyze temporal trends in connectivity data.
    
    Args:
        points: List of ConnectivityPoint objects
        time_window: Time window for analysis
    
    Returns:
        Dictionary with temporal analysis results
    """
    if not points:
        return {}
    
    # Sort points by timestamp
    sorted_points = sorted(points, key=lambda p: p.timestamp)
    
    # Group by time periods
    periods = defaultdict(list)
    
    for point in sorted_points:
        period_key = point.timestamp.strftime('%Y-%m-%d')
        periods[period_key].append(point)
    
    # Calculate statistics for each period
    period_stats = {}
    for period, period_points in periods.items():
        avg_scores = []
        for point in period_points:
            if point.quality_score:
                avg_scores.append(point.quality_score.overall_score)
        
        period_stats[period] = {
            'num_points': len(period_points),
            'avg_quality_score': sum(avg_scores) / len(avg_scores) if avg_scores else 0,
            'min_quality_score': min(avg_scores) if avg_scores else 0,
            'max_quality_score': max(avg_scores) if avg_scores else 0
        }
    
    return {
        'total_points': len(points),
        'date_range': {
            'start': sorted_points[0].timestamp.isoformat(),
            'end': sorted_points[-1].timestamp.isoformat()
        },
        'periods': period_stats
    }


def compare_providers(points: List[ConnectivityPoint]) -> Dict[str, Any]:
    """
    Compare connectivity quality across providers.
    
    Args:
        points: List of ConnectivityPoint objects
    
    Returns:
        Dictionary with provider comparison results
    """
    provider_data = defaultdict(lambda: {
        'points': [],
        'quality_scores': [],
        'download_speeds': [],
        'upload_speeds': [],
        'latencies': []
    })
    
    for point in points:
        provider = point.provider or 'Unknown'
        provider_data[provider]['points'].append(point)
        
        if point.quality_score:
            provider_data[provider]['quality_scores'].append(point.quality_score.overall_score)
        
        for st in point.speed_tests:
            provider_data[provider]['download_speeds'].append(st.download_speed)
            provider_data[provider]['upload_speeds'].append(st.upload_speed)
            provider_data[provider]['latencies'].append(st.latency)
    
    # Calculate statistics for each provider
    comparison = {}
    for provider, data in provider_data.items():
        comparison[provider] = {
            'num_points': len(data['points']),
            'avg_quality_score': sum(data['quality_scores']) / len(data['quality_scores']) if data['quality_scores'] else 0,
            'avg_download_speed': sum(data['download_speeds']) / len(data['download_speeds']) if data['download_speeds'] else 0,
            'avg_upload_speed': sum(data['upload_speeds']) / len(data['upload_speeds']) if data['upload_speeds'] else 0,
            'avg_latency': sum(data['latencies']) / len(data['latencies']) if data['latencies'] else 0
        }
    
    return comparison


def get_summary_statistics(points: List[ConnectivityPoint]) -> Dict[str, Any]:
    """
    Get summary statistics for all points.
    
    Args:
        points: List of ConnectivityPoint objects
    
    Returns:
        Dictionary with summary statistics
    """
    if not points:
        return {}
    
    quality_scores = []
    download_speeds = []
    upload_speeds = []
    latencies = []
    providers = set()
    tags = set()
    
    for point in points:
        if point.provider:
            providers.add(point.provider)
        tags.update(point.tags)
        
        if point.quality_score:
            quality_scores.append(point.quality_score.overall_score)
        
        for st in point.speed_tests:
            download_speeds.append(st.download_speed)
            upload_speeds.append(st.upload_speed)
            latencies.append(st.latency)
    
    return {
        'total_points': len(points),
        'num_providers': len(providers),
        'providers': list(providers),
        'num_tags': len(tags),
        'tags': list(tags),
        'quality_scores': {
            'avg': sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            'min': min(quality_scores) if quality_scores else 0,
            'max': max(quality_scores) if quality_scores else 0
        },
        'download_speeds': {
            'avg': sum(download_speeds) / len(download_speeds) if download_speeds else 0,
            'min': min(download_speeds) if download_speeds else 0,
            'max': max(download_speeds) if download_speeds else 0
        },
        'upload_speeds': {
            'avg': sum(upload_speeds) / len(upload_speeds) if upload_speeds else 0,
            'min': min(upload_speeds) if upload_speeds else 0,
            'max': max(upload_speeds) if upload_speeds else 0
        },
        'latencies': {
            'avg': sum(latencies) / len(latencies) if latencies else 0,
            'min': min(latencies) if latencies else 0,
            'max': max(latencies) if latencies else 0
        }
    }
