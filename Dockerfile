# Use pre-built PyTorch image with Python 3.11 and torch 2.1.0
FROM pytorch/pytorch:2.1.0-cpu-py3.11


# Set working directory
WORKDIR /app

# Install system dependencies for pydub (ffmpeg) and other libraries
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libpng-dev \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirement.txt .

# Install additional Python dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirement.txt \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --timeout 120 \
    --retries 5

# Copy the rest of the project files
COPY . .

# Command to run the gRPC server
CMD ["python", "api/server.py"]