"""Validation utilities for data integrity checks."""

from typing import Any, Optional
import logging
from .config_utils import get_providers, get_default_country

logger = logging.getLogger(__name__)


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


def validate_speed_test(speed_test: Any) -> bool:
    """Validate speed test measurements.
    
    Args:
        speed_test: SpeedTest object or dict to validate
        
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
        
        return True
    except Exception as e:
        logger.error(f"Error validating speed test: {e}")
        return False


def validate_provider(provider: str, country_code: Optional[str] = None) -> bool:
    """Validate internet service provider name.
    
    Args:
        provider: Provider name to validate
        country_code: ISO country code for provider list (default: uses default country)
        
    Returns:
        bool: True if provider is known, False otherwise
    """
    if not provider or not isinstance(provider, str):
        logger.warning(f"Invalid provider: {provider}")
        return False
    
    # Get providers for the specified country
    if country_code is None:
        country_code = get_default_country()
    
    known_providers = get_providers(country_code)
    
    if provider not in known_providers:
        logger.warning(
            f"Unknown provider: {provider}. Known providers for {country_code}: {', '.join(known_providers)}"
        )
        return False
    
    return True
