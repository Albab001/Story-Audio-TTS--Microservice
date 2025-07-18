"""
Tests for input validation module.
"""
import pytest
from src.validators import StoryValidator


class TestStoryValidator:
    """Test cases for StoryValidator."""
    
    def test_valid_story(self):
        """Test valid story text."""
        text = "Once upon a time, there was a brave knight."
        is_valid, error = StoryValidator.validate_story_text(text)
        assert is_valid is True
        assert error is None
    
    def test_empty_story(self):
        """Test empty story text."""
        is_valid, error = StoryValidator.validate_story_text("")
        assert is_valid is False
        assert error is not None
    
    def test_only_numbers(self):
        """Test story with only numbers."""
        is_valid, error = StoryValidator.validate_story_text("12345")
        assert is_valid is False
        assert "numbers" in error.lower()
    
    def test_only_special_chars(self):
        """Test story with only special characters."""
        is_valid, error = StoryValidator.validate_story_text("!!!@@@###")
        assert is_valid is False
        assert "special" in error.lower()
    
    def test_sanitize_text(self):
        """Test text sanitization."""
        text = "  Hello    world  \n\n  "
        sanitized = StoryValidator.sanitize_text(text)
        assert sanitized == "Hello world"
    
    def test_too_long_story(self):
        """Test story exceeding word limit."""
        long_text = "word " * 10001
        is_valid, error = StoryValidator.validate_story_text(long_text)
        assert is_valid is False
        assert "too long" in error.lower()
