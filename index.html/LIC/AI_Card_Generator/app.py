# AI Aadhaar Realistic Image Generator PRO (FULLY FIXED VERSION)
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from PIL import Image
import gradio as gr
import os
import numpy as np
import cv2
from typing import List
import tempfile

# ==========================
# DEVICE SETUP (AUTO CPU/GPU)
# ==========================
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
print(f"Using device: {device} with dtype: {dtype}")

# ==========================
# LOAD MODELS WITH ERROR HANDLING
# ==========================
def load_models():
    """Load models with proper error handling"""
    try:
        print("Loading ControlNet...")
        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_canny",
            torch_dtype=dtype,
            use_safetensors=True
        )
        
        print("Loading Stable Diffusion pipeline...")
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "SG161222/Realistic_Vision_V5.1_noVAE",
            controlnet=controlnet,
            torch_dtype=dtype,
            use_safetensors=True,
            safety_checker=None,  # Disable safety checker for faster loading
            requires_safety_checker=False
        )
        
        # Move to device
        pipe = pipe.to(device)
        
        # Enable memory efficient attention if available
        if device == "cuda":
            pipe.enable_xformers_memory_efficient_attention()
            
        print("Models loaded successfully!")
        return pipe
        
    except Exception as e:
        print(f"Error loading models: {e}")
        return None

# Load the pipeline
pipe = load_models()

# ==========================
# IMAGE PREPROCESSING
# ==========================
def process_control_image(image):
    """Process image for ControlNet (canny edge detection)"""
    if image is None:
        return None
    
    # Convert PIL to numpy
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Apply canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    
    # Convert back to PIL
    edges_image = Image.fromarray(edges).convert("RGB")
    
    # Resize to 512x512 (optimal for model)
    edges_image = edges_image.resize((512, 512), Image.Resampling.LANCZOS)
    
    return edges_image

# ==========================
# PROMPT BUILDER
# ==========================
def build_prompt(background, card_type="aadhaar"):
    """Build prompt based on parameters"""
    
    base_prompt = f"""hyper realistic {card_type} card on {background} surface, 
    laminated plastic card, soft shadow on surface, professional product photography,
    soft natural lighting, slight reflection, sharp focus, detailed texture,
    DSLR photo, 8k resolution, ultra high detail, depth of field"""
    
    return base_prompt

# ==========================
# SINGLE IMAGE GENERATION (FIXED)
# ==========================
def generate_realistic(image, background, steps, scale, seed=None):
    """Generate realistic image with proper error handling"""
    
    if pipe is None:
        return None, "Model failed to load. Please check console for errors."
    
    if image is None:
        return None, "Please upload an image first."
    
    try:
        # Process image for ControlNet
        control_image = process_control_image(image)
        
        # Build prompt
        prompt = build_prompt(background)
        
        # Set seed for reproducibility
        if seed is not None and seed >= 0:
            torch.manual_seed(seed)
            if device == "cuda":
                torch.cuda.manual_seed(seed)
        
        # Generate image
        with torch.autocast(device):
            result = pipe(
                prompt=prompt,
                negative_prompt="blurry, fake, distorted, low quality, watermark, text errors, bad anatomy, ugly, deformed",
                image=control_image,
                num_inference_steps=int(steps),
                guidance_scale=float(scale),
                height=512,
                width=512
            ).images[0]
        
        return result, "Generation successful!"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# ==========================
# BATCH GENERATION (FIXED)
# ==========================
def batch_generate(files, background, steps, scale):
    """Process multiple images"""
    
    if not files:
        return [], "No files uploaded."
    
    outputs = []
    status_messages = []
    
    # Create output directory
    output_dir = tempfile.mkdtemp()
    
    for i, file in enumerate(files):
        try:
            # Load image
            img = Image.open(file.name)
            
            # Generate
            result, status = generate_realistic(img, background, steps, scale)
            
            if result:
                # Save image
                output_path = os.path.join(output_dir, f"output_{i}.png")
                result.save(output_path)
                outputs.append(result)
                status_messages.append(f"✅ Image {i+1}: Success")
            else:
                status_messages.append(f"❌ Image {i+1}: {status}")
                
        except Exception as e:
            status_messages.append(f"❌ Image {i+1}: Error - {str(e)}")
    
    return outputs, "\n".join(status_messages)

# ==========================
# UI (FIXED GRADIO INTERFACE)
# ==========================
# Custom CSS for better UI
custom_css = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}
.output-image {
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
"""

with gr.Blocks(css=custom_css, title="AI Aadhaar Generator PRO") as app:
    gr.Markdown("""
    # 🔥 AI Aadhaar Generator PRO (Fixed Version)
    ### Generate realistic Aadhaar card images with AI
    """)
    
    # Status indicator
    if pipe is None:
        gr.Warning("⚠️ Models failed to load. Check console for errors.")
    else:
        gr.Info(f"✅ Models loaded successfully on {device.upper()}")
    
    with gr.Tabs():
        # Single Image Tab
        with gr.TabItem("📷 Single Image"):
            with gr.Row():
                with gr.Column(scale=1):
                    # Input section
                    input_image = gr.Image(
                        type="pil", 
                        label="Upload Card Image",
                        height=400
                    )
                    
                    # Controls
                    background = gr.Dropdown(
                        choices=[
                            "wooden table", 
                            "marble table", 
                            "office desk", 
                            "dark table",
                            "glass table",
                            "white surface"
                        ],
                        value="wooden table",
                        label="Background Surface"
                    )
                    
                    with gr.Row():
                        steps = gr.Slider(
                            minimum=10, 
                            maximum=50, 
                            value=25, 
                            step=1,
                            label="Inference Steps"
                        )
                        scale = gr.Slider(
                            minimum=1, 
                            maximum=15, 
                            value=7, 
                            step=0.5,
                            label="CFG Scale"
                        )
                    
                    seed = gr.Number(
                        value=-1, 
                        label="Seed (-1 for random)",
                        precision=0
                    )
                    
                    generate_btn = gr.Button(
                        "🚀 Generate Image", 
                        variant="primary",
                        size="lg"
                    )
                    
                with gr.Column(scale=1):
                    # Output section
                    output_image = gr.Image(
                        label="Generated Result",
                        height=400
                    )
                    
                    status_text = gr.Textbox(
                        label="Status",
                        interactive=False
                    )
            
            # Wire up the generate button
            generate_btn.click(
                fn=generate_realistic,
                inputs=[input_image, background, steps, scale, seed],
                outputs=[output_image, status_text]
            )
        
        # Batch Processing Tab
        with gr.TabItem("📁 Batch Processing"):
            with gr.Row():
                with gr.Column():
                    batch_files = gr.File(
                        file_count="multiple",
                        label="Upload Multiple Images",
                        file_types=["image"]
                    )
                    
                    # Reuse controls from single mode
                    batch_background = gr.Dropdown(
                        choices=[
                            "wooden table", 
                            "marble table", 
                            "office desk", 
                            "dark table",
                            "glass table",
                            "white surface"
                        ],
                        value="wooden table",
                        label="Background Surface"
                    )
                    
                    with gr.Row():
                        batch_steps = gr.Slider(
                            minimum=10, 
                            maximum=50, 
                            value=25, 
                            step=1,
                            label="Inference Steps"
                        )
                        batch_scale = gr.Slider(
                            minimum=1, 
                            maximum=15, 
                            value=7, 
                            step=0.5,
                            label="CFG Scale"
                        )
                    
                    batch_btn = gr.Button(
                        "🚀 Generate Batch", 
                        variant="primary"
                    )
                    
                with gr.Column():
                    batch_gallery = gr.Gallery(
                        label="Generated Images",
                        columns=3,
                        rows=2,
                        height=400
                    )
                    
                    batch_status = gr.Textbox(
                        label="Batch Status",
                        interactive=False,
                        lines=5
                    )
            
            # Wire up batch button
            batch_btn.click(
                fn=batch_generate,
                inputs=[batch_files, batch_background, batch_steps, batch_scale],
                outputs=[batch_gallery, batch_status]
            )
        
        # Instructions Tab
        with gr.TabItem("ℹ️ Instructions"):
            gr.Markdown("""
            ## How to Use
            
            1. **Upload Image**: Upload a clear image of an Aadhaar card
            2. **Select Background**: Choose a surface for the card to rest on
            3. **Adjust Settings**: 
               - **Steps**: Higher = better quality but slower (25-30 recommended)
               - **CFG Scale**: How closely to follow prompt (7-9 recommended)
               - **Seed**: Use same seed for reproducible results
            4. **Generate**: Click generate and wait for results
            
            ## Tips for Best Results
            
            - Use well-lit, clear input images
            - Ensure the card is straight in the input
            - Avoid complex backgrounds in input
            - Start with 25 steps and adjust if needed
            
            ## Notes
            
            - First run will download models (may take a few minutes)
            - CPU mode will be slower than GPU
            - All images are processed locally
            """)
    
    gr.Markdown("---")
    gr.Markdown("Made with ❤️ using Stable Diffusion & Gradio")

# ==========================
# LAUNCH APP
# ==========================
if __name__ == "__main__":
    # Install required packages if missing
    required_packages = ['diffusers', 'transformers', 'accelerate', 'opencv-python']
    
    app.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,        # Default Gradio port
        share=False,              # Set to True for public link
        debug=True                # Show errors in browser
    )