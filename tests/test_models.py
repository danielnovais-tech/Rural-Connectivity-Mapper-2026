"""Tests for connectivity models."""

import pytest
from datetime import datetime
from src.models.connectivity_point import ConnectivityPoint
from src.models.speed_test import SpeedTest
from src.models.quality_score import QualityScore


class TestConnectivityPoint:
    """Test ConnectivityPoint model."""
    
    def test_create_point(self):
        """Test creating a connectivity point."""
        point = ConnectivityPoint(
            latitude=-23.5505,
            longitude=-46.6333,
            address="São Paulo, Brazil",
            provider="Starlink"
        )
        
        assert point.latitude == -23.5505
        assert point.longitude == -46.6333
        assert point.address == "São Paulo, Brazil"
        assert point.provider == "Starlink"
        assert point.point_id is not None
        assert len(point.speed_tests) == 0
    
    def test_add_speed_test(self):
        """Test adding speed test to point."""
        point = ConnectivityPoint(latitude=-23.5505, longitude=-46.6333)
        speed_test = SpeedTest(
            download_speed=100.5,
            upload_speed=20.3,
            latency=25.0
        )
        
        point.add_speed_test(speed_test)
        assert len(point.speed_tests) == 1
        assert point.speed_tests[0] == speed_test
    
    def test_to_dict(self):
        """Test converting point to dictionary."""
        point = ConnectivityPoint(
            latitude=-23.5505,
            longitude=-46.6333,
            tags=["rural", "test"]
        )
        
        data = point.to_dict()
        assert data["latitude"] == -23.5505
        assert data["longitude"] == -46.6333
        assert data["tags"] == ["rural", "test"]
    
    def test_from_dict(self):
        """Test creating point from dictionary."""
        data = {
            "latitude": -23.5505,
            "longitude": -46.6333,
            "address": "São Paulo",
            "provider": "Starlink",
            "tags": ["rural"],
            "timestamp": "2024-01-01T12:00:00",
            "speed_tests": [],
            "quality_score": None
        }
        
        point = ConnectivityPoint.from_dict(data)
        assert point.latitude == -23.5505
        assert point.longitude == -46.6333
        assert point.address == "São Paulo"


class TestSpeedTest:
    """Test SpeedTest model."""
    
    def test_create_speed_test(self):
        """Test creating a speed test."""
        st = SpeedTest(
            download_speed=150.0,
            upload_speed=25.0,
            latency=20.0,
            jitter=5.0,
            packet_loss=0.1
        )
        
        assert st.download_speed == 150.0
        assert st.upload_speed == 25.0
        assert st.latency == 20.0
        assert st.jitter == 5.0
        assert st.packet_loss == 0.1
    
    def test_calculate_stability(self):
        """Test stability calculation."""
        st = SpeedTest(
            download_speed=100.0,
            upload_speed=20.0,
            latency=30.0,
            jitter=10.0,
            packet_loss=1.0
        )
        
        stability = st.calculate_stability()
        assert 0 <= stability <= 100
    
    def test_to_dict(self):
        """Test converting speed test to dictionary."""
        st = SpeedTest(
            download_speed=100.0,
            upload_speed=20.0,
            latency=30.0
        )
        
        data = st.to_dict()
        assert data["download_speed"] == 100.0
        assert data["upload_speed"] == 20.0
        assert data["latency"] == 30.0
        assert "stability" in data


class TestQualityScore:
    """Test QualityScore model."""
    
    def test_create_quality_score(self):
        """Test creating a quality score."""
        qs = QualityScore(
            speed_score=85.0,
            latency_score=90.0,
            stability_score=80.0
        )
        
        assert qs.speed_score == 85.0
        assert qs.latency_score == 90.0
        assert qs.stability_score == 80.0
        assert qs.overall_score > 0
    
    def test_overall_score_calculation(self):
        """Test overall score weighted calculation."""
        qs = QualityScore(
            speed_score=100.0,
            latency_score=100.0,
            stability_score=100.0
        )
        
        assert qs.overall_score == 100.0
    
    def test_get_rating(self):
        """Test quality rating."""
        qs_excellent = QualityScore(95.0, 95.0, 95.0)
        assert qs_excellent.get_rating() == "Excellent"
        
        qs_good = QualityScore(80.0, 80.0, 80.0)
        assert qs_good.get_rating() == "Good"
        
        qs_poor = QualityScore(45.0, 45.0, 45.0)
        assert qs_poor.get_rating() == "Poor"
    
    def test_to_dict(self):
        """Test converting quality score to dictionary."""
        qs = QualityScore(85.0, 90.0, 80.0)
        data = qs.to_dict()
        
        assert "overall_score" in data
        assert "rating" in data
        assert data["speed_score"] == 85.0
