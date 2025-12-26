"""Quality score calculation utilities."""

from typing import List
import logging

from src.models.speed_test import SpeedTest
from src.models.quality_score import QualityScore

logger = logging.getLogger(__name__)


def calculate_speed_score(download: float, upload: float) -> float:
    """
    Calculate speed score based on download and upload speeds.
    
    Args:
        download: Download speed in Mbps
        upload: Upload speed in Mbps
    
    Returns:
        Speed score (0-100)
    """
    # Starlink targets: 50-200 Mbps download, 10-20 Mbps upload
    download_score = min(100, (download / 200) * 100)
    upload_score = min(100, (upload / 20) * 100)
    
    # Weight download more heavily (70/30)
    return download_score * 0.7 + upload_score * 0.3


def calculate_latency_score(latency: float) -> float:
    """
    Calculate latency score.
    
    Args:
        latency: Latency in milliseconds
    
    Returns:
        Latency score (0-100)
    """
    # Starlink targets: 20-40ms latency
    # Lower is better
    if latency <= 20:
        return 100
    elif latency <= 40:
        return 100 - ((latency - 20) / 20) * 25
    elif latency <= 100:
        return 75 - ((latency - 40) / 60) * 50
    else:
        return max(0, 25 - ((latency - 100) / 100) * 25)


def calculate_quality_score(speed_tests: List[SpeedTest]) -> QualityScore:
    """
    Calculate quality score from speed test results.
    
    Args:
        speed_tests: List of SpeedTest objects
    
    Returns:
        QualityScore object
    """
    if not speed_tests:
        logger.warning("No speed tests provided for quality calculation")
        return QualityScore(0, 0, 0)
    
    # Average metrics across all tests
    avg_download = sum(st.download_speed for st in speed_tests) / len(speed_tests)
    avg_upload = sum(st.upload_speed for st in speed_tests) / len(speed_tests)
    avg_latency = sum(st.latency for st in speed_tests) / len(speed_tests)
    avg_stability = sum(st.calculate_stability() for st in speed_tests) / len(speed_tests)
    
    speed_score = calculate_speed_score(avg_download, avg_upload)
    latency_score = calculate_latency_score(avg_latency)
    
    quality_score = QualityScore(
        speed_score=speed_score,
        latency_score=latency_score,
        stability_score=avg_stability
    )
    
    logger.info(f"Calculated quality score: {quality_score}")
    return quality_score
