# Rural Connectivity Mapper 2026

[![GitHub License](https://img.shields.io/github/license/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/network)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![Last Commit](https://img.shields.io/github/last-commit/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/commits/main)
[![Release](https://img.shields.io/github/v/release/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/releases/latest)

Python-based tool to map and analyze rural internet connectivity across Latin America, aligned with Starlink's 2026 expansion roadmap.

## 🌍 Overview

The Rural Connectivity Mapper 2026 is a comprehensive platform for analyzing and visualizing internet connectivity quality across Latin America, with a focus on Starlink's satellite internet expansion. The tool measures, analyzes, and reports on connectivity metrics including download/upload speeds, latency, stability, and overall quality scores.

**NEW in v1.1:** Real ANATEL & IBGE data integration, Starlink API, Interactive Streamlit Dashboard, and support for 10 LATAM countries!

**Aligned with Starlink's 2026 roadmap:** 10M rural connections & 20-30% agricultural productivity gains.

---

## ✨ Features

### Core Features
- 🖥️ **CLI Application** - Full command-line interface with 6 operational modes
- 📊 **Data Models** - ConnectivityPoint, SpeedTest, QualityScore with serialization
- 🛠️ **12 Utility Modules** - Measurement, geocoding, validation, reporting, simulation, mapping, analysis, ANATEL, IBGE, Starlink, country config
- 🗺️ **Interactive Folium Maps** - Color-coded quality markers with popups
- 📈 **Router Impact Simulation** - Model 15-25% quality improvements
- 📋 **Multi-Format Reporting** - JSON, CSV, TXT, HTML exports
- 🔍 **Temporal Analysis** - Track connectivity trends over time
- 🏢 **Provider Comparison** - Benchmark ISPs (Starlink, Viasat, HughesNet, Claro, etc.)
- 🏷️ **Tag System** - Categorize points with custom tags
- 🐛 **Debug Mode** - Enhanced logging for troubleshooting
- 🧪 **73 Comprehensive Tests** - 80%+ code coverage with pytest

### NEW Features v1.1
- 🇧🇷 **ANATEL Integration** - Real Brazilian telecom data from National Telecommunications Agency
- 📊 **IBGE Integration** - Demographic and geographic data from Brazilian Institute of Statistics
- 🛰️ **Starlink API** - Check service availability, coverage maps, and service plans
- 🌎 **LATAM Support** - Support for 10 Latin American countries (BR, AR, CL, CO, MX, PE, EC, UY, PY, BO)
- 📱 **Streamlit Dashboard** - Interactive web dashboard with real-time data visualization
- 🗺️ **Country Configurations** - Country-specific data sources, providers, and regulators
- 🌐 **Multi-language** - Portuguese and Spanish field translations

---

## 🚀 Installation

### Requirements
- **Python 3.8+**
- pip package manager
- Internet connection (for geocoding and speedtest APIs)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026.git
cd Rural-Connectivity-Mapper-2026

# Install dependencies
pip install -r requirements.txt

# Run demo workflow
python demo_workflow.py
```

### Dependencies

```
speedtest-cli>=2.1.3   # Network speed testing
geopy>=2.3.0           # Geocoding services
pytest>=7.4.0          # Testing framework
pytest-cov>=4.1.0      # Code coverage
colorama>=0.4.6        # Colored console output
pandas>=2.0.0          # Data manipulation
requests>=2.31.0       # HTTP client
folium>=0.14.0         # Interactive maps
matplotlib>=3.7.0      # Data visualization
streamlit>=1.28.0      # Web dashboard
streamlit-folium>=0.15.0  # Folium maps in Streamlit
plotly>=5.17.0         # Interactive charts
```

---

## 📖 Usage

### Quick Start - Streamlit Dashboard (NEW!)

Launch the interactive web dashboard:

```bash
streamlit run dashboard.py
```

**Features:**
- 🌍 Select from 10 LATAM countries
- 📊 View ANATEL broadband and mobile data
- 👥 Explore IBGE demographic statistics
- 🛰️ Check Starlink availability and service plans
- 🌎 Compare connectivity across LATAM countries
- 🗺️ Interactive maps with real-time data

### Quick Start - Demo Workflow

Run the complete demo to see all features:

```bash
python demo_workflow.py
```

**Auto-generates:**
- `demo_report.json`, `.csv`, `.txt`, `.html`
- `demo_connectivity_map.html` (interactive map)
- Console output with statistics

### CLI Commands

#### Import Data
```bash
python main.py --importar src/data/sample_data.csv
```

#### Generate Reports
```bash
python main.py --relatorio html    # HTML report
python main.py --relatorio json    # JSON report
python main.py --relatorio csv     # CSV report
python main.py --relatorio txt     # Text report
```

#### Simulate Router Improvements
```bash
python main.py --simulate
```
*Models 15-25% quality score boost from router upgrades*

#### Create Interactive Map
```bash
python main.py --map
```
*Generates Folium HTML map with color-coded markers*

#### Analyze Temporal Evolution
```bash
python main.py --analyze
```
*Shows trends, insights, provider statistics*

#### Enable Debug Mode
```bash
python main.py --debug --importar data.csv
```

#### Combined Workflow
```bash
python main.py --debug \
  --importar src/data/sample_data.csv \
  --simulate \
  --map \
  --analyze \
  --relatorio html
```

### Using the New Data Integration Features

#### Fetch ANATEL Data
```python
from src.utils import fetch_anatel_broadband_data, fetch_anatel_mobile_data

# Get broadband data
broadband = fetch_anatel_broadband_data(state='SP')

# Get mobile coverage data
mobile = fetch_anatel_mobile_data(state='RJ')
```

#### Fetch IBGE Demographics
```python
from src.utils import get_rural_areas_needing_connectivity, get_ibge_statistics_summary

# Get priority rural areas
priority_areas = get_rural_areas_needing_connectivity()

# Get Brazil connectivity summary
summary = get_ibge_statistics_summary()
```

#### Check Starlink Availability
```python
from src.utils import check_starlink_availability, get_starlink_service_plans

# Check availability at coordinates
availability = check_starlink_availability(-15.7801, -47.9292)

# Get service plans
plans = get_starlink_service_plans()
```

#### Work with LATAM Countries
```python
from src.utils import get_supported_countries, get_country_config

# Get all supported countries
countries = get_supported_countries()  # ['BR', 'AR', 'CL', 'CO', 'MX', ...]

# Get country configuration
config = get_country_config('AR')
print(config.name)  # 'Argentina'
print(config.telecom_regulator)  # 'ENACOM'
```

### CLI Arguments Reference

| Argument | Description | Choices/Format |
|----------|-------------|----------------|
| `--debug` | Enable verbose logging | Flag |
| `--relatorio <format>` | Generate report | json, csv, txt, html |
| `--importar <csv>` | Import from CSV | Path to file |
| `--simulate` | Simulate router impact | Flag |
| `--map` | Generate interactive map | Flag |
| `--analyze` | Analyze temporal trends | Flag |

---

## 📁 Project Structure

```
Rural-Connectivity-Mapper-2026/
├── main.py                      # CLI application
├── dashboard.py                 # NEW: Streamlit web dashboard
├── demo_workflow.py             # Complete demo
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore
│
├── src/
│   ├── models/                  # Data models
│   │   ├── ConnectivityPoint.py
│   │   ├── SpeedTest.py
│   │   └── QualityScore.py
│   │
│   ├── utils/                   # Utility modules (12 modules)
│   │   ├── validation_utils.py
│   │   ├── data_utils.py
│   │   ├── measurement_utils.py
│   │   ├── geocoding_utils.py
│   │   ├── report_utils.py
│   │   ├── simulation_utils.py
│   │   ├── mapping_utils.py
│   │   ├── analysis_utils.py
│   │   ├── anatel_utils.py      # NEW: ANATEL data integration
│   │   ├── ibge_utils.py        # NEW: IBGE demographics
│   │   ├── starlink_utils.py    # NEW: Starlink API
│   │   └── country_config.py    # NEW: LATAM country configs
│   │
│   └── data/
│       ├── sample_data.csv      # Sample points
│       └── pontos.json          # Data storage
│
├── tests/                       # Test suite (73 tests)
│   ├── test_models.py
│   ├── test_validation_utils.py
│   ├── test_data_utils.py
│   ├── test_measurement_utils.py
│   ├── test_geocoding_utils.py
│   ├── test_report_utils.py
│   ├── test_simulation_utils.py
│   ├── test_mapping_utils.py
│   ├── test_analysis_utils.py
│   ├── test_anatel_utils.py     # NEW: ANATEL tests
│   ├── test_ibge_utils.py       # NEW: IBGE tests
│   ├── test_starlink_utils.py   # NEW: Starlink tests
│   └── test_country_config.py   # NEW: Country config tests
│
└── docs/
    └── API.md                   # API reference
```

---

## 📊 Sample Data

Pre-configured connectivity data for 5 Brazilian cities:

| City | Provider | Download | Upload | Latency | Quality Score |
|------|----------|----------|--------|---------|---------------|
| **São Paulo** | Various | 85.2 Mbps | 12.5 Mbps | 45.3 ms | 78.2/100 (Good) |
| **Rio de Janeiro** | Claro | 92.1 Mbps | 15.3 Mbps | 38.7 ms | 82.2/100 (Excellent) |
| **Brasília** | **Starlink** ⭐ | 165.4 Mbps | 22.8 Mbps | 28.5 ms | **100/100 (Excellent)** |
| **Salvador** | Viasat | 75.3 Mbps | 9.8 Mbps | 68.2 ms | 50.6/100 (Fair) |
| **Fortaleza** | HughesNet | 62.8 Mbps | 7.2 Mbps | 95.4 ms | 25.1/100 (Poor) |

---

## 🎯 Starlink 2026 Metrics

### Target Specifications
- **Download Speed:** 50-200 Mbps
- **Upload Speed:** 10-20 Mbps
- **Latency:** 20-40 ms
- **Quality Score Weighting:** Speed (40%) + Latency (30%) + Stability (30%)

### Quality Score Algorithm
```python
Overall Score = (Speed Score × 0.40) + (Latency Score × 0.30) + (Stability Score × 0.30)

# Component calculations:
Speed Score = ((download/200 + upload/20) / 2) × 100
Latency Score = 100 - (latency - 20) × 1.25  # Capped at 100
Stability Score = 100 - (jitter × 2 + packet_loss × 10)
```

### Rating Tiers
- **Excellent:** ≥80/100 (Starlink target)
- **Good:** 60-79/100
- **Fair:** 40-59/100
- **Poor:** <40/100

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

**Test Coverage:**
- 73 total tests (365% of original requirement)
- 5 model tests
- 31 original utility tests
- 37 new integration tests (ANATEL, IBGE, Starlink, Country Config)
- 80%+ code coverage

---

## 🌍 Use Cases

1. **Rural Expansion Planning** - Identify priority areas for Starlink installations across LATAM
2. **ISP Performance Benchmarking** - Compare Starlink vs. traditional providers
3. **Infrastructure ROI Modeling** - Estimate impact of router upgrades
4. **Policy Advocacy** - Generate reports for government stakeholders using real ANATEL/IBGE data
5. **Academic Research** - Analyze connectivity's socioeconomic impact with demographic integration
6. **Cross-Country Analysis** - Compare connectivity metrics across 10 LATAM countries
7. **Starlink Market Entry** - Assess service availability and competitive landscape
8. **Digital Divide Studies** - Track rural-urban connectivity gaps with IBGE statistics

---

## 🌎 Supported Countries

The tool now supports **10 Latin American countries**:

| Country | Code | Telecom Regulator | Stats Agency | Starlink Status |
|---------|------|-------------------|--------------|-----------------|
| 🇧🇷 Brazil | BR | ANATEL | IBGE | Active (98.5% coverage) |
| 🇦🇷 Argentina | AR | ENACOM | INDEC | Active (97.0% coverage) |
| 🇨🇱 Chile | CL | SUBTEL | INE | Active (98.0% coverage) |
| 🇨🇴 Colombia | CO | CRC | DANE | Active (90.0% coverage) |
| 🇲🇽 Mexico | MX | IFT | INEGI | Active (95.0% coverage) |
| 🇵🇪 Peru | PE | OSIPTEL | INEI | Active (88.0% coverage) |
| 🇪🇨 Ecuador | EC | ARCOTEL | INEC | Active |
| 🇺🇾 Uruguay | UY | URSEC | INE | Active |
| 🇵🇾 Paraguay | PY | CONATEL | DGEEC | Active |
| 🇧🇴 Bolivia | BO | ATT | INE | Active |

---

## 🗺️ Roadmap

### v1.1.0 (Q1 2026) ✅ COMPLETED
- [x] Real-time ANATEL data integration
- [x] IBGE demographics integration  
- [x] Starlink API integration
- [x] Streamlit web dashboard
- [x] Support for 10 LATAM countries
- [x] Country-specific configurations
- [ ] SQLite database backend
- [ ] GitHub Actions CI/CD
- [ ] Docker containerization

### v1.2.0 (Q2 2026)
- [ ] REST API endpoints
- [ ] Machine learning predictions
- [ ] GeoJSON/KML export

### v2.0.0 (H2 2026)
- [ ] Multi-language UI (Portuguese/Spanish/English)
- [ ] Mobile app for field data collection
- [ ] Advanced analytics (churn prediction)
- [ ] Live Starlink satellite tracking

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Run tests: `pytest tests/ -v`
4. Submit Pull Request

**Guidelines:**
- Follow PEP 8 style
- Add docstrings (Google-style)
- Include tests for new features
- Update documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## 📄 License

**MIT License** - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Daniel Azevedo Novais

---

## 🙏 Acknowledgments

- **SpaceX Starlink** - 2026 expansion targets and satellite innovation
- **ANATEL** - Brazilian telecommunications data and regulatory framework
- **IBGE** - Brazilian demographic and geographic statistics
- **LATAM Regulators** - ENACOM, SUBTEL, CRC, IFT, OSIPTEL, and others
- **Brazilian ISPs** - Claro, Vivo, TIM, Oi for benchmarking
- **Satellite ISPs** - Viasat, HughesNet for rural comparisons
- **Open Source Community** - geopy, folium, pytest, pandas, streamlit, plotly

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)
- **Discussions:** [GitHub Discussions](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions)
- **Repository:** [Rural-Connectivity-Mapper-2026](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026)

---

## 📊 Project Statistics

- **40 files** across models, utilities, tests, documentation
- **5,119 lines of code** (Python)
- **73 passing tests** (100% success rate)
- **10 LATAM countries** fully configured
- **4 data sources** (ANATEL, IBGE, Starlink API, Manual)
- **6 dashboard views** in Streamlit
- **4 export formats** (JSON, CSV, TXT, HTML)
- **80%+ test coverage**

---

**🇧🇷 🇦🇷 🇨🇱 🇨🇴 🇲🇽 Made with ❤️ for improving rural connectivity across Latin America**

*Supporting Starlink's 2026 roadmap to connect 10M rural users and enable 20-30% agricultural productivity gains.*

---

## 📚 Additional Documentation

- **[New Features Guide](docs/NEW_FEATURES.md)** - Comprehensive guide for ANATEL, IBGE, Starlink API, and LATAM support
- **[API Reference](docs/API.md)** - Full API documentation

---

**Release Date:** January 4, 2026  
**Version:** 1.1.0  
**Status:** Production Ready ✅
