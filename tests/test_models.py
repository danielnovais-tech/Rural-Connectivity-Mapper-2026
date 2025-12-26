"""
Unit tests for models.py - AccessPoint class
"""

import pytest
from datetime import datetime
from models import AccessPoint


class TestAccessPoint:
    """Test cases for AccessPoint class."""
    
    def test_create_access_point_minimal(self):
        """Test creating an access point with minimal parameters."""
        ap = AccessPoint(lat=-15.7801, lon=-47.9292)
        
        assert ap.lat == -15.7801
        assert ap.lon == -47.9292
        assert ap.provider == "Unknown"
        assert ap.address == ""
        assert ap.download == 0.0
        assert ap.upload == 0.0
        assert ap.latency == 0.0
        assert ap.stability == 100.0
        assert ap.tags == []
        assert isinstance(ap.timestamp, str)
    
    def test_create_access_point_full(self):
        """Test creating an access point with all parameters."""
        ap = AccessPoint(
            lat=-15.7801,
            lon=-47.9292,
            provider="Starlink",
            address="Brasília, DF, Brazil",
            download=150.5,
            upload=20.3,
            latency=25.0,
            stability=98.5,
            timestamp="2026-01-01T10:00:00",
            tags=["rural", "satellite"]
        )
        
        assert ap.lat == -15.7801
        assert ap.lon == -47.9292
        assert ap.provider == "Starlink"
        assert ap.address == "Brasília, DF, Brazil"
        assert ap.download == 150.5
        assert ap.upload == 20.3
        assert ap.latency == 25.0
        assert ap.stability == 98.5
        assert ap.timestamp == "2026-01-01T10:00:00"
        assert ap.tags == ["rural", "satellite"]
    
    def test_quality_score_calculation(self):
        """Test quality score calculation."""
        ap = AccessPoint(
            lat=0, lon=0,
            download=100.0,
            upload=20.0,
            latency=20.0,
            stability=100.0
        )
        
        # Formula: (download + upload) / (latency * (1 + stability/100))
        # (100 + 20) / (20 * (1 + 100/100)) = 120 / 40 = 3.0
        assert ap.quality_score == 3.0
    
    def test_quality_score_with_low_stability(self):
        """Test quality score calculation with lower stability."""
        ap = AccessPoint(
            lat=0, lon=0,
            download=100.0,
            upload=20.0,
            latency=20.0,
            stability=50.0
        )
        
        # (100 + 20) / (20 * (1 + 50/100)) = 120 / 30 = 4.0
        assert ap.quality_score == 4.0
    
    def test_quality_score_zero_latency(self):
        """Test quality score with zero latency returns 0."""
        ap = AccessPoint(
            lat=0, lon=0,
            download=100.0,
            upload=20.0,
            latency=0.0,
            stability=100.0
        )
        
        assert ap.quality_score == 0.0
    
    def test_update_quality_score(self):
        """Test updating quality score after changing metrics."""
        ap = AccessPoint(
            lat=0, lon=0,
            download=100.0,
            upload=20.0,
            latency=20.0,
            stability=100.0
        )
        
        initial_score = ap.quality_score
        
        # Change metrics
        ap.download = 200.0
        ap.update_quality_score()
        
        assert ap.quality_score > initial_score
    
    def test_to_dict(self):
        """Test converting AccessPoint to dictionary."""
        ap = AccessPoint(
            lat=-15.7801,
            lon=-47.9292,
            provider="Starlink",
            address="Brasília, DF, Brazil",
            download=150.5,
            upload=20.3,
            latency=25.0,
            stability=98.5,
            tags=["rural"]
        )
        
        data = ap.to_dict()
        
        assert isinstance(data, dict)
        assert data['lat'] == -15.7801
        assert data['lon'] == -47.9292
        assert data['provider'] == "Starlink"
        assert data['address'] == "Brasília, DF, Brazil"
        assert data['download'] == 150.5
        assert data['upload'] == 20.3
        assert data['latency'] == 25.0
        assert data['stability'] == 98.5
        assert data['tags'] == ["rural"]
        assert 'quality_score' in data
        assert 'timestamp' in data
    
    def test_from_dict(self):
        """Test creating AccessPoint from dictionary."""
        data = {
            "lat": -15.7801,
            "lon": -47.9292,
            "provider": "Starlink",
            "address": "Brasília, DF, Brazil",
            "download": 150.5,
            "upload": 20.3,
            "latency": 25.0,
            "stability": 98.5,
            "timestamp": "2026-01-01T10:00:00",
            "tags": ["rural", "satellite"],
            "quality_score": 3.395
        }
        
        ap = AccessPoint.from_dict(data)
        
        assert ap.lat == -15.7801
        assert ap.lon == -47.9292
        assert ap.provider == "Starlink"
        assert ap.address == "Brasília, DF, Brazil"
        assert ap.download == 150.5
        assert ap.upload == 20.3
        assert ap.latency == 25.0
        assert ap.stability == 98.5
        assert ap.timestamp == "2026-01-01T10:00:00"
        assert ap.tags == ["rural", "satellite"]
        assert ap.quality_score == 3.395
    
    def test_from_dict_partial(self):
        """Test creating AccessPoint from partial dictionary."""
        data = {
            "lat": -15.7801,
            "lon": -47.9292
        }
        
        ap = AccessPoint.from_dict(data)
        
        assert ap.lat == -15.7801
        assert ap.lon == -47.9292
        assert ap.provider == "Unknown"
        assert ap.download == 0.0
    
    def test_roundtrip_conversion(self):
        """Test converting to dict and back preserves data."""
        original = AccessPoint(
            lat=-15.7801,
            lon=-47.9292,
            provider="Starlink",
            download=150.5,
            upload=20.3,
            latency=25.0,
            stability=98.5,
            tags=["rural"]
        )
        
        data = original.to_dict()
        restored = AccessPoint.from_dict(data)
        
        assert restored.lat == original.lat
        assert restored.lon == original.lon
        assert restored.provider == original.provider
        assert restored.download == original.download
        assert restored.upload == original.upload
        assert restored.latency == original.latency
        assert restored.stability == original.stability
        assert restored.tags == original.tags
        assert restored.quality_score == original.quality_score
    
    def test_repr(self):
        """Test string representation."""
        ap = AccessPoint(
            lat=-15.7801,
            lon=-47.9292,
            provider="Starlink",
            download=150.5,
            upload=20.3,
            latency=25.0
        )
        
        repr_str = repr(ap)
        
        assert "AccessPoint" in repr_str
        assert "-15.7801" in repr_str
        assert "-47.9292" in repr_str
        assert "Starlink" in repr_str
    
    def test_str(self):
        """Test human-readable string."""
        ap = AccessPoint(
            lat=-15.7801,
            lon=-47.9292,
            provider="Starlink",
            download=150.5,
            upload=20.3,
            latency=25.0
        )
        
        str_repr = str(ap)
        
        assert "Starlink" in str_repr
        assert "150.5" in str_repr
        assert "20.3" in str_repr
        assert "25.0" in str_repr
