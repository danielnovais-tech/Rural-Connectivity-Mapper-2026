"""Geocoding utilities for coordinate and address conversion."""

import logging
import time
from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderUnavailable, GeocoderQuotaExceeded

logger = logging.getLogger(__name__)

# Initialize geocoder with user agent
geolocator = Nominatim(user_agent="rural-connectivity-mapper-2026")

# Rate limiting configuration (Nominatim allows 1 request per second)
RATE_LIMIT_DELAY = 1.0  # seconds between requests
_last_request_time = 0


def _wait_for_rate_limit():
    """Ensure we respect the rate limit by waiting if necessary."""
    global _last_request_time
    current_time = time.time()
    time_since_last_request = current_time - _last_request_time
    
    if time_since_last_request < RATE_LIMIT_DELAY:
        sleep_time = RATE_LIMIT_DELAY - time_since_last_request
        logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
        time.sleep(sleep_time)
    
    _last_request_time = time.time()


def geocode_coordinates(
    latitude: float,
    longitude: float,
    timeout: int = 10,
    max_retries: int = 3
) -> Optional[str]:
    """Convert coordinates to address using reverse geocoding.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        timeout: Request timeout in seconds (default: 10)
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        Optional[str]: Address string if successful, None otherwise
    """
    # Validate coordinates first
    try:
        lat = float(latitude)
        lon = float(longitude)
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            logger.error(f"Invalid coordinates: ({latitude}, {longitude})")
            return None
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid coordinate types: {e}")
        return None
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Geocoding coordinates: ({latitude}, {longitude}) - Attempt {attempt + 1}/{max_retries}")
            
            # Respect rate limiting
            _wait_for_rate_limit()
            
            location = geolocator.reverse(
                f"{latitude}, {longitude}",
                timeout=timeout,
                language='pt'
            )
            
            if location:
                address = location.address
                logger.info(f"Geocoded to: {address}")
                return address
            else:
                logger.warning(f"No address found for coordinates ({latitude}, {longitude})")
                return None
        
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timeout for coordinates ({latitude}, {longitude}) - Attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.debug(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Geocoding failed after {max_retries} attempts due to timeout")
                return None
                
        except GeocoderQuotaExceeded:
            logger.error(f"Geocoding quota exceeded. Please try again later.")
            return None
            
        except GeocoderUnavailable:
            logger.warning(f"Geocoding service unavailable - Attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.debug(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Geocoding service unavailable after {max_retries} attempts")
                return None
                
        except GeocoderServiceError as e:
            logger.error(f"Geocoder service error: {e}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error geocoding coordinates: {e}")
            return None
    
    return None


def geocode_address(
    address: str,
    timeout: int = 10,
    max_retries: int = 3
) -> Optional[Tuple[float, float]]:
    """Convert address to coordinates using forward geocoding.
    
    Args:
        address: Address string to geocode
        timeout: Request timeout in seconds (default: 10)
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        Optional[Tuple[float, float]]: (latitude, longitude) if successful, None otherwise
    """
    if not address or not isinstance(address, str):
        logger.error(f"Invalid address: {address}")
        return None
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Geocoding address: {address} - Attempt {attempt + 1}/{max_retries}")
            
            # Respect rate limiting
            _wait_for_rate_limit()
            
            location = geolocator.geocode(address, timeout=timeout)
            
            if location:
                coords = (location.latitude, location.longitude)
                logger.info(f"Geocoded '{address}' to: {coords}")
                return coords
            else:
                logger.warning(f"No coordinates found for address: {address}")
                return None
        
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timeout for address: {address} - Attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.debug(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Geocoding failed after {max_retries} attempts due to timeout")
                return None
                
        except GeocoderQuotaExceeded:
            logger.error(f"Geocoding quota exceeded. Please try again later.")
            return None
            
        except GeocoderUnavailable:
            logger.warning(f"Geocoding service unavailable - Attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.debug(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Geocoding service unavailable after {max_retries} attempts")
                return None
                
        except GeocoderServiceError as e:
            logger.error(f"Geocoder service error: {e}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error geocoding address: {e}")
            return None
    
    return None
