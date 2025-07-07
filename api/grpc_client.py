"""
gRPC client for Story2Audio service.

Provides async client interface for generating audio from stories.
"""
import grpc
import asyncio
import logging
from typing import Tuple, Optional
import story2audio_pb2
import story2audio_pb2_grpc
from config import Config

logger = logging.getLogger(__name__)


class Story2AudioClient:
    """Client for Story2Audio gRPC service."""
    
    def __init__(self, host: str = "localhost", port: int = None):
        """
        Initialize client.
        
        Args:
            host: Server hostname
            port: Server port (defaults to Config.GRPC_PORT)
        """
        self.host = host
        self.port = port or Config.GRPC_PORT
        self.address = f"{host}:{self.port}"
    
    async def generate_audio(
        self, 
        story_text: str,
        timeout: Optional[float] = None
    ) -> Tuple[str, str, str]:
        """
        Generate audio from story text.
        
        Args:
            story_text: Story text to convert
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (audio_base64, status, message)
        """
        try:
            options = [
                ('grpc.max_message_length', Config.GRPC_MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', Config.GRPC_MAX_MESSAGE_LENGTH),
            ]
            
            async with grpc.aio.insecure_channel(self.address, options=options) as channel:
                stub = story2audio_pb2_grpc.StoryServiceStub(channel)
                request = story2audio_pb2.StoryRequest(story_text=story_text)
                
                if timeout:
                    response = await asyncio.wait_for(
                        stub.GenerateAudio(request),
                        timeout=timeout
                    )
                else:
                    response = await stub.GenerateAudio(request)
                
                return response.audio_base64, response.status, response.message
                
        except asyncio.TimeoutError:
            logger.error(f"Request timeout after {timeout}s")
            return "", "error", "Request timeout"
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e.code()} - {e.details()}")
            return "", "error", f"gRPC error: {e.details()}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "", "error", f"Client error: {str(e)}"


# Backward compatibility function
async def generate_audio(story_text: str) -> Tuple[str, str, str]:
    """
    Generate audio from story text (backward compatibility).
    
    Args:
        story_text: Story text to convert
        
    Returns:
        Tuple of (audio_base64, status, message)
    """
    client = Story2AudioClient()
    return await client.generate_audio(story_text)