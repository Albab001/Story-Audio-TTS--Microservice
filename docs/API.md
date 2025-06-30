# Story2Audio API Documentation

## Overview

Story2Audio provides a gRPC-based API for converting text stories into audio narratives.

## Endpoints

### GenerateAudio

Converts a text story into an audio file.

**Request:**
```protobuf
message StoryRequest {
  string story_text = 1;
}
```

**Response:**
```protobuf
message AudioResponse {
  string status = 1;           // "success" or "error"
  string audio_base64 = 2;     // Base64-encoded MP3 audio
  string message = 3;          // Status message
}
```

**Example:**
```python
import asyncio
from api.grpc_client import generate_audio

async def main():
    story = "Once upon a time..."
    audio_base64, status, message = await generate_audio(story)
    print(f"Status: {status}, Message: {message}")

asyncio.run(main())
```

## Error Codes

- `INVALID_ARGUMENT`: Invalid input (empty, too long, etc.)
- `INTERNAL`: Server-side processing error
- `NOT_FOUND`: File not found error

## Rate Limits

- Maximum words per request: 1000 (configurable)
- Concurrent requests: Limited by MAX_WORKERS setting

## Best Practices

1. Validate input before sending
2. Handle errors gracefully
3. Implement retry logic for transient failures
4. Monitor request duration and size
