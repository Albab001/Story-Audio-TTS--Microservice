import re
from typing import List

def chunk_story(text: str, chunk_size: int = 150) -> List[str]:
    """
    Split a story into chunks of approximately chunk_size words.

    Args:
        text (str): Input story text.
        chunk_size (int): Approximate number of words per chunk (default: 150).

    Returns:
        List[str]: List of text chunks.

    Raises:
        ValueError: If text is empty or chunk_size is non-positive.
    """
    if not text.strip():
        raise ValueError("Input text cannot be empty")
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    # Clean text: remove extra whitespace, normalize newlines
    text = re.sub(r'\s+', ' ', text.strip())
    words = text.split()
    if not words:
        return []

    # Split into chunks of approximately chunk_size words
    chunks = [' '.join(words[i:i + chunk_size]) 
              for i in range(0, len(words), chunk_size)]
    return chunks