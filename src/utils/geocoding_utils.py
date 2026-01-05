"""Geocoding utilities for coordinate and address conversion."""

import logging
from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from .config_utils import get_language, get_default_country

logger = logging.getLogger(__name__)

# Initialize geocoder with user agent
geolocator = Nominatim(user_agent="rural-connectivity-mapper-2026")


def geocode_coordinates(
    latitude: float, 
    longitude: float, 
    timeout: int = 10,
    country_code: Optional[str] = None
) -> Optional[str]:
    """Convert coordinates to address using reverse geocoding.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        timeout: Request timeout in seconds (default: 10)
        country_code: ISO country code for language preference (default: uses default country)
        
    Returns:
        Optional[str]: Address string if successful, None otherwise
    """
    try:
        logger.debug(f"Geocoding coordinates: ({latitude}, {longitude})")
        
        # Determine language from country code
        if country_code is None:
            country_code = get_default_country()
        language = get_language(country_code)
        
        location = geolocator.reverse(
            f"{latitude}, {longitude}",
            timeout=timeout,
            language=language
        )
        
        if location:
            address = location.address
            logger.info(f"Geocoded to: {address}")
            return address
        else:
            logger.warning(f"No address found for coordinates ({latitude}, {longitude})")
            return None
    
    except GeocoderTimedOut:
        logger.error(f"Geocoding timeout for coordinates ({latitude}, {longitude})")
        return None
    except GeocoderServiceError as e:
        logger.error(f"Geocoder service error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error geocoding coordinates: {e}")
        return None


def geocode_address(
    address: str, 
    timeout: int = 10,
    country_code: Optional[str] = None
) -> Optional[Tuple[float, float]]:
    """Convert address to coordinates using forward geocoding.
    
    Args:
        address: Address string to geocode
        timeout: Request timeout in seconds (default: 10)
        country_code: ISO country code (optional, for future enhancements)
        
    Returns:
        Optional[Tuple[float, float]]: (latitude, longitude) if successful, None otherwise
        
    Note:
        The country_code parameter is currently used for API consistency but not 
        applied to Nominatim's geocode method, which primarily uses address content
        to determine location.
    """
    try:
        logger.debug(f"Geocoding address: {address}")
        
        location = geolocator.geocode(address, timeout=timeout)
        
        if location:
            coords = (location.latitude, location.longitude)
            logger.info(f"Geocoded '{address}' to: {coords}")
            return coords
        else:
            logger.warning(f"No coordinates found for address: {address}")
            return None
    
    except GeocoderTimedOut:
        logger.error(f"Geocoding timeout for address: {address}")
        return None
    except GeocoderServiceError as e:
        logger.error(f"Geocoder service error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error geocoding address: {e}")
        return None
