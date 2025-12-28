"""Tests for geocoding utilities."""

import pytest
from unittest.mock import Mock, patch

from src.utils.geocoding_utils import geocode_coordinates, geocode_address


def test_geocoding_coordinates():
    """Test reverse geocoding from coordinates to address."""
    with patch('src.utils.geocoding_utils.geolocator.reverse') as mock_reverse:
        # Setup mock
        mock_location = Mock()
        mock_location.address = "São Paulo, Brazil"
        mock_reverse.return_value = mock_location
        
        # Test geocoding
        address = geocode_coordinates(-23.5505, -46.6333)
        
        assert address == "São Paulo, Brazil"
        mock_reverse.assert_called_once()


def test_geocoding_address():
    """Test forward geocoding from address to coordinates."""
    with patch('src.utils.geocoding_utils.geolocator.geocode') as mock_geocode:
        # Setup mock
        mock_location = Mock()
        mock_location.latitude = -23.5505
        mock_location.longitude = -46.6333
        mock_geocode.return_value = mock_location
        
        # Test geocoding
        coords = geocode_address("São Paulo, Brazil")
        
        assert coords is not None
        assert coords[0] == -23.5505
        assert coords[1] == -46.6333
        mock_geocode.assert_called_once()
