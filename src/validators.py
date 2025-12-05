"""
Input validation module for Story2Audio.

Provides comprehensive validation for story text inputs.
"""
import re
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class StoryValidator:
    """Validates story text inputs before processing."""
    
    MIN_WORDS = 1
    MAX_WORDS = 10000
    MIN_CHARS = 10
    MAX_CHARS = 50000
    MAX_LINES = 1000
    
    # Patterns for invalid content
    ONLY_NUMBERS_PATTERN = re.compile(r'^\d+$')
    ONLY_SPECIAL_CHARS_PATTERN = re.compile(r'^[^a-zA-Z0-9\s]+$')
    EXCESSIVE_WHITESPACE_PATTERN = re.compile(r'\s{10,}')
    
    @classmethod
    def validate_story_text(cls, text: str) -> Tuple[bool, Optional[str]]:
        """
        Validate story text.
        
        Args:
            text: Story text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text:
            return False, "Story text cannot be empty"
        
        if not isinstance(text, str):
            return False, "Story text must be a string"
        
        text = text.strip()
        
        # Check minimum length
        if len(text) < cls.MIN_CHARS:
            return False, f"Story text too short (minimum {cls.MIN_CHARS} characters)"
        
        # Check maximum length
        if len(text) > cls.MAX_CHARS:
            return False, f"Story text too long (maximum {cls.MAX_CHARS} characters)"
        
        # Count words
        words = text.split()
        word_count = len(words)
        
        if word_count < cls.MIN_WORDS:
            return False, f"Story must contain at least {cls.MIN_WORDS} word"
        
        if word_count > cls.MAX_WORDS:
            return False, f"Story text too long (maximum {cls.MAX_WORDS} words, found {word_count})"
        
        # Check for only numbers
        if cls.ONLY_NUMBERS_PATTERN.match(text):
            return False, "Story cannot consist only of numbers"
        
        # Check for only special characters
        if cls.ONLY_SPECIAL_CHARS_PATTERN.match(text):
            return False, "Story cannot consist only of special characters"
        
        # Check for excessive whitespace
        if cls.EXCESSIVE_WHITESPACE_PATTERN.search(text):
            return False, "Story contains excessive whitespace"
        
        # Check line count
        line_count = len(text.split('\n'))
        if line_count > cls.MAX_LINES:
            return False, f"Story has too many lines (max {cls.MAX_LINES})"
        
        # Check for meaningful words (at least some words longer than 1 char)
        meaningful_words = [w for w in words if len(w) > 1 and w.isalnum()]
        if len(meaningful_words) < cls.MIN_WORDS:
            return False, "Story must contain meaningful words"
        
        return True, None
    
    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Sanitize story text by removing excessive whitespace.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
