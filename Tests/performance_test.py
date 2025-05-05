from locust import task, TaskSet, HttpUser
import grpc
import story2audio_pb2
import story2audio_pb2_grpc
import time

class GrpcUser(HttpUser):
    host = "localhost:50051"
    wait_time = lambda x: 1  # Constant wait time of 1 second

    def on_start(self):
        self.channel = grpc.insecure_channel(self.host)
        self.stub = story2audio_pb2_grpc.StoryServiceStub(self.channel)

    def on_stop(self):
        self.channel.close()

    @task
    def generate_audio(self):
        start_time = time.time()
        request = story2audio_pb2.StoryRequest(story_text="A brave knight went on a quest to save the kingdom.")
        try:
            response = self.stub.GenerateAudio(request)
            self.environment.events.request.fire(
                request_type="gRPC",
                name="GenerateAudio",
                response_time=(time.time() - start_time) * 1000,  # Convert to milliseconds
                response_length=len(response.audio_base64),
                exception=None
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="gRPC",
                name="GenerateAudio",
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e
            )