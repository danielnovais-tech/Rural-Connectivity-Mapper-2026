"""ConnectivityPoint model for location-based connectivity data."""

from typing import Dict, Optional
from datetime import datetime
import uuid
from .SpeedTest import SpeedTest
from .QualityScore import QualityScore


class ConnectivityPoint:
    """Represents a connectivity measurement point with location and quality data.
    
    Attributes:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        provider (str): Internet service provider name
        speed_test (SpeedTest): Speed test measurement results
        quality_score (QualityScore): Calculated quality score
        timestamp (str): ISO format timestamp of measurement
        id (str): Unique identifier for the point
    """
    
    def __init__(
        self,
        latitude: float,
        longitude: float,
        provider: str,
        speed_test: SpeedTest,
        quality_score: Optional[QualityScore] = None,
        timestamp: Optional[str] = None,
        point_id: Optional[str] = None
    ):
        """Initialize ConnectivityPoint instance.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            provider: Internet service provider name
            speed_test: SpeedTest instance with measurements
            quality_score: QualityScore instance, auto-calculated if None
            timestamp: ISO format timestamp, auto-generated if None
            point_id: Unique identifier, auto-generated if None
        """
        self.latitude = latitude
        self.longitude = longitude
        self.provider = provider
        self.speed_test = speed_test
        self.quality_score = quality_score if quality_score else QualityScore.calculate(speed_test)
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        self.id = point_id if point_id else str(uuid.uuid4())
    
    def to_dict(self) -> Dict:
        """Convert ConnectivityPoint to dictionary representation.
        
        Returns:
            Dict: Dictionary containing all connectivity point data
        """
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'provider': self.provider,
            'speed_test': self.speed_test.to_dict(),
            'quality_score': self.quality_score.to_dict(),
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConnectivityPoint':
        """Create ConnectivityPoint instance from dictionary.
        
        Args:
            data: Dictionary containing connectivity point data
            
        Returns:
            ConnectivityPoint: New ConnectivityPoint instance
        """
        speed_test = SpeedTest.from_dict(data.get('speed_test', {}))
        
        # If quality_score exists in dict, use it; otherwise it will be auto-calculated
        quality_score = None
        if 'quality_score' in data:
            qs_data = data['quality_score']
            quality_score = QualityScore(
                overall_score=qs_data.get('overall_score', 0.0),
                speed_score=qs_data.get('speed_score', 0.0),
                latency_score=qs_data.get('latency_score', 0.0),
                stability_score=qs_data.get('stability_score', 0.0)
            )
        
        return cls(
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            provider=data.get('provider', 'Unknown'),
            speed_test=speed_test,
            quality_score=quality_score,
            timestamp=data.get('timestamp'),
            point_id=data.get('id')
        )
    
    def __repr__(self) -> str:
        """String representation of ConnectivityPoint.
        
        Returns:
            str: Formatted string representation
        """
        return (
            f"ConnectivityPoint(id={self.id[:8]}..., "
            f"provider={self.provider}, "
            f"location=({self.latitude:.4f}, {self.longitude:.4f}), "
            f"quality={self.quality_score.rating})"
        )
