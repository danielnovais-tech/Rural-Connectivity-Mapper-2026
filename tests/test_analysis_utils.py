"""Tests for analysis utilities."""

import pytest
from datetime import datetime

from src.utils.analysis_utils import analyze_temporal_evolution


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
