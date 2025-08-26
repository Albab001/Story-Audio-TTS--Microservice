import gradio as gr
import asyncio
import base64
import os
import re
from api.grpc_client import generate_audio

# Custom CSS for an attractive design
custom_css = """
    .gradio-container {
        background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .gr-button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .gr-button:hover {
        background-color: #45a049;
    }
    .gr-textbox {
        border-radius: 10px;
        padding: 10px;
    }
    h1 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
"""

# Function to validate input text
def validate_input(story_text):
    if not story_text or not story_text.strip():
        return False, "Please enter a story!"
    # Check if the input is only numbers
    if re.fullmatch(r'\d+', story_text.strip()):
        return False, "Story cannot be only numbers!"
    # Check if the input is only special characters
    if re.fullmatch(r'[^a-zA-Z0-9\s]+', story_text.strip()):
        return False, "Story cannot be only special characters!"
    # Ensure the input has at least some meaningful words
    if not any(len(word) > 1 for word in story_text.split()):
        return False, "Story must contain meaningful words!"
    return True, ""

# Function to process the story and generate audio
async def process_story(story_text):
    # Validate input
    is_valid, error_message = validate_input(story_text)
    if not is_valid:
        return None, None, "error", error_message

    try:
        # Generate audio via gRPC
        audio_base64, status, message = await generate_audio(story_text)
        if status != "success":
            return None, None, status, message

        # Decode base64 and save to a temporary file
        audio_data = base64.b64decode(audio_base64)
        temp_audio_path = "temp_audio.mp3"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_data)

        return temp_audio_path, temp_audio_path, "success", "Audio generated successfully! Click play to listen or download the file."
    except Exception as e:
        return None, None, "error", f"Failed to generate audio: {str(e)}"

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="Story2Audio") as demo:
    gr.Markdown("# 🎧 Story2Audio Generator")
    gr.Markdown("Enter your story below and listen to the audio version!")
    
    with gr.Row():
        with gr.Column(scale=1):
            story_input = gr.Textbox(label="Your Story", lines=5, placeholder="Type your story here...")
        with gr.Column(scale=1):
            audio_output = gr.Audio(label="Generated Audio", type="filepath", interactive=False)
            download_output = gr.File(label="Download Audio")
            status_output = gr.Textbox(label="Status", interactive=False)
    
    submit_btn = gr.Button("Generate Audio", variant="primary")
    
    submit_btn.click(
        fn=lambda x: asyncio.run(process_story(x)),
        inputs=story_input,
        outputs=[audio_output, download_output, status_output, status_output]
    )
    
    # Add word count display
    word_count = gr.Textbox(label="Word Count", value="0", interactive=False)
    story_input.change(
        fn=lambda x: str(len(x.split()) if x else 0),
        inputs=story_input,
        outputs=word_count
    )

# Launch the interface
demo.launch()