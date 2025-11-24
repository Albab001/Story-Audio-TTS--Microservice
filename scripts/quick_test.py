#!/usr/bin/env python3
"""Quick test script."""
import sys
from src.validators import StoryValidator

test_text = "This is a test story."
is_valid, error = StoryValidator.validate_story_text(test_text)
if is_valid:
    print("✓ Validation works")
    sys.exit(0)
else:
    print(f"✗ Validation failed: {error}")
    sys.exit(1)
