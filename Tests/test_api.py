import grpc
import story2audio_pb2
import story2audio_pb2_grpc
import pytest
import asyncio

@pytest.mark.asyncio
async def test_generate_audio_success():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = story2audio_pb2_grpc.StoryServiceStub(channel)
        request = story2audio_pb2.StoryRequest(story_text="A brave knight went on a quest.")
        response = await stub.GenerateAudio(request)
        assert response.status == "success"
        assert len(response.audio_base64) > 0
        assert "successfully" in response.message

@pytest.mark.asyncio
async def test_generate_audio_empty_input():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = story2audio_pb2_grpc.StoryServiceStub(channel)
        request = story2audio_pb2.StoryRequest(story_text="")
        response = await stub.GenerateAudio(request)
        assert response.status == "error"
        assert response.audio_base64 == ""
        assert "Empty input" in response.message

@pytest.mark.asyncio
async def test_generate_audio_long_input():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = story2audio_pb2_grpc.StoryServiceStub(channel)
        long_text = "word " * 1001  # Exceeds 1000-word limit
        request = story2audio_pb2.StoryRequest(story_text=long_text)
        response = await stub.GenerateAudio(request)
        assert response.status == "error"
        assert response.audio_base64 == ""
        assert "Text too long" in response.message

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", __file__]))