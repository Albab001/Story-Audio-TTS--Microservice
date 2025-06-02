"""
Text preprocessing module for Story2Audio.

This module handles story text preprocessing, including cleaning,
normalization, and intelligent chunking for optimal processing.
"""
import re
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean and normalize text input.
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text with normalized whitespace
    """
    if not text:
        return ""
    # Remove extra whitespace, normalize newlines, and strip
    cleaned = re.sub(r'\s+', ' ', text.strip())
    return cleaned


def chunk_story(text: str, chunk_size: int = 150, overlap: int = 0) -> List[str]:
    """
    Split a story into chunks of approximately chunk_size words.
    
    Uses intelligent chunking to preserve sentence boundaries when possible.

    Args:
        text: Input story text
        chunk_size: Approximate number of words per chunk (default: 150)
        overlap: Number of words to overlap between chunks (default: 0)

    Returns:
        List of text chunks

    Raises:
        ValueError: If text is empty or chunk_size is non-positive
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and less than chunk_size")

    # Clean text
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    if not words:
        logger.warning("Empty word list after cleaning")
        return []

    chunks: List[str] = []
    i = 0
    
    while i < len(words):
        # Calculate chunk end
        chunk_end = min(i + chunk_size, len(words))
        chunk_words = words[i:chunk_end]
        
        # Try to end at sentence boundary if not at end
        if chunk_end < len(words) and chunk_size > 20:
            # Look for sentence endings in the last 20% of chunk
            lookback_start = max(0, len(chunk_words) - int(chunk_size * 0.2))
            for j in range(len(chunk_words) - 1, lookback_start - 1, -1):
                if chunk_words[j].endswith(('.', '!', '?')):
                    chunk_words = chunk_words[:j + 1]
                    chunk_end = i + len(chunk_words)
                    break
        
        chunk = ' '.join(chunk_words)
        chunks.append(chunk)
        
        # Move to next chunk with overlap
        i = chunk_end - overlap if overlap > 0 else chunk_end
        
        if i >= len(words):
            break

    logger.info(f"Split story into {len(chunks)} chunks (avg {len(words) // len(chunks) if chunks else 0} words/chunk)")
    return chunks