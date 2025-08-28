"""
Audio quality enhancement utilities.
"""
import logging

logger = logging.getLogger(__name__)


def normalize_audio_levels(audio_segment):
    """Normalize audio levels for consistent output."""
    if audio_segment.max_possible_amplitude == 0:
        return audio_segment
    return audio_segment.normalize()
