from kokoro import KPipeline
import soundfile as sf
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

def text_to_coqui_audio(chunks: list, output_dir: str = "outputs/temp") -> list:
    """
    Generate audio files from enhanced text chunks using Kokoro-82M.

    Args:
        chunks (list): List of enhanced text chunks.
        output_dir (str): Directory to save temporary audio files.

    Returns:
        list: List of paths to generated audio files.

    Raises:
        Exception: If audio generation fails.
    """
    try:
        # Initialize the pipeline with auto-detect language
        pipeline = KPipeline(lang_code='a')
        audio_files = []

        # Generate audio for each chunk
        os.makedirs(output_dir, exist_ok=True)
        for i, chunk in enumerate(chunks):
            out_path = f"{output_dir}/chunk_{i}.wav"
            generator = pipeline(chunk, voice='af_heart')
            for j, (gs, ps, audio) in enumerate(generator):
                sf.write(out_path, audio, 24000)
                logger.info(f"Generated audio for chunk {i+1} - Graphemes: {gs}, Phonemes: {ps}")
            audio_files.append(out_path)
            logger.info(f"Audio saved to {out_path}")

        return audio_files
    except Exception as e:
        logger.error(f"Error in audio generation: {e}")
        raise