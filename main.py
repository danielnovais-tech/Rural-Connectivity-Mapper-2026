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
    generate_map, analyze_temporal_evolution, validate_coordinates,

    list_available_countries, get_default_country

    export_for_hybrid_simulator, export_for_agrix_boost, export_ecosystem_bundle

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


def import_csv(csv_path: str, output_path: str = 'src/data/pontos.json', country_code: str = None) -> None:
    """Import connectivity data from CSV file.
    
    Args:
        csv_path: Path to CSV file
        output_path: Path to save JSON data
        country_code: ISO country code for the data (default: uses default country)
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Importing data from {csv_path}...")
    
    if country_code is None:
        country_code = get_default_country()
    
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
                    packet_loss=float(row.get('packet_loss', 0)),
                    obstruction=float(row.get('obstruction', 0))
                )
                
                # Create ConnectivityPoint
                point = ConnectivityPoint(
                    latitude=lat,
                    longitude=lon,
                    provider=row['provider'],
                    speed_test=speed_test,
                    timestamp=row.get('timestamp', datetime.now().isoformat()),
                    point_id=row.get('id'),
                    country=row.get('country', country_code)
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
        description='Rural Connectivity Mapper 2026 - Analyze rural connectivity worldwide',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --debug --importar src/data/sample_data.csv --relatorio json
  %(prog)s --simulate --map --country US
  %(prog)s --analyze --relatorio html --country CA
  %(prog)s --list-countries
        """
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with verbose logging'
    )
    
    parser.add_argument(
        '--country',
        metavar='CODE',
        help='ISO country code (e.g., BR, US, CA, GB). Use --list-countries to see all available.'
    )
    
    parser.add_argument(
        '--list-countries',
        action='store_true',
        help='List all available country codes and exit'
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
        '--no-starlink-coverage',
        action='store_true',
        help='Disable Starlink coverage overlay on the map'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze temporal evolution'
    )
    
    parser.add_argument(

        '--language',
        '--lang',
        choices=['en', 'pt'],
        default='en',
        help='Language for reports and analysis output (en=English, pt=Portuguese)'

        '--export',
        choices=['hybrid', 'agrix', 'ecosystem'],
        help='Export data for ecosystem integration (hybrid=Hybrid Architecture Simulator, agrix=AgriX-Boost, ecosystem=Full bundle)'

    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    # Handle list-countries command
    if args.list_countries:
        countries = list_available_countries()
        print("\nAvailable country codes:")
        print("=" * 50)
        from src.utils.config_utils import get_country_info
        for code in sorted(countries):
            info = get_country_info(code)
            print(f"  {code}: {info['name']}")
        print("=" * 50)
        sys.exit(0)
    
    logger.info("Rural Connectivity Mapper 2026 - Starting")
    
    # Get country code
    country_code = args.country if args.country else get_default_country()
    logger.info(f"Using country: {country_code}")
    
    # Check if any action was specified
    if not any([args.importar, args.relatorio, args.simulate, args.map, args.analyze, args.export]):
        parser.print_help()
        sys.exit(0)
    
    data_path = 'src/data/pontos.json'
    
    # Import CSV data
    if args.importar:
        import_csv(args.importar, data_path, country_code)
    
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
        analysis = analyze_temporal_evolution(data, args.language)
        
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
        report_path = generate_report(data, args.relatorio, language=args.language)
        logger.info(f"Report generated: {report_path}")
    
    # Generate map
    # Note: Map generation does not currently support multilingual features
    if args.map:
        logger.info("Generating interactive map...")

        map_path = generate_map(data, country_code=country_code)

        include_coverage = not args.no_starlink_coverage
        if include_coverage:
            logger.info("Including Starlink coverage overlay layer")
        map_path = generate_map(data, include_starlink_coverage=include_coverage)

        logger.info(f"Map generated: {map_path}")
    
    # Export for ecosystem integration
    if args.export:
        logger.info(f"Exporting data for ecosystem integration ({args.export})...")
        
        if args.export == 'hybrid':
            export_path = export_for_hybrid_simulator(data)
            logger.info(f"Exported for Hybrid Architecture Simulator: {export_path}")
            print(f"\n✓ Data exported for Hybrid Architecture Simulator: {export_path}")
        
        elif args.export == 'agrix':
            export_path = export_for_agrix_boost(data)
            logger.info(f"Exported for AgriX-Boost: {export_path}")
            print(f"\n✓ Data exported for AgriX-Boost: {export_path}")
        
        elif args.export == 'ecosystem':
            export_paths = export_ecosystem_bundle(data)
            logger.info("Exported complete ecosystem bundle")
            print("\n" + "=" * 80)
            print("ECOSYSTEM BUNDLE EXPORTED")
            print("=" * 80)
            print(f"  Hybrid Architecture Simulator: {export_paths['hybrid_simulator']}")
            print(f"  AgriX-Boost: {export_paths['agrix_boost']}")
            print(f"  Ecosystem Manifest: {export_paths['manifest']}")
            print("=" * 80 + "\n")
    
    logger.info("Rural Connectivity Mapper 2026 - Completed successfully")


if __name__ == '__main__':
    main()
