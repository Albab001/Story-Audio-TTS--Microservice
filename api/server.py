import grpc
import os
import logging
from concurrent import futures
import asyncio
import story2audio_pb2
import story2audio_pb2_grpc
from src.preprocess import chunk_story
from src.enhancer_local import StoryEnhancer
from src.kokoro_tts import text_to_coqui_audio
from src.utils import combine_audio
import base64
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class StoryServiceServicer(story2audio_pb2_grpc.StoryServiceServicer):
    async def GenerateAudio(self, request, context):
        try:
            story_text = request.story_text
            if not story_text.strip():
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Story text cannot be empty")
                return story2audio_pb2.AudioResponse(status="error", audio_base64="", message="Empty input")
            if len(story_text.split()) > Config.MAX_WORDS:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(f"Story text too long (max {Config.MAX_WORDS} words)")
                return story2audio_pb2.AudioResponse(status="error", audio_base64="", message="Text too long")

            # Preprocess and enhance
            chunks = chunk_story(story_text, chunk_size=Config.CHUNK_SIZE)
            enhancer = StoryEnhancer()
            enhanced_chunks = [enhancer.enhance_chunk(chunk) for chunk in chunks]

            # Generate audio asynchronously
            loop = asyncio.get_event_loop()
            audio_files = await loop.run_in_executor(None, lambda: text_to_coqui_audio(enhanced_chunks, output_dir=Config.OUTPUT_DIR))

            # Stitch audio
            output_path = Config.get_output_path()
            await loop.run_in_executor(None, lambda: combine_audio(audio_files, output_path))

            # Convert to base64
            with open(output_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode("utf-8")

            return story2audio_pb2.AudioResponse(
                status="success",
                audio_base64=audio_base64,
                message="Audio generated successfully"
            )
        except Exception as e:
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