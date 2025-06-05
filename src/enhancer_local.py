"""
Text enhancement module for Story2Audio.

This module uses transformer models to enhance storytelling tone
and emotional depth of text chunks.
"""
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import logging
from typing import Optional
import os
import sys

logger = logging.getLogger(__name__)


class StoryEnhancer:
    """
    Enhances story text using transformer models for better storytelling.
    
    Uses lazy loading and caching for optimal performance.
    """
    
    _instance: Optional['StoryEnhancer'] = None
    _initialized = False
    
    def __init__(self, model_name: str = "tiiuae/falcon-rw-1b", cache_dir: Optional[str] = None):
        """
        Initialize the StoryEnhancer.
        
        Args:
            model_name: HuggingFace model identifier
            cache_dir: Optional directory for model caching
        """
        if StoryEnhancer._initialized:
            logger.warning("StoryEnhancer already initialized, reusing existing instance")
            return
            
        self.model_name = model_name
        self.cache_dir = cache_dir or os.getenv("HF_HOME", os.path.join(os.path.expanduser("~"), ".cache", "huggingface"))
        self.tokenizer: Optional[AutoTokenizer] = None
        self.generator: Optional[pipeline] = None
        
        self._load_model()
        StoryEnhancer._initialized = True
        StoryEnhancer._instance = self
    
    def _load_model(self) -> None:
        """Load the tokenizer and model with optimized settings."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                trust_remote_code=True
            )
            
            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Determine optimal dtype
            use_cuda = torch.cuda.is_available()
            dtype = torch.float16 if use_cuda else torch.float32
            
            logger.info(f"Using device: {'CUDA' if use_cuda else 'CPU'}, dtype: {dtype}")
            
            # Load model with optimization
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=dtype,
                device_map="auto" if use_cuda else None,
                offload_folder=os.path.join(self.cache_dir, "offload") if use_cuda else None,
                cache_dir=self.cache_dir,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            if not use_cuda:
                model = model.to("cpu")
            
            # Set up text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=model,
                tokenizer=self.tokenizer,
                device=0 if use_cuda else -1
            )
            
            logger.info(f"Successfully initialized StoryEnhancer with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            raise RuntimeError(f"Model loading failed: {e}") from e
    
    def enhance_chunk(
        self, 
        text_chunk: str, 
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Enhance a text chunk for better storytelling.
        
        Args:
            text_chunk: Text to enhance
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            
        Returns:
            Enhanced text chunk
            
        Raises:
            ValueError: If text chunk is empty
            RuntimeError: If enhancement fails
        """
        if not text_chunk or not text_chunk.strip():
            raise ValueError("Text chunk cannot be empty")
        
        if self.generator is None or self.tokenizer is None:
            raise RuntimeError("Model not initialized")
        
        try:
            # Prepare prompt
            prompt = (
                f"Improve the storytelling tone of this text to make it more engaging and emotional:\n"
                f"{text_chunk}\nEnhanced version:"
            )
            
            # Tokenize and check length
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            input_length = inputs['input_ids'].shape[1]
            
            if input_length > 400:  # Warn if input is very long
                logger.warning(f"Long input detected: {input_length} tokens")
            
            # Generate enhanced output with optimized parameters
            output = self.generator(
                prompt,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                truncation=True,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
                num_return_sequences=1
            )[0]["generated_text"]
            
            # Extract the enhanced portion
            enhanced = output.split("Enhanced version:")[-1].strip()
            
            # Fallback to original if enhancement failed
            if not enhanced or len(enhanced) < len(text_chunk) * 0.5:
                logger.warning("Enhancement produced short output, using original")
                return text_chunk
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Error enhancing chunk: {e}")
            # Return original on error
            logger.warning("Returning original text due to enhancement error")
            return text_chunk
    
    @classmethod
    def get_instance(cls) -> 'StoryEnhancer':
        """Get or create singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
