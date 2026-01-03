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


def compare_providers(data: List[Dict]) -> Dict:
    """Compare ISP performance with detailed metrics analysis.
    
    Analyzes and compares providers including satellite-specific metrics
    like jitter, packet loss, and obstruction for Starlink comparisons.
    
    Args:
        data: List of connectivity point dictionaries
        
    Returns:
        Dict: Detailed provider comparison with metrics breakdown
    """
    try:
        logger.info(f"Comparing providers across {len(data)} points...")
        
        if not data:
            logger.warning("No data provided for provider comparison")
            return {'providers': {}}
        
        # Collect metrics by provider
        provider_metrics = defaultdict(lambda: {
            'quality_scores': [],
            'download_speeds': [],
            'upload_speeds': [],
            'latencies': [],
            'jitters': [],
            'packet_losses': [],
            'obstructions': [],
            'stabilities': []
        })
        
        for point in data:
            provider = point.get('provider', 'Unknown')
            quality_score = point.get('quality_score', {})
            speed_test = point.get('speed_test', {})
            
            provider_metrics[provider]['quality_scores'].append(
                quality_score.get('overall_score', 0)
            )
            provider_metrics[provider]['download_speeds'].append(
                speed_test.get('download', 0)
            )
            provider_metrics[provider]['upload_speeds'].append(
                speed_test.get('upload', 0)
            )
            provider_metrics[provider]['latencies'].append(
                speed_test.get('latency', 0)
            )
            provider_metrics[provider]['jitters'].append(
                speed_test.get('jitter', 0)
            )
            provider_metrics[provider]['packet_losses'].append(
                speed_test.get('packet_loss', 0)
            )
            provider_metrics[provider]['obstructions'].append(
                speed_test.get('obstruction', 0)
            )
            provider_metrics[provider]['stabilities'].append(
                speed_test.get('stability', 0)
            )
        
        # Calculate statistics for each provider
        providers_summary = {}
        
        def calculate_avg(lst):
            """Helper to calculate average of a list."""
            return round(sum(lst) / len(lst), 2) if lst else 0
        
        def calculate_max(lst):
            """Helper to calculate max of a list."""
            return round(max(lst), 2) if lst else 0
        
        def calculate_min(lst):
            """Helper to calculate min of a list."""
            return round(min(lst), 2) if lst else 0
        
        for provider, metrics in provider_metrics.items():
            providers_summary[provider] = {
                'count': len(metrics['quality_scores']),
                'quality_score': {
                    'avg': calculate_avg(metrics['quality_scores']),
                    'min': calculate_min(metrics['quality_scores']),
                    'max': calculate_max(metrics['quality_scores'])
                },
                'download': {
                    'avg': calculate_avg(metrics['download_speeds']),
                    'min': calculate_min(metrics['download_speeds']),
                    'max': calculate_max(metrics['download_speeds'])
                },
                'upload': {
                    'avg': calculate_avg(metrics['upload_speeds']),
                    'min': calculate_min(metrics['upload_speeds']),
                    'max': calculate_max(metrics['upload_speeds'])
                },
                'latency': {
                    'avg': calculate_avg(metrics['latencies']),
                    'min': calculate_min(metrics['latencies']),
                    'max': calculate_max(metrics['latencies'])
                },
                'jitter': {
                    'avg': calculate_avg(metrics['jitters']),
                    'min': calculate_min(metrics['jitters']),
                    'max': calculate_max(metrics['jitters'])
                },
                'packet_loss': {
                    'avg': calculate_avg(metrics['packet_losses']),
                    'min': calculate_min(metrics['packet_losses']),
                    'max': calculate_max(metrics['packet_losses'])
                },
                'obstruction': {
                    'avg': calculate_avg(metrics['obstructions']),
                    'min': calculate_min(metrics['obstructions']),
                    'max': calculate_max(metrics['obstructions'])
                },
                'stability': {
                    'avg': calculate_avg(metrics['stabilities']),
                    'min': calculate_min(metrics['stabilities']),
                    'max': calculate_max(metrics['stabilities'])
                }
            }
        
        # Identify satellite providers (Starlink variants, Viasat, HughesNet)
        satellite_providers = [
            p for p in providers_summary.keys() 
            if any(sat in p for sat in ['Starlink', 'Viasat', 'HughesNet'])
        ]
        
        # Generate insights
        insights = []
        
        # Find best provider overall
        best_provider = max(
            providers_summary.items(),
            key=lambda x: x[1]['quality_score']['avg']
        )
        insights.append(
            f"{best_provider[0]} leads with {best_provider[1]['quality_score']['avg']}/100 average quality score"
        )
        
        # Compare Starlink variants if present
        starlink_variants = [p for p in satellite_providers if 'Starlink' in p]
        if len(starlink_variants) >= 2:
            starlink_comparison = {
                p: providers_summary[p] for p in starlink_variants
            }
            best_starlink = max(
                starlink_comparison.items(),
                key=lambda x: x[1]['quality_score']['avg']
            )
            insights.append(
                f"Among Starlink options, {best_starlink[0]} performs best with "
                f"{best_starlink[1]['download']['avg']} Mbps avg download and "
                f"{best_starlink[1]['obstruction']['avg']}% avg obstruction"
            )
        
        # Satellite vs terrestrial comparison
        if satellite_providers:
            terrestrial_providers = [
                p for p in providers_summary.keys() 
                if p not in satellite_providers
            ]
            
            if terrestrial_providers:
                sat_avg_latency = calculate_avg([
                    providers_summary[p]['latency']['avg'] 
                    for p in satellite_providers
                ])
                terr_avg_latency = calculate_avg([
                    providers_summary[p]['latency']['avg'] 
                    for p in terrestrial_providers
                ])
                
                if sat_avg_latency < terr_avg_latency:
                    insights.append(
                        f"Satellite providers show lower latency ({sat_avg_latency} ms) "
                        f"compared to terrestrial ({terr_avg_latency} ms)"
                    )
                else:
                    insights.append(
                        f"Terrestrial providers have lower latency ({terr_avg_latency} ms) "
                        f"vs satellite ({sat_avg_latency} ms)"
                    )
        
        result = {
            'total_providers': len(providers_summary),
            'providers': providers_summary,
            'satellite_providers': satellite_providers,
            'insights': insights
        }
        
        logger.info("Provider comparison completed")
        return result
    
    except Exception as e:
        logger.error(f"Error comparing providers: {e}")
        raise
