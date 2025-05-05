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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryServiceServicer(story2audio_pb2_grpc.StoryServiceServicer):
    async def GenerateAudio(self, request, context):
        try:
            story_text = request.story_text
            if not story_text.strip():
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Story text cannot be empty")
                return story2audio_pb2.AudioResponse(status="error", audio_base64="", message="Empty input")
            if len(story_text.split()) > 1000:  # Example limit
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Story text too long (max 1000 words)")
                return story2audio_pb2.AudioResponse(status="error", audio_base64="", message="Text too long")

            # Preprocess and enhance
            chunks = chunk_story(story_text, chunk_size=150)
            enhancer = StoryEnhancer()
            enhanced_chunks = [enhancer.enhance_chunk(chunk) for chunk in chunks]

            # Generate audio asynchronously
            loop = asyncio.get_event_loop()
            audio_files = await loop.run_in_executor(None, lambda: text_to_coqui_audio(enhanced_chunks, output_dir="outputs/temp"))

            # Stitch audio
            output_path = "outputs/temp/final_audio.mp3"
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
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    story2audio_pb2_grpc.add_StoryServiceServicer_to_server(StoryServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logger.info("gRPC server started on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())