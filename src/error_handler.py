"""Centralized error handling utilities."""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Handle and format errors consistently."""
    
    @staticmethod
    def format_error(error: Exception, context: Optional[str] = None) -> str:
        """Format error message with optional context."""
        msg = str(error)
        if context:
            return f"{context}: {msg}"
        return msg
    
    @staticmethod
    def log_error(error: Exception, context: Optional[str] = None, level: str = "error"):
        """Log error with context."""
        log_func = getattr(logger, level, logger.error)
        formatted = ErrorHandler.format_error(error, context)
        log_func(formatted, exc_info=True)
    
    @staticmethod
    def handle_gracefully(error: Exception, fallback_value=None):
        """Handle error gracefully with fallback."""
        ErrorHandler.log_error(error)
        return fallback_value
