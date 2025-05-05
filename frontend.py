import gradio as gr
import asyncio
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

# Function to process the story and generate audio
async def process_story(story_text):
    if not story_text or not story_text.strip():
        return None, "error", "Please enter a story!"
    try:
        audio_base64, status, message = await generate_audio(story_text)
        if status == "success":
            return f"data:audio/mp3;base64,{audio_base64}", status, message
        return None, status, message
    except Exception as e:
        return None, "error", f"Failed to generate audio: {str(e)}"

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="Story2Audio") as demo:
    gr.Markdown("# 🎧 Story2Audio Generator")
    gr.Markdown("Enter your story below and listen to the audio version!")
    
    with gr.Row():
        with gr.Column(scale=1):
            story_input = gr.Textbox(label="Your Story", lines=5, placeholder="Type your story here...")
        with gr.Column(scale=1):
            audio_output = gr.Audio(label="Generated Audio", type="numpy", interactive=False)
            status_output = gr.Textbox(label="Status", interactive=False)
    
    submit_btn = gr.Button("Generate Audio", variant="primary")
    
    submit_btn.click(
        fn=lambda x: asyncio.run(process_story(x)),
        inputs=story_input,
        outputs=[audio_output, status_output, status_output]
    )

# Launch the interface
demo.launch()