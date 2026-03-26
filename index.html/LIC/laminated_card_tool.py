import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageOps
import os
import random
import math

class LaminatedCardGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("PVC Aadhaar Card Studio - Real Table Background")
        self.root.geometry("600x400")
        self.root.configure(bg='#8B5A2B')  # Wooden theme
        
        # Make window non-resizable
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Style
        title_frame = tk.Frame(root, bg='#8B5A2B')
        title_frame.pack(pady=20)
        
        title = tk.Label(root, text="🪵 Realistic Table Background Aadhaar Cards", 
                        font=("Arial", 18, "bold"), 
                        bg='#8B5A2B', fg='#F5DEB3')
        title.pack()
        
        subtitle = tk.Label(root, 
                           text="Place your laminated Aadhaar cards on realistic wooden table surfaces\n"
                                "with natural lighting, shadows, and depth", 
                           font=("Arial", 10), 
                           bg='#8B5A2B', fg='#E6D5B8')
        subtitle.pack(pady=10)
        
        # Background options
        options_frame = tk.Frame(root, bg='#8B5A2B')
        options_frame.pack(pady=10)
        
        tk.Label(options_frame, text="Table Type:", bg='#8B5A2B', fg='#F5DEB3', 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.table_type = tk.StringVar(value="oak")
        table_options = ttk.Combobox(options_frame, textvariable=self.table_type, 
                                     values=["oak", "walnut", "pine", "mahogany", "vintage"],
                                     state="readonly", width=15)
        table_options.pack(side=tk.LEFT, padx=5)
        
        tk.Label(options_frame, text="Lighting:", bg='#8B5A2B', fg='#F5DEB3',
                font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.lighting = tk.StringVar(value="warm")
        lighting_options = ttk.Combobox(options_frame, textvariable=self.lighting,
                                       values=["warm", "cool", "natural", "studio"],
                                       state="readonly", width=10)
        lighting_options.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=15)
        
        # Buttons
        btn_frame = tk.Frame(root, bg='#8B5A2B')
        btn_frame.pack(pady=15)
        
        self.select_btn = tk.Button(btn_frame, 
                                   text="📸 Generate Cards on Table", 
                                   command=self.select_images,
                                   font=("Arial", 11, "bold"),
                                   bg='#C19A6B', fg='#2C1810',
                                   padx=25, pady=12,
                                   cursor='hand2',
                                   relief=tk.RAISED, bd=3)
        self.select_btn.pack(side=tk.LEFT, padx=10)
        
        self.quit_btn = tk.Button(btn_frame,
                                 text="❌ Exit",
                                 command=root.quit,
                                 font=("Arial", 11),
                                 bg='#B22222', fg='white',
                                 padx=25, pady=12,
                                 cursor='hand2',
                                 relief=tk.RAISED, bd=3)
        self.quit_btn.pack(side=tk.LEFT, padx=10)
        
        # Status
        self.status = tk.Label(root, 
                              text="Ready to create realistic table background cards", 
                              font=("Arial", 10),
                              bg='#8B5A2B', fg='#F5DEB3')
        self.status.pack(pady=10)
        
        # Counter label
        self.counter_label = tk.Label(root, 
                                     text="", 
                                     font=("Arial", 9, "italic"),
                                     bg='#8B5A2B', fg='#FFD700')
        self.counter_label.pack()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_realistic_wood_texture(self, size, wood_type="oak"):
        """Create ultra-realistic wood texture with grain patterns"""
        texture = Image.new("RGBA", size, (0,0,0,0))
        draw = ImageDraw.Draw(texture)
        w, h = size
        
        # Base wood colors based on type
        wood_colors = {
            "oak": [(205, 170, 125), (185, 150, 105), (165, 130, 85)],
            "walnut": [(101, 67, 33), (81, 47, 13), (61, 27, 0)],
            "pine": [(255, 215, 175), (235, 195, 155), (215, 175, 135)],
            "mahogany": [(150, 75, 50), (130, 55, 30), (110, 35, 10)],
            "vintage": [(139, 90, 43), (119, 70, 23), (99, 50, 10)]
        }
        
        colors = wood_colors.get(wood_type, wood_colors["oak"])
        
        # Create base gradient (darker at edges)
        for y in range(h):
            # Edge darkening
            edge_factor = 1 - (min(y, h-y) / (h/2)) * 0.3
            for x in range(w):
                # Wood grain lines
                grain = random.randint(-20, 20)
                color_idx = 0
                
                # Create wood grain pattern
                if random.random() > 0.95:  # Dark grain lines
                    color_idx = 2
                elif random.random() > 0.8:  # Medium grain
                    color_idx = 1
                else:  # Base color
                    color_idx = 0
                
                # Apply grain variation
                r = int(colors[color_idx][0] * edge_factor + grain)
                g = int(colors[color_idx][1] * edge_factor + grain)
                b = int(colors[color_idx][2] * edge_factor + grain)
                
                # Add knots occasionally
                if random.random() > 0.995:
                    r, g, b = 80, 40, 10
                
                draw.point((x, y), fill=(r, g, b, 255))
        
        # Add wood grain lines
        for _ in range(h // 3):
            y = random.randint(0, h)
            # Wavy grain lines
            points = []
            for x in range(0, w, 10):
                offset = random.randint(-3, 3)
                points.append((x, y + offset))
            if len(points) > 1:
                draw.line(points, fill=(60, 40, 20, 80), width=1)
        
        # Add knots
        for _ in range(3):
            knot_x = random.randint(w//4, 3*w//4)
            knot_y = random.randint(h//4, 3*h//4)
            draw.ellipse([knot_x-15, knot_y-10, knot_x+15, knot_y+10], 
                        fill=(80, 40, 10, 200))
            # Knot rings
            for r in range(5, 20, 5):
                draw.ellipse([knot_x-r, knot_y-r, knot_x+r, knot_y+r], 
                            outline=(40, 20, 0, 150), width=1)
        
        return texture
    
    def create_lighting_effects(self, image, lighting_type="warm"):
        """Add realistic lighting effects"""
        w, h = image.size
        lighting = Image.new("RGBA", image.size, (0,0,0,0))
        draw = ImageDraw.Draw(lighting)
        
        if lighting_type == "warm":
            # Warm amber light from top-left
            for i in range(h):
                opacity = int(30 * (1 - i/h))
                draw.rectangle([0, i, w, i+1], fill=(255, 200, 150, opacity))
        
        elif lighting_type == "cool":
            # Cool blue light from top-right
            for i in range(h):
                opacity = int(25 * (1 - i/h))
                draw.rectangle([0, i, w, i+1], fill=(200, 220, 255, opacity))
        
        elif lighting_type == "natural":
            # Natural daylight (even lighting)
            gradient = Image.new("RGBA", image.size, (255, 255, 230, 15))
            lighting = gradient
        
        elif lighting_type == "studio":
            # Studio lighting (spotlight effect)
            center_x, center_y = w//2, h//4
            for y in range(h):
                for x in range(w):
                    distance = math.sqrt((x-center_x)**2 + (y-center_y)**2)
                    opacity = max(0, 40 - int(distance / 20))
                    if opacity > 0:
                        draw.point((x, y), fill=(255, 255, 255, opacity))
        
        return Image.alpha_composite(image, lighting)
    
    def create_surface_reflection(self, image, card_region):
        """Create realistic surface reflection around card"""
        w, h = image.size
        reflection = Image.new("RGBA", image.size, (0,0,0,0))
        draw = ImageDraw.Draw(reflection)
        
        # Add subtle glossy reflection around card edges
        x, y, x2, y2 = card_region
        padding = 20
        
        # Soft glow around card
        for i in range(padding):
            opacity = 15 - i
            if opacity > 0:
                # Top edge
                draw.rectangle([x-i, y-i, x2+i, y-i+1], fill=(255,255,255,opacity))
                # Bottom edge
                draw.rectangle([x-i, y2+i-1, x2+i, y2+i], fill=(255,255,255,opacity))
                # Left edge
                draw.rectangle([x-i, y-i, x-i+1, y2+i], fill=(255,255,255,opacity))
                # Right edge
                draw.rectangle([x2+i-1, y-i, x2+i, y2+i], fill=(255,255,255,opacity))
        
        return Image.alpha_composite(image, reflection)
    
    def create_card_shadow(self, image, card_region, shadow_intensity=80):
        """Create realistic drop shadow for card"""
        w, h = image.size
        x, y, x2, y2 = card_region
        card_w = x2 - x
        card_h = y2 - y
        
        # Create shadow layer
        shadow = Image.new("RGBA", image.size, (0,0,0,0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw soft shadow
        for offset in range(10, 0, -1):
            opacity = shadow_intensity - offset * 8
            if opacity > 0:
                shadow_draw.rounded_rectangle(
                    [x+offset+5, y+offset+5, x2+offset+5, y2+offset+5],
                    radius=30,
                    fill=(0, 0, 0, opacity)
                )
        
        # Blur shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        
        return Image.alpha_composite(image, shadow)
    
    def create_table_background_card(self, image_path, index, total):
        """Create card with realistic wooden table background"""
        try:
            # Update status
            filename = os.path.basename(image_path)
            self.status.config(text=f"Processing {index+1}/{total}: Creating realistic table scene...")
            self.counter_label.config(text=f"Card {index+1} of {total}")
            self.root.update()
            
            # Open main card image
            card = Image.open(image_path).convert("RGBA")
            
            # Standard card size (maintain aspect ratio)
            target_width = 600
            aspect = card.height / card.width
            target_height = int(target_width * aspect)
            card = card.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Create rounded corners for card
            card_with_corners = Image.new("RGBA", card.size, (0,0,0,0))
            card_draw = ImageDraw.Draw(card_with_corners)
            card_draw.rounded_rectangle([0, 0, card.width, card.height], 
                                        radius=20, fill=(255,255,255,255))
            card = Image.composite(card, card_with_corners, card_with_corners)
            
            # Add laminate effect to card
            laminate = Image.new("RGBA", card.size, (255,255,255,30))
            card = Image.alpha_composite(card, laminate)
            
            # Create larger canvas for table background
            bg_width = 1200
            bg_height = 900
            
            # Create realistic wood table
            table = self.create_realistic_wood_texture((bg_width, bg_height), 
                                                       self.table_type.get())
            
            # Position card on table (slightly angled for realism)
            card_x = bg_width//2 - card.width//2
            card_y = bg_height//2 - card.height//2
            
            # Add slight rotation for natural look
            card = card.rotate(random.uniform(-0.5, 0.5), expand=True, 
                              fillcolor=(0,0,0,0))
            
            # Calculate card region for shadows
            card_region = (card_x, card_y, card_x + card.width, card_y + card.height)
            
            # Add shadow first
            table_with_shadow = self.create_card_shadow(table, card_region, 60)
            
            # Place card on table
            table_with_shadow.paste(card, (card_x, card_y), card)
            
            # Add surface reflections
            final_image = self.create_surface_reflection(table_with_shadow, card_region)
            
            # Add lighting effects
            final_image = self.create_lighting_effects(final_image, self.lighting.get())
            
            # Add depth with subtle vignette
            vignette = Image.new("RGBA", final_image.size, (0,0,0,0))
            v_draw = ImageDraw.Draw(vignette)
            for i in range(100, 0, -1):
                opacity = 1
                v_draw.rectangle([i, i, bg_width-i, bg_height-i], 
                                outline=(0,0,0,opacity))
            final_image = Image.alpha_composite(final_image, vignette)
            
            # Add some paper/photos on table for realism
            if random.random() > 0.7:
                # Add another card slightly visible in background
                second_card = card.copy()
                second_card = second_card.resize(
                    (int(card.width*0.3), int(card.height*0.3)), 
                    Image.Resampling.LANCZOS)
                second_card = second_card.rotate(15, expand=True, fillcolor=(0,0,0,0))
                
                # Make it semi-transparent and place in corner
                second_card.putalpha(100)
                final_image.paste(second_card, (50, 600), second_card)
            
            # Save with high quality
            output_dir = os.path.join(os.path.dirname(image_path), "Table_Background_Cards")
            os.makedirs(output_dir, exist_ok=True)
            
            # Get selected options for filename
            table_type = self.table_type.get()
            lighting = self.lighting.get()
            
            output_name = f"Table_{table_type}_{lighting}_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_dir, output_name)
            final_image.save(output_path, "PNG", optimize=True, quality=95)
            
            return output_path
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select Aadhaar Images for Table Background",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if not files:
            return
        
        # Show selected options
        response = messagebox.askyesno(
            "Confirm Generation",
            f"Generate {len(files)} card(s) with:\n\n"
            f"Table Type: {self.table_type.get().title()}\n"
            f"Lighting: {self.lighting.get().title()}\n\n"
            f"Features:\n"
            f"✓ Realistic wood grain texture\n"
            f"✓ Natural lighting effects\n"
            f"✓ Soft drop shadows\n"
            f"✓ Surface reflections\n"
            f"✓ Depth and vignette\n"
            f"✓ Random background elements"
        )
        
        if not response:
            return
        
        # Disable button during processing
        self.select_btn.config(state='disabled')
        
        self.progress['maximum'] = len(files)
        self.progress['value'] = 0
        results = []
        
        for i, file in enumerate(files):
            self.progress['value'] = i + 1
            output = self.create_table_background_card(file, i, len(files))
            if output:
                results.append(output)
            self.root.update()
        
        # Re-enable button
        self.select_btn.config(state='normal')
        
        if results:
            messagebox.showinfo(
                "Cards Generated Successfully!", 
                f"✅ Created {len(results)} cards with realistic table backgrounds!\n\n"
                f"Table Type: {self.table_type.get().title()}\n"
                f"Lighting: {self.lighting.get().title()}\n\n"
                f"Saved in: {os.path.dirname(results[0])}"
            )
            self.status.config(text=f"Completed! {len(results)} table background cards")
            self.counter_label.config(text="")
            
            # Open output folder
            try:
                os.startfile(os.path.dirname(results[0]))
            except:
                pass
        else:
            messagebox.showerror("Error", "Failed to generate cards")
            self.status.config(text="Error occurred")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LaminatedCardGenerator(root)
    root.mainloop()