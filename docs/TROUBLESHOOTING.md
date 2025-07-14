# Troubleshooting Guide

Common issues and solutions for Story2Audio Microservice.

## Server Won't Start

### Port Already in Use
```bash
# Find process using port 50051
lsof -i :50051  # Linux/Mac
netstat -ano | findstr :50051  # Windows

# Kill the process or change port
export GRPC_PORT=50052
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

## Audio Generation Fails

### FFmpeg Not Found
```bash
# Install FFmpeg
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### Model Loading Errors
- Check internet connection for model downloads
- Verify disk space for model cache
- Check HuggingFace token if using private models

## Performance Issues

### Slow Processing
- Enable GPU if available
- Increase MAX_WORKERS
- Reduce CHUNK_SIZE for faster processing
- Enable caching

### Memory Issues
- Reduce MAX_WORKERS
- Use CPU instead of GPU
- Increase system memory
- Enable model offloading

## Connection Errors

### gRPC Connection Refused
- Verify server is running
- Check firewall settings
- Verify port configuration
- Check network connectivity

### Timeout Errors
- Increase timeout values
- Check server load
- Verify network stability

## Logging

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python api/server.py
```

### View Logs
```bash
# Docker
docker logs story2audio-container

# Systemd
journalctl -u story2audio -f
```

## Common Error Messages

### "Model not found"
- Download models manually
- Check model cache directory
- Verify model names in config

### "Audio generation failed"
- Check FFmpeg installation
- Verify output directory permissions
- Check disk space

### "Invalid input"
- Verify input text format
- Check word count limits
- Ensure text is not empty
