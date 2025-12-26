#!/usr/bin/env python3
"""
Rural Connectivity Mapper 2026
Main CLI application for mapping and analyzing rural internet connectivity in Brazil.
Aligned with Starlink's 2026 roadmap.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List
import json

from src.models.connectivity_point import ConnectivityPoint
from src.utils.geocoding import geocode_address, reverse_geocode
from src.utils.speed_testing import run_speed_test
from src.utils.quality_calculator import calculate_quality_score
from src.utils.report_generator import ReportGenerator
from src.utils.csv_handler import import_from_csv, export_to_csv
from src.utils.data_analysis import (
    analyze_temporal_trends,
    compare_providers,
    get_summary_statistics
)


def setup_logging(debug: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def create_point_interactive() -> ConnectivityPoint:
    """Create a connectivity point interactively."""
    print("\n=== Create New Connectivity Point ===")
    
    # Get location
    use_address = input("Enter address? (y/n): ").strip().lower() == 'y'
    
    if use_address:
        address = input("Enter address: ").strip()
        coords = geocode_address(address)
        if coords:
            latitude, longitude = coords
            print(f"Geocoded to: ({latitude}, {longitude})")
        else:
            print("Could not geocode address. Please enter coordinates manually.")
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            address = None
    else:
        latitude = float(input("Enter latitude: "))
        longitude = float(input("Enter longitude: "))
        address = reverse_geocode(latitude, longitude)
        if address:
            print(f"Address: {address}")
    
    # Get provider
    provider = input("Enter provider name (optional): ").strip() or None
    
    # Get tags
    tags_input = input("Enter tags (comma-separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
    
    point = ConnectivityPoint(
        latitude=latitude,
        longitude=longitude,
        address=address,
        provider=provider,
        tags=tags
    )
    
    print(f"\nCreated point: {point}")
    return point


def run_tests(point: ConnectivityPoint, num_tests: int = 1) -> None:
    """Run speed tests for a connectivity point."""
    print(f"\n=== Running {num_tests} Speed Test(s) ===")
    
    for i in range(num_tests):
        if num_tests > 1:
            print(f"\nTest {i+1}/{num_tests}...")
        
        speed_test = run_speed_test()
        if speed_test:
            point.add_speed_test(speed_test)
            print(f"Download: {speed_test.download_speed:.2f} Mbps")
            print(f"Upload: {speed_test.upload_speed:.2f} Mbps")
            print(f"Latency: {speed_test.latency:.2f} ms")
            print(f"Stability: {speed_test.calculate_stability():.1f}%")
        else:
            print("Speed test failed.")
    
    # Calculate quality score
    if point.speed_tests:
        point.quality_score = calculate_quality_score(point.speed_tests)
        print(f"\nQuality Score: {point.quality_score}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Rural Connectivity Mapper 2026 - Starlink expansion analysis for Brazil',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new point interactively
  python main.py --interactive

  # Import points from CSV
  python main.py --import data/points.csv

  # Generate reports from existing data
  python main.py --import data/points.json --report --output reports/

  # Analyze provider comparison
  python main.py --import data/points.json --analyze providers

  # Debug mode
  python main.py --interactive --debug
        """
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode to create and test points'
    )
    parser.add_argument(
        '--import',
        dest='import_file',
        help='Import points from CSV or JSON file'
    )
    parser.add_argument(
        '--export',
        dest='export_file',
        help='Export points to CSV file'
    )
    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help='Generate reports (TXT, JSON, CSV, HTML)'
    )
    parser.add_argument(
        '--output', '-o',
        default='reports',
        help='Output directory for reports (default: reports)'
    )
    parser.add_argument(
        '--analyze', '-a',
        choices=['temporal', 'providers', 'summary'],
        help='Run analysis: temporal trends, provider comparison, or summary statistics'
    )
    parser.add_argument(
        '--num-tests', '-n',
        type=int,
        default=1,
        help='Number of speed tests to run per point (default: 1)'
    )
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    logger.info("Rural Connectivity Mapper 2026 started")
    
    points: List[ConnectivityPoint] = []
    
    # Import data
    if args.import_file:
        import_path = Path(args.import_file)
        if not import_path.exists():
            logger.error(f"Import file not found: {import_path}")
            sys.exit(1)
        
        if import_path.suffix == '.csv':
            points = import_from_csv(str(import_path))
        elif import_path.suffix == '.json':
            with open(import_path, 'r') as f:
                data = json.load(f)
                points = [ConnectivityPoint.from_dict(p) for p in data.get('points', [])]
        else:
            logger.error("Unsupported import format. Use .csv or .json")
            sys.exit(1)
        
        logger.info(f"Imported {len(points)} points")
    
    # Interactive mode
    if args.interactive:
        while True:
            point = create_point_interactive()
            points.append(point)
            
            # Run tests
            run_tests_choice = input("\nRun speed test? (y/n): ").strip().lower()
            if run_tests_choice == 'y':
                run_tests(point, args.num_tests)
            
            # Continue?
            continue_choice = input("\nAdd another point? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break
    
    # Export data
    if args.export_file:
        export_to_csv(points, args.export_file)
        logger.info(f"Exported to {args.export_file}")
    
    # Generate reports
    if args.report and points:
        reporter = ReportGenerator(args.output)
        report_files = reporter.generate_all_reports(points)
        
        print("\n=== Generated Reports ===")
        for format_type, filepath in report_files.items():
            print(f"{format_type.upper()}: {filepath}")
    
    # Run analysis
    if args.analyze and points:
        print("\n=== Analysis Results ===")
        
        if args.analyze == 'temporal':
            results = analyze_temporal_trends(points)
            print(json.dumps(results, indent=2))
        
        elif args.analyze == 'providers':
            results = compare_providers(points)
            print(json.dumps(results, indent=2))
        
        elif args.analyze == 'summary':
            results = get_summary_statistics(points)
            print(json.dumps(results, indent=2))
    
    # Summary
    if points:
        print(f"\n=== Summary ===")
        print(f"Total points: {len(points)}")
        print(f"Total speed tests: {sum(len(p.speed_tests) for p in points)}")
        
        quality_scores = [p.quality_score.overall_score for p in points if p.quality_score]
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            print(f"Average quality score: {avg_quality:.1f}/100")
    
    logger.info("Rural Connectivity Mapper 2026 completed")


if __name__ == '__main__':
    main()
