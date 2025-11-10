"""
Audio utility functions for Story2Audio.

This module handles audio file operations including combining,
format conversion, and quality optimization.
"""
from pydub import AudioSegment
from typing import List, Optional
import logging
import os
from config import Config

logger = logging.getLogger(__name__)


def validate_audio_file(file_path: str) -> bool:
    """
    Validate that an audio file exists and is readable.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        True if file is valid, False otherwise
    """
    if not os.path.exists(file_path):
        logger.error(f"Audio file not found: {file_path}")
        return False
    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        return False
    if os.path.getsize(file_path) == 0:
        logger.error(f"Audio file is empty: {file_path}")
        return False
    return True


def combine_audio(
    files: List[str], 
    output_path: str = "outputs/final_story.mp3",
    bitrate: str = "192k",
    fade_duration: int = 100
) -> str:
    """
    Combine multiple WAV audio files into a single MP3 file.
    
    Adds smooth transitions between chunks and optimizes output quality.

    Args:
        files: List of WAV file paths to combine
        output_path: Path to save the final MP3 file
        bitrate: MP3 bitrate (default: "192k")
        fade_duration: Fade duration in milliseconds between chunks (default: 100)

    Returns:
        Path to the created output file

    Raises:
        ValueError: If files list is empty or output_path is invalid
        FileNotFoundError: If any input file doesn't exist
        RuntimeError: If audio processing or export fails
    """
    if not files:
        raise ValueError("Audio files list cannot be empty")
    if not output_path.endswith(".mp3"):
        raise ValueError("Output path must have .mp3 extension")
    
    # Validate all input files
    for file_path in files:
        if not validate_audio_file(file_path):
            raise FileNotFoundError(f"Invalid audio file: {file_path}")

    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        logger.info(f"Combining {len(files)} audio files into {output_path}")
        final = AudioSegment.empty()
        
        for i, file_path in enumerate(files):
            try:
                audio = AudioSegment.from_wav(file_path)
                
                # Normalize audio if enabled
                if Config.NORMALIZE_AUDIO:
                    from src.audio_quality import normalize_audio_levels
                    audio = normalize_audio_levels(audio)
                
                # Add fade in/out for smoother transitions (except first and last)
                if i > 0 and fade_duration > 0:
                    audio = audio.fade_in(fade_duration)
                if i < len(files) - 1 and fade_duration > 0:
                    audio = audio.fade_out(fade_duration)
                
                final += audio
                logger.debug(f"Added chunk {i+1}/{len(files)}: {len(audio)}ms")
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                raise
        
        # Export with specified bitrate
        final.export(
            output_path, 
            format="mp3",
            bitrate=bitrate,
            parameters=["-q:a", "2"]  # High quality
        )
        
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        duration_sec = len(final) / 1000.0
        logger.info(f"Audio stitched successfully: {output_path} ({file_size_mb:.2f} MB, {duration_sec:.1f}s)")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Audio stitching failed: {e}")
        raise RuntimeError(f"Failed to combine audio files: {e}") from e