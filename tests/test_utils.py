"""
Unit tests for utils.py - Utility functions
"""

import pytest
import os
import json
import tempfile
from models import AccessPoint
from utils import (
    validate_coordinates, validate_access_point,
    load_data, save_data, backup_data,
    export_csv, import_csv,
    generate_report_txt, generate_report_json, generate_report_html,
    get_provider_stats, is_platform_supported
)


class TestValidation:
    """Test cases for validation functions."""
    
    def test_validate_coordinates_valid(self):
        """Test validation with valid coordinates."""
        assert validate_coordinates(0, 0) is True
        assert validate_coordinates(-15.7801, -47.9292) is True
        assert validate_coordinates(90, 180) is True
        assert validate_coordinates(-90, -180) is True
    
    def test_validate_coordinates_invalid_lat(self):
        """Test validation with invalid latitude."""
        assert validate_coordinates(91, 0) is False
        assert validate_coordinates(-91, 0) is False
    
    def test_validate_coordinates_invalid_lon(self):
        """Test validation with invalid longitude."""
        assert validate_coordinates(0, 181) is False
        assert validate_coordinates(0, -181) is False
    
    def test_validate_access_point_valid(self):
        """Test validation with valid access point."""
        ap = AccessPoint(
            lat=-15.7801,
            lon=-47.9292,
            download=100.0,
            upload=20.0,
            latency=25.0,
            stability=95.0
        )
        
        errors = validate_access_point(ap)
        assert len(errors) == 0
    
    def test_validate_access_point_invalid_coordinates(self):
        """Test validation with invalid coordinates."""
        ap = AccessPoint(lat=100, lon=200)
        
        errors = validate_access_point(ap)
        assert len(errors) > 0
        assert any("coordinates" in error.lower() for error in errors)
    
    def test_validate_access_point_negative_download(self):
        """Test validation with negative download speed."""
        ap = AccessPoint(lat=0, lon=0, download=-10)
        
        errors = validate_access_point(ap)
        assert len(errors) > 0
        assert any("download" in error.lower() for error in errors)
    
    def test_validate_access_point_negative_upload(self):
        """Test validation with negative upload speed."""
        ap = AccessPoint(lat=0, lon=0, upload=-5)
        
        errors = validate_access_point(ap)
        assert len(errors) > 0
        assert any("upload" in error.lower() for error in errors)
    
    def test_validate_access_point_negative_latency(self):
        """Test validation with negative latency."""
        ap = AccessPoint(lat=0, lon=0, latency=-1)
        
        errors = validate_access_point(ap)
        assert len(errors) > 0
        assert any("latency" in error.lower() for error in errors)
    
    def test_validate_access_point_invalid_stability(self):
        """Test validation with invalid stability."""
        ap = AccessPoint(lat=0, lon=0, stability=150)
        
        errors = validate_access_point(ap)
        assert len(errors) > 0
        assert any("stability" in error.lower() for error in errors)


class TestDataManagement:
    """Test cases for data management functions."""
    
    def test_save_and_load_data(self):
        """Test saving and loading data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Create test data
            access_points = [
                AccessPoint(lat=-15.7801, lon=-47.9292, provider="Starlink"),
                AccessPoint(lat=-3.7319, lon=-38.5267, provider="Starlink")
            ]
            
            # Save
            result = save_data(access_points, temp_file)
            assert result is True
            
            # Load
            loaded_points = load_data(temp_file)
            assert len(loaded_points) == 2
            assert loaded_points[0].lat == -15.7801
            assert loaded_points[1].lat == -3.7319
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        result = load_data("/tmp/nonexistent_file_12345.json")
        assert result == []
    
    def test_backup_data(self):
        """Test creating backup."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            f.write('{"test": "data"}')
        
        try:
            backup_path = backup_data(temp_file)
            
            assert backup_path is not None
            assert os.path.exists(backup_path)
            
            # Cleanup backup
            if backup_path and os.path.exists(backup_path):
                os.remove(backup_path)
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_backup_nonexistent_file(self):
        """Test backup of non-existent file."""
        result = backup_data("/tmp/nonexistent_file_12345.json")
        assert result is None


class TestCSVOperations:
    """Test cases for CSV import/export."""
    
    def test_export_and_import_csv(self):
        """Test exporting and importing CSV."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Create test data
            access_points = [
                AccessPoint(
                    lat=-15.7801,
                    lon=-47.9292,
                    provider="Starlink",
                    address="Brasília, DF, Brazil",
                    download=150.5,
                    upload=20.3,
                    latency=25.0,
                    stability=98.5,
                    tags=["rural", "satellite"]
                )
            ]
            
            # Export
            result = export_csv(access_points, temp_file)
            assert result is True
            
            # Import
            imported_points = import_csv(temp_file)
            assert len(imported_points) == 1
            assert imported_points[0].lat == -15.7801
            assert imported_points[0].provider == "Starlink"
            assert "rural" in imported_points[0].tags
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_import_nonexistent_csv(self):
        """Test importing from non-existent CSV."""
        with pytest.raises(FileNotFoundError):
            import_csv("/tmp/nonexistent_file_12345.csv")


class TestReportGeneration:
    """Test cases for report generation."""
    
    def test_generate_report_txt(self):
        """Test generating text report."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            access_points = [
                AccessPoint(lat=-15.7801, lon=-47.9292, provider="Starlink", download=150.5)
            ]
            
            result = generate_report_txt(access_points, temp_file)
            assert result is True
            assert os.path.exists(temp_file)
            
            # Check content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "RURAL CONNECTIVITY MAPPER" in content
                assert "Starlink" in content
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_generate_report_json(self):
        """Test generating JSON report."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            access_points = [
                AccessPoint(lat=-15.7801, lon=-47.9292, provider="Starlink", download=150.5)
            ]
            
            result = generate_report_json(access_points, temp_file)
            assert result is True
            assert os.path.exists(temp_file)
            
            # Check content
            with open(temp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert 'generated_at' in data
                assert 'total_points' in data
                assert data['total_points'] == 1
                assert 'statistics' in data
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_generate_report_html(self):
        """Test generating HTML report."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            temp_file = f.name
        
        try:
            access_points = [
                AccessPoint(lat=-15.7801, lon=-47.9292, provider="Starlink", download=150.5)
            ]
            
            result = generate_report_html(access_points, temp_file)
            assert result is True
            assert os.path.exists(temp_file)
            
            # Check content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "<!DOCTYPE html>" in content
                assert "Rural Connectivity Mapper" in content
                assert "Starlink" in content
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_generate_empty_report(self):
        """Test generating report with no data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            result = generate_report_txt([], temp_file)
            assert result is True
            
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Nenhum ponto" in content or "Total de pontos: 0" in content
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestStatistics:
    """Test cases for statistics functions."""
    
    def test_get_provider_stats(self):
        """Test getting provider statistics."""
        access_points = [
            AccessPoint(lat=0, lon=0, provider="Starlink", download=100, upload=20, latency=25),
            AccessPoint(lat=0, lon=0, provider="Starlink", download=120, upload=25, latency=30),
            AccessPoint(lat=0, lon=0, provider="Other", download=50, upload=10, latency=50)
        ]
        
        stats = get_provider_stats(access_points)
        
        assert "Starlink" in stats
        assert "Other" in stats
        assert stats["Starlink"]["count"] == 2
        assert stats["Other"]["count"] == 1
        assert "avg_download" in stats["Starlink"]
        assert stats["Starlink"]["avg_download"] == 110.0
    
    def test_get_provider_stats_empty(self):
        """Test getting provider statistics with empty list."""
        stats = get_provider_stats([])
        assert stats == {}
    
    def test_is_platform_supported(self):
        """Test platform support check."""
        result = is_platform_supported()
        assert isinstance(result, bool)
