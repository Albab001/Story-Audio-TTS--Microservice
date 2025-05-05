from pydub import AudioSegment
from typing import List
import logging

# Set up logging
logger = logging.getLogger(__name__)

def combine_audio(files: List[str], output_path: str = "outputs/final_story.mp3") -> None:
    """
    Combine multiple WAV audio files into a single MP3 file.

    Args:
        files (List[str]): List of WAV file paths to combine.
        output_path (str): Path to save the final MP3 file.

    Raises:
        ValueError: If files list is empty or output_path is invalid.
        RuntimeError: If audio processing or export fails.
    """
    if not files:
        raise ValueError("Audio files list cannot be empty")
    if not output_path.endswith(".mp3"):
        raise ValueError("Output path must have .mp3 extension")

    try:
        final = AudioSegment.empty()
        for file in files:
            audio = AudioSegment.from_wav(file)
            final += audio
        final.export(output_path, format="mp3")
        logger.info(f"Audio stitched and saved to {output_path}")
    except Exception as e:
        logger.error(f"Audio stitching failed: {e}")
        raise