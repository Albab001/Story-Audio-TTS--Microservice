"""Tests for utility functions."""
import pytest
import os
from src.utils import validate_audio_file


class TestUtils:
    """Test utility functions."""
    
    def test_validate_audio_file_nonexistent(self):
        """Test validation of non-existent file."""
        assert validate_audio_file("nonexistent.wav") is False
    
    def test_validate_audio_file_empty(self, tmp_path):
        """Test validation of empty file."""
        empty_file = tmp_path / "empty.wav"
        empty_file.touch()
        assert validate_audio_file(str(empty_file)) is False
