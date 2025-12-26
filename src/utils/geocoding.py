"""Geocoding utilities using geopy."""

from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def geocode_address(address: str, timeout: int = 10) -> Optional[Tuple[float, float]]:
    """
    Convert an address to coordinates.
    
    Args:
        address: Address string to geocode
        timeout: Request timeout in seconds
    
    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    try:
        from geopy.geocoders import Nominatim
        
        geolocator = Nominatim(user_agent="rural_connectivity_mapper_2026")
        location = geolocator.geocode(address, timeout=timeout)
        
        if location:
            logger.info(f"Geocoded address '{address}' to ({location.latitude}, {location.longitude})")
            return (location.latitude, location.longitude)
        else:
            logger.warning(f"Could not geocode address: {address}")
            return None
    except Exception as e:
        logger.error(f"Error geocoding address '{address}': {e}")
        return None


def reverse_geocode(
    latitude: float, 
    longitude: float, 
    timeout: int = 10
) -> Optional[str]:
    """
    Convert coordinates to an address.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        timeout: Request timeout in seconds
    
    Returns:
        Address string or None if not found
    """
    try:
        from geopy.geocoders import Nominatim
        
        geolocator = Nominatim(user_agent="rural_connectivity_mapper_2026")
        location = geolocator.reverse(f"{latitude}, {longitude}", timeout=timeout)
        
        if location:
            logger.info(f"Reverse geocoded ({latitude}, {longitude}) to '{location.address}'")
            return location.address
        else:
            logger.warning(f"Could not reverse geocode: ({latitude}, {longitude})")
            return None
    except Exception as e:
        logger.error(f"Error reverse geocoding ({latitude}, {longitude}): {e}")
        return None
