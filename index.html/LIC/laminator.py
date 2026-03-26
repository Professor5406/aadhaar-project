import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import os

class LaminatedCardGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Laminated Card Generator")
        self.root.geometry("500x300")
        self.root.configure(bg='#2b2b2b')
        
        # Style
        title = tk.Label(root, text="📇 Aadhaar Lamination Studio", 
                        font=("Arial", 18, "bold"), 
                        bg='#2b2b2b', fg='#e6d5b8')
        title.pack(pady=20)
        
        desc = tk.Label(root, 
                       text="Convert your digital Aadhaar into realistic laminated card photos\n"
                            "Perfect for KYC verification", 
                       font=("Arial", 10), 
                       bg='#2b2b2b', fg='#b9aa99')
        desc.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(root, bg='#2b2b2b')
        btn_frame.pack(pady=20)
        
        self.select_btn = tk.Button(btn_frame, 
                                   text="📂 Select Aadhaar Images", 
                                   command=self.select_images,
                                   font=("Arial", 12),
                                   bg='#4a5b6b', fg='white',
                                   padx=20, pady=10,
                                   cursor='hand2')
        self.select_btn.pack(side=tk.LEFT, padx=10)
        
        self.quit_btn = tk.Button(btn_frame,
                                 text="❌ Exit",
                                 command=root.quit,
                                 font=("Arial", 12),
                                 bg='#6b4a4a', fg='white',
                                 padx=20, pady=10,
                                 cursor='hand2')
        self.quit_btn.pack(side=tk.LEFT, padx=10)
        
        # Status
        self.status = tk.Label(root, 
                              text="Ready", 
                              font=("Arial", 9),
                              bg='#2b2b2b', fg='#8f8476')
        self.status.pack(pady=10)
        
    def create_laminated(self, image_path, index, total):
        try:
            # Update status
            filename = os.path.basename(image_path)
            self.status.config(text=f"Processing {index+1}/{total}: {filename}")
            self.root.update()
            
            # Open image
            card = Image.open(image_path).convert("RGBA")
            
            # Maintain aspect ratio (Aadhaar is ~1.58:1)
            target_width = 800
            aspect = card.height / card.width
            target_height = int(target_width * aspect)
            card = card.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            w, h = card.size
            
            # Create larger canvas with wooden texture background
            bg_width = w + 200
            bg_height = h + 200
            
            # Create wooden background
            bg = Image.new("RGBA", (bg_width, bg_height), (90, 70, 50, 255))
            
            # Add wood grain texture
            texture = Image.new("RGBA", (bg_width, bg_height), (0,0,0,0))
            draw_texture = ImageDraw.Draw(texture)
            for i in range(0, bg_width, 5):
                draw_texture.line([(i, 0), (i, bg_height)], 
                                 fill=(60, 45, 30, 30), width=1)
            bg = Image.alpha_composite(bg.convert("RGBA"), texture)
            
            # Create realistic shadow (offset, blurred)
            shadow = Image.new("RGBA", (w+60, h+60), (0,0,0,0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.rounded_rectangle(
                [30, 30, w+30, h+30],
                radius=20,
                fill=(0,0,0,180)
            )
            shadow = shadow.filter(ImageFilter.GaussianBlur(15))
            
            # Paste shadow on background (offset slightly)
            shadow_x = 70
            shadow_y = 70
            bg.paste(shadow, (shadow_x, shadow_y), shadow)
            
            # Create card with rounded corners
            card_with_corners = Image.new("RGBA", (w, h), (0,0,0,0))
            card_draw = ImageDraw.Draw(card_with_corners)
            card_draw.rounded_rectangle([0, 0, w, h], radius=30, fill=(255,255,255,255))
            card = Image.composite(card, card_with_corners, card_with_corners)
            
            # Paste card on background
            card_x = 100
            card_y = 100
            bg.paste(card, (card_x, card_y), card)
            
            # Add laminate shine (gradient overlay)
            shine = Image.new("RGBA", bg.size, (255,255,255,0))
            shine_draw = ImageDraw.Draw(shine)
            
            # Top-left to bottom-right shine
            for i in range(0, 100, 2):
                opacity = int(50 * (1 - i/100))
                shine_draw.polygon([
                    (card_x - 20 + i, card_y - 20),
                    (card_x + w//2, card_y - 20),
                    (card_x + w//4, card_y + h + 20),
                    (card_x - 20, card_y + h + 20 - i)
                ], fill=(255, 255, 255, opacity))
            
            shine = shine.filter(ImageFilter.GaussianBlur(15))
            bg = Image.alpha_composite(bg, shine)
            
            # Add edge highlight (white border effect)
            edge_draw = ImageDraw.Draw(bg)
            edge_draw.rounded_rectangle(
                [card_x-2, card_y-2, card_x+w+2, card_y+h+2],
                radius=32,
                outline=(255,255,255,150),
                width=3
            )
            
            # Add subtle emboss effect
            emboss = Image.new("RGBA", bg.size, (0,0,0,0))
            emboss_draw = ImageDraw.Draw(emboss)
            emboss_draw.rounded_rectangle(
                [card_x, card_y, card_x+w, card_y+h],
                radius=30,
                outline=(255,255,240,40),
                width=2
            )
            bg = Image.alpha_composite(bg, emboss)
            
            # Add micro-texture (paper grain) as a subtle white overlay
            grain = Image.effect_noise(bg.size, 64).convert("L")
            grain = ImageEnhance.Brightness(grain).enhance(0.12)
            overlay = Image.new("RGBA", bg.size, (255, 255, 255, 0))
            overlay.putalpha(grain)
            bg = Image.alpha_composite(bg, overlay)
            
            # Save
            output_dir = os.path.join(os.path.dirname(image_path), "laminated_output")
            os.makedirs(output_dir, exist_ok=True)
            
            output_name = f"laminated_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_dir, output_name)
            bg.save(output_path, "PNG")
            
            return output_path
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select Aadhaar Images (Front/Back)",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not files:
            return
        
        self.progress['maximum'] = len(files)
        results = []
        
        for i, file in enumerate(files):
            self.progress['value'] = i + 1
            output = self.create_laminated(file, i, len(files))
            if output:
                results.append(output)
            self.root.update()
        
        if results:
            messagebox.showinfo(
                "Success!", 
                f"✅ Created {len(results)} laminated cards!\n\n"
                f"Saved in: {os.path.dirname(results[0])}"
            )
            self.status.config(text=f"Completed! {len(results)} files processed")
            
            # Open output folder
            os.startfile(os.path.dirname(results[0]))
        else:
            messagebox.showerror("Error", "Failed to process images")
            self.status.config(text="Error occurred")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LaminatedCardGenerator(root)
    root.mainloop()