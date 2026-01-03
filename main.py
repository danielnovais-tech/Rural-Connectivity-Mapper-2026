#!/usr/bin/env python3
"""Main CLI application for Rural Connectivity Mapper 2026."""

import argparse
import logging
import sys
from pathlib import Path
import csv
from datetime import datetime

from src.models import ConnectivityPoint, SpeedTest, QualityScore
from src.utils import (
    load_data, save_data, generate_report, simulate_router_impact,
    generate_map, analyze_temporal_evolution, validate_coordinates
)


def setup_logging(debug: bool = False) -> None:
    """Configure logging settings.
    
    Args:
        debug: Enable debug level logging if True
    """
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def import_csv(csv_path: str, output_path: str = 'src/data/pontos.json') -> None:
    """Import connectivity data from CSV file.
    
    Args:
        csv_path: Path to CSV file
        output_path: Path to save JSON data
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Importing data from {csv_path}...")
    
    try:
        points = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Validate coordinates
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                
                if not validate_coordinates(lat, lon):
                    logger.warning(f"Skipping row with invalid coordinates: {row}")
                    continue
                
                # Create SpeedTest
                speed_test = SpeedTest(
                    download=float(row['download']),
                    upload=float(row['upload']),
                    latency=float(row['latency']),
                    jitter=float(row.get('jitter', 0)),
                    packet_loss=float(row.get('packet_loss', 0))
                )
                
                # Create ConnectivityPoint
                point = ConnectivityPoint(
                    latitude=lat,
                    longitude=lon,
                    provider=row['provider'],
                    speed_test=speed_test,
                    timestamp=row.get('timestamp', datetime.now().isoformat()),
                    point_id=row.get('id')
                )
                
                points.append(point.to_dict())
                logger.debug(f"Imported point: {point}")
        
        # Save to JSON
        save_data(output_path, points)
        logger.info(f"Successfully imported {len(points)} points to {output_path}")
    
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error importing CSV: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Rural Connectivity Mapper 2026 - Analyze Starlink expansion in Brazil',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --debug --importar src/data/sample_data.csv --relatorio json
  %(prog)s --simulate --map
  %(prog)s --analyze --relatorio html
        """
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with verbose logging'
    )
    
    parser.add_argument(
        '--relatorio',
        choices=['json', 'csv', 'txt', 'html'],
        help='Generate report in specified format'
    )
    
    parser.add_argument(
        '--importar',
        metavar='CSV',
        help='Import data from CSV file'
    )
    
    parser.add_argument(
        '--simulate',
        action='store_true',
        help='Simulate router impact on quality scores'
    )
    
    parser.add_argument(
        '--map',
        action='store_true',
        help='Generate interactive Folium map'
    )
    
    parser.add_argument(
        '--starlink-coverage',
        action='store_true',
        help='Add Starlink coverage overlay to the map (requires --map)'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze temporal evolution'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    logger.info("Rural Connectivity Mapper 2026 - Starting")
    
    # Check if any action was specified
    if not any([args.importar, args.relatorio, args.simulate, args.map, args.analyze]):
        parser.print_help()
        sys.exit(0)
    
    data_path = 'src/data/pontos.json'
    
    # Import CSV data
    if args.importar:
        import_csv(args.importar, data_path)
    
    # Load existing data
    data = load_data(data_path)
    
    if not data:
        logger.warning("No data available. Import data first with --importar")
        if not args.importar:
            sys.exit(1)
    
    # Simulate router impact
    if args.simulate:
        logger.info("Simulating router impact...")
        data = simulate_router_impact(data)
        save_data(data_path, data)
        logger.info("Router impact simulation completed and saved")
    
    # Analyze temporal evolution
    if args.analyze:
        logger.info("Analyzing temporal evolution...")
        analysis = analyze_temporal_evolution(data)
        
        print("\n" + "=" * 80)
        print("TEMPORAL ANALYSIS RESULTS")
        print("=" * 80)
        print(f"\nTotal Points: {analysis['total_points']}")
        print(f"Date Range: {analysis['date_range'].get('start', 'N/A')} to {analysis['date_range'].get('end', 'N/A')}")
        print(f"\nOverall Trends:")
        print(f"  Average Quality Score: {analysis['trends']['avg_quality_score']}/100")
        print(f"  Average Download: {analysis['trends']['avg_download']} Mbps")
        print(f"  Average Latency: {analysis['trends']['avg_latency']} ms")
        print(f"\nInsights:")
        for insight in analysis['insights']:
            print(f"  • {insight}")
        print("=" * 80 + "\n")
    
    # Generate report
    if args.relatorio:
        logger.info(f"Generating {args.relatorio.upper()} report...")
        report_path = generate_report(data, args.relatorio)
        logger.info(f"Report generated: {report_path}")
    
    # Generate map
    if args.map:
        logger.info("Generating interactive map...")
        map_path = generate_map(data, show_starlink_coverage=args.starlink_coverage)
        logger.info(f"Map generated: {map_path}")
        if args.starlink_coverage:
            logger.info("Starlink coverage overlay enabled")
    
    logger.info("Rural Connectivity Mapper 2026 - Completed successfully")


if __name__ == '__main__':
    main()
