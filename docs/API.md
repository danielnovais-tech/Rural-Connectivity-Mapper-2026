# API Documentation

## Models

### ConnectivityPoint

```python
class ConnectivityPoint:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        address: Optional[str] = None,
        provider: Optional[str] = None,
        tags: Optional[List[str]] = None,
        timestamp: Optional[datetime] = None,
        point_id: Optional[str] = None
    )
```

**Methods:**
- `add_speed_test(speed_test: SpeedTest)`: Add a speed test result
- `to_dict() -> Dict[str, Any]`: Convert to dictionary
- `from_dict(data: Dict[str, Any]) -> ConnectivityPoint`: Create from dictionary

### SpeedTest

```python
class SpeedTest:
    def __init__(
        self,
        download_speed: float,
        upload_speed: float,
        latency: float,
        jitter: Optional[float] = None,
        packet_loss: Optional[float] = None,
        server: Optional[str] = None,
        timestamp: Optional[datetime] = None
    )
```

**Methods:**
- `calculate_stability() -> float`: Calculate stability score (0-100)
- `to_dict() -> Dict[str, Any]`: Convert to dictionary
- `from_dict(data: Dict[str, Any]) -> SpeedTest`: Create from dictionary

### QualityScore

```python
class QualityScore:
    def __init__(
        self,
        speed_score: float,
        latency_score: float,
        stability_score: float,
        overall_score: Optional[float] = None
    )
```

**Methods:**
- `get_rating() -> str`: Get quality rating (Excellent/Good/Fair/Poor/Very Poor)
- `to_dict() -> Dict[str, Any]`: Convert to dictionary
- `from_dict(data: Dict[str, Any]) -> QualityScore`: Create from dictionary

## Utilities

### Geocoding

```python
def geocode_address(address: str, timeout: int = 10) -> Optional[Tuple[float, float]]
```
Convert an address to coordinates.

```python
def reverse_geocode(latitude: float, longitude: float, timeout: int = 10) -> Optional[str]
```
Convert coordinates to an address.

### Speed Testing

```python
def run_speed_test(server_id: Optional[int] = None) -> Optional[SpeedTest]
```
Run an internet speed test using speedtest-cli.

```python
def get_available_servers(limit: int = 10) -> list
```
Get list of available speed test servers.

### Quality Calculator

```python
def calculate_speed_score(download: float, upload: float) -> float
```
Calculate speed score (0-100) based on download/upload speeds.

```python
def calculate_latency_score(latency: float) -> float
```
Calculate latency score (0-100).

```python
def calculate_quality_score(speed_tests: List[SpeedTest]) -> QualityScore
```
Calculate overall quality score from speed test results.

### Report Generator

```python
class ReportGenerator:
    def __init__(self, output_dir: str = "reports")
```

**Methods:**
- `generate_txt_report(points: List[ConnectivityPoint], filename: str = None) -> str`
- `generate_json_report(points: List[ConnectivityPoint], filename: str = None) -> str`
- `generate_csv_report(points: List[ConnectivityPoint], filename: str = None) -> str`
- `generate_html_report(points: List[ConnectivityPoint], filename: str = None) -> str`
- `generate_all_reports(points: List[ConnectivityPoint]) -> Dict[str, str]`

### CSV Handler

```python
def export_to_csv(points: List[ConnectivityPoint], filepath: str) -> None
```
Export connectivity points to CSV file.

```python
def import_from_csv(filepath: str) -> List[ConnectivityPoint]
```
Import connectivity points from CSV file.

### Data Analysis

```python
def analyze_temporal_trends(
    points: List[ConnectivityPoint],
    time_window: timedelta = timedelta(days=30)
) -> Dict[str, Any]
```
Analyze temporal trends in connectivity data.

```python
def compare_providers(points: List[ConnectivityPoint]) -> Dict[str, Any]
```
Compare connectivity quality across providers.

```python
def get_summary_statistics(points: List[ConnectivityPoint]) -> Dict[str, Any]
```
Get summary statistics for all points.

## CLI Options

```
usage: main.py [-h] [--interactive] [--import IMPORT_FILE] [--export EXPORT_FILE]
               [--report] [--output OUTPUT] [--analyze {temporal,providers,summary}]
               [--num-tests NUM_TESTS] [--debug]

options:
  -h, --help            show this help message and exit
  --interactive, -i     Interactive mode to create and test points
  --import IMPORT_FILE  Import points from CSV or JSON file
  --export EXPORT_FILE  Export points to CSV file
  --report, -r          Generate reports (TXT, JSON, CSV, HTML)
  --output OUTPUT, -o OUTPUT
                        Output directory for reports (default: reports)
  --analyze {temporal,providers,summary}, -a {temporal,providers,summary}
                        Run analysis
  --num-tests NUM_TESTS, -n NUM_TESTS
                        Number of speed tests to run per point (default: 1)
  --debug, -d           Enable debug logging
```
