"""Tests for utility modules."""

import pytest
from pathlib import Path
import tempfile
import os

from src.models.connectivity_point import ConnectivityPoint
from src.models.speed_test import SpeedTest
from src.utils.quality_calculator import (
    calculate_speed_score,
    calculate_latency_score,
    calculate_quality_score
)
from src.utils.csv_handler import export_to_csv, import_from_csv
from src.utils.report_generator import ReportGenerator
from src.utils.data_analysis import (
    compare_providers,
    get_summary_statistics
)


class TestQualityCalculator:
    """Test quality calculation utilities."""
    
    def test_calculate_speed_score(self):
        """Test speed score calculation."""
        # Perfect speeds
        score = calculate_speed_score(200, 20)
        assert score == 100.0
        
        # Half of optimal
        score = calculate_speed_score(100, 10)
        assert 40 <= score <= 60
    
    def test_calculate_latency_score(self):
        """Test latency score calculation."""
        # Excellent latency
        score = calculate_latency_score(15)
        assert score == 100.0
        
        # Good latency
        score = calculate_latency_score(30)
        assert 70 <= score <= 90
    
    def test_calculate_quality_score(self):
        """Test overall quality score calculation."""
        speed_tests = [
            SpeedTest(150, 15, 25),
            SpeedTest(160, 18, 22)
        ]
        
        quality = calculate_quality_score(speed_tests)
        assert 0 <= quality.overall_score <= 100
        assert quality.get_rating() in ["Excellent", "Good", "Fair", "Poor", "Very Poor"]


class TestCSVHandler:
    """Test CSV import/export."""
    
    def test_export_import_csv(self):
        """Test CSV export and import."""
        # Create test points
        points = [
            ConnectivityPoint(
                latitude=-23.5505,
                longitude=-46.6333,
                address="São Paulo",
                provider="Starlink",
                tags=["rural", "test"]
            ),
            ConnectivityPoint(
                latitude=-22.9068,
                longitude=-43.1729,
                address="Rio de Janeiro",
                provider="Starlink"
            )
        ]
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            temp_path = f.name
        
        try:
            export_to_csv(points, temp_path)
            
            # Import back
            imported_points = import_from_csv(temp_path)
            
            assert len(imported_points) == 2
            assert imported_points[0].latitude == -23.5505
            assert imported_points[0].provider == "Starlink"
            assert "rural" in imported_points[0].tags
        
        finally:
            os.unlink(temp_path)


class TestReportGenerator:
    """Test report generation."""
    
    def test_generate_txt_report(self):
        """Test TXT report generation."""
        points = [
            ConnectivityPoint(
                latitude=-23.5505,
                longitude=-46.6333,
                provider="Starlink"
            )
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            reporter = ReportGenerator(temp_dir)
            filepath = reporter.generate_txt_report(points)
            
            assert Path(filepath).exists()
            assert Path(filepath).suffix == '.txt'
    
    def test_generate_json_report(self):
        """Test JSON report generation."""
        points = [
            ConnectivityPoint(
                latitude=-23.5505,
                longitude=-46.6333,
                provider="Starlink"
            )
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            reporter = ReportGenerator(temp_dir)
            filepath = reporter.generate_json_report(points)
            
            assert Path(filepath).exists()
            assert Path(filepath).suffix == '.json'
    
    def test_generate_all_reports(self):
        """Test generating all report formats."""
        points = [
            ConnectivityPoint(
                latitude=-23.5505,
                longitude=-46.6333
            )
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            reporter = ReportGenerator(temp_dir)
            reports = reporter.generate_all_reports(points)
            
            assert 'txt' in reports
            assert 'json' in reports
            assert 'csv' in reports
            assert 'html' in reports
            
            for filepath in reports.values():
                assert Path(filepath).exists()


class TestDataAnalysis:
    """Test data analysis utilities."""
    
    def test_compare_providers(self):
        """Test provider comparison."""
        points = [
            ConnectivityPoint(latitude=-23.5505, longitude=-46.6333, provider="Starlink"),
            ConnectivityPoint(latitude=-22.9068, longitude=-43.1729, provider="Viasat"),
            ConnectivityPoint(latitude=-15.7801, longitude=-47.9292, provider="Starlink")
        ]
        
        # Add speed tests
        for point in points:
            point.add_speed_test(SpeedTest(100, 20, 30))
        
        comparison = compare_providers(points)
        
        assert "Starlink" in comparison
        assert "Viasat" in comparison
        assert comparison["Starlink"]["num_points"] == 2
        assert comparison["Viasat"]["num_points"] == 1
    
    def test_get_summary_statistics(self):
        """Test summary statistics."""
        points = [
            ConnectivityPoint(latitude=-23.5505, longitude=-46.6333, provider="Starlink"),
            ConnectivityPoint(latitude=-22.9068, longitude=-43.1729, provider="Viasat")
        ]
        
        # Add speed tests
        for point in points:
            point.add_speed_test(SpeedTest(100, 20, 30))
            point.quality_score = calculate_quality_score(point.speed_tests)
        
        stats = get_summary_statistics(points)
        
        assert stats["total_points"] == 2
        assert stats["num_providers"] == 2
        assert "quality_scores" in stats
        assert "download_speeds" in stats
