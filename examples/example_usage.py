"""
Example usage script for Story2Audio Microservice

This script demonstrates how to use the Story2Audio gRPC API
to generate audio from text stories.
"""

import asyncio
import base64
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.grpc_client import generate_audio


async def generate_story_audio(story_text: str, output_filename: str = "generated_story.mp3"):
    """
    Generate audio from a story text and save it to a file.
    
    Args:
        story_text (str): The story text to convert to audio
        output_filename (str): Name of the output audio file
    """
    print(f"Generating audio for story ({len(story_text.split())} words)...")
    print("-" * 50)
    
    try:
        # Generate audio via gRPC
        audio_base64, status, message = await generate_audio(story_text)
        
        if status == "success":
            # Decode base64 audio
            audio_data = base64.b64decode(audio_base64)
            
            # Save to file
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(audio_data)
            
            file_size = len(audio_data) / 1024  # Size in KB
            print(f"✅ Success! Audio saved to: {output_path}")
            print(f"📊 File size: {file_size:.2f} KB")
            print(f"💬 Message: {message}")
            return output_path
        else:
            print(f"❌ Error: {message}")
            return None
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return None


async def main():
    """Main function with example stories"""
    
    # Example story 1: Short story
    short_story = """
    Once upon a time, in a magical forest, there lived a wise old owl.
    Every night, the owl would tell stories to the young animals.
    The stories were filled with adventure, wisdom, and wonder.
    All the animals loved listening to the owl's tales.
    """
    
    # Example story 2: Adventure story
    adventure_story = """
    In a distant kingdom, a brave knight embarked on a quest to find the lost treasure.
    The journey was long and filled with challenges. Along the way, the knight met
    a wise wizard who provided guidance. Together, they overcame obstacles and
    discovered the treasure hidden in an ancient castle. The kingdom celebrated
    their return with great joy and feasting.
    """
    
    print("=" * 50)
    print("Story2Audio Example Usage")
    print("=" * 50)
    print()
    
    # Generate audio for short story
    print("Example 1: Short Story")
    await generate_story_audio(short_story.strip(), "example_short_story.mp3")
    print()
    
    # Uncomment to generate audio for adventure story
    # print("Example 2: Adventure Story")
    # await generate_story_audio(adventure_story.strip(), "example_adventure_story.mp3")
    # print()
    
    print("=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    # Make sure the gRPC server is running before executing this script
    print("⚠️  Make sure the gRPC server is running (python api/server.py)")
    print()
    
    asyncio.run(main())
