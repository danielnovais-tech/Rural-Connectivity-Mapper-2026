"""Tests for validation utilities."""

import pytest

from src.utils.validation_utils import (
    validate_coordinates,
    validate_speed_test,
    validate_provider
)
from src.models import SpeedTest


def test_validate_coordinates_valid():
    """Test validation of valid coordinates."""
    # Valid coordinates
    assert validate_coordinates(0, 0) is True
    assert validate_coordinates(-23.5505, -46.6333) is True  # São Paulo
    assert validate_coordinates(90, 180) is True  # Max valid
    assert validate_coordinates(-90, -180) is True  # Min valid


def test_validate_coordinates_invalid():
    """Test validation of invalid coordinates."""
    # Invalid latitude
    assert validate_coordinates(91, 0) is False
    assert validate_coordinates(-91, 0) is False
    
    # Invalid longitude
    assert validate_coordinates(0, 181) is False
    assert validate_coordinates(0, -181) is False
    
    # Both invalid
    assert validate_coordinates(100, 200) is False


def test_validate_speed_test_valid():
    """Test validation of valid speed test data."""
    speed_test = SpeedTest(
        download=100.0,
        upload=15.0,
        latency=30.0,
        jitter=5.0,
        packet_loss=0.5
    )
    
    assert validate_speed_test(speed_test) is True
    
    # Test with dict
    speed_dict = {
        'download': 100.0,
        'upload': 15.0,
        'latency': 30.0
    }
    
    assert validate_speed_test(speed_dict) is True


def test_validate_speed_test_invalid():
    """Test validation of invalid speed test data."""
    # Negative values
    invalid_dict = {
        'download': -10.0,
        'upload': 15.0,
        'latency': 30.0
    }
    
    assert validate_speed_test(invalid_dict) is False
    
    # Missing required fields
    incomplete_dict = {
        'download': 100.0
    }
    
    assert validate_speed_test(incomplete_dict) is False


def test_validate_provider_valid():
    """Test validation of valid provider names."""
    assert validate_provider('Starlink') is True
    assert validate_provider('Viasat') is True
    assert validate_provider('HughesNet') is True
    assert validate_provider('Claro') is True


def test_validate_provider_invalid():
    """Test validation of invalid provider names."""
    assert validate_provider('Unknown Provider') is False
    assert validate_provider('') is False
    assert validate_provider(None) is False
