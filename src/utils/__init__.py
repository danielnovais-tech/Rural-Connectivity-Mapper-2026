"""Utils package for Rural Connectivity Mapper."""

from .validation_utils import validate_coordinates, validate_speed_test, validate_provider
from .data_utils import load_data, save_data, backup_data
from .measurement_utils import measure_speed
from .geocoding_utils import geocode_coordinates, geocode_address
from .report_utils import generate_report
from .simulation_utils import simulate_router_impact
from .mapping_utils import generate_map
from .analysis_utils import analyze_temporal_evolution
from .anatel_utils import (
    fetch_anatel_broadband_data,
    fetch_anatel_mobile_data,
    get_anatel_provider_stats,
    convert_anatel_to_connectivity_points
)
from .ibge_utils import (
    fetch_ibge_municipalities,
    get_rural_areas_needing_connectivity,
    get_ibge_statistics_summary
)
from .starlink_utils import (
    check_starlink_availability,
    get_starlink_service_plans,
    get_starlink_coverage_map
)
from .country_config import (
    get_supported_countries,
    get_country_config,
    get_latam_summary
)

__all__ = [
    'validate_coordinates',
    'validate_speed_test',
    'validate_provider',
    'load_data',
    'save_data',
    'backup_data',
    'measure_speed',
    'geocode_coordinates',
    'geocode_address',
    'generate_report',
    'simulate_router_impact',
    'generate_map',
    'analyze_temporal_evolution',
    'fetch_anatel_broadband_data',
    'fetch_anatel_mobile_data',
    'get_anatel_provider_stats',
    'convert_anatel_to_connectivity_points',
    'fetch_ibge_municipalities',
    'get_rural_areas_needing_connectivity',
    'get_ibge_statistics_summary',
    'check_starlink_availability',
    'get_starlink_service_plans',
    'get_starlink_coverage_map',
    'get_supported_countries',
    'get_country_config',
    'get_latam_summary'
]
