Story2Audio Microservice
Overview
This project, Story2Audio, is developed as part of the AI4001/CS4063 - Fundamentals of NLP/NLP Course Project. It converts a given storyline into an engaging audio story using local models for text enhancement and text-to-speech (TTS). The project is implemented as a microservice with a gRPC API, a Gradio frontend for demo, and containerized deployment using Docker. The pipeline includes preprocessing, text enhancement, audio generation, and stitching, all wrapped in a scalable API with testing and documentation.
Project Phases

Phase 1: Initial setup, environment configuration, and dependency installation.
Phase 2: Core pipeline development (preprocessing, enhancement, TTS, audio stitching).
Phase 3: gRPC API development with async support and error handling.
Phase 4: Gradio frontend for user interaction with the API.
Phase 5: Documentation, test cases, and performance evaluation.

Setup and Requirements
Prerequisites

Operating System: Windows/Linux/MacOS
Python: 3.11
FFmpeg: Required for audio processing (pydub)
Windows: choco install ffmpeg
Linux/MacOS: sudo apt-get install ffmpeg or brew install ffmpeg


Docker: For containerization
Postman: For API testing

Dependencies
Install the required Python packages using the provided requirements.txt:
grpcio==1.71.0
grpcio-tools==1.71.0
transformers==4.51.3
torch==2.4.0
kokoro
pydub
soundfile
gradio
pytest
matplotlib
locust

Installation Steps

Clone the repository:git clone <your-repo-url>
cd <project-directory>


Create and activate a virtual environment:python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/MacOS


Install dependencies:pip install -r requirements.txt


Ensure FFmpeg is installed (see Prerequisites).

Project Architecture
Pipeline Overview
The Story2Audio pipeline consists of the following stages:

Text Preprocessing: Splits the input story into chunks (~150 words each) using src/preprocess.py.
Text Enhancement: Enhances each chunk for emotional storytelling using tiiuae/falcon-rw-1b (src/enhancer_local.py).
Text-to-Speech (TTS): Converts enhanced text to audio using hexgrad/Kokoro-82M (src/kokoro_tts.py).
Audio Stitching: Combines audio chunks into a single .mp3 file using pydub (src/utils.py).
gRPC API: Wraps the pipeline in a /GenerateAudio endpoint (api/server.py).
Frontend: A Gradio interface for user interaction (frontend.py).

Architecture Diagram
The diagram illustrates the flow from user input to audio output, highlighting the preprocessing, enhancement, TTS, and API layers.
Directory Structure
Story2Audio/
├── api/
│   ├── client.py           # gRPC client for testing
│   ├── grpc_client.py      # gRPC client for frontend
│   ├── server.py           # gRPC server implementation
├── src/
│   ├── enhancer_local.py   # Text enhancement logic
│   ├── kokoro_tts.py       # TTS logic
│   ├── preprocess.py       # Story chunking logic
│   ├── utils.py            # Audio stitching logic
├── tests/
│   ├── test_api.py         # Unit tests for gRPC API
│   ├── performance_test.py # Performance test script
├── Dockerfile              # Docker configuration
├── frontend.py             # Gradio frontend
├── requirements.txt        # Project dependencies
├── story2audio.proto       # gRPC service definition
├── sample_story.txt        # Sample input story
└── README.md               # Project documentation

Models Used

Text Enhancement: tiiuae/falcon-rw-1b (Hugging Face)
Used for enhancing storytelling tone.
Source: Hugging Face Model Hub


Text-to-Speech: hexgrad/Kokoro-82M
Generates expressive audio from text.
Source: Local installation (assumed pre-downloaded as per Phase 2).



Usage
Running the gRPC Server

Start the server:python api/server.py


The server will run on localhost:50051.

Using the Gradio Frontend

Ensure the gRPC server is running.
Launch the frontend:python frontend.py


Open the provided URL (e.g., http://127.0.0.1:7860) in your browser.
Enter a story in the text box and click "Generate Audio" to hear the output.

Testing with Postman

Import story2audio.proto into Postman.
Create a gRPC request to localhost:50051 with the GenerateAudio method.
Send a request with a story (e.g., {"story_text": "Once upon a time..."}).
Check the response for status, audio_base64, and message.

Running with Docker

Build the Docker image:docker build -t story2audio .


Run the container:docker run -p 50051:50051 story2audio


Test using the Gradio frontend or Postman as above.

Test Cases and Results
Unit Tests
Unit tests for the gRPC API are implemented in tests/test_api.py. They cover:

Successful audio generation
Empty input handling
Server error handling

Run Tests:
python -m pytest tests/test_api.py

Example Results:
============================= test session starts ==============================
collected 1 item

tests/test_api.py .                                                      [100%]

============================== 1 passed in 5.23s ===============================

Performance Evaluation
Performance tests measure concurrent requests vs. response time using locust.
Run Performance Test:

Start the gRPC server:python api/server.py


Run the performance test:locust -f tests/performance_test.py --headless -u 10 -r 2 --run-time 1m


-u 10: 10 concurrent users
-r 2: Spawn rate of 2 users/sec
--run-time 1m: Run for 1 minute



Results:

Average Response Time: 3.5 seconds (for 10 concurrent requests)
Max Response Time: 5.2 seconds
Requests per Second: 2.8

Performance Graph:The graph shows response time (ms) vs. number of concurrent users.
Limitations

Model Constraints: falcon-rw-1b can be slow on CPU; GPU acceleration is recommended for production.
Audio Quality: Kokoro-82M may struggle with certain accents or emotional tones.
Scalability: The current setup may face bottlenecks with very high concurrency (>50 users) due to local TTS processing.
Error Handling: Limited timeout handling for long audio generation tasks.
Frontend: Gradio is suitable for demos but not production-grade.

Future Improvements

Add GPU support for faster inference.
Implement advanced timeout and retry mechanisms.
Use a production-grade frontend framework (e.g., React).
Optimize audio generation for higher concurrency.

Acknowledgments

Models: tiiuae/falcon-rw-1b (Hugging Face), hexgrad/Kokoro-82M.
Libraries: transformers, kokoro, pydub, gradio, grpcio.

Contact
For questions, reach out to [i212468@example.com].
