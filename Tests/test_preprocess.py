"""
Tests for text preprocessing module.
"""
import pytest
from src.preprocess import chunk_story, clean_text


class TestPreprocessing:
    """Test cases for preprocessing functions."""
    
    def test_chunk_story_basic(self):
        """Test basic chunking."""
        text = "word " * 300
        chunks = chunk_story(text, chunk_size=150)
        assert len(chunks) == 2
        assert all(len(chunk.split()) <= 150 for chunk in chunks)
    
    def test_chunk_story_empty(self):
        """Test chunking empty text."""
        with pytest.raises(ValueError):
            chunk_story("", chunk_size=150)
    
    def test_chunk_story_invalid_size(self):
        """Test chunking with invalid chunk size."""
        with pytest.raises(ValueError):
            chunk_story("test text", chunk_size=0)
    
    def test_clean_text(self):
        """Test text cleaning."""
        text = "  Hello    world  \n\n  "
        cleaned = clean_text(text)
        assert cleaned == "Hello world"
    
    def test_chunk_story_sentence_boundary(self):
        """Test chunking preserves sentence boundaries."""
        text = "First sentence. Second sentence. " * 50
        chunks = chunk_story(text, chunk_size=20)
        # Most chunks should end with sentence punctuation
        assert any(chunk.endswith(('.', '!', '?')) for chunk in chunks)
