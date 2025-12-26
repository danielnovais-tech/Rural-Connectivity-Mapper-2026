"""Report generation utilities for various output formats."""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import logging

from src.models.connectivity_point import ConnectivityPoint

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate reports in various formats."""
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_txt_report(
        self, 
        points: List[ConnectivityPoint], 
        filename: str = None
    ) -> str:
        """
        Generate a text report.
        
        Args:
            points: List of ConnectivityPoint objects
            filename: Output filename (auto-generated if None)
        
        Returns:
            Path to generated report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RURAL CONNECTIVITY MAPPER 2026 - REPORT\n")
            f.write("Starlink Expansion Analysis for Brazil\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Points: {len(points)}\n\n")
            
            for idx, point in enumerate(points, 1):
                f.write(f"\n{'=' * 80}\n")
                f.write(f"Point #{idx}: {point.point_id}\n")
                f.write(f"{'=' * 80}\n")
                f.write(f"Location: ({point.latitude}, {point.longitude})\n")
                if point.address:
                    f.write(f"Address: {point.address}\n")
                if point.provider:
                    f.write(f"Provider: {point.provider}\n")
                if point.tags:
                    f.write(f"Tags: {', '.join(point.tags)}\n")
                f.write(f"Timestamp: {point.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if point.speed_tests:
                    f.write("Speed Tests:\n")
                    for st_idx, st in enumerate(point.speed_tests, 1):
                        f.write(f"  Test #{st_idx}:\n")
                        f.write(f"    Download: {st.download_speed:.2f} Mbps\n")
                        f.write(f"    Upload: {st.upload_speed:.2f} Mbps\n")
                        f.write(f"    Latency: {st.latency:.2f} ms\n")
                        if st.jitter:
                            f.write(f"    Jitter: {st.jitter:.2f} ms\n")
                        f.write(f"    Stability: {st.calculate_stability():.1f}%\n")
                        if st.server:
                            f.write(f"    Server: {st.server}\n")
                    f.write("\n")
                
                if point.quality_score:
                    f.write("Quality Score:\n")
                    f.write(f"  Overall: {point.quality_score.overall_score:.1f}/100 ({point.quality_score.get_rating()})\n")
                    f.write(f"  Speed: {point.quality_score.speed_score:.1f}/100\n")
                    f.write(f"  Latency: {point.quality_score.latency_score:.1f}/100\n")
                    f.write(f"  Stability: {point.quality_score.stability_score:.1f}/100\n")
        
        logger.info(f"Generated TXT report: {filepath}")
        return str(filepath)
    
    def generate_json_report(
        self, 
        points: List[ConnectivityPoint], 
        filename: str = None
    ) -> str:
        """
        Generate a JSON report.
        
        Args:
            points: List of ConnectivityPoint objects
            filename: Output filename (auto-generated if None)
        
        Returns:
            Path to generated report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        report_data = {
            "generated": datetime.now().isoformat(),
            "total_points": len(points),
            "points": [point.to_dict() for point in points]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated JSON report: {filepath}")
        return str(filepath)
    
    def generate_csv_report(
        self, 
        points: List[ConnectivityPoint], 
        filename: str = None
    ) -> str:
        """
        Generate a CSV report.
        
        Args:
            points: List of ConnectivityPoint objects
            filename: Output filename (auto-generated if None)
        
        Returns:
            Path to generated report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'point_id', 'latitude', 'longitude', 'address', 'provider', 'tags',
                'timestamp', 'avg_download_mbps', 'avg_upload_mbps', 'avg_latency_ms',
                'avg_stability', 'quality_score', 'quality_rating', 'num_tests'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for point in points:
                # Calculate averages
                if point.speed_tests:
                    avg_download = sum(st.download_speed for st in point.speed_tests) / len(point.speed_tests)
                    avg_upload = sum(st.upload_speed for st in point.speed_tests) / len(point.speed_tests)
                    avg_latency = sum(st.latency for st in point.speed_tests) / len(point.speed_tests)
                    avg_stability = sum(st.calculate_stability() for st in point.speed_tests) / len(point.speed_tests)
                else:
                    avg_download = avg_upload = avg_latency = avg_stability = 0
                
                writer.writerow({
                    'point_id': point.point_id,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'address': point.address or '',
                    'provider': point.provider or '',
                    'tags': ','.join(point.tags) if point.tags else '',
                    'timestamp': point.timestamp.isoformat(),
                    'avg_download_mbps': f"{avg_download:.2f}",
                    'avg_upload_mbps': f"{avg_upload:.2f}",
                    'avg_latency_ms': f"{avg_latency:.2f}",
                    'avg_stability': f"{avg_stability:.1f}",
                    'quality_score': f"{point.quality_score.overall_score:.1f}" if point.quality_score else '',
                    'quality_rating': point.quality_score.get_rating() if point.quality_score else '',
                    'num_tests': len(point.speed_tests)
                })
        
        logger.info(f"Generated CSV report: {filepath}")
        return str(filepath)
    
    def generate_html_report(
        self, 
        points: List[ConnectivityPoint], 
        filename: str = None
    ) -> str:
        """
        Generate an HTML report.
        
        Args:
            points: List of ConnectivityPoint objects
            filename: Output filename (auto-generated if None)
        
        Returns:
            Path to generated report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = self.output_dir / filename
        
        html_content = self._generate_html_content(points)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Generated HTML report: {filepath}")
        return str(filepath)
    
    def _generate_html_content(self, points: List[ConnectivityPoint]) -> str:
        """Generate HTML content for the report."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rural Connectivity Mapper 2026 - Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .summary {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .point {
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .point h2 {
            color: #4CAF50;
            margin-top: 0;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
        }
        .metric-label {
            font-weight: bold;
            color: #666;
        }
        .quality-excellent { color: #4CAF50; }
        .quality-good { color: #8BC34A; }
        .quality-fair { color: #FFC107; }
        .quality-poor { color: #FF9800; }
        .quality-very-poor { color: #F44336; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        .tags {
            display: inline-block;
            background-color: #e0e0e0;
            padding: 3px 8px;
            border-radius: 3px;
            margin: 2px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Rural Connectivity Mapper 2026</h1>
    <div class="summary">
        <h2>Report Summary</h2>
        <p><strong>Generated:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p><strong>Total Points:</strong> """ + str(len(points)) + """</p>
        <p><strong>Purpose:</strong> Starlink Expansion Analysis for Brazil</p>
    </div>
"""
        
        for idx, point in enumerate(points, 1):
            quality_class = ""
            if point.quality_score:
                rating = point.quality_score.get_rating().lower().replace(" ", "-")
                quality_class = f"quality-{rating}"
            
            html += f"""
    <div class="point">
        <h2>Point #{idx}: {point.point_id}</h2>
        <div>
            <div class="metric">
                <span class="metric-label">Location:</span> ({point.latitude}, {point.longitude})
            </div>
"""
            if point.address:
                html += f"""
            <div class="metric">
                <span class="metric-label">Address:</span> {point.address}
            </div>
"""
            if point.provider:
                html += f"""
            <div class="metric">
                <span class="metric-label">Provider:</span> {point.provider}
            </div>
"""
            if point.tags:
                html += """
            <div class="metric">
                <span class="metric-label">Tags:</span> """
                for tag in point.tags:
                    html += f'<span class="tags">{tag}</span>'
                html += """
            </div>
"""
            html += f"""
            <div class="metric">
                <span class="metric-label">Timestamp:</span> {point.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
"""
            
            if point.speed_tests:
                html += """
        <h3>Speed Tests</h3>
        <table>
            <tr>
                <th>#</th>
                <th>Download (Mbps)</th>
                <th>Upload (Mbps)</th>
                <th>Latency (ms)</th>
                <th>Stability (%)</th>
                <th>Server</th>
            </tr>
"""
                for st_idx, st in enumerate(point.speed_tests, 1):
                    html += f"""
            <tr>
                <td>{st_idx}</td>
                <td>{st.download_speed:.2f}</td>
                <td>{st.upload_speed:.2f}</td>
                <td>{st.latency:.2f}</td>
                <td>{st.calculate_stability():.1f}</td>
                <td>{st.server or 'N/A'}</td>
            </tr>
"""
                html += """
        </table>
"""
            
            if point.quality_score:
                html += f"""
        <h3>Quality Score</h3>
        <div>
            <div class="metric">
                <span class="metric-label">Overall:</span> 
                <span class="{quality_class}">{point.quality_score.overall_score:.1f}/100 ({point.quality_score.get_rating()})</span>
            </div>
            <div class="metric">
                <span class="metric-label">Speed:</span> {point.quality_score.speed_score:.1f}/100
            </div>
            <div class="metric">
                <span class="metric-label">Latency:</span> {point.quality_score.latency_score:.1f}/100
            </div>
            <div class="metric">
                <span class="metric-label">Stability:</span> {point.quality_score.stability_score:.1f}/100
            </div>
        </div>
"""
            
            html += """
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def generate_all_reports(self, points: List[ConnectivityPoint]) -> Dict[str, str]:
        """
        Generate all report formats.
        
        Args:
            points: List of ConnectivityPoint objects
        
        Returns:
            Dictionary mapping format to filepath
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return {
            'txt': self.generate_txt_report(points, f"report_{timestamp}.txt"),
            'json': self.generate_json_report(points, f"report_{timestamp}.json"),
            'csv': self.generate_csv_report(points, f"report_{timestamp}.csv"),
            'html': self.generate_html_report(points, f"report_{timestamp}.html")
        }
