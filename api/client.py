import grpc
import story2audio_pb2
import story2audio_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = story2audio_pb2_grpc.StoryServiceStub(channel)
        request = story2audio_pb2.StoryRequest(story_text="Once upon a time, there was a brave knight...")
        response = stub.GenerateAudio(request)
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        print(f"Audio Base64 (first 100 chars): {response.audio_base64[:100]}...")

if __name__ == "__main__":
    run()