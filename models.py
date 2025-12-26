"""
Models for Rural Connectivity Mapper 2026

This module defines the AccessPoint class for representing internet connectivity points.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any


class AccessPoint:
    """
    Represents an internet access point with connectivity metrics.
    
    Attributes:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        provider (str): Internet service provider name
        address (str): Physical address or location description
        download (float): Download speed in Mbps
        upload (float): Upload speed in Mbps
        latency (float): Latency in milliseconds
        stability (float): Connection stability percentage (0-100)
        timestamp (str): ISO format timestamp of measurement
        tags (List[str]): List of tags for categorization
        quality_score (float): Calculated quality score
    """
    
    def __init__(
        self,
        lat: float,
        lon: float,
        provider: str = "Unknown",
        address: str = "",
        download: float = 0.0,
        upload: float = 0.0,
        latency: float = 0.0,
        stability: float = 100.0,
        timestamp: Optional[str] = None,
        tags: Optional[List[str]] = None,
        quality_score: Optional[float] = None
    ):
        """
        Initialize an AccessPoint instance.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            provider: Internet service provider name
            address: Physical address or location description
            download: Download speed in Mbps
            upload: Upload speed in Mbps
            latency: Latency in milliseconds
            stability: Connection stability percentage (0-100)
            timestamp: ISO format timestamp of measurement
            tags: List of tags for categorization
            quality_score: Pre-calculated quality score (will be auto-calculated if None)
        """
        self.lat = lat
        self.lon = lon
        self.provider = provider
        self.address = address
        self.download = download
        self.upload = upload
        self.latency = latency
        self.stability = stability
        self.timestamp = timestamp or datetime.now().isoformat()
        self.tags = tags or []
        self.quality_score = quality_score if quality_score is not None else self.calculate_quality_score()
    
    def calculate_quality_score(self) -> float:
        """
        Calculate quality score based on connectivity metrics.
        
        Formula: (download + upload) / (latency * (1 + stability/100))
        
        Returns:
            float: Quality score (higher is better)
        """
        if self.latency <= 0:
            return 0.0
        
        stability_factor = 1 + (self.stability / 100)
        score = (self.download + self.upload) / (self.latency * stability_factor)
        return round(score, 4)
    
    def update_quality_score(self) -> None:
        """Recalculate and update the quality score."""
        self.quality_score = self.calculate_quality_score()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert AccessPoint to dictionary representation.
        
        Returns:
            dict: Dictionary representation of the access point
        """
        return {
            "lat": self.lat,
            "lon": self.lon,
            "provider": self.provider,
            "address": self.address,
            "download": self.download,
            "upload": self.upload,
            "latency": self.latency,
            "stability": self.stability,
            "timestamp": self.timestamp,
            "tags": self.tags,
            "quality_score": self.quality_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AccessPoint':
        """
        Create AccessPoint instance from dictionary.
        
        Args:
            data: Dictionary containing access point data
            
        Returns:
            AccessPoint: New AccessPoint instance
        """
        return cls(
            lat=data.get("lat", 0.0),
            lon=data.get("lon", 0.0),
            provider=data.get("provider", "Unknown"),
            address=data.get("address", ""),
            download=data.get("download", 0.0),
            upload=data.get("upload", 0.0),
            latency=data.get("latency", 0.0),
            stability=data.get("stability", 100.0),
            timestamp=data.get("timestamp"),
            tags=data.get("tags", []),
            quality_score=data.get("quality_score")
        )
    
    def __repr__(self) -> str:
        """String representation of AccessPoint."""
        return (
            f"AccessPoint(lat={self.lat}, lon={self.lon}, provider='{self.provider}', "
            f"download={self.download}, upload={self.upload}, latency={self.latency}, "
            f"quality_score={self.quality_score})"
        )
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"{self.provider} @ ({self.lat}, {self.lon})\n"
            f"  Download: {self.download} Mbps, Upload: {self.upload} Mbps\n"
            f"  Latency: {self.latency} ms, Stability: {self.stability}%\n"
            f"  Quality Score: {self.quality_score}"
        )
