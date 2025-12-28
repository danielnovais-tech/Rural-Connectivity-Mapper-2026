# Rural Connectivity Mapper 2026

Python-based tool to map and analyze rural internet connectivity in Brazil, aligned with Starlink's 2026 expansion roadmap.

## 📋 Overview

The Rural Connectivity Mapper 2026 is a comprehensive platform for analyzing and visualizing internet connectivity quality across Brazil, with a focus on Starlink's satellite internet expansion. The tool measures, analyzes, and reports on connectivity metrics including download/upload speeds, latency, stability, and overall quality scores.

### Key Features

- **Multi-Provider Analysis**: Track connectivity from Starlink, Viasat, HughesNet, Claro, Vivo, and other ISPs
- **Quality Scoring**: Automated quality assessment based on Starlink 2026 target metrics
- **Interactive Mapping**: Generate Folium-based interactive maps with color-coded quality markers
- **Multi-Format Reporting**: Export data in JSON, CSV, TXT, and HTML formats
- **Temporal Analysis**: Track connectivity evolution over time with trend insights
- **Router Impact Simulation**: Model the effect of router improvements on quality scores
- **CSV Data Import**: Easy bulk import from CSV files
- **Comprehensive Testing**: 20+ pytest test cases ensuring reliability

### Starlink 2026 Target Metrics

- **Download Speed**: 50-200 Mbps
- **Upload Speed**: 10-20 Mbps
- **Latency**: 20-40 ms
- **Quality Score Weighting**: Speed (40%) + Latency (30%) + Stability (30%)

---

## 🚀 Installation

### Requirements

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026.git
cd Rural-Connectivity-Mapper-2026
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python main.py --help
```

---

## 📖 Usage

### Quick Start - Demo Workflow

Run the complete demo workflow to see all features:

```bash
python demo_workflow.py
```

This will:
1. Import sample CSV data (5 Brazilian cities)
2. Calculate quality scores
3. Simulate router improvements (15-25% boost)
4. Generate multi-format reports (JSON, CSV, TXT, HTML)
5. Create interactive map
6. Perform temporal analysis with insights

**Generated files:**
- `demo_report.json` - JSON format report
- `demo_report.csv` - CSV format report
- `demo_report.txt` - Text format report
- `demo_report.html` - HTML format report
- `demo_connectivity_map.html` - Interactive map

### Command-Line Interface (CLI)

#### Basic Commands

**Import CSV data:**
```bash
python main.py --importar src/data/sample_data.csv
```

**Generate JSON report:**
```bash
python main.py --relatorio json
```

**Generate HTML report:**
```bash
python main.py --relatorio html
```

**Create interactive map:**
```bash
python main.py --map
```

**Simulate router impact:**
```bash
python main.py --simulate
```

**Analyze temporal evolution:**
```bash
python main.py --analyze
```

**Enable debug logging:**
```bash
python main.py --debug --importar src/data/sample_data.csv
```

#### Combined Workflow

```bash
python main.py --debug --importar src/data/sample_data.csv --simulate --map --analyze --relatorio html
```

This command will:
1. Enable verbose debug logging
2. Import data from CSV
3. Simulate router improvements
4. Generate interactive map
5. Analyze temporal trends
6. Create HTML report

### CLI Arguments Reference

| Argument | Description | Choices/Format |
|----------|-------------|----------------|
| `--debug` | Enable debug mode with verbose logging | Flag |
| `--relatorio <format>` | Generate report in specified format | json, csv, txt, html |
| `--importar <csv>` | Import data from CSV file | Path to CSV file |
| `--simulate` | Simulate router impact on quality scores | Flag |
| `--map` | Generate interactive Folium map | Flag |
| `--analyze` | Analyze temporal evolution | Flag |

---

## 📁 Project Structure

```
Rural-Connectivity-Mapper-2026/
├── main.py                      # Main CLI application
├── demo_workflow.py             # Complete demo workflow
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── src/                         # Source code
│   ├── __init__.py
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   ├── ConnectivityPoint.py # Location-based connectivity data
│   │   ├── SpeedTest.py         # Speed test measurements
│   │   └── QualityScore.py      # Quality assessment
│   │
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py
│   │   ├── validation_utils.py  # Data validation
│   │   ├── data_utils.py        # Data loading/saving
│   │   ├── measurement_utils.py # Speed testing
│   │   ├── geocoding_utils.py   # Coordinate conversion
│   │   ├── report_utils.py      # Multi-format reports
│   │   ├── simulation_utils.py  # Router impact simulation
│   │   ├── mapping_utils.py     # Interactive map generation
│   │   └── analysis_utils.py    # Temporal analysis
│   │
│   └── data/                    # Data files
│       ├── sample_data.csv      # Sample connectivity data
│       └── pontos.json          # Stored connectivity points
│
├── tests/                       # Test suite (20+ tests)
│   ├── __init__.py
│   ├── test_models.py           # Model tests (5)
│   ├── test_validation_utils.py # Validation tests (2)
│   ├── test_data_utils.py       # Data utils tests (2)
│   ├── test_measurement_utils.py# Measurement tests (1)
│   ├── test_geocoding_utils.py  # Geocoding tests (2)
│   ├── test_report_utils.py     # Report tests (3)
│   ├── test_simulation_utils.py # Simulation tests (2)
│   ├── test_mapping_utils.py    # Mapping tests (1)
│   └── test_analysis_utils.py   # Analysis tests (2)
│
└── docs/                        # Documentation
    └── API.md                   # Complete API reference
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`

### Run Specific Test File

```bash
pytest tests/test_models.py -v
pytest tests/test_report_utils.py -v
```

### Test Categories

- **Model Tests (5)**: SpeedTest, QualityScore, ConnectivityPoint
- **Validation Tests (2)**: Coordinates, speed test, provider validation
- **Data Tests (2)**: Load, save, backup operations
- **Measurement Tests (1)**: Speed testing with mocked API
- **Geocoding Tests (2)**: Forward and reverse geocoding
- **Report Tests (3)**: JSON, CSV, HTML report generation
- **Simulation Tests (2)**: Router impact and improvement range
- **Mapping Tests (1)**: Interactive map generation
- **Analysis Tests (2)**: Temporal evolution and grouping

---

## 📊 Sample Data

The project includes sample data for 5 Brazilian cities:

| City | Provider | Coordinates | Download | Upload | Latency | Quality |
|------|----------|-------------|----------|--------|---------|---------|
| São Paulo | Various | -23.55, -46.63 | 85.2 Mbps | 12.5 Mbps | 45.3 ms | Good |
| Rio de Janeiro | Claro | -22.91, -43.17 | 92.1 Mbps | 15.3 Mbps | 38.7 ms | Good |
| Brasília | Starlink | -15.78, -47.93 | 165.4 Mbps | 22.8 Mbps | 28.5 ms | Excellent |
| Salvador | Viasat | -12.97, -38.50 | 75.3 Mbps | 9.8 Mbps | 68.2 ms | Fair |
| Fortaleza | HughesNet | -3.72, -38.54 | 62.8 Mbps | 7.2 Mbps | 95.4 ms | Poor |

**CSV Format:**
```csv
id,city,provider,latitude,longitude,download,upload,latency,jitter,packet_loss,timestamp
```

---

## 🔧 Development

### Code Quality Standards

- **PEP 8 Compliance**: Follow Python style guide
- **Type Hints**: Use type annotations where practical
- **Docstrings**: Google-style docstrings for all public functions/classes
- **Error Handling**: Comprehensive try-except blocks
- **Logging**: DEBUG, INFO, WARNING, ERROR levels
- **Modularity**: Single responsibility principle

### Adding New Features

1. Create feature in appropriate module (`src/models/` or `src/utils/`)
2. Add comprehensive docstrings
3. Write tests in `tests/`
4. Update API documentation in `docs/API.md`
5. Run test suite to ensure no regressions

### Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open Pull Request

**Contribution Guidelines:**
- Write clear commit messages
- Include tests for new features
- Update documentation
- Follow existing code style
- Ensure all tests pass

---

## 📚 Documentation

- **[API Reference](docs/API.md)**: Complete API documentation with examples
- **[Sample Data](src/data/sample_data.csv)**: CSV format reference
- **Inline Documentation**: All modules have comprehensive docstrings

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2025 Daniel Azevedo Novais**

---

## 🤝 Acknowledgments

- **Starlink**: For 2026 target metrics and satellite internet innovation
- **Brazilian ISPs**: Claro, Vivo, TIM, Oi for traditional connectivity
- **Satellite ISPs**: Viasat, HughesNet for rural internet access
- **Open Source**: geopy, folium, pytest, pandas, and other excellent libraries

---

## 📧 Contact

- **Author**: Daniel Azevedo Novais
- **Repository**: [github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026)
- **Issues**: [GitHub Issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)

---

## 🗺️ Roadmap

### Future Enhancements

- [ ] Real-time speed testing integration
- [ ] Database backend (PostgreSQL/MongoDB)
- [ ] Web dashboard with Flask/Django
- [ ] Mobile app for field measurements
- [ ] Advanced statistical analysis
- [ ] Machine learning quality predictions
- [ ] Integration with ISP APIs
- [ ] Multi-language support (Portuguese/English)
- [ ] Export to GIS formats (GeoJSON, KML)
- [ ] Historical trend visualizations

---

**Made with ❤️ for improving rural connectivity in Brazil**
