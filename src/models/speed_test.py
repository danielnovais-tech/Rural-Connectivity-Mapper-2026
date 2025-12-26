"""Speed Test model for storing internet speed test results."""

from datetime import datetime
from typing import Optional, Dict, Any


class SpeedTest:
    """Represents a speed test measurement."""
    
    def __init__(
        self,
        download_speed: float,
        upload_speed: float,
        latency: float,
        jitter: Optional[float] = None,
        packet_loss: Optional[float] = None,
        server: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a speed test result.
        
        Args:
            download_speed: Download speed in Mbps
            upload_speed: Upload speed in Mbps
            latency: Latency in milliseconds
            jitter: Jitter in milliseconds (optional)
            packet_loss: Packet loss percentage (optional)
            server: Test server name/location (optional)
            timestamp: Time of test (defaults to now)
        """
        self.download_speed = download_speed
        self.upload_speed = upload_speed
        self.latency = latency
        self.jitter = jitter
        self.packet_loss = packet_loss or 0.0
        self.server = server
        self.timestamp = timestamp or datetime.now()
    
    def calculate_stability(self) -> float:
        """
        Calculate connection stability score (0-100).
        
        Lower jitter and packet loss indicate better stability.
        """
        jitter_score = max(0, 100 - (self.jitter or 0) * 2)
        packet_loss_score = max(0, 100 - self.packet_loss * 10)
        return (jitter_score + packet_loss_score) / 2
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "download_speed": self.download_speed,
            "upload_speed": self.upload_speed,
            "latency": self.latency,
            "jitter": self.jitter,
            "packet_loss": self.packet_loss,
            "server": self.server,
            "timestamp": self.timestamp.isoformat(),
            "stability": self.calculate_stability()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpeedTest':
        """Create SpeedTest from dictionary."""
        return cls(
            download_speed=data["download_speed"],
            upload_speed=data["upload_speed"],
            latency=data["latency"],
            jitter=data.get("jitter"),
            packet_loss=data.get("packet_loss", 0.0),
            server=data.get("server"),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"SpeedTest(down={self.download_speed}Mbps, up={self.upload_speed}Mbps, latency={self.latency}ms)"
