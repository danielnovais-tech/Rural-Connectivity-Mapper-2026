#!/usr/bin/env python3
"""Demo workflow for Rural Connectivity Mapper 2026."""

import logging
import sys
from pathlib import Path

from src.models import ConnectivityPoint, SpeedTest
from src.utils import (
    load_data, save_data, generate_report, simulate_router_impact,
    generate_map, analyze_temporal_evolution, compare_providers
)


def setup_logging():
    """Configure logging for demo."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    """Execute complete demo workflow."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("\n" + "=" * 80)
    print("RURAL CONNECTIVITY MAPPER 2026 - DEMO WORKFLOW")
    print("Demonstrating Starlink's 2026 expansion analysis in Brazil")
    print("=" * 80 + "\n")
    
    try:
        # Step 1: Import CSV data
        logger.info("Step 1: Importing sample data from CSV...")
        import csv
        from datetime import datetime
        
        csv_path = 'src/data/sample_data.csv'
        data_path = 'src/data/pontos.json'
        
        points = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                speed_test = SpeedTest(
                    download=float(row['download']),
                    upload=float(row['upload']),
                    latency=float(row['latency']),
                    jitter=float(row.get('jitter', 0)),
                    packet_loss=float(row.get('packet_loss', 0)),
                    obstruction=float(row.get('obstruction', 0))
                )
                
                point = ConnectivityPoint(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    provider=row['provider'],
                    speed_test=speed_test,
                    timestamp=row.get('timestamp', datetime.now().isoformat()),
                    point_id=row.get('id')
                )
                
                points.append(point.to_dict())
        
        save_data(data_path, points)
        print(f"✓ Imported {len(points)} connectivity points from CSV")
        
        # Step 2: Load data
        logger.info("Step 2: Loading data...")
        data = load_data(data_path)
        print(f"✓ Loaded {len(data)} points from database")
        
        # Step 3: Display initial statistics
        print("\n" + "-" * 80)
        print("INITIAL CONNECTIVITY STATISTICS")
        print("-" * 80)
        for point in data:
            provider = point['provider']
            qs = point['quality_score']
            st = point['speed_test']
            print(f"{provider:15} | Score: {qs['overall_score']:5.1f}/100 ({qs['rating']:9}) | "
                  f"Download: {st['download']:6.1f} Mbps | Latency: {st['latency']:5.1f} ms")
        print("-" * 80 + "\n")
        
        # Step 4: Simulate router impact
        logger.info("Step 3: Simulating router impact (15-25% improvement)...")
        improved_data = simulate_router_impact(data)
        save_data(data_path, improved_data)
        print("✓ Router impact simulation completed")
        
        # Step 5: Display improved statistics
        print("\n" + "-" * 80)
        print("POST-SIMULATION CONNECTIVITY STATISTICS")
        print("-" * 80)
        for i, point in enumerate(improved_data):
            provider = point['provider']
            qs = point['quality_score']
            st = point['speed_test']
            original_score = data[i]['quality_score']['overall_score']
            improvement = qs['overall_score'] - original_score
            print(f"{provider:15} | Score: {qs['overall_score']:5.1f}/100 ({qs['rating']:9}) | "
                  f"Improvement: +{improvement:4.1f} | Download: {st['download']:6.1f} Mbps")
        print("-" * 80 + "\n")
        
        # Step 6: Analyze temporal evolution
        logger.info("Step 4: Analyzing temporal evolution...")
        analysis = analyze_temporal_evolution(improved_data)
        
        print("\n" + "-" * 80)
        print("TEMPORAL ANALYSIS")
        print("-" * 80)
        print(f"Total Points Analyzed: {analysis['total_points']}")
        print(f"Average Quality Score: {analysis['trends']['avg_quality_score']}/100")
        print(f"Average Download Speed: {analysis['trends']['avg_download']} Mbps")
        print(f"Average Latency: {analysis['trends']['avg_latency']} ms")
        print("\nKey Insights:")
        for insight in analysis['insights']:
            print(f"  • {insight}")
        print("-" * 80 + "\n")
        
        # Step 6.5: Compare providers
        logger.info("Step 4.5: Comparing provider performance...")
        provider_comparison = compare_providers(improved_data)
        
        print("\n" + "-" * 80)
        print("PROVIDER COMPARISON (2026 Data)")
        print("-" * 80)
        print(f"Total Providers: {provider_comparison['total_providers']}")
        print(f"Satellite Providers: {', '.join(provider_comparison['satellite_providers'])}")
        print("\nProvider Performance Summary:")
        
        # Sort providers by average quality score
        sorted_providers = sorted(
            provider_comparison['providers'].items(),
            key=lambda x: x[1]['quality_score']['avg'],
            reverse=True
        )
        
        for provider, metrics in sorted_providers:
            is_satellite = provider in provider_comparison['satellite_providers']
            sat_marker = "🛰️ " if is_satellite else "🌐 "
            
            print(f"\n{sat_marker}{provider}:")
            print(f"  Quality Score: {metrics['quality_score']['avg']}/100 "
                  f"(min: {metrics['quality_score']['min']}, max: {metrics['quality_score']['max']})")
            print(f"  Download: {metrics['download']['avg']} Mbps "
                  f"(min: {metrics['download']['min']}, max: {metrics['download']['max']})")
            print(f"  Upload: {metrics['upload']['avg']} Mbps")
            print(f"  Latency: {metrics['latency']['avg']} ms")
            print(f"  Jitter: {metrics['jitter']['avg']} ms")
            print(f"  Packet Loss: {metrics['packet_loss']['avg']}%")
            if is_satellite and metrics['obstruction']['avg'] > 0:
                print(f"  Obstruction: {metrics['obstruction']['avg']}%")
            print(f"  Stability: {metrics['stability']['avg']}/100")
        
        print("\nKey Provider Insights:")
        for insight in provider_comparison['insights']:
            print(f"  • {insight}")
        print("-" * 80 + "\n")
        
        # Step 7: Generate reports in multiple formats
        logger.info("Step 5: Generating multi-format reports...")
        formats = ['json', 'csv', 'txt', 'html']
        for fmt in formats:
            report_path = generate_report(improved_data, fmt, f'demo_report.{fmt}')
            print(f"✓ Generated {fmt.upper()} report: {report_path}")
        
        # Step 8: Generate interactive map
        logger.info("Step 6: Generating interactive map...")
        map_path = generate_map(improved_data, 'demo_connectivity_map.html')
        print(f"✓ Generated interactive map: {map_path}")
        
        # Final summary
        print("\n" + "=" * 80)
        print("DEMO WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nGenerated Files:")
        print("  • demo_report.json - JSON format report")
        print("  • demo_report.csv - CSV format report")
        print("  • demo_report.txt - Text format report")
        print("  • demo_report.html - HTML format report")
        print("  • demo_connectivity_map.html - Interactive Folium map")
        print("\nNext Steps:")
        print("  1. Open demo_connectivity_map.html in your browser to view the interactive map")
        print("  2. Review the generated reports for detailed connectivity analysis")
        print("  3. Use main.py with different flags for custom analysis")
        print("\nExample: python main.py --debug --importar src/data/sample_data.csv --relatorio json")
        print("=" * 80 + "\n")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n❌ Error: Required file not found - {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        print(f"\n❌ Demo workflow failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
