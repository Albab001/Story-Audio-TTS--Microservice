"""
Text-to-Speech module for Story2Audio.

Uses Kokoro-82M for high-quality TTS generation with voice options.
"""
from kokoro import KPipeline
import soundfile as sf
import logging
import os
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Global pipeline instance for reuse
_pipeline_instance: Optional[KPipeline] = None


def get_pipeline(lang_code: str = 'a') -> KPipeline:
    """
    Get or create TTS pipeline instance (singleton pattern).
    
    Args:
        lang_code: Language code ('a' for auto-detect)
        
    Returns:
        KPipeline instance
    """
    global _pipeline_instance
    if _pipeline_instance is None:
        logger.info("Initializing Kokoro TTS pipeline...")
        _pipeline_instance = KPipeline(lang_code=lang_code)
        logger.info("TTS pipeline initialized successfully")
    return _pipeline_instance


def text_to_coqui_audio(
    chunks: List[str], 
    output_dir: str = "outputs/temp",
    voice: str = 'af_heart',
    sample_rate: int = 24000
) -> List[str]:
    """
    Generate audio files from enhanced text chunks using Kokoro-82M.

    Args:
        chunks: List of enhanced text chunks
        output_dir: Directory to save temporary audio files
        voice: Voice style to use (default: 'af_heart')
        sample_rate: Audio sample rate in Hz (default: 24000)

    Returns:
        List of paths to generated audio files

    Raises:
        ValueError: If chunks list is empty
        RuntimeError: If audio generation fails
    """
    if not chunks:
        raise ValueError("Chunks list cannot be empty")
    
    if not isinstance(chunks, list):
        raise ValueError("Chunks must be a list")
    
    try:
        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get pipeline instance
        pipeline = get_pipeline()
        audio_files: List[str] = []
        
        logger.info(f"Generating audio for {len(chunks)} chunks with voice '{voice}'")
        
        # Generate audio for each chunk
        for i, chunk in enumerate(chunks):
            if not chunk or not chunk.strip():
                logger.warning(f"Skipping empty chunk {i+1}")
                continue
            
            try:
                out_path = str(output_path / f"chunk_{i:04d}.wav")
                
                # Generate audio
                generator = pipeline(chunk, voice=voice)
                audio_generated = False
                
                for j, (gs, ps, audio) in enumerate(generator):
                    sf.write(out_path, audio, sample_rate)
                    audio_generated = True
                    if j == 0:  # Log only first iteration
                        logger.debug(
                            f"Generated audio for chunk {i+1}/{len(chunks)} - "
                            f"Graphemes: {gs}, Phonemes: {ps}"
                        )
                
                if audio_generated:
                    audio_files.append(out_path)
                    file_size_kb = os.path.getsize(out_path) / 1024
                    logger.info(
                        f"Audio saved: {out_path} ({file_size_kb:.2f} KB)"
                    )
                else:
                    logger.warning(f"No audio generated for chunk {i+1}")
                    
            except Exception as e:
                logger.error(f"Error generating audio for chunk {i+1}: {e}")
                # Continue with other chunks instead of failing completely
                continue
        
        if not audio_files:
            raise RuntimeError("No audio files were generated")
        
        logger.info(f"Successfully generated {len(audio_files)} audio files")
        return audio_files
        
    except Exception as e:
        logger.error(f"Error in audio generation: {e}")
        raise RuntimeError(f"Audio generation failed: {e}") from e