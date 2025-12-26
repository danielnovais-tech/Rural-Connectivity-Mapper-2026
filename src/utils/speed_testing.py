"""Speed testing utilities using speedtest-cli."""

from typing import Optional
import logging

from src.models.speed_test import SpeedTest

logger = logging.getLogger(__name__)


def run_speed_test(server_id: Optional[int] = None) -> Optional[SpeedTest]:
    """
    Run an internet speed test.
    
    Args:
        server_id: Optional specific server ID to use
    
    Returns:
        SpeedTest object with results or None if test fails
    """
    try:
        import speedtest
        
        logger.info("Starting speed test...")
        st = speedtest.Speedtest()
        
        if server_id:
            st.get_servers([server_id])
        else:
            st.get_best_server()
        
        logger.info("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        logger.info("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        results = st.results.dict()
        latency = results.get('ping', 0)
        server = results.get('server', {}).get('name', 'Unknown')
        
        speed_test = SpeedTest(
            download_speed=download_speed,
            upload_speed=upload_speed,
            latency=latency,
            server=server
        )
        
        logger.info(f"Speed test completed: {speed_test}")
        return speed_test
    
    except Exception as e:
        logger.error(f"Error running speed test: {e}")
        return None


def get_available_servers(limit: int = 10) -> list:
    """
    Get list of available speed test servers.
    
    Args:
        limit: Maximum number of servers to return
    
    Returns:
        List of server dictionaries
    """
    try:
        import speedtest
        
        st = speedtest.Speedtest()
        servers = st.get_servers()
        
        server_list = []
        for server_group in servers.values():
            server_list.extend(server_group[:limit])
            if len(server_list) >= limit:
                break
        
        return server_list[:limit]
    
    except Exception as e:
        logger.error(f"Error getting servers: {e}")
        return []
