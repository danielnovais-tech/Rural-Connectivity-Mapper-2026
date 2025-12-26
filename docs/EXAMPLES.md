# Usage Examples

## Example 1: Quick Start

Create a point and run a speed test interactively:

```bash
python main.py --interactive
```

Follow the prompts to:
1. Enter an address or coordinates
2. Optionally geocode the location
3. Enter provider name and tags
4. Run speed tests
5. View quality scores

## Example 2: Import and Analyze Sample Data

Import sample data and generate all reports:

```bash
python main.py --import src/data/sample_points.csv --report
```

This will:
- Import 5 sample points from different Brazilian cities
- Generate reports in TXT, JSON, CSV, and HTML formats
- Save reports to the `reports/` directory

## Example 3: Provider Comparison

Compare connectivity quality across different providers:

```bash
python main.py --import src/data/sample_points.csv --analyze providers
```

Output example:
```json
{
  "Starlink": {
    "num_points": 3,
    "avg_quality_score": 85.5,
    "avg_download_speed": 150.2,
    "avg_upload_speed": 18.5,
    "avg_latency": 28.3
  },
  "Viasat": {
    "num_points": 1,
    "avg_quality_score": 65.2,
    "avg_download_speed": 75.0,
    "avg_upload_speed": 10.0,
    "avg_latency": 45.0
  }
}
```

## Example 4: Batch Processing with Python

Create multiple points programmatically:

```python
from src.models.connectivity_point import ConnectivityPoint
from src.models.speed_test import SpeedTest
from src.utils.quality_calculator import calculate_quality_score
from src.utils.report_generator import ReportGenerator

# Create points
points = []

# São Paulo
sp_point = ConnectivityPoint(
    latitude=-23.5505,
    longitude=-46.6333,
    address="São Paulo, Brazil",
    provider="Starlink",
    tags=["urban", "test"]
)

# Add speed test
sp_point.add_speed_test(SpeedTest(
    download_speed=150.0,
    upload_speed=20.0,
    latency=25.0
))

# Calculate quality
sp_point.quality_score = calculate_quality_score(sp_point.speed_tests)
points.append(sp_point)

# Rio de Janeiro
rj_point = ConnectivityPoint(
    latitude=-22.9068,
    longitude=-43.1729,
    address="Rio de Janeiro, Brazil",
    provider="Starlink",
    tags=["coastal"]
)

rj_point.add_speed_test(SpeedTest(
    download_speed=165.0,
    upload_speed=22.0,
    latency=23.0
))

rj_point.quality_score = calculate_quality_score(rj_point.speed_tests)
points.append(rj_point)

# Generate reports
reporter = ReportGenerator("my_reports")
reports = reporter.generate_all_reports(points)

for format_type, filepath in reports.items():
    print(f"{format_type}: {filepath}")
```

## Example 5: Custom CSV Import/Export

Export collected data to CSV:

```python
from src.utils.csv_handler import export_to_csv, import_from_csv

# Export
export_to_csv(points, "my_data/connectivity_points.csv")

# Import
loaded_points = import_from_csv("my_data/connectivity_points.csv")
print(f"Loaded {len(loaded_points)} points")
```

## Example 6: Temporal Analysis

Analyze connectivity trends over time:

```bash
python main.py --import historical_data.json --analyze temporal
```

Output shows statistics grouped by date:
```json
{
  "total_points": 50,
  "date_range": {
    "start": "2024-01-01T00:00:00",
    "end": "2024-01-31T23:59:59"
  },
  "periods": {
    "2024-01-01": {
      "num_points": 5,
      "avg_quality_score": 82.3,
      "min_quality_score": 75.0,
      "max_quality_score": 90.0
    }
  }
}
```

## Example 7: Debug Mode

Enable detailed logging for troubleshooting:

```bash
python main.py --interactive --debug
```

This shows:
- API calls to geocoding services
- Speed test progress
- Quality score calculations
- Report generation steps
- Any errors with stack traces

## Example 8: Summary Statistics

Get comprehensive statistics:

```bash
python main.py --import src/data/sample_points.csv --analyze summary
```

Output:
```json
{
  "total_points": 5,
  "num_providers": 3,
  "providers": ["Starlink", "Viasat", "HughesNet"],
  "num_tags": 4,
  "tags": ["urban", "coastal", "rural", "capital"],
  "quality_scores": {
    "avg": 78.5,
    "min": 65.0,
    "max": 92.0
  },
  "download_speeds": {
    "avg": 125.3,
    "min": 60.0,
    "max": 180.0
  }
}
```

## Example 9: Multiple Speed Tests

Run multiple tests for better accuracy:

```bash
python main.py --interactive --num-tests 5
```

This runs 5 speed tests and averages the results for more reliable quality scores.

## Example 10: Combining Operations

Import, analyze, and generate reports in one command:

```bash
python main.py \
  --import src/data/sample_points.csv \
  --analyze providers \
  --report \
  --output starlink_analysis_2026
```

This will:
1. Import sample data
2. Run provider comparison analysis
3. Generate all report formats
4. Save everything to `starlink_analysis_2026/` directory
