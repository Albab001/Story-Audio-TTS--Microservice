from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryEnhancer:
    def __init__(self, model_name="tiiuae/falcon-rw-1b"):
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            offload_folder="offload"
        )

        # Set up text generation pipeline
        self.generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
            # No device= needed due to device_map="auto"
        )

        # Save tokenizer reference for later use
        self.tokenizer = tokenizer

        logger.info(f"Initialized StoryEnhancer locally with model: {model_name}")

    def enhance_chunk(self, text_chunk: str, max_new_tokens=50) -> str:
        if not text_chunk.strip():
            raise ValueError("Text chunk cannot be empty")

        # Prepare prompt
        prompt = (
            f"Improve the storytelling tone of this text to make it more engaging and emotional:\n"
            f"{text_chunk}\nEnhanced version:"
        )

        # Log tokenized input length (optional)
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        logger.info(f"Tokenized input length: {inputs['input_ids'].shape[1]} tokens")

        # Generate enhanced output
        output = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            truncation=True,
            pad_token_id=self.tokenizer.eos_token_id
        )[0]["generated_text"]

        # Extract the enhanced portion
        return output.split("Enhanced version:")[-1].strip()
