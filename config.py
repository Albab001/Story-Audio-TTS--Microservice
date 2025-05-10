"""
Configuration file for Story2Audio Microservice
"""
import os
from typing import Optional

class Config:
    """Application configuration settings"""
    
    # Server settings
    GRPC_PORT: int = int(os.getenv("GRPC_PORT", "50051"))
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "10"))
    
    # Pipeline settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "150"))
    MAX_WORDS: int = int(os.getenv("MAX_WORDS", "1000"))
    
    # Model settings
    ENHANCER_MODEL: str = os.getenv("ENHANCER_MODEL", "tiiuae/falcon-rw-1b")
    TTS_MODEL: str = os.getenv("TTS_MODEL", "hexgrad/Kokoro-82M")
    
    # Output settings
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs/temp")
    FINAL_AUDIO_NAME: str = os.getenv("FINAL_AUDIO_NAME", "final_audio.mp3")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_output_path(cls) -> str:
        """Get the full path for final audio output"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        return os.path.join(cls.OUTPUT_DIR, cls.FINAL_AUDIO_NAME)
