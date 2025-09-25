"""Progress tracking for long operations."""
from typing import Callable, Optional


class ProgressTracker:
    """Track progress of operations."""
    
    def __init__(self, total: int, callback: Optional[Callable] = None):
        self.total = total
        self.current = 0
        self.callback = callback
    
    def update(self, increment: int = 1):
        """Update progress."""
        self.current += increment
        if self.callback:
            self.callback(self.current, self.total)
    
    @property
    def percent(self) -> float:
        """Get completion percentage."""
        return (self.current / self.total * 100) if self.total > 0 else 0
