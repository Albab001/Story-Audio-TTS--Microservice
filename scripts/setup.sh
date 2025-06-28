#!/bin/bash
# Setup script for Story2Audio Microservice

set -e

echo "Setting up Story2Audio Microservice..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg not found. Please install FFmpeg for audio processing."
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
fi

# Create output directories
mkdir -p outputs/temp
mkdir -p outputs/final

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
