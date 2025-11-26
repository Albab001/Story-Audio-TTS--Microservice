"""
Metrics and monitoring for Story2Audio.

Tracks performance metrics, request statistics, and system health.
"""
import time
import logging
from typing import Dict, Optional
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    request_id: str
    start_time: float
    end_time: Optional[float] = None
    word_count: int = 0
    chunk_count: int = 0
    status: str = "processing"
    error: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Get request duration in seconds."""
        if self.end_time:
            return self.end_time - self.start_time
        return None


class MetricsCollector:
    """Collects and aggregates metrics for the service."""
    
    def __init__(self):
        self._requests: Dict[str, RequestMetrics] = {}
        self._stats = defaultdict(int)
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._total_processing_time = 0.0
    
    def start_request(self, request_id: str, word_count: int = 0) -> None:
        """Start tracking a request."""
        self._requests[request_id] = RequestMetrics(
            request_id=request_id,
            start_time=time.time(),
            word_count=word_count
        )
        self._total_requests += 1
        self._stats["requests_started"] += 1
    
    def end_request(
        self, 
        request_id: str, 
        status: str = "success",
        error: Optional[str] = None,
        chunk_count: int = 0
    ) -> None:
        """End tracking a request."""
        if request_id not in self._requests:
            logger.warning(f"Request {request_id} not found in metrics")
            return
        
        metric = self._requests[request_id]
        metric.end_time = time.time()
        metric.status = status
        metric.error = error
        metric.chunk_count = chunk_count
        
        duration = metric.duration
        if duration:
            self._total_processing_time += duration
        
        if status == "success":
            self._successful_requests += 1
            self._stats["requests_succeeded"] += 1
        else:
            self._failed_requests += 1
            self._stats["requests_failed"] += 1
    
    def get_stats(self) -> Dict:
        """Get aggregated statistics."""
        avg_time = (
            self._total_processing_time / self._successful_requests
            if self._successful_requests > 0
            else 0
        )
        
        return {
            "total_requests": self._total_requests,
            "successful_requests": self._successful_requests,
            "failed_requests": self._failed_requests,
            "success_rate": (
                self._successful_requests / self._total_requests
                if self._total_requests > 0
                else 0
            ),
            "average_processing_time": avg_time,
            "total_processing_time": self._total_processing_time,
            "additional_stats": dict(self._stats)
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self._requests.clear()
        self._stats.clear()
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._total_processing_time = 0.0
        logger.info("Metrics reset")


# Global metrics collector instance
metrics = MetricsCollector()
