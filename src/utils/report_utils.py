"""Report generation utilities for multi-format output."""

import json
import logging
from typing import List, Dict
from pathlib import Path
from datetime import datetime
import csv

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

logger = logging.getLogger(__name__)


def generate_report(data: List[Dict], format: str, output_path: str = None) -> str:
    """Generate report in specified format.
    
    Args:
        data: List of connectivity point dictionaries
        format: Report format (json, csv, txt, html)
        output_path: Optional output file path
        
    Returns:
        str: Path to generated report file or report content
        
    Raises:
        ValueError: If format is not supported
    """
    format = format.lower()
    
    if format == 'json':
        return _generate_json_report(data, output_path)
    elif format == 'csv':
        return _generate_csv_report(data, output_path)
    elif format == 'txt':
        return _generate_txt_report(data, output_path)
    elif format == 'html':
        return _generate_html_report(data, output_path)
    else:
        raise ValueError(f"Unsupported format: {format}. Use json, csv, txt, or html.")


def _generate_json_report(data: List[Dict], output_path: str = None) -> str:
    """Generate JSON format report."""
    try:
        if output_path is None:
            output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON report generated: {path}")
        return str(path)
    except Exception as e:
        logger.error(f"Error generating JSON report: {e}")
        raise


def _generate_csv_report(data: List[Dict], output_path: str = None) -> str:
    """Generate CSV format report."""
    try:
        if output_path is None:
            output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if not data:
            logger.warning("No data to write to CSV")
            with open(path, 'w', encoding='utf-8') as f:
                f.write("")
            return str(path)
        
        # Flatten nested dictionaries for CSV
        flattened_data = []
        for point in data:
            flat = {
                'id': point.get('id', ''),
                'latitude': point.get('latitude', ''),
                'longitude': point.get('longitude', ''),
                'provider': point.get('provider', ''),
                'timestamp': point.get('timestamp', ''),
            }
            
            # Add speed test data
            if 'speed_test' in point:
                st = point['speed_test']
                flat.update({
                    'download': st.get('download', ''),
                    'upload': st.get('upload', ''),
                    'latency': st.get('latency', ''),
                    'jitter': st.get('jitter', ''),
                    'packet_loss': st.get('packet_loss', ''),
                    'stability': st.get('stability', ''),
                })
            
            # Add quality score data
            if 'quality_score' in point:
                qs = point['quality_score']
                flat.update({
                    'overall_score': qs.get('overall_score', ''),
                    'speed_score': qs.get('speed_score', ''),
                    'latency_score': qs.get('latency_score', ''),
                    'stability_score': qs.get('stability_score', ''),
                    'rating': qs.get('rating', ''),
                })
            
            flattened_data.append(flat)
        
        # Write CSV
        with open(path, 'w', encoding='utf-8', newline='') as f:
            if flattened_data:
                writer = csv.DictWriter(f, fieldnames=flattened_data[0].keys())
                writer.writeheader()
                writer.writerows(flattened_data)
        
        logger.info(f"CSV report generated: {path}")
        return str(path)
    except Exception as e:
        logger.error(f"Error generating CSV report: {e}")
        raise


def _generate_txt_report(data: List[Dict], output_path: str = None) -> str:
    """Generate TXT format report with color."""
    try:
        if output_path is None:
            output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        lines = []
        lines.append("=" * 80)
        lines.append("RURAL CONNECTIVITY MAPPER 2026 - REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        lines.append(f"\nTotal Points: {len(data)}\n")
        
        for i, point in enumerate(data, 1):
            lines.append(f"\n--- Point {i} ---")
            lines.append(f"ID: {point.get('id', 'N/A')}")
            lines.append(f"Location: ({point.get('latitude', 'N/A')}, {point.get('longitude', 'N/A')})")
            lines.append(f"Provider: {point.get('provider', 'N/A')}")
            lines.append(f"Timestamp: {point.get('timestamp', 'N/A')}")
            
            if 'speed_test' in point:
                st = point['speed_test']
                lines.append("\nSpeed Test:")
                lines.append(f"  Download: {st.get('download', 'N/A')} Mbps")
                lines.append(f"  Upload: {st.get('upload', 'N/A')} Mbps")
                lines.append(f"  Latency: {st.get('latency', 'N/A')} ms")
                lines.append(f"  Stability: {st.get('stability', 'N/A')}/100")
            
            if 'quality_score' in point:
                qs = point['quality_score']
                lines.append("\nQuality Score:")
                lines.append(f"  Overall: {qs.get('overall_score', 'N/A')}/100")
                lines.append(f"  Rating: {qs.get('rating', 'N/A')}")
        
        lines.append("\n" + "=" * 80)
        
        report_text = "\n".join(lines)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        # Print colored version to console if colorama is available
        if COLORAMA_AVAILABLE:
            print(Fore.CYAN + report_text)
        
        logger.info(f"TXT report generated: {path}")
        return str(path)
    except Exception as e:
        logger.error(f"Error generating TXT report: {e}")
        raise


def _generate_html_report(data: List[Dict], output_path: str = None) -> str:
    """Generate HTML format report."""
    try:
        if output_path is None:
            output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("<meta charset='utf-8'>")
        html.append("<title>Rural Connectivity Mapper 2026 - Report</title>")
        html.append("<style>")
        html.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        html.append("h1 { color: #2c3e50; }")
        html.append("table { border-collapse: collapse; width: 100%; margin-top: 20px; }")
        html.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
        html.append("th { background-color: #3498db; color: white; }")
        html.append("tr:nth-child(even) { background-color: #f2f2f2; }")
        html.append(".excellent { color: green; font-weight: bold; }")
        html.append(".good { color: blue; font-weight: bold; }")
        html.append(".fair { color: orange; font-weight: bold; }")
        html.append(".poor { color: red; font-weight: bold; }")
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        html.append("<h1>Rural Connectivity Mapper 2026 - Report</h1>")
        html.append(f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        html.append(f"<p>Total Points: {len(data)}</p>")
        
        html.append("<table>")
        html.append("<tr>")
        html.append("<th>Provider</th>")
        html.append("<th>Location</th>")
        html.append("<th>Download (Mbps)</th>")
        html.append("<th>Upload (Mbps)</th>")
        html.append("<th>Latency (ms)</th>")
        html.append("<th>Overall Score</th>")
        html.append("<th>Rating</th>")
        html.append("</tr>")
        
        for point in data:
            html.append("<tr>")
            html.append(f"<td>{point.get('provider', 'N/A')}</td>")
            html.append(f"<td>{point.get('latitude', 'N/A')}, {point.get('longitude', 'N/A')}</td>")
            
            st = point.get('speed_test', {})
            html.append(f"<td>{st.get('download', 'N/A')}</td>")
            html.append(f"<td>{st.get('upload', 'N/A')}</td>")
            html.append(f"<td>{st.get('latency', 'N/A')}</td>")
            
            qs = point.get('quality_score', {})
            html.append(f"<td>{qs.get('overall_score', 'N/A')}</td>")
            
            rating = qs.get('rating', 'N/A')
            rating_class = rating.lower() if rating != 'N/A' else ''
            html.append(f"<td class='{rating_class}'>{rating}</td>")
            
            html.append("</tr>")
        
        html.append("</table>")
        html.append("</body>")
        html.append("</html>")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(html))
        
        logger.info(f"HTML report generated: {path}")
        return str(path)
    except Exception as e:
        logger.error(f"Error generating HTML report: {e}")
        raise
