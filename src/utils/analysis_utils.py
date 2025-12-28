"""Analysis utilities for temporal evolution and trends."""

import logging
from typing import List, Dict
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


def analyze_temporal_evolution(data: List[Dict]) -> Dict:
    """Analyze temporal evolution of connectivity quality.
    
    Groups data by date and calculates statistics to identify trends.
    
    Args:
        data: List of connectivity point dictionaries
        
    Returns:
        Dict: Analysis results with trends and insights
    """
    try:
        logger.info(f"Analyzing temporal evolution of {len(data)} points...")
        
        if not data:
            logger.warning("No data provided for temporal analysis")
            return {
                'total_points': 0,
                'date_range': {},
                'daily_averages': {},
                'trends': {},
                'insights': []
            }
        
        # Group data by date
        daily_data = defaultdict(list)
        
        for point in data:
            timestamp = point.get('timestamp')
            if not timestamp:
                continue
            
            try:
                # Parse timestamp and extract date
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                date_key = dt.date().isoformat()
                
                # Extract quality score
                qs = point.get('quality_score', {})
                overall_score = qs.get('overall_score', 0)
                
                daily_data[date_key].append({
                    'overall_score': overall_score,
                    'provider': point.get('provider', 'Unknown'),
                    'speed_test': point.get('speed_test', {})
                })
            except Exception as e:
                logger.warning(f"Error parsing timestamp '{timestamp}': {e}")
                continue
        
        # Calculate daily averages
        daily_averages = {}
        for date, points in daily_data.items():
            scores = [p['overall_score'] for p in points]
            downloads = [p['speed_test'].get('download', 0) for p in points]
            latencies = [p['speed_test'].get('latency', 0) for p in points]
            
            daily_averages[date] = {
                'count': len(points),
                'avg_quality_score': round(sum(scores) / len(scores), 2) if scores else 0,
                'avg_download': round(sum(downloads) / len(downloads), 2) if downloads else 0,
                'avg_latency': round(sum(latencies) / len(latencies), 2) if latencies else 0,
                'min_quality_score': round(min(scores), 2) if scores else 0,
                'max_quality_score': round(max(scores), 2) if scores else 0
            }
        
        # Calculate overall trends
        all_scores = [p.get('quality_score', {}).get('overall_score', 0) for p in data]
        all_downloads = [p.get('speed_test', {}).get('download', 0) for p in data]
        all_latencies = [p.get('speed_test', {}).get('latency', 0) for p in data]
        
        trends = {
            'avg_quality_score': round(sum(all_scores) / len(all_scores), 2) if all_scores else 0,
            'avg_download': round(sum(all_downloads) / len(all_downloads), 2) if all_downloads else 0,
            'avg_latency': round(sum(all_latencies) / len(all_latencies), 2) if all_latencies else 0,
            'min_quality_score': round(min(all_scores), 2) if all_scores else 0,
            'max_quality_score': round(max(all_scores), 2) if all_scores else 0
        }
        
        # Generate insights
        insights = []
        
        if trends['avg_quality_score'] >= 80:
            insights.append("Overall connectivity quality is excellent across all points")
        elif trends['avg_quality_score'] >= 60:
            insights.append("Overall connectivity quality is good with room for improvement")
        else:
            insights.append("Overall connectivity quality needs significant improvement")
        
        if trends['avg_download'] >= 100:
            insights.append("Download speeds meet Starlink 2026 target expectations")
        elif trends['avg_download'] >= 50:
            insights.append("Download speeds are acceptable but below optimal targets")
        else:
            insights.append("Download speeds are below target thresholds")
        
        if trends['avg_latency'] <= 40:
            insights.append("Latency is within Starlink 2026 target range")
        else:
            insights.append("Latency exceeds target thresholds and needs optimization")
        
        # Analyze by provider
        provider_stats = defaultdict(list)
        for point in data:
            provider = point.get('provider', 'Unknown')
            score = point.get('quality_score', {}).get('overall_score', 0)
            provider_stats[provider].append(score)
        
        best_provider = None
        best_avg = 0
        for provider, scores in provider_stats.items():
            avg = sum(scores) / len(scores) if scores else 0
            if avg > best_avg:
                best_avg = avg
                best_provider = provider
        
        if best_provider:
            insights.append(f"{best_provider} shows the best average quality score ({best_avg:.1f}/100)")
        
        # Prepare date range
        dates = sorted(daily_data.keys())
        date_range = {
            'start': dates[0] if dates else None,
            'end': dates[-1] if dates else None,
            'days': len(dates)
        }
        
        result = {
            'total_points': len(data),
            'date_range': date_range,
            'daily_averages': daily_averages,
            'trends': trends,
            'insights': insights,
            'provider_stats': {
                provider: {
                    'count': len(scores),
                    'avg_score': round(sum(scores) / len(scores), 2) if scores else 0
                }
                for provider, scores in provider_stats.items()
            }
        }
        
        logger.info("Temporal analysis completed")
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing temporal evolution: {e}")
        raise
