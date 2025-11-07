"""
Configuration management for Story2Audio Microservice.

Centralized configuration with environment variable support,
validation, and type safety.
"""
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """
    Application configuration settings.
    
    All settings can be overridden via environment variables.
    """
    
    # Server settings
    GRPC_PORT: int = int(os.getenv("GRPC_PORT", "50051"))
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "10"))
    GRPC_MAX_MESSAGE_LENGTH: int = int(os.getenv("GRPC_MAX_MESSAGE_LENGTH", "4194304"))  # 4MB
    
    # Pipeline settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "150"))
    MAX_WORDS: int = int(os.getenv("MAX_WORDS", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "0"))
    
    # Model settings
    ENHANCER_MODEL: str = os.getenv("ENHANCER_MODEL", "tiiuae/falcon-rw-1b")
    TTS_MODEL: str = os.getenv("TTS_MODEL", "hexgrad/Kokoro-82M")
    MODEL_CACHE_DIR: Optional[str] = os.getenv("MODEL_CACHE_DIR")
    
    # Enhancement settings
    ENHANCEMENT_MAX_TOKENS: int = int(os.getenv("ENHANCEMENT_MAX_TOKENS", "50"))
    ENHANCEMENT_TEMPERATURE: float = float(os.getenv("ENHANCEMENT_TEMPERATURE", "0.7"))
    ENHANCEMENT_TOP_P: float = float(os.getenv("ENHANCEMENT_TOP_P", "0.9"))
    
    # Output settings
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs/temp")
    FINAL_AUDIO_NAME: str = os.getenv("FINAL_AUDIO_NAME", "final_audio.mp3")
    AUDIO_BITRATE: str = os.getenv("AUDIO_BITRATE", "192k")
    AUDIO_FADE_DURATION: int = int(os.getenv("AUDIO_FADE_DURATION", "100"))
    
    # Retry settings
    RETRY_MAX_ATTEMPTS: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
    RETRY_INITIAL_DELAY: float = float(os.getenv("RETRY_INITIAL_DELAY", "1.0"))
    RETRY_MAX_DELAY: float = float(os.getenv("RETRY_MAX_DELAY", "60.0"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Performance
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "false").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    
    # Audio quality
    NORMALIZE_AUDIO: bool = os.getenv("NORMALIZE_AUDIO", "true").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration values.
        
        Returns:
            True if configuration is valid
        """
        errors = []
        
        if cls.GRPC_PORT < 1024 or cls.GRPC_PORT > 65535:
            errors.append(f"GRPC_PORT must be between 1024 and 65535, got {cls.GRPC_PORT}")
        
        if cls.MAX_WORKERS < 1:
            errors.append(f"MAX_WORKERS must be at least 1, got {cls.MAX_WORKERS}")
        
        if cls.CHUNK_SIZE < 10:
            errors.append(f"CHUNK_SIZE must be at least 10, got {cls.CHUNK_SIZE}")
        
        if cls.MAX_WORDS < cls.CHUNK_SIZE:
            errors.append(f"MAX_WORDS ({cls.MAX_WORDS}) must be >= CHUNK_SIZE ({cls.CHUNK_SIZE})")
        
        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            return False
        
        return True
    
    @classmethod
    def get_output_path(cls) -> str:
        """
        Get the full path for final audio output.
        
        Returns:
            Full path to output file
        """
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        return os.path.join(cls.OUTPUT_DIR, cls.FINAL_AUDIO_NAME)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary of configuration values
        """
        return {
            "grpc_port": cls.GRPC_PORT,
            "max_workers": cls.MAX_WORKERS,
            "chunk_size": cls.CHUNK_SIZE,
            "max_words": cls.MAX_WORDS,
            "enhancer_model": cls.ENHANCER_MODEL,
            "tts_model": cls.TTS_MODEL,
            "output_dir": cls.OUTPUT_DIR,
            "log_level": cls.LOG_LEVEL,
        }
    
    @classmethod
    def setup_logging(cls) -> None:
        """Configure logging based on settings."""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO),
            format=cls.LOG_FORMAT,
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True
        )