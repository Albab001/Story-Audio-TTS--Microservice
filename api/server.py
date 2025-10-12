"""
gRPC server implementation for Story2Audio Microservice.

Handles audio generation requests with comprehensive error handling,
validation, and metrics collection.
"""
import grpc
import os
import logging
import uuid
from concurrent import futures
import asyncio
import story2audio_pb2
import story2audio_pb2_grpc
from src.preprocess import chunk_story
from src.enhancer_local import StoryEnhancer
from src.kokoro_tts import text_to_coqui_audio
from src.utils import combine_audio
from src.validators import StoryValidator
from src.metrics import metrics
from src.error_handler import ErrorHandler
import base64
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Set up logging
Config.setup_logging()
logger = logging.getLogger(__name__)

class StoryServiceServicer(story2audio_pb2_grpc.StoryServiceServicer):
    def __init__(self):
        self.enhancer = None  # Lazy initialization
    
    def _get_enhancer(self):
        """Lazy initialization of enhancer to avoid loading on import"""
        if self.enhancer is None:
            logger.info("Initializing StoryEnhancer...")
            self.enhancer = StoryEnhancer()
        return self.enhancer
    
    async def GenerateAudio(self, request, context):
        request_id = str(uuid.uuid4())[:8]
        story_text = request.story_text
        
        try:
            # Sanitize and validate input
            story_text = StoryValidator.sanitize_text(story_text)
            is_valid, error_message = StoryValidator.validate_story_text(story_text)
            
            if not is_valid:
                logger.warning(f"[{request_id}] Validation failed: {error_message}")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(error_message or "Invalid input")
                return story2audio_pb2.AudioResponse(
                    status="error", 
                    audio_base64="", 
                    message=error_message or "Invalid input"
                )
            
            word_count = len(story_text.split())
            logger.info(f"[{request_id}] Processing request: {word_count} words")
            
            # Estimate processing time
            estimated_time = word_count * 0.035  # ~35ms per word
            logger.debug(f"[{request_id}] Estimated processing time: {estimated_time:.1f}s")
            
            # Start metrics tracking
            metrics.start_request(request_id, word_count=word_count)

            # Preprocess
            logger.info("Preprocessing story into chunks...")
            chunks = chunk_story(story_text, chunk_size=Config.CHUNK_SIZE)
            logger.info(f"Story split into {len(chunks)} chunks")
            
            # Enhance
            logger.info("Enhancing text chunks...")
            enhancer = self._get_enhancer()
            enhanced_chunks = []
            for i, chunk in enumerate(chunks):
                try:
                    enhanced = enhancer.enhance_chunk(chunk)
                    enhanced_chunks.append(enhanced)
                    logger.debug(f"Enhanced chunk {i+1}/{len(chunks)}")
                except Exception as e:
                    logger.error(f"Error enhancing chunk {i+1}: {e}")
                    # Fallback to original chunk if enhancement fails
                    enhanced_chunks.append(chunk)

            # Generate audio asynchronously
            logger.info("Generating audio from enhanced chunks...")
            loop = asyncio.get_event_loop()
            try:
                audio_files = await loop.run_in_executor(
                    None, 
                    lambda: text_to_coqui_audio(enhanced_chunks, output_dir=Config.OUTPUT_DIR)
                )
                logger.info(f"Generated {len(audio_files)} audio files")
            except Exception as e:
                logger.error(f"Audio generation failed: {e}")
                raise

            # Stitch audio
            logger.info("Stitching audio chunks together...")
            output_path = Config.get_output_path()
            try:
                await loop.run_in_executor(None, lambda: combine_audio(audio_files, output_path))
                logger.info(f"Audio stitched and saved to {output_path}")
            except Exception as e:
                logger.error(f"Audio stitching failed: {e}")
                raise

            # Convert to base64
            logger.info("Encoding audio to base64...")
            try:
                with open(output_path, "rb") as f:
                    audio_base64 = base64.b64encode(f.read()).decode("utf-8")
                logger.info("Audio generation completed successfully")
            except FileNotFoundError:
                logger.error(f"Output file not found: {output_path}")
                raise
            except Exception as e:
                logger.error(f"Error reading output file: {e}")
                raise

            return story2audio_pb2.AudioResponse(
                status="success",
                audio_base64=audio_base64,
                message="Audio generated successfully"
            )
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return story2audio_pb2.AudioResponse(status="error", audio_base64="", message=f"Validation error: {str(e)}")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            return story2audio_pb2.AudioResponse(status="error", audio_base64="", message=f"File error: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error during audio generation: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return story2audio_pb2.AudioResponse(status="error", audio_base64="", message=f"Server error: {str(e)}")

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=Config.MAX_WORKERS))
    story2audio_pb2_grpc.add_StoryServiceServicer_to_server(StoryServiceServicer(), server)
    server.add_insecure_port(f"[::]:{Config.GRPC_PORT}")
    await server.start()
    logger.info(f"gRPC server started on port {Config.GRPC_PORT}")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())