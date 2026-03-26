# AI Aadhaar Realistic Image Generator PRO (FIXED VERSION)
# Includes CPU support + batch fix

import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from PIL import Image
import gradio as gr
import os

# ==========================
# DEVICE SETUP (AUTO CPU/GPU)
# ==========================

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# ==========================
# LOAD MODELS
# ==========================

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    controlnet=controlnet,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

# ==========================
# PROMPT BUILDER
# ==========================

def build_prompt(background):
    return f"""
    hyper realistic aadhaar card on {background} surface,
    laminated plastic card, soft shadow, reflection,
    DSLR photo, ultra high detail, depth of field,
    realistic lighting, slight blur background, camera grain
    """

# ==========================
# SINGLE IMAGE GENERATION
# ==========================

def generate_realistic(image, background, steps, scale):
    prompt = build_prompt(background)

    result = pipe(
        prompt=prompt,
        negative_prompt="blurry, fake text, distorted, low quality, watermark",
        image=image,
        num_inference_steps=int(steps),
        guidance_scale=float(scale)
    ).images[0]

    return result

# ==========================
# BATCH GENERATION (FIXED)
# ==========================

def batch_generate(files, background, steps, scale):
    outputs = []
    os.makedirs("outputs", exist_ok=True)

    for i, file in enumerate(files):
        img = Image.open(file.name)
        result = generate_realistic(img, background, steps, scale)

        path = f"outputs/output_{i}.png"
        result.save(path)
        outputs.append(result)

    return outputs

# ==========================
# UI
# ==========================

with gr.Blocks() as app:
    gr.Markdown("# 🔥 AI Aadhaar Generator PRO (Fixed)")

    with gr.Row():
        input_image = gr.Image(type="pil", label="Upload Card")
        output_image = gr.Image(label="Output")

    background = gr.Dropdown(
        choices=["wooden table", "marble table", "office desk", "dark table"],
        value="wooden table",
        label="Background"
    )

    steps = gr.Slider(10, 50, value=30, label="Steps")
    scale = gr.Slider(1, 15, value=7, label="CFG Scale")

    btn = gr.Button("Generate Image")

    btn.click(
        fn=generate_realistic,
        inputs=[input_image, background, steps, scale],
        outputs=output_image
    )

    gr.Markdown("---")
    gr.Markdown("## Batch Mode")

    batch_input = gr.File(file_count="multiple", label="Upload Multiple Images")
    batch_output = gr.Gallery(label="Outputs")

    batch_btn = gr.Button("Generate Batch")

    batch_btn.click(
        fn=batch_generate,
        inputs=[batch_input, background, steps, scale],
        outputs=batch_output
    )

app.launch()
