# Use pre-built PyTorch image with Python 3.11 and torch 2.1.0
FROM pytorch/pytorch:2.1.0-cpu-py3.11

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GRPC_PORT=50051 \
    MAX_WORKERS=10

# Install system dependencies for pydub (ffmpeg) and other libraries
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libpng-dev \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
COPY requirements.txt .

# Install additional Python dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    --timeout 120 \
    --retries 5

# Create output directory
RUN mkdir -p /app/outputs/temp

# Copy the rest of the project files
COPY . .

# Expose gRPC port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import grpc; import story2audio_pb2_grpc; print('OK')" || exit 1

# Command to run the gRPC server
CMD ["python", "api/server.py"]