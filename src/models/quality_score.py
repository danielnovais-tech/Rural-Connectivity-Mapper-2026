"""Quality Score model for calculating connectivity quality metrics."""

from typing import Dict, Any, Optional


class QualityScore:
    """Represents a quality score based on connectivity metrics."""
    
    def __init__(
        self,
        speed_score: float,
        latency_score: float,
        stability_score: float,
        overall_score: Optional[float] = None
    ):
        """
        Initialize a quality score.
        
        Args:
            speed_score: Score based on download/upload speeds (0-100)
            latency_score: Score based on latency (0-100)
            stability_score: Score based on connection stability (0-100)
            overall_score: Overall quality score (defaults to weighted average)
        """
        self.speed_score = speed_score
        self.latency_score = latency_score
        self.stability_score = stability_score
        self.overall_score = overall_score or self._calculate_overall()
    
    def _calculate_overall(self) -> float:
        """Calculate overall score as weighted average."""
        # Weight: speed 40%, latency 30%, stability 30%
        return (
            self.speed_score * 0.4 +
            self.latency_score * 0.3 +
            self.stability_score * 0.3
        )
    
    def get_rating(self) -> str:
        """Get quality rating based on overall score."""
        if self.overall_score >= 90:
            return "Excellent"
        elif self.overall_score >= 75:
            return "Good"
        elif self.overall_score >= 60:
            return "Fair"
        elif self.overall_score >= 40:
            return "Poor"
        else:
            return "Very Poor"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "speed_score": round(self.speed_score, 2),
            "latency_score": round(self.latency_score, 2),
            "stability_score": round(self.stability_score, 2),
            "overall_score": round(self.overall_score, 2),
            "rating": self.get_rating()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QualityScore':
        """Create QualityScore from dictionary."""
        return cls(
            speed_score=data["speed_score"],
            latency_score=data["latency_score"],
            stability_score=data["stability_score"],
            overall_score=data.get("overall_score")
        )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"QualityScore(overall={self.overall_score:.1f}, rating={self.get_rating()})"
