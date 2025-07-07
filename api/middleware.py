"""
Middleware for gRPC server.

Provides request/response logging and error handling.
"""
import logging
import time
from typing import Callable, Any
import functools

logger = logging.getLogger(__name__)


def log_request(func: Callable) -> Callable:
    """Decorator to log gRPC requests."""
    @functools.wraps(func)
    async def wrapper(self, request, context):
        start_time = time.time()
        method_name = func.__name__
        
        try:
            logger.info(f"Received {method_name} request")
            response = await func(self, request, context)
            duration = time.time() - start_time
            logger.info(f"Completed {method_name} in {duration:.2f}s")
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{method_name} failed after {duration:.2f}s: {e}")
            raise
    
    return wrapper


def handle_errors(func: Callable) -> Callable:
    """Decorator to handle errors gracefully."""
    @functools.wraps(func)
    async def wrapper(self, request, context):
        try:
            return await func(self, request, context)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            logger.warning(f"Validation error: {e}")
            raise
        except FileNotFoundError as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            logger.exception(f"Unexpected error: {e}")
            raise
    
    return wrapper
