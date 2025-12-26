"""Connectivity Point model representing a geographic location with connectivity data."""

import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any


class ConnectivityPoint:
    """Represents a geographic point with connectivity information."""
    
    def __init__(
        self,
        latitude: float,
        longitude: float,
        address: Optional[str] = None,
        provider: Optional[str] = None,
        tags: Optional[List[str]] = None,
        timestamp: Optional[datetime] = None,
        point_id: Optional[str] = None
    ):
        """
        Initialize a connectivity point.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            address: Human-readable address (optional)
            provider: Internet service provider name (optional)
            tags: List of tags for categorization (optional)
            timestamp: Time of measurement (defaults to now)
            point_id: Unique identifier (optional)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.provider = provider
        self.tags = tags or []
        self.timestamp = timestamp or datetime.now()
        self.point_id = point_id or self._generate_id()
        self.speed_tests: List[Any] = []
        self.quality_score: Optional[Any] = None
    
    def _generate_id(self) -> str:
        """Generate a unique ID based on coordinates and timestamp."""
        data = f"{self.latitude}_{self.longitude}_{self.timestamp.isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def add_speed_test(self, speed_test: Any) -> None:
        """Add a speed test result to this point."""
        self.speed_tests.append(speed_test)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "point_id": self.point_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "provider": self.provider,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
            "speed_tests": [st.to_dict() for st in self.speed_tests],
            "quality_score": self.quality_score.to_dict() if self.quality_score else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConnectivityPoint':
        """Create ConnectivityPoint from dictionary."""
        from .speed_test import SpeedTest
        from .quality_score import QualityScore
        
        point = cls(
            latitude=data["latitude"],
            longitude=data["longitude"],
            address=data.get("address"),
            provider=data.get("provider"),
            tags=data.get("tags", []),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            point_id=data.get("point_id")
        )
        
        for st_data in data.get("speed_tests", []):
            point.add_speed_test(SpeedTest.from_dict(st_data))
        
        if data.get("quality_score"):
            point.quality_score = QualityScore.from_dict(data["quality_score"])
        
        return point
    
    def __repr__(self) -> str:
        """String representation."""
        return f"ConnectivityPoint(id={self.point_id}, lat={self.latitude}, lon={self.longitude}, provider={self.provider})"
