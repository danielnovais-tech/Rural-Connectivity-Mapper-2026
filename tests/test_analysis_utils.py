"""Tests for analysis utilities."""

import pytest
from datetime import datetime

from src.utils.analysis_utils import analyze_temporal_evolution, compare_providers


@pytest.fixture
def sample_data():
    """Sample connectivity data for testing."""
    return [
        {
            'id': 'test-1',
            'provider': 'Starlink',
            'timestamp': '2026-01-15T10:30:00',
            'speed_test': {
                'download': 150.0,
                'upload': 18.0,
                'latency': 25.0
            },
            'quality_score': {
                'overall_score': 85.5
            }
        },
        {
            'id': 'test-2',
            'provider': 'Claro',
            'timestamp': '2026-01-15T11:00:00',
            'speed_test': {
                'download': 92.1,
                'upload': 15.3,
                'latency': 38.7
            },
            'quality_score': {
                'overall_score': 72.0
            }
        },
        {
            'id': 'test-3',
            'provider': 'Viasat',
            'timestamp': '2026-01-16T09:00:00',
            'speed_test': {
                'download': 75.3,
                'upload': 9.8,
                'latency': 68.2
            },
            'quality_score': {
                'overall_score': 60.0
            }
        }
    ]


@pytest.fixture
def satellite_test_data():
    """Test data with multiple satellite providers."""
    return [
        {
            'provider': 'Starlink Gen2',
            'speed_test': {'download': 150, 'upload': 20, 'latency': 30, 'jitter': 3, 'packet_loss': 0.1, 'obstruction': 2.5, 'stability': 90},
            'quality_score': {'overall_score': 85}
        },
        {
            'provider': 'Starlink High Performance',
            'speed_test': {'download': 200, 'upload': 25, 'latency': 25, 'jitter': 2, 'packet_loss': 0.05, 'obstruction': 1.2, 'stability': 95},
            'quality_score': {'overall_score': 95}
        },
        {
            'provider': 'Viasat',
            'speed_test': {'download': 75, 'upload': 10, 'latency': 70, 'jitter': 15, 'packet_loss': 2.5, 'obstruction': 0, 'stability': 50},
            'quality_score': {'overall_score': 55}
        },
        {
            'provider': 'Claro',
            'speed_test': {'download': 90, 'upload': 15, 'latency': 40, 'jitter': 6, 'packet_loss': 0.8, 'obstruction': 0, 'stability': 80},
            'quality_score': {'overall_score': 75}
        }
    ]


def test_analyze_temporal_evolution(sample_data):
    """Test temporal analysis calculation."""
    analysis = analyze_temporal_evolution(sample_data)
    
    assert 'total_points' in analysis
    assert 'date_range' in analysis
    assert 'daily_averages' in analysis
    assert 'trends' in analysis
    assert 'insights' in analysis
    
    assert analysis['total_points'] == 3
    
    # Check trends
    trends = analysis['trends']
    assert 'avg_quality_score' in trends
    assert 'avg_download' in trends
    assert 'avg_latency' in trends
    
    # Average quality score should be around (85.5 + 72.0 + 60.0) / 3 = 72.5
    assert 70 <= trends['avg_quality_score'] <= 75


def test_temporal_grouping(sample_data):
    """Test grouping by date."""
    analysis = analyze_temporal_evolution(sample_data)
    
    daily_averages = analysis['daily_averages']
    
    # Should have 2 different dates
    assert len(daily_averages) == 2
    
    # Check that dates are present
    assert '2026-01-15' in daily_averages
    assert '2026-01-16' in daily_averages
    
    # Jan 15 should have 2 points
    assert daily_averages['2026-01-15']['count'] == 2
    
    # Jan 16 should have 1 point
    assert daily_averages['2026-01-16']['count'] == 1


def test_analyze_empty_data():
    """Test analysis with empty data."""
    analysis = analyze_temporal_evolution([])
    
    assert analysis['total_points'] == 0
    assert analysis['daily_averages'] == {}


def test_analyze_insights(sample_data):
    """Test that insights are generated."""
    analysis = analyze_temporal_evolution(sample_data)
    
    insights = analysis['insights']
    
    # Should have some insights
    assert len(insights) > 0
    assert all(isinstance(insight, str) for insight in insights)


def test_analyze_insights_portuguese(sample_data):
    """Test that Portuguese insights are generated."""
    analysis = analyze_temporal_evolution(sample_data, language='pt')
    
    insights = analysis['insights']
    
    # Should have some insights
    assert len(insights) > 0
    assert all(isinstance(insight, str) for insight in insights)
    
    # Check that at least one insight is in Portuguese
    # (e.g., contains Portuguese words like "qualidade", "velocidade", etc.)
    insights_text = ' '.join(insights)
    # Check for Portuguese-specific characters or words
    assert any(word in insights_text.lower() for word in ['qualidade', 'velocidade', 'latência', 'atendem', 'apresenta'])


def test_provider_stats(sample_data):
    """Test provider statistics in analysis."""
    analysis = analyze_temporal_evolution(sample_data)
    
    assert 'provider_stats' in analysis
    
    provider_stats = analysis['provider_stats']
    
    # Should have stats for each provider
    assert 'Starlink' in provider_stats
    assert 'Claro' in provider_stats
    assert 'Viasat' in provider_stats
    
    # Each provider should have count and avg_score
    for provider, stats in provider_stats.items():
        assert 'count' in stats
        assert 'avg_score' in stats
        assert stats['count'] > 0


def test_compare_providers(sample_data):
    """Test provider comparison functionality."""
    comparison = compare_providers(sample_data)
    
    assert 'total_providers' in comparison
    assert 'providers' in comparison
    assert 'insights' in comparison
    
    assert comparison['total_providers'] == 3
    
    # Check that each provider has detailed metrics
    providers = comparison['providers']
    assert 'Starlink' in providers
    
    starlink_metrics = providers['Starlink']
    assert 'quality_score' in starlink_metrics
    assert 'download' in starlink_metrics
    assert 'upload' in starlink_metrics
    assert 'latency' in starlink_metrics
    assert 'jitter' in starlink_metrics
    assert 'packet_loss' in starlink_metrics
    assert 'obstruction' in starlink_metrics
    assert 'stability' in starlink_metrics
    
    # Each metric should have avg, min, max
    for metric_name, metric_data in starlink_metrics.items():
        if metric_name != 'count':
            assert 'avg' in metric_data
            assert 'min' in metric_data
            assert 'max' in metric_data


def test_compare_providers_satellite_identification(satellite_test_data):
    """Test that satellite providers are correctly identified."""
    comparison = compare_providers(satellite_test_data)
    
    # Check satellite providers are identified
    assert 'satellite_providers' in comparison
    satellite_providers = comparison['satellite_providers']
    
    assert 'Starlink Gen2' in satellite_providers
    assert 'Starlink High Performance' in satellite_providers
    assert 'Viasat' in satellite_providers
    assert 'Claro' not in satellite_providers


def test_compare_providers_empty_data():
    """Test provider comparison with empty data."""
    comparison = compare_providers([])
    
    assert comparison['providers'] == {}
