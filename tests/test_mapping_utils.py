"""Tests for mapping utilities."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.utils.mapping_utils import generate_map


@pytest.fixture
def sample_data():
    """Sample connectivity data for testing."""
    return [
        {
            'id': 'test-1',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'provider': 'Starlink',
            'speed_test': {
                'download': 150.0,
                'upload': 18.0,
                'latency': 25.0
            },
            'quality_score': {
                'overall_score': 85.5,
                'rating': 'Excellent'
            }
        },
        {
            'id': 'test-2',
            'latitude': -22.9068,
            'longitude': -43.1729,
            'provider': 'Claro',
            'speed_test': {
                'download': 92.1,
                'upload': 15.3,
                'latency': 38.7
            },
            'quality_score': {
                'overall_score': 72.0,
                'rating': 'Good'
            }
        }
    ]


def test_generate_map(sample_data, tmp_path):
    """Test interactive map generation."""
    output_path = tmp_path / "test_map.html"
    
    map_path = generate_map(sample_data, str(output_path))
    
    assert Path(map_path).exists()
    
    # Verify HTML content
    with open(map_path, 'r') as f:
        content = f.read()
    
    # Should contain Folium map elements
    assert 'folium' in content.lower() or 'leaflet' in content.lower()
    
    # Should contain provider names
    assert 'Starlink' in content
    assert 'Claro' in content


def test_generate_map_empty_data(tmp_path):
    """Test map generation with empty data."""
    output_path = tmp_path / "empty_map.html"
    
    map_path = generate_map([], str(output_path))
    
    # Should still create a map file
    assert Path(map_path).exists()


def test_generate_map_default_path(sample_data, tmp_path, monkeypatch):
    """Test map generation with default output path."""
    # Change to tmp directory for test
    monkeypatch.chdir(tmp_path)
    
    map_path = generate_map(sample_data)
    
    assert Path(map_path).exists()
    assert 'connectivity_map' in map_path
    assert map_path.endswith('.html')


def test_generate_map_with_starlink_coverage(sample_data, tmp_path):
    """Test that map includes Starlink coverage layers."""
    output_path = tmp_path / "coverage_map.html"
    
    map_path = generate_map(sample_data, str(output_path))
    
    assert Path(map_path).exists()
    
    # Verify HTML content includes Starlink coverage elements
    with open(map_path, 'r') as f:
        content = f.read()
    
    # Should contain Starlink coverage zone references
    assert 'Starlink Coverage' in content or 'coverage' in content.lower()
    
    # Should contain layer control for toggling layers
    assert 'LayerControl' in content or 'layer' in content.lower()
    
    # Should contain legend with coverage information
    assert 'Legend' in content or 'legend' in content.lower()
    
    # Should still contain original connectivity data
    assert 'Starlink' in content
    assert 'Claro' in content

