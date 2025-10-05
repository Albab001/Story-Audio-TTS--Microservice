"""
Caching mechanism for Story2Audio.

Provides in-memory caching for enhanced text chunks and audio generation.
"""
import hashlib
import logging
import time
from typing import Optional, Dict, Any
from functools import lru_cache

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, ttl: int = 3600):
        """
        Initialize cache.
        
        Args:
            ttl: Time to live in seconds (default: 1 hour)
        """
        self._cache: Dict[str, tuple[Any, float]] = {}
        self.ttl = ttl
    
    def _generate_key(self, text: str) -> str:
        """Generate cache key from text."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None
        
        value, timestamp = self._cache[key]
        
        if time.time() - timestamp > self.ttl:
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get number of cached items."""
        # Clean expired entries before returning size
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self._cache.items()
            if current_time - timestamp > self.ttl
        ]
        for key in expired_keys:
            del self._cache[key]
        return len(self._cache)


# Global cache instance
text_cache = SimpleCache(ttl=3600)
