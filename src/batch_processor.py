"""Batch processing utilities for multiple stories."""
import asyncio
from typing import List, Callable, Any
import logging

logger = logging.getLogger(__name__)


async def process_batch(
    items: List[Any],
    processor: Callable,
    max_concurrent: int = 3
) -> List[Any]:
    """Process items in batches with concurrency control."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(item):
        async with semaphore:
            return await processor(item)
    
    tasks = [process_with_semaphore(item) for item in items]
    return await asyncio.gather(*tasks)
