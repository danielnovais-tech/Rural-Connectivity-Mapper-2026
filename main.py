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
    generate_ml_report
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
        '--analyze',
        action='store_true',
        help='Analyze temporal evolution'
    )
    
    parser.add_argument(
        '--ml-analyze',
        action='store_true',
        help='Perform ML-enhanced geospatial analysis for rural connectivity and Starlink expansion'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    logger.info("Rural Connectivity Mapper 2026 - Starting")
    
    # Check if any action was specified
    if not any([args.importar, args.relatorio, args.simulate, args.map, args.analyze, args.ml_analyze]):
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
    
    # ML-enhanced geospatial analysis
    if args.ml_analyze:
        logger.info("Performing ML-enhanced geospatial analysis...")
        ml_report = generate_ml_report(data)
        
        print("\n" + "=" * 80)
        print("ML-ENHANCED GEOSPATIAL ANALYSIS FOR RURAL CONNECTIVITY")
        print("=" * 80)
        print(f"\n📊 SUMMARY")
        print(f"  Total Points Analyzed: {ml_report['summary']['total_points_analyzed']}")
        print(f"  ML Model Version: {ml_report['summary']['ml_model_version']}")
        
        print(f"\n💰 STARLINK ROI ANALYSIS")
        roi = ml_report['roi_analysis']
        print(f"  Rural Coverage: {roi['rural_percentage']:.1f}% ({roi['rural_points']}/{roi['total_points']} points)")
        print(f"  High Priority Areas: {roi['high_priority_points']} points need immediate attention")
        print(f"  Current Avg Quality: {roi['avg_current_quality']:.1f}/100")
        print(f"  Starlink Suitability Score: {roi['starlink_suitability_score']:.1f}/100")
        print(f"\n  Recommendations:")
        for rec in roi['recommendations']:
            print(f"    • {rec}")
        
        print(f"\n🗺️  EXPANSION ZONES")
        zones = ml_report['expansion_zones']
        print(f"  Identified {zones['total_zones']} optimal expansion zones")
        print(f"  Top Priority: {zones['top_priority_zone']}")
        print(f"\n  Zone Details:")
        for zone_id, zone_data in zones['zones'].items():
            print(f"\n  {zone_id.upper()}:")
            print(f"    Location: ({zone_data['center']['latitude']:.4f}, {zone_data['center']['longitude']:.4f})")
            print(f"    Points: {zone_data['point_count']}")
            print(f"    Avg Quality: {zone_data['avg_quality_score']:.1f}/100")
            print(f"    Distance from City: {zone_data['avg_distance_from_city_km']:.1f} km")
            print(f"    Rural Area: {'Yes' if zone_data['is_primarily_rural'] else 'No'}")
            print(f"    Priority Score: {zone_data['priority_score']:.1f}")
            print(f"    → {zone_data['recommendation']}")
        
        print(f"\n🎯 TOP 5 PRIORITY AREAS FOR IMPROVEMENT")
        for i, area in enumerate(ml_report['top_priority_areas'], 1):
            print(f"\n  #{i} - {area['provider']}")
            print(f"    Location: ({area['latitude']:.4f}, {area['longitude']:.4f})")
            print(f"    Current Quality: {area['current_quality']:.1f}/100")
            print(f"    Priority Score: {area['priority_score']:.1f}/100")
            print(f"    Distance from City: {area['distance_from_city_km']:.1f} km")
            print(f"    Rural: {'Yes' if area['is_rural'] else 'No'}")
        
        print("\n" + "=" * 80 + "\n")
        
        # Save ML analysis to JSON
        import json
        ml_output_path = 'ml_analysis_report.json'
        with open(ml_output_path, 'w', encoding='utf-8') as f:
            json.dump(ml_report, f, indent=2, ensure_ascii=False)
        logger.info(f"ML analysis saved to {ml_output_path}")
        print(f"✓ ML analysis report saved to {ml_output_path}\n")
    
    # Generate report
    if args.relatorio:
        logger.info(f"Generating {args.relatorio.upper()} report...")
        report_path = generate_report(data, args.relatorio)
        logger.info(f"Report generated: {report_path}")
    
    # Generate map
    if args.map:
        logger.info("Generating interactive map...")
        map_path = generate_map(data)
        logger.info(f"Map generated: {map_path}")
    
    logger.info("Rural Connectivity Mapper 2026 - Completed successfully")


if __name__ == '__main__':
    main()
