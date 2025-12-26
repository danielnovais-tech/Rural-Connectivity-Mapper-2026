# 🛰️ Rural Connectivity Mapper 2026

A Python-based tool for analyzing and optimizing Starlink's rural internet expansion in Brazil. This system maps connectivity points, measures performance metrics, and generates comprehensive reports to support rural connectivity planning for 2026.

**Powered by SpaceX Starlink Technology**

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Development](#development)
- [Testing](#testing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## ✨ Features

### Core Functionality
- **Speed Testing**: Measure download/upload speeds, latency, and connection stability using speedtest-cli
- **Geocoding**: Convert addresses to coordinates using geopy
- **Quality Scoring**: Calculate connectivity quality based on performance metrics
- **Multi-Format Reports**: Generate reports in TXT, JSON, CSV, and HTML formats
- **Data Management**: Import/export CSV data with automatic backups
- **Provider Analysis**: Compare performance across different internet providers
- **Tag System**: Categorize access points with custom tags
- **Temporal Analysis**: Track connectivity metrics over time

### Quality Score Algorithm
The quality score is calculated using the formula:
```
quality_score = (download + upload) / (latency * (1 + stability/100))
```
Higher scores indicate better overall connectivity quality.

### Supported Features
- ✅ Robust error handling with graceful degradation
- ✅ Data validation for all inputs
- ✅ Automatic backup before data modifications
- ✅ Modular, maintainable code structure
- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ Colorized terminal output
- ✅ Debug mode for troubleshooting
- ✅ Comprehensive unit tests

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Libraries
- `speedtest-cli` - Internet speed testing
- `geopy` - Geocoding and address lookup
- `pytest` - Unit testing framework
- `colorama` - Colored terminal output
- `pandas` - Data analysis (optional, for advanced features)

## 📖 Usage

### Basic Commands

#### View Help
```bash
python main.py --help
```

#### Add a New Access Point

**With speed test:**
```bash
python main.py add --lat -15.7801 --lon -47.9292 --provider Starlink --test-speed
```

**By address (with geocoding):**
```bash
python main.py add --address "Brasília, DF, Brazil" --provider Starlink --test-speed
```

**Manual entry:**
```bash
python main.py add --lat -15.7801 --lon -47.9292 --provider Starlink \
  --download 150.5 --upload 20.3 --latency 25 --stability 98.5 \
  --tags rural satellite test
```

#### List All Access Points
```bash
python main.py list
```

#### Show Statistics
```bash
python main.py stats
```

#### Generate Reports

**All formats:**
```bash
python main.py --relatorio
```

**Specific formats:**
```bash
python main.py --relatorio txt json html
```

#### Import from CSV
```bash
python main.py --importar data.csv
```

#### Export to CSV
```bash
python main.py export --output export_2026.csv
```

### Advanced Options

**Enable debug mode:**
```bash
python main.py --debug list
```

**Combine multiple operations:**
```bash
python main.py --debug --importar rural_points.csv --relatorio json html
```

## 📁 Project Structure

```
Rural-Connectivity-Mapper-2026/
├── main.py                 # CLI entry point
├── models.py               # AccessPoint class definition
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── data/                  # Data directory
│   ├── pontos.json       # Main database (JSON)
│   ├── relatorios/       # Generated reports
│   └── backups/          # Automatic backups
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_utils.py
└── docs/                  # Additional documentation
```

## 💡 Examples

### Example 1: Complete Workflow

```bash
# Add multiple points by address
python main.py add --address "Fortaleza, CE, Brazil" --provider Starlink --test-speed
python main.py add --address "Manaus, AM, Brazil" --provider Starlink --test-speed
python main.py add --address "Belém, PA, Brazil" --provider Starlink --test-speed

# View statistics
python main.py stats

# Generate comprehensive reports
python main.py --relatorio txt json csv html
```

### Example 2: Import Bulk Data

Create a CSV file `rural_brazil.csv`:
```csv
lat,lon,provider,address,download,upload,latency,stability,tags
-15.7801,-47.9292,Starlink,"Brasília, DF",150.5,20.3,25.0,98.5,"rural,satellite,test"
-3.7319,-38.5267,Starlink,"Fortaleza, CE",145.2,18.7,28.5,97.0,"rural,satellite"
-9.6658,-35.7353,Starlink,"Maceió, AL",138.9,19.5,30.2,96.5,"rural,satellite,expansion"
```

Import the data:
```bash
python main.py --importar rural_brazil.csv
```

### Example 3: Debug Mode

```bash
python main.py --debug add --address "São Paulo, SP, Brazil" --provider Starlink --test-speed
```

This will show detailed output including geocoding attempts, speed test progress, and data validation steps.

## 🔧 Development

### Code Structure

**models.py** - AccessPoint Class
- Represents an internet access point with connectivity metrics
- Calculates quality scores automatically
- Provides serialization (to_dict/from_dict)

**utils.py** - Utility Functions
- `measure_speed()` - Run internet speed tests
- `geocode_address()` - Convert addresses to coordinates
- `validate_*()` - Data validation functions
- `load_data()` / `save_data()` - JSON data management
- `import_csv()` / `export_csv()` - CSV operations
- `generate_report_*()` - Report generation
- `backup_data()` - Automatic backups
- `get_provider_stats()` - Provider analytics

**main.py** - CLI Interface
- Argument parsing with argparse
- Colorized output with colorama
- Command routing (add, list, stats, export)
- Error handling and user feedback

### Adding New Features

To add a new report format:
1. Create a function in `utils.py`: `generate_report_<format>()`
2. Add the format to the choices in `main.py`
3. Update the report generation command handler

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_models.py -v
```

### Test Features
- Unit tests for AccessPoint class
- Validation function tests
- Data import/export tests
- Report generation tests
- Provider statistics tests

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- **SpaceX Starlink**: For pioneering satellite internet technology that makes rural connectivity possible
- **Rural Brazil Communities**: The focus of this 2026 expansion analysis
- **Open Source Libraries**: speedtest-cli, geopy, pytest, colorama, pandas

## 🎯 Focus Areas

This tool is specifically designed for:
- **Rural Brazil**: Analyzing connectivity in underserved rural areas
- **2026 Expansion**: Aligned with Starlink's planned expansion timeline
- **Performance Analysis**: Measuring real-world connectivity metrics
- **Strategic Planning**: Supporting infrastructure deployment decisions

## 🔮 Future Enhancements

- Interactive map visualization
- Real-time monitoring dashboard
- Machine learning predictions for coverage gaps
- Mobile app integration
- Multi-language support (Portuguese)
- API for external integrations

## 📞 Support

For issues, questions, or contributions, please use the GitHub issue tracker.

---

**Built with ❤️ for rural Brazil's connectivity future**
