# Rural Connectivity Mapper 2026

Python-based tool to map and analyze rural internet connectivity in Brazil, aligned with Starlink's 2026 expansion roadmap.

## Features

- **Connectivity Point Mapping**: Map geographic locations with connectivity data
- **Speed Testing**: Automated internet speed tests using speedtest-cli
- **Geocoding**: Address-to-coordinate conversion using geopy
- **Quality Scoring**: Calculate comprehensive quality scores based on speed, latency, and stability
- **Report Generation**: Generate reports in multiple formats (TXT, JSON, CSV, HTML)
- **CSV Import/Export**: Easy data import/export for batch processing
- **Temporal Analysis**: Analyze connectivity trends over time
- **Provider Comparison**: Compare connectivity quality across providers
- **Tag System**: Categorize points with custom tags
- **Debug Mode**: Enhanced logging for troubleshooting
- **CLI Interface**: User-friendly command-line interface

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026.git
cd Rural-Connectivity-Mapper-2026
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Create and test connectivity points interactively:

```bash
python main.py --interactive
```

### Import Data

Import points from CSV:

```bash
python main.py --import src/data/sample_points.csv
```

### Run Speed Tests

Import points and run speed tests:

```bash
python main.py --import src/data/sample_points.csv --num-tests 3
```

### Generate Reports

Generate all report formats:

```bash
python main.py --import src/data/sample_points.csv --report --output reports/
```

### Analyze Data

Compare providers:

```bash
python main.py --import src/data/sample_points.csv --analyze providers
```

Analyze temporal trends:

```bash
python main.py --import src/data/sample_points.csv --analyze temporal
```

Get summary statistics:

```bash
python main.py --import src/data/sample_points.csv --analyze summary
```

### Export Data

Export to CSV:

```bash
python main.py --interactive --export data/my_points.csv
```

### Debug Mode

Enable detailed logging:

```bash
python main.py --interactive --debug
```

## Project Structure

```
Rural-Connectivity-Mapper-2026/
├── main.py                 # Main CLI application
├── src/
│   ├── __init__.py
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   ├── connectivity_point.py
│   │   ├── speed_test.py
│   │   └── quality_score.py
│   ├── utils/              # Utility modules
│   │   ├── __init__.py
│   │   ├── geocoding.py
│   │   ├── speed_testing.py
│   │   ├── quality_calculator.py
│   │   ├── report_generator.py
│   │   ├── csv_handler.py
│   │   └── data_analysis.py
│   └── data/               # Sample data
│       └── sample_points.csv
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   └── test_utils.py
├── docs/                   # Documentation
│   ├── API.md
│   └── EXAMPLES.md
├── reports/                # Generated reports (created automatically)
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Models

### ConnectivityPoint

Represents a geographic location with connectivity information:
- Latitude/Longitude coordinates
- Optional address (geocoded)
- Provider name
- Custom tags
- Timestamp
- Speed test results
- Quality score

### SpeedTest

Stores internet speed test results:
- Download speed (Mbps)
- Upload speed (Mbps)
- Latency (ms)
- Jitter (ms)
- Packet loss (%)
- Test server
- Stability calculation

### QualityScore

Calculates connectivity quality metrics:
- Speed score (0-100)
- Latency score (0-100)
- Stability score (0-100)
- Overall weighted score
- Quality rating (Excellent/Good/Fair/Poor/Very Poor)

## Quality Scoring

The quality score is calculated using:
- **Speed Score (40%)**: Based on download/upload speeds (Starlink target: 50-200 Mbps down, 10-20 Mbps up)
- **Latency Score (30%)**: Based on ping latency (Starlink target: 20-40ms)
- **Stability Score (30%)**: Based on jitter and packet loss

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Error Handling

The application includes comprehensive error handling:
- Graceful failures for network operations
- Validation of input data
- Detailed error messages in debug mode
- Logging of all operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

Daniel Azevedo Novais

## Acknowledgments

- Built for Starlink's 2026 expansion roadmap in Brazil
- Uses speedtest-cli for speed testing
- Uses geopy for geocoding services
- Designed for rural connectivity analysis and improvement
