# Deployment Guide

This guide covers deployment options for Story2Audio Microservice.

## Local Deployment

### Prerequisites
- Python 3.11+
- FFmpeg installed
- Virtual environment

### Steps

1. Clone the repository:
```bash
git clone https://github.com/Albab001/-Story2Audio-Microservice.git
cd -Story2Audio-Microservice
```

2. Set up environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the server:
```bash
python api/server.py
```

## Docker Deployment

### Build Image
```bash
docker build -t story2audio:latest .
```

### Run Container
```bash
docker run -p 50051:50051 story2audio:latest
```

### Docker Compose
```bash
docker-compose up -d
```

## Production Deployment

### Environment Variables

Set the following environment variables:

```bash
export GRPC_PORT=50051
export MAX_WORKERS=20
export CHUNK_SIZE=150
export MAX_WORDS=1000
export LOG_LEVEL=INFO
```

### Systemd Service

Create `/etc/systemd/system/story2audio.service`:

```ini
[Unit]
Description=Story2Audio Microservice
After=network.target

[Service]
Type=simple
User=story2audio
WorkingDirectory=/opt/story2audio
Environment="PATH=/opt/story2audio/venv/bin"
ExecStart=/opt/story2audio/venv/bin/python api/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

Example Nginx configuration for gRPC:

```nginx
server {
    listen 443 http2;
    server_name story2audio.example.com;

    location / {
        grpc_pass grpc://localhost:50051;
    }
}
```

## Monitoring

- Health checks: Implement health check endpoint
- Logging: Configure centralized logging
- Metrics: Use metrics collection for monitoring

## Scaling

- Horizontal scaling: Run multiple instances behind load balancer
- Vertical scaling: Increase MAX_WORKERS and resources
- Caching: Enable caching for frequently requested stories
