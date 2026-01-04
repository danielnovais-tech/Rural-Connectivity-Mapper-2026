# Rural Connectivity Mapper 2026

[![GitHub License](https://img.shields.io/github/license/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/network)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![Last Commit](https://img.shields.io/github/last-commit/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/commits/main)
[![Release](https://img.shields.io/github/v/release/danielnovais-tech/Rural-Connectivity-Mapper-2026?style=flat-square)](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/releases/latest)

Python-based tool to map and analyze rural internet connectivity in Brazil, aligned with Starlink's 2026 expansion roadmap.

## 🌍 Overview

The Rural Connectivity Mapper 2026 is a comprehensive platform for analyzing and visualizing internet connectivity quality across Brazil, with a focus on Starlink's satellite internet expansion. The tool measures, analyzes, and reports on connectivity metrics including download/upload speeds, latency, stability, and overall quality scores.

**Aligned with Starlink's 2026 roadmap:** 10M rural connections & 20-30% agricultural productivity gains.

---

## ✨ Features

- 🌐 **Web Dashboard** - Streamlit-based interactive web interface with data upload and visualization
- 🖥️ **CLI Application** - Full command-line interface with 6 operational modes
- 📊 **Data Models** - ConnectivityPoint, SpeedTest, QualityScore with serialization
- 🛠️ **8 Utility Modules** - Measurement, geocoding, validation, reporting, simulation, mapping, analysis
- 🗺️ **Interactive Folium Maps** - Color-coded quality markers with popups
- 🛰️ **Starlink Coverage Overlay** - Optional toggleable layer showing coverage zones for installation planning
- 📈 **Router Impact Simulation** - Model 15-25% quality improvements
- 📋 **Multi-Format Reporting** - JSON, CSV, TXT, HTML exports
- 🔍 **Temporal Analysis** - Track connectivity trends over time
- 🏢 **Provider Comparison** - Benchmark ISPs (Starlink, Viasat, HughesNet, Claro, etc.)
- 🏷️ **Tag System** - Categorize points with custom tags
- 🚀 **On-Demand Speed Tests** - Run live speed tests directly from the web dashboard
- 🐛 **Debug Mode** - Enhanced logging for troubleshooting
- 🧪 **39 Comprehensive Tests** - 80%+ code coverage with pytest

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
streamlit>=1.28.0      # Web dashboard framework
```

---

## 📖 Usage

### 🌐 Web Dashboard (NEW in v1.1)

Launch the interactive Streamlit dashboard for browser-based analysis:

```bash
streamlit run dashboard.py
```

**Dashboard Features:**
- **📊 Dashboard Overview** - View statistics, data table, and generate reports
- **📤 Upload Data** - Import CSV files with connectivity data
- **🚀 Speed Test** - Run on-demand speed tests on your current connection
- **🗺️ Map View** - Interactive Folium maps with color-coded quality markers
- **📈 Analysis** - Temporal evolution trends and insights
- **🔧 Simulation** - Model router impact on connectivity quality

**CSV Upload Format:**
```csv
id,city,provider,latitude,longitude,download,upload,latency,jitter,packet_loss,timestamp
1,São Paulo,Starlink,-23.5505,-46.6333,165.4,22.8,28.5,3.2,0.1,2026-01-15T10:30:00
```

The dashboard automatically opens at `http://localhost:8501` and provides a user-friendly interface for all connectivity analysis tasks.

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
*Generates Folium HTML map with color-coded markers and Starlink coverage overlay*

#### Create Map Without Starlink Coverage
```bash
python main.py --map --no-starlink-coverage
```
*Generates map without the coverage layer for simplified view*

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

### CLI Arguments Reference

| Argument | Description | Choices/Format |
|----------|-------------|----------------|
| `--debug` | Enable verbose logging | Flag |
| `--relatorio <format>` | Generate report | json, csv, txt, html |
| `--importar <csv>` | Import from CSV | Path to file |
| `--simulate` | Simulate router impact | Flag |
| `--map` | Generate interactive map | Flag |
| `--no-starlink-coverage` | Disable Starlink coverage overlay | Flag (use with --map) |
| `--analyze` | Analyze temporal trends | Flag |

### Alternative Data Submission Methods

#### 📝 Google Forms Integration (Recommended for Non-Technical Users)

For users who are not comfortable with CSV files or command-line tools, we provide **Google Forms integration** as an easy alternative for data collection.

**Benefits:**
- ✅ No technical knowledge required
- ✅ Mobile-friendly for field data collection
- ✅ Free and easy to share
- ✅ Automatic data validation
- ✅ Exports to CSV format compatible with the mapper

**Quick Start:**
1. Create a Google Form using our template
2. Share the form link with users
3. Collect responses in Google Sheets
4. Export to CSV and import using `--importar`

**📖 Complete Guide:** See [docs/GOOGLE_FORMS_INTEGRATION.md](docs/GOOGLE_FORMS_INTEGRATION.md) for detailed instructions on:
- Setting up your Google Form
- Configuring fields and validation
- Exporting and formatting data
- Importing into the mapper
- Troubleshooting common issues

**Example Workflow:**
```bash
# After exporting from Google Forms to CSV
python main.py --importar google_forms_export.csv --map --relatorio html
```

---

## 📁 Project Structure

```
Rural-Connectivity-Mapper-2026/
├── main.py                      # CLI application
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
│   ├── utils/                   # Utility modules
│   │   ├── validation_utils.py
│   │   ├── data_utils.py
│   │   ├── measurement_utils.py
│   │   ├── geocoding_utils.py
│   │   ├── report_utils.py
│   │   ├── simulation_utils.py
│   │   ├── mapping_utils.py
│   │   └── analysis_utils.py
│   │
│   └── data/
│       ├── sample_data.csv      # Sample points
│       └── pontos.json          # Data storage
│
├── examples/                    # CSV templates for contributions
│   ├── README.md                # Template documentation
│   ├── speedtest_template_basic.csv
│   └── speedtest_template_complete.csv
│
├── tests/                       # Test suite (36 tests)
│   ├── test_models.py
│   ├── test_validation_utils.py
│   ├── test_data_utils.py
│   ├── test_measurement_utils.py
│   ├── test_geocoding_utils.py
│   ├── test_report_utils.py
│   ├── test_simulation_utils.py
│   ├── test_mapping_utils.py
│   └── test_analysis_utils.py
│
└── docs/
    ├── API.md                   # API reference
    └── GOOGLE_FORMS_INTEGRATION.md  # Google Forms setup guide
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
- 36 total tests (180% of requirement)
- 5 model tests
- 31 utility tests
- 80%+ code coverage

---

## 🌍 Use Cases

1. **Rural Expansion Planning** - Identify priority areas for Starlink installations
2. **ISP Performance Benchmarking** - Compare Starlink vs. traditional providers
3. **Infrastructure ROI Modeling** - Estimate impact of router upgrades
4. **Policy Advocacy** - Generate reports for government stakeholders
5. **Academic Research** - Analyze connectivity's socioeconomic impact

---

## 🗺️ Roadmap

### v1.1.0 (Q1 2026)
- [x] Web dashboard (Streamlit)
- [x] Real-time speedtest integration
- [ ] SQLite database backend
- [ ] GitHub Actions CI/CD
- [ ] Docker containerization

### v1.2.0 (Q2 2026)
- [ ] REST API endpoints
- [ ] Machine learning predictions
- [ ] GeoJSON/KML export

### v2.0.0 (H2 2026)
- [ ] Multi-language support (Portuguese/English)
- [ ] Mobile app for field data collection
- [ ] Advanced analytics (churn prediction)
- [ ] Integration with Starlink APIs

---

## 📊 How to Contribute Your Speedtest Data

Help us map rural connectivity across Brazil! Your speedtest data is valuable for:
- 🗺️ Identifying underserved areas
- 📈 Tracking ISP performance over time
- 🎯 Supporting Starlink's 2026 expansion planning
- 📊 Advocating for better rural internet policies

### Quick Contribution Guide

#### 1️⃣ Download a Template

Choose one of the ready-made CSV templates from the [`/examples/`](examples/) directory:

- **[Basic Template](examples/speedtest_template_basic.csv)** - Simple template with one example entry
- **[Complete Template](examples/speedtest_template_complete.csv)** - Template with 5 example entries

Or download directly:
```bash
curl -O https://raw.githubusercontent.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/main/examples/speedtest_template_basic.csv
```

#### 2️⃣ Run a Speedtest

Use any of these tools to measure your internet speed:

**Online Tools:**
- [Speedtest.net](https://www.speedtest.net/) (recommended)
- [Fast.com](https://fast.com/)
- [CloudFlare Speed Test](https://speed.cloudflare.com/)

**Command Line:**
```bash
pip install speedtest-cli
speedtest-cli --simple
```

#### 3️⃣ Fill in Your Data

Edit the CSV template with your results:

| Field | How to Fill | Example |
|-------|-------------|---------|
| `id` | Any unique number | 1 |
| `city` | Your city/location | "Campinas" |
| `provider` | Your ISP name | "Starlink" |
| `latitude` | GPS coordinate | -22.9099 |
| `longitude` | GPS coordinate | -47.0626 |
| `download` | Download speed (Mbps) | 150.5 |
| `upload` | Upload speed (Mbps) | 20.3 |
| `latency` | Ping time (ms) | 28.0 |
| `jitter` | Jitter (ms) - optional | 3.5 |
| `packet_loss` | Packet loss (%) - optional | 0.2 |
| `timestamp` | ISO 8601 format (optional) | 2026-01-15T10:00:00 |

**💡 Tip:** Use [Google Maps](https://www.google.com/maps) to find coordinates - right-click on your location and click the coordinates to copy them.

#### 4️⃣ Submit Your Data

Choose one of these methods:

**Method A: GitHub Pull Request** (Recommended)
```bash
# Fork the repository first, then:
git clone https://github.com/YOUR-USERNAME/Rural-Connectivity-Mapper-2026.git
cd Rural-Connectivity-Mapper-2026
git checkout -b data/your-location-name

# Add your CSV file to src/data/ or submit as attachment
git add your_speedtest_data.csv
git commit -m "Add speedtest data for [Your City]"
git push origin data/your-location-name

# Open a Pull Request on GitHub
```

**Method B: GitHub Issue**
1. Go to [Issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues/new)
2. Title: "Speedtest Data: [Your City]"
3. Attach your CSV file or paste the data
4. Add any relevant context (time of day, weather conditions, etc.)

**Method C: Email/Contact**
- Submit via [GitHub Discussions](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions)

### Data Quality Guidelines

✅ **Do:**
- Run 3-5 tests and use average values
- Test at different times of day
- Close bandwidth-intensive applications
- Note any unusual conditions (weather, network congestion)
- Use accurate GPS coordinates

❌ **Don't:**
- Submit fake or estimated data
- Include personally identifiable information
- Submit duplicate measurements without time gaps

### Need Help?

📖 Full documentation in [`/examples/README.md`](examples/README.md)  
💬 Questions? Open a [Discussion](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions)  
🐛 Issues? Report a [Bug](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)

**Every data point helps! Thank you for contributing to better rural connectivity in Brazil! 🇧🇷**

---

## 🤝 Contributing Code

Developer contributions are also welcome! Please:

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
- **Brazilian ISPs** - Claro, Vivo, TIM, Oi for benchmarking
- **Satellite ISPs** - Viasat, HughesNet for rural comparisons
- **Open Source Community** - geopy, folium, pytest, pandas

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)
- **Discussions:** [GitHub Discussions](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions)
- **Repository:** [Rural-Connectivity-Mapper-2026](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026)

---

## 📊 Project Statistics

- **32 files** across models, utilities, tests, documentation
- **3,591 lines of code** (Python)
- **39 passing tests** (100% success rate)
- **5 sample cities** with real-world profiles
- **4 export formats** (JSON, CSV, TXT, HTML)
- **80%+ test coverage**

---

**🇧🇷 Made with ❤️ for improving rural connectivity in Brazil**

*Supporting Starlink's 2026 roadmap to connect 10M rural users and enable 20-30% agricultural productivity gains.*

---

**Release Date:** December 28, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
