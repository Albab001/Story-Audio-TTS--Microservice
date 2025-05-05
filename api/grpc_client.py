import grpc
import asyncio
import story2audio_pb2
import story2audio_pb2_grpc

async def generate_audio(story_text):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = story2audio_pb2_grpc.StoryServiceStub(channel)
        request = story2audio_pb2.StoryRequest(story_text=story_text)
        response = await stub.GenerateAudio(request)
        return response.audio_base64, response.status, response.message