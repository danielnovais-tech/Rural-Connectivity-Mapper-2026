#!/usr/bin/env python3
"""
Rural Connectivity Mapper 2026 - Main CLI Entry Point

A Python-based tool for analyzing and optimizing Starlink's rural internet expansion in Brazil.
Focuses on mapping connectivity points, measuring performance, and generating comprehensive reports.

Developed for rural Brazil simulations aligned with Starlink's 2026 expansion roadmap.
Acknowledging SpaceX Starlink technology.
"""

import argparse
import sys
import os
from datetime import datetime
from typing import Optional

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback for when colorama is not available
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = RESET_ALL = ''

from models import AccessPoint
from utils import (
    measure_speed, geocode_address, validate_access_point,
    load_data, save_data, backup_data,
    import_csv, export_csv,
    generate_report_txt, generate_report_json, generate_report_html,
    get_provider_stats, is_platform_supported,
    DATA_FILE, REPORTS_DIR
)


def print_banner():
    """Print application banner."""
    banner = f"""
{Fore.CYAN}{'=' * 80}
{Fore.BLUE}       🛰️  RURAL CONNECTIVITY MAPPER 2026  🛰️
{Fore.CYAN}{'=' * 80}
{Fore.WHITE}    Mapping Starlink's Rural Internet Expansion in Brazil
{Fore.GREEN}    Powered by SpaceX Starlink Technology
{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}
"""
    print(banner)


def cmd_add_point(args):
    """Add a new access point with optional speed test."""
    if args.debug:
        print(f"{Fore.YELLOW}Debug mode enabled{Style.RESET_ALL}")
    
    # Load existing data
    access_points = load_data(DATA_FILE, args.debug)
    
    # Backup before modification
    if access_points:
        backup_data(DATA_FILE, args.debug)
    
    # Get coordinates
    lat = args.lat
    lon = args.lon
    
    # If address provided, try to geocode
    if args.address and (lat is None or lon is None):
        print(f"{Fore.CYAN}Geocoding address: {args.address}{Style.RESET_ALL}")
        coords = geocode_address(args.address, args.debug)
        if coords:
            lat = coords['lat']
            lon = coords['lon']
            print(f"{Fore.GREEN}✓ Location found: ({lat}, {lon}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Could not geocode address{Style.RESET_ALL}")
            if lat is None or lon is None:
                print(f"{Fore.RED}Error: Coordinates required when geocoding fails{Style.RESET_ALL}")
                return 1
    
    if lat is None or lon is None:
        print(f"{Fore.RED}Error: Latitude and longitude are required{Style.RESET_ALL}")
        return 1
    
    # Speed test
    download = args.download or 0.0
    upload = args.upload or 0.0
    latency = args.latency or 0.0
    stability = args.stability or 100.0
    
    if args.test_speed:
        print(f"{Fore.CYAN}Running speed test...{Style.RESET_ALL}")
        try:
            speed_results = measure_speed(args.debug)
            download = speed_results['download']
            upload = speed_results['upload']
            latency = speed_results['latency']
            stability = speed_results['stability']
            print(f"{Fore.GREEN}✓ Speed test completed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Speed test failed: {e}{Style.RESET_ALL}")
            if args.debug:
                import traceback
                traceback.print_exc()
    
    # Create access point
    ap = AccessPoint(
        lat=lat,
        lon=lon,
        provider=args.provider or "Unknown",
        address=args.address or "",
        download=download,
        upload=upload,
        latency=latency,
        stability=stability,
        tags=args.tags or []
    )
    
    # Validate
    errors = validate_access_point(ap)
    if errors:
        print(f"{Fore.RED}Validation errors:{Style.RESET_ALL}")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    # Add to list
    access_points.append(ap)
    
    # Save
    if save_data(access_points, DATA_FILE, args.debug):
        print(f"{Fore.GREEN}✓ Access point added successfully{Style.RESET_ALL}")
        print(f"\n{ap}")
        return 0
    else:
        print(f"{Fore.RED}✗ Failed to save access point{Style.RESET_ALL}")
        return 1


def cmd_list_points(args):
    """List all access points."""
    access_points = load_data(DATA_FILE, args.debug)
    
    if not access_points:
        print(f"{Fore.YELLOW}No access points found{Style.RESET_ALL}")
        return 0
    
    print(f"{Fore.CYAN}Total access points: {len(access_points)}{Style.RESET_ALL}\n")
    
    for i, ap in enumerate(access_points, 1):
        print(f"{Fore.BLUE}[{i}] {Style.RESET_ALL}{ap}")
        print()
    
    return 0


def cmd_import_csv(args):
    """Import access points from CSV file."""
    if not os.path.exists(args.importar):
        print(f"{Fore.RED}Error: File not found: {args.importar}{Style.RESET_ALL}")
        return 1
    
    print(f"{Fore.CYAN}Importing from {args.importar}...{Style.RESET_ALL}")
    
    try:
        imported_points = import_csv(args.importar, args.debug)
        
        if not imported_points:
            print(f"{Fore.YELLOW}No valid access points found in CSV{Style.RESET_ALL}")
            return 0
        
        # Load existing data
        existing_points = load_data(DATA_FILE, args.debug)
        
        # Backup before merging
        if existing_points:
            backup_data(DATA_FILE, args.debug)
        
        # Merge
        all_points = existing_points + imported_points
        
        # Save
        if save_data(all_points, DATA_FILE, args.debug):
            print(f"{Fore.GREEN}✓ Imported {len(imported_points)} access points{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Total points: {len(all_points)}{Style.RESET_ALL}")
            return 0
        else:
            print(f"{Fore.RED}✗ Failed to save imported data{Style.RESET_ALL}")
            return 1
    
    except Exception as e:
        print(f"{Fore.RED}Error importing CSV: {e}{Style.RESET_ALL}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def cmd_export_csv(args):
    """Export access points to CSV file."""
    access_points = load_data(DATA_FILE, args.debug)
    
    if not access_points:
        print(f"{Fore.YELLOW}No access points to export{Style.RESET_ALL}")
        return 0
    
    output_file = args.output or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    print(f"{Fore.CYAN}Exporting to {output_file}...{Style.RESET_ALL}")
    
    if export_csv(access_points, output_file, args.debug):
        print(f"{Fore.GREEN}✓ Exported {len(access_points)} access points{Style.RESET_ALL}")
        return 0
    else:
        print(f"{Fore.RED}✗ Failed to export data{Style.RESET_ALL}")
        return 1


def cmd_generate_report(args):
    """Generate reports in various formats."""
    access_points = load_data(DATA_FILE, args.debug)
    
    if not access_points:
        print(f"{Fore.YELLOW}No access points found. Cannot generate report.{Style.RESET_ALL}")
        return 0
    
    # Ensure reports directory exists
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    formats = args.relatorio or ['txt', 'json', 'csv', 'html']
    success_count = 0
    
    for fmt in formats:
        filename = os.path.join(REPORTS_DIR, f"relatorio_{timestamp}.{fmt}")
        
        print(f"{Fore.CYAN}Generating {fmt.upper()} report...{Style.RESET_ALL}")
        
        try:
            if fmt == 'txt':
                success = generate_report_txt(access_points, filename, args.debug)
            elif fmt == 'json':
                success = generate_report_json(access_points, filename, args.debug)
            elif fmt == 'csv':
                success = export_csv(access_points, filename, args.debug)
            elif fmt == 'html':
                success = generate_report_html(access_points, filename, args.debug)
            else:
                print(f"{Fore.YELLOW}Unknown format: {fmt}{Style.RESET_ALL}")
                continue
            
            if success:
                print(f"{Fore.GREEN}✓ {fmt.upper()} report: {filename}{Style.RESET_ALL}")
                success_count += 1
            else:
                print(f"{Fore.RED}✗ Failed to generate {fmt.upper()} report{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Error generating {fmt.upper()} report: {e}{Style.RESET_ALL}")
            if args.debug:
                import traceback
                traceback.print_exc()
    
    if success_count > 0:
        print(f"\n{Fore.GREEN}✓ Generated {success_count} report(s){Style.RESET_ALL}")
        return 0
    else:
        return 1


def cmd_stats(args):
    """Display statistics about access points."""
    access_points = load_data(DATA_FILE, args.debug)
    
    if not access_points:
        print(f"{Fore.YELLOW}No access points found{Style.RESET_ALL}")
        return 0
    
    # Overall stats
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}STATISTICS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
    
    avg_download = sum(ap.download for ap in access_points) / len(access_points)
    avg_upload = sum(ap.upload for ap in access_points) / len(access_points)
    avg_latency = sum(ap.latency for ap in access_points) / len(access_points)
    avg_quality = sum(ap.quality_score for ap in access_points) / len(access_points)
    
    print(f"Total Points: {Fore.GREEN}{len(access_points)}{Style.RESET_ALL}")
    print(f"Average Download: {Fore.GREEN}{avg_download:.2f} Mbps{Style.RESET_ALL}")
    print(f"Average Upload: {Fore.GREEN}{avg_upload:.2f} Mbps{Style.RESET_ALL}")
    print(f"Average Latency: {Fore.YELLOW}{avg_latency:.2f} ms{Style.RESET_ALL}")
    print(f"Average Quality Score: {Fore.GREEN}{avg_quality:.4f}{Style.RESET_ALL}")
    
    # Provider stats
    provider_stats = get_provider_stats(access_points)
    
    if provider_stats:
        print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}PROVIDER BREAKDOWN{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        for provider, stats in sorted(provider_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"{Fore.MAGENTA}{provider}{Style.RESET_ALL}")
            print(f"  Points: {stats['count']}")
            print(f"  Avg Download: {stats['avg_download']} Mbps")
            print(f"  Avg Upload: {stats['avg_upload']} Mbps")
            print(f"  Avg Latency: {stats['avg_latency']} ms")
            print(f"  Avg Quality: {stats['avg_quality']}")
            print()
    
    return 0


def main():
    """Main entry point."""
    # Check platform
    if not is_platform_supported():
        print(f"{Fore.RED}Warning: Platform may not be fully supported{Style.RESET_ALL}")
    
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Rural Connectivity Mapper 2026 - Starlink Expansion Tool for Rural Brazil',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a point with speed test
  %(prog)s add --lat -15.7801 --lon -47.9292 --provider Starlink --test-speed
  
  # Add a point by address
  %(prog)s add --address "Brasília, DF, Brazil" --provider Starlink --test-speed
  
  # Import from CSV
  %(prog)s --importar data.csv
  
  # Generate reports
  %(prog)s --relatorio txt json html
  
  # List all points
  %(prog)s list
  
  # Show statistics
  %(prog)s stats

Powered by SpaceX Starlink Technology
"""
    )
    
    # Global options
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--relatorio', nargs='*', choices=['txt', 'json', 'csv', 'html'],
                       help='Generate reports in specified formats (default: all formats)')
    parser.add_argument('--importar', metavar='CSV_FILE', help='Import access points from CSV file')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new access point')
    add_parser.add_argument('--lat', type=float, help='Latitude')
    add_parser.add_argument('--lon', type=float, help='Longitude')
    add_parser.add_argument('--address', help='Address to geocode')
    add_parser.add_argument('--provider', help='Internet provider name')
    add_parser.add_argument('--download', type=float, help='Download speed in Mbps')
    add_parser.add_argument('--upload', type=float, help='Upload speed in Mbps')
    add_parser.add_argument('--latency', type=float, help='Latency in ms')
    add_parser.add_argument('--stability', type=float, help='Stability percentage (0-100)')
    add_parser.add_argument('--tags', nargs='+', help='Tags for categorization')
    add_parser.add_argument('--test-speed', action='store_true', help='Run speed test')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all access points')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export access points to CSV')
    export_parser.add_argument('--output', help='Output CSV file path')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Display statistics')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Show banner
    print_banner()
    
    # Handle global options
    if args.relatorio is not None:
        return cmd_generate_report(args)
    
    if args.importar:
        return cmd_import_csv(args)
    
    # Handle subcommands
    if args.command == 'add':
        return cmd_add_point(args)
    elif args.command == 'list':
        return cmd_list_points(args)
    elif args.command == 'export':
        return cmd_export_csv(args)
    elif args.command == 'stats':
        return cmd_stats(args)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)
