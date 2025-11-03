"""
Health check endpoint for Story2Audio service.

Provides health status and system information.
"""
import logging
import psutil
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)


def get_health_status() -> Dict[str, Any]:
    """Get current health status of the service."""
    """
    Get current health status of the service.
    
    Returns:
        Dictionary with health information
    """
    try:
        process = psutil.Process(os.getpid())
        
        return {
            "status": "healthy",
            "memory": {
                "used_mb": process.memory_info().rss / 1024 / 1024,
                "percent": process.memory_percent()
            },
            "cpu": {
                "percent": process.cpu_percent(interval=0.1)
            },
            "disk": {
                "free_gb": psutil.disk_usage('/').free / 1024 / 1024 / 1024
            }
        }
    except Exception as e:
        logger.error(f"Error getting health status: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
