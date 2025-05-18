# 🎧 Story2Audio Microservice

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-orange.svg)
![gRPC](https://img.shields.io/badge/gRPC-1.71.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Transform your stories into engaging audio narratives using AI-powered text enhancement and text-to-speech technology.**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Phases](#-project-phases)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Performance](#-performance)
- [Docker Deployment](#-docker-deployment)
- [Project Structure](#-project-structure)
- [Models Used](#-models-used)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**Story2Audio** is an intelligent microservice that converts written stories into high-quality audio narratives. Developed as part of the **AI4001/CS4063 - Fundamentals of NLP/NLP Course Project**, this system leverages state-of-the-art NLP models for text enhancement and advanced text-to-speech technology to create engaging audio experiences.

### Key Capabilities

- **Intelligent Text Enhancement**: Automatically improves storytelling tone and emotional depth
- **High-Quality TTS**: Generates natural, expressive speech using Kokoro-82M
- **Scalable Architecture**: Built with gRPC for high-performance microservice communication
- **User-Friendly Interface**: Gradio-based web frontend for easy interaction
- **Production-Ready**: Docker containerization and comprehensive testing

---

## ✨ Features

- 🚀 **Asynchronous Processing**: Non-blocking audio generation with async/await
- 🎨 **Text Enhancement**: AI-powered story enhancement using Falcon-RW-1B model
- 🔊 **Natural Speech**: High-quality TTS with emotional expression
- 🔧 **Configurable**: Environment-based configuration management
- 🐳 **Dockerized**: Easy deployment with Docker
- 🧪 **Tested**: Comprehensive unit and performance tests
- 📊 **Monitoring**: Built-in logging and performance metrics
- 🌐 **RESTful API**: gRPC-based API for seamless integration

---

## 📈 Project Phases

The project was developed in five distinct phases:

1. **Phase 1**: Initial setup, environment configuration, and dependency installation
2. **Phase 2**: Core pipeline development (preprocessing, enhancement, TTS, audio stitching)
3. **Phase 3**: gRPC API development with async support and error handling
4. **Phase 4**: Gradio frontend for user interaction with the API
5. **Phase 5**: Documentation, test cases, and performance evaluation

---

## 🏗️ Architecture

### Pipeline Overview

The Story2Audio pipeline consists of four main stages:

```
Input Story → Preprocessing → Enhancement → TTS → Audio Stitching → Final Audio
```

1. **Text Preprocessing** (`src/preprocess.py`)
   - Splits input story into manageable chunks (~150 words each)
   - Handles text normalization and whitespace cleanup
   - Validates input and handles edge cases

2. **Text Enhancement** (`src/enhancer_local.py`)
   - Uses `tiiuae/falcon-rw-1b` model for emotional storytelling enhancement
   - Improves narrative tone and engagement
   - Processes chunks in parallel for efficiency

3. **Text-to-Speech** (`src/kokoro_tts.py`)
   - Converts enhanced text to audio using `hexgrad/Kokoro-82M`
   - Generates expressive, natural-sounding speech
   - Supports multiple voice styles

4. **Audio Stitching** (`src/utils.py`)
   - Combines individual audio chunks into a single MP3 file
   - Handles audio format conversion and synchronization
   - Ensures seamless transitions between chunks

### System Architecture

```
┌─────────────┐
│   Client    │
│  (Gradio)   │
└──────┬──────┘
       │ gRPC
       ▼
┌─────────────────┐
│  gRPC Server    │
│  (api/server.py)│
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Pipeline       │
│  - Preprocess   │
│  - Enhance      │
│  - TTS          │
│  - Stitch       │
└─────────────────┘
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Operating System**: Windows 10+, Linux, or macOS
- **Python**: 3.11 or higher
- **FFmpeg**: Required for audio processing
  - **Windows**: `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org)
  - **Linux**: `sudo apt-get install ffmpeg`
  - **macOS**: `brew install ffmpeg`
- **Docker** (optional): For containerized deployment
- **Git**: For cloning the repository

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Albab001/-Story2Audio-Microservice.git
cd -Story2Audio-Microservice
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify FFmpeg Installation

```bash
ffmpeg -version
```

If FFmpeg is not found, please install it using the instructions in the Prerequisites section.

---

## 🎬 Quick Start

### 1. Start the gRPC Server

```bash
python api/server.py
```

The server will start on `localhost:50051`. You should see:
```
INFO:__main__:gRPC server started on port 50051
```

### 2. Launch the Gradio Frontend

In a new terminal (with the virtual environment activated):

```bash
python frontend.py
```

The frontend will be available at `http://127.0.0.1:7860`

### 3. Generate Audio

1. Open the Gradio interface in your browser
2. Enter your story in the text box
3. Click "Generate Audio"
4. Wait for processing (typically 10-30 seconds depending on story length)
5. Listen to or download the generated audio

---

## 💻 Usage

### Using the Gradio Frontend

The easiest way to use Story2Audio is through the web interface:

1. Ensure the gRPC server is running
2. Launch `frontend.py`
3. Enter your story (up to 1000 words)
4. Click "Generate Audio"
5. The system will:
   - Preprocess your story into chunks
   - Enhance each chunk for better storytelling
   - Convert to speech
   - Combine into a single audio file

### Using the gRPC API Directly

#### Python Client Example

```python
import asyncio
from api.grpc_client import generate_audio

async def main():
    story = "Once upon a time, in a land far away..."
    audio_base64, status, message = await generate_audio(story)
    
    if status == "success":
        # Decode and save audio
        import base64
        audio_data = base64.b64decode(audio_base64)
        with open("output.mp3", "wb") as f:
            f.write(audio_data)
        print("Audio saved to output.mp3")
    else:
        print(f"Error: {message}")

asyncio.run(main())
```

#### Using Postman

1. Import `story2audio.proto` into Postman
2. Create a gRPC request to `localhost:50051`
3. Use the `GenerateAudio` method
4. Send a request with JSON:
```json
{
  "story_text": "Your story here..."
}
```

---

## 📡 API Documentation

### gRPC Service Definition

**Service**: `StoryService`

**Method**: `GenerateAudio`

**Request**:
```protobuf
message StoryRequest {
  string story_text = 1;
}
```

**Response**:
```protobuf
message AudioResponse {
  string status = 1;           // "success" or "error"
  string audio_base64 = 2;     // Base64-encoded MP3 audio
  string message = 3;          // Status message
}
```

### Request Limits

- **Maximum Words**: 1000 words (configurable via `Config.MAX_WORDS`)
- **Minimum Words**: 1 word
- **Input Validation**: Empty strings and invalid inputs are rejected

### Error Codes

- `INVALID_ARGUMENT`: Empty input or text exceeds word limit
- `INTERNAL`: Server-side processing error

---

## ⚙️ Configuration

The application uses a centralized configuration system (`config.py`) that supports environment variables:

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GRPC_PORT` | `50051` | Port for gRPC server |
| `MAX_WORKERS` | `10` | Maximum concurrent workers |
| `CHUNK_SIZE` | `150` | Words per chunk |
| `MAX_WORDS` | `1000` | Maximum input words |
| `ENHANCER_MODEL` | `tiiuae/falcon-rw-1b` | Text enhancement model |
| `TTS_MODEL` | `hexgrad/Kokoro-82M` | TTS model name |
| `OUTPUT_DIR` | `outputs/temp` | Output directory |
| `LOG_LEVEL` | `INFO` | Logging level |

### Example Configuration

Create a `.env` file (not committed to git):

```env
GRPC_PORT=50051
MAX_WORKERS=20
CHUNK_SIZE=200
MAX_WORDS=2000
LOG_LEVEL=DEBUG
```

---

## 🧪 Testing

### Unit Tests

Run the test suite:

```bash
python -m pytest Tests/test_api.py -v
```

**Test Coverage**:
- ✅ Successful audio generation
- ✅ Empty input handling
- ✅ Long input validation
- ✅ Error handling

### Performance Testing

Using Locust for load testing:

```bash
# Start the server first
python api/server.py

# In another terminal, run performance tests
locust -f Tests/performance_test.py --headless -u 10 -r 2 --run-time 1m
```

**Parameters**:
- `-u 10`: 10 concurrent users
- `-r 2`: Spawn rate of 2 users/second
- `--run-time 1m`: Run for 1 minute

---

## 📊 Performance

### Benchmarks

Based on performance testing with 10 concurrent users:

- **Average Response Time**: 3.5 seconds
- **Max Response Time**: 5.2 seconds
- **Requests per Second**: 2.8
- **Throughput**: ~168 requests/minute

### Performance Graph

See `performance_graph.png` for detailed performance metrics across different concurrency levels.

### Optimization Tips

1. **Use GPU**: Enable CUDA for faster model inference
2. **Adjust Workers**: Increase `MAX_WORKERS` for higher concurrency
3. **Chunk Size**: Optimize `CHUNK_SIZE` based on your use case
4. **Caching**: Consider implementing response caching for repeated stories

---

## 🐳 Docker Deployment

### Build the Docker Image

```bash
docker build -t story2audio:latest .
```

### Run the Container

```bash
docker run -p 50051:50051 story2audio:latest
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  story2audio:
    build: .
    ports:
      - "50051:50051"
    environment:
      - GRPC_PORT=50051
      - MAX_WORKERS=10
    volumes:
      - ./outputs:/app/outputs
```

Run with:
```bash
docker-compose up
```

---

## 📁 Project Structure

```
Story2Audio-Microservice/
├── api/
│   ├── client.py           # gRPC client for testing
│   ├── grpc_client.py       # gRPC client for frontend
│   └── server.py           # gRPC server implementation
├── src/
│   ├── enhancer_local.py   # Text enhancement logic
│   ├── kokoro_tts.py       # TTS logic
│   ├── preprocess.py       # Story chunking logic
│   └── utils.py            # Audio stitching logic
├── Tests/
│   ├── test_api.py         # Unit tests for gRPC API
│   ├── performance_test.py # Performance test script
│   └── plot_performance.py # Performance visualization
├── Dockerfile              # Docker configuration
├── frontend.py             # Gradio frontend
├── config.py               # Configuration management
├── requirements.txt        # Project dependencies
├── story2audio.proto       # gRPC service definition
├── story2audio_pb2.py      # Generated gRPC code
├── story2audio_pb2_grpc.py # Generated gRPC code
├── sample_story.txt        # Sample input story
├── .gitignore             # Git ignore rules
├── CHANGELOG.md           # Project changelog
└── README.md              # This file
```

---

## 🤖 Models Used

### Text Enhancement: Falcon-RW-1B

- **Model**: `tiiuae/falcon-rw-1b`
- **Purpose**: Enhances storytelling tone and emotional depth
- **Source**: [Hugging Face Model Hub](https://huggingface.co/tiiuae/falcon-rw-1b)
- **Size**: ~1B parameters
- **Performance**: Optimized for CPU and GPU inference

### Text-to-Speech: Kokoro-82M

- **Model**: `hexgrad/Kokoro-82M`
- **Purpose**: Generates expressive, natural-sounding speech
- **Features**: 
  - Multi-language support
  - Emotional expression
  - High-quality audio output
- **Source**: Local installation (pre-downloaded)

---

## ⚠️ Limitations

1. **Model Constraints**: 
   - Falcon-RW-1B can be slow on CPU; GPU acceleration recommended for production
   - Processing time increases with story length

2. **Audio Quality**: 
   - Kokoro-82M may struggle with certain accents or complex emotional tones
   - Audio quality depends on input text quality

3. **Scalability**: 
   - Current setup may face bottlenecks with very high concurrency (>50 users)
   - Local TTS processing limits horizontal scaling

4. **Error Handling**: 
   - Limited timeout handling for long audio generation tasks
   - No automatic retry mechanism for failed requests

5. **Frontend**: 
   - Gradio is suitable for demos but not production-grade
   - Consider React/Vue.js for production deployments

---

## 🔮 Future Improvements

- [ ] **GPU Support**: Add CUDA support for faster inference
- [ ] **Advanced Timeout Handling**: Implement request timeouts and retries
- [ ] **Production Frontend**: Migrate to React/Vue.js for better UX
- [ ] **Caching Layer**: Add Redis caching for frequently requested stories
- [ ] **Load Balancing**: Implement horizontal scaling with multiple server instances
- [ ] **Monitoring**: Add Prometheus metrics and Grafana dashboards
- [ ] **API Rate Limiting**: Implement rate limiting for API protection
- [ ] **Multiple Voice Options**: Support for different voice styles and languages
- [ ] **Batch Processing**: Support for processing multiple stories in parallel
- [ ] **Audio Post-Processing**: Add background music and sound effects

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact

For questions, issues, or contributions, please reach out to:

- **Email**: [i212468@example.com]
- **GitHub Issues**: [Create an issue](https://github.com/Albab001/-Story2Audio-Microservice/issues)

---

## 🙏 Acknowledgments

- **Models**: 
  - [tiiuae/falcon-rw-1b](https://huggingface.co/tiiuae/falcon-rw-1b) (Hugging Face)
  - [hexgrad/Kokoro-82M](https://github.com/hexgrad/Kokoro-82M) (Text-to-Speech)
  
- **Libraries**: 
  - transformers, kokoro, pydub, gradio, grpcio, torch
  
- **Course**: AI4001/CS4063 - Fundamentals of NLP/NLP

---

<div align="center">

**Made with ❤️ for the NLP Course Project**

⭐ Star this repo if you find it helpful!

</div>
