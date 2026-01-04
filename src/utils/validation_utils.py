"""Validation utilities for data integrity checks."""

from typing import Any, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# Known providers in Brazil
KNOWN_PROVIDERS = [
    'Starlink', 'Viasat', 'HughesNet', 'Claro', 'Vivo', 
    'TIM', 'Oi', 'Various', 'Unknown'
]

# Realistic bounds for speed test values
SPEED_TEST_BOUNDS = {
    'download': (0.0, 1000.0),  # Mbps - max for satellite/fiber
    'upload': (0.0, 500.0),     # Mbps
    'latency': (0.0, 2000.0),   # ms - max for satellite
    'jitter': (0.0, 500.0),     # ms
    'packet_loss': (0.0, 100.0) # percentage
}


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate geographic coordinates.
    
    Args:
        latitude: Latitude value to validate
        longitude: Longitude value to validate
        
    Returns:
        bool: True if coordinates are valid, False otherwise
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if lat < -90 or lat > 90:
            logger.warning(f"Invalid latitude: {lat}. Must be between -90 and 90.")
            return False
        
        if lon < -180 or lon > 180:
            logger.warning(f"Invalid longitude: {lon}. Must be between -180 and 180.")
            return False
        
        return True
    except (ValueError, TypeError) as e:
        logger.error(f"Error validating coordinates: {e}")
        return False


def validate_speed_test(speed_test: Any, check_bounds: bool = True) -> bool:
    """Validate speed test measurements.
    
    Args:
        speed_test: SpeedTest object or dict to validate
        check_bounds: If True, validate values are within realistic bounds
        
    Returns:
        bool: True if speed test data is valid, False otherwise
    """
    try:
        # Handle both SpeedTest objects and dicts
        if hasattr(speed_test, 'to_dict'):
            data = speed_test.to_dict()
        else:
            data = speed_test
        
        # Check required fields exist and are positive
        required_fields = ['download', 'upload', 'latency']
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return False
            
            value = data[field]
            if not isinstance(value, (int, float)):
                logger.warning(f"Field {field} must be numeric, got {type(value)}")
                return False
            
            if value < 0:
                logger.warning(f"Field {field} must be positive, got {value}")
                return False
            
            # Check realistic bounds if enabled
            if check_bounds and field in SPEED_TEST_BOUNDS:
                min_val, max_val = SPEED_TEST_BOUNDS[field]
                if value < min_val or value > max_val:
                    logger.warning(
                        f"Field {field} value {value} is outside realistic bounds "
                        f"[{min_val}, {max_val}]"
                    )
                    return False
        
        # Validate optional fields if present
        optional_fields = ['jitter', 'packet_loss', 'stability']
        for field in optional_fields:
            if field in data:
                value = data[field]
                if not isinstance(value, (int, float)):
                    logger.warning(f"Field {field} must be numeric, got {type(value)}")
                    return False
                if value < 0:
                    logger.warning(f"Field {field} must be positive, got {value}")
                    return False
                
                # Check realistic bounds if enabled
                if check_bounds and field in SPEED_TEST_BOUNDS:
                    min_val, max_val = SPEED_TEST_BOUNDS[field]
                    if value < min_val or value > max_val:
                        logger.warning(
                            f"Field {field} value {value} is outside realistic bounds "
                            f"[{min_val}, {max_val}]"
                        )
                        return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating speed test: {e}")
        return False


def validate_provider(provider: str) -> bool:
    """Validate internet service provider name.
    
    Args:
        provider: Provider name to validate
        
    Returns:
        bool: True if provider is known, False otherwise
    """
    if not provider or not isinstance(provider, str):
        logger.warning(f"Invalid provider: {provider}")
        return False
    
    if provider not in KNOWN_PROVIDERS:
        logger.warning(
            f"Unknown provider: {provider}. Known providers: {', '.join(KNOWN_PROVIDERS)}"
        )
        return False
    
    return True


def validate_csv_row(row: Dict[str, str], row_num: int) -> Tuple[bool, str]:
    """Validate a CSV row for required fields and data types.
    
    Args:
        row: Dictionary representing a CSV row
        row_num: Row number for error reporting
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    required_fields = ['latitude', 'longitude', 'provider', 'download', 'upload', 'latency']
    
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in row or not row[field]]
    if missing_fields:
        return False, f"Row {row_num}: Missing required fields: {', '.join(missing_fields)}"
    
    # Validate numeric fields can be converted to float
    numeric_fields = ['latitude', 'longitude', 'download', 'upload', 'latency', 'jitter', 'packet_loss']
    for field in numeric_fields:
        if field in row and row[field]:
            try:
                value = float(row[field])
                
                # Validate specific field ranges
                if field == 'latitude':
                    if value < -90 or value > 90:
                        return False, f"Row {row_num}: Invalid latitude {value} (must be between -90 and 90)"
                elif field == 'longitude':
                    if value < -180 or value > 180:
                        return False, f"Row {row_num}: Invalid longitude {value} (must be between -180 and 180)"
                elif field in SPEED_TEST_BOUNDS:
                    min_val, max_val = SPEED_TEST_BOUNDS[field]
                    if value < min_val or value > max_val:
                        return False, f"Row {row_num}: Invalid {field} {value} (must be between {min_val} and {max_val})"
                        
            except (ValueError, TypeError) as e:
                return False, f"Row {row_num}: Invalid numeric value for {field}: {row[field]}"
    
    # Validate provider
    if row['provider'] not in KNOWN_PROVIDERS:
        logger.info(f"Row {row_num}: Unknown provider '{row['provider']}' will be accepted but logged")
    
    return True, ""
