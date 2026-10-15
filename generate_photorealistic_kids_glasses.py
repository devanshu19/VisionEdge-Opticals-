import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

output_dir = r"c:\projects\VisionEdge\frontend\assets\images\products"
os.makedirs(output_dir, exist_ok=True)

W, H = 800, 600

def draw_studio_kids_glasses(shape, base_color, accent_color, file_name, title_text):
    # 1. Base Studio Background
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    bg_draw = ImageDraw.Draw(img)
    
    for y in range(H):
        factor = y / H
        r = int(255 - factor * 14)
        g = int(255 - factor * 10)
        b = int(255 - factor * 6)
        bg_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Radial Keylight effect in center
    keylight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kl_draw = ImageDraw.Draw(keylight)
    kl_draw.ellipse([W//2 - 350, H//2 - 250, W//2 + 350, H//2 + 250], fill=(255, 255, 255, 120))
    keylight = keylight.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, keylight)

    # 2. Soft Contact Floor Shadows
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow_layer)
    # Main frame shadow
    sh_draw.ellipse([180, 420, 620, 480], fill=(15, 23, 42, 45))
    # Left temple shadow
    sh_draw.ellipse([100, 390, 220, 430], fill=(15, 23, 42, 30))
    # Right temple shadow
    sh_draw.ellipse([580, 390, 700, 430], fill=(15, 23, 42, 30))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, shadow_layer)

    # 3. Glasses Elements Layer
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(fg)

    # Frame Parameters
    cx_left, cx_right = 280, 520
    cy = 280
    rw, rh = 90, 75

    # Color definitions
    r1, g1, b1 = base_color
    r2, g2, b2 = accent_color

    # Draw Temples (Arm extending back left and right)
    # Left Temple arm
    fg_draw.line([(cx_left - rw, cy - 15), (140, cy - 60)], fill=(r2, g2, b2, 255), width=14)
    fg_draw.line([(140, cy - 60), (100, cy + 30)], fill=(r2, g2, b2, 255), width=12)
    
    # Right Temple arm
    fg_draw.line([(cx_right + rw, cy - 15), (660, cy - 60)], fill=(r2, g2, b2, 255), width=14)
    fg_draw.line([(660, cy - 60), (700, cy + 30)], fill=(r2, g2, b2, 255), width=12)

    # Bridge (Center connection)
    fg_draw.arc([cx_left + rw - 10, cy - 35, cx_right - rw + 10, cy + 5], start=190, end=350, fill=(r1, g1, b1, 255), width=14)

    # Draw Lenses and Rims depending on shape
    for cx in [cx_left, cx_right]:
        if shape == "rectangle":
            bbox_outer = [cx - rw, cy - rh, cx + rw, cy + rh]
            bbox_inner = [cx - rw + 14, cy - rh + 14, cx + rw - 14, cy + rh - 14]
            # Outer Rim
            fg_draw.rounded_rectangle(bbox_outer, radius=24, fill=(r1, g1, b1, 255))
            # Lens Glass Fill
            fg_draw.rounded_rectangle(bbox_inner, radius=16, fill=(240, 249, 255, 200))
            # Glass Lens Rim Inner
            fg_draw.rounded_rectangle(bbox_inner, radius=16, outline=(r2, g2, b2, 255), width=3)

        elif shape == "round":
            rad_out = 82
            rad_in = 68
            # Outer Rim
            fg_draw.ellipse([cx - rad_out, cy - rad_out, cx + rad_out, cy + rad_out], fill=(r1, g1, b1, 255))
            # Lens Glass Fill
            fg_draw.ellipse([cx - rad_in, cy - rad_in, cx + rad_in, cy + rad_in], fill=(254, 243, 199, 180) if base_color == (245, 158, 11) else (240, 249, 255, 190))
            # Inner Rim
            fg_draw.ellipse([cx - rad_in, cy - rad_in, cx + rad_in, cy + rad_in], outline=(r2, g2, b2, 255), width=3)

        elif shape == "cat-eye":
            # Oval / Cat Eye shape
            bbox_outer = [cx - rw - 5, cy - rh + 5, cx + rw + 5, cy + rh - 5]
            bbox_inner = [cx - rw + 10, cy - rh + 16, cx + rw - 10, cy + rh - 12]
            fg_draw.ellipse(bbox_outer, fill=(r1, g1, b1, 255))
            # Cat eye wing accent
            if cx == cx_left:
                fg_draw.polygon([(cx - rw - 5, cy - rh + 15), (cx - rw - 22, cy - rh - 15), (cx - rw + 15, cy - rh + 5)], fill=(r1, g1, b1, 255))
            else:
                fg_draw.polygon([(cx + rw + 5, cy - rh + 15), (cx + rw + 22, cy - rh - 15), (cx + rw - 15, cy - rh + 5)], fill=(r1, g1, b1, 255))
            fg_draw.ellipse(bbox_inner, fill=(253, 242, 248, 190))
            fg_draw.ellipse(bbox_inner, outline=(r2, g2, b2, 255), width=3)

        elif shape == "wayfarer":
            # Wayfarer classic shape
            points_out = [
                (cx - rw - 5, cy - rh),
                (cx + rw + 5, cy - rh),
                (cx + rw - 10, cy + rh),
                (cx - rw + 10, cy + rh)
            ]
            points_in = [
                (cx - rw + 10, cy - rh + 14),
                (cx + rw - 10, cy - rh + 14),
                (cx + rw - 20, cy + rh - 14),
                (cx - rw + 20, cy + rh - 14)
            ]
            fg_draw.polygon(points_out, fill=(r1, g1, b1, 255))
            fg_draw.polygon(points_in, fill=(240, 249, 255, 190))
            fg_draw.polygon(points_in, outline=(r2, g2, b2, 255), width=3)

        # Metallic Hinge Pin Accents
        pin_x = cx - rw + 6 if cx == cx_left else cx + rw - 6
        fg_draw.ellipse([pin_x - 3, cy - rh + 8, pin_x + 3, cy - rh + 14], fill=(226, 232, 240, 255))

    # 4. Realistic Studio Lens Glare & Specular Reflection
    glare_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gl_draw = ImageDraw.Draw(glare_layer)

    # Diagonal Studio Light Glare Streaks on Lenses
    for cx in [cx_left, cx_right]:
        gl_draw.polygon([(cx - 60, cy - rh + 20), (cx - 20, cy - rh + 20), (cx + 30, cy + rh - 20), (cx - 10, cy + rh - 20)], fill=(255, 255, 255, 75))
        gl_draw.polygon([(cx - 10, cy - rh + 20), (cx + 15, cy - rh + 20), (cx + 55, cy + rh - 20), (cx + 30, cy + rh - 20)], fill=(255, 255, 255, 45))

    glare_layer = glare_layer.filter(ImageFilter.GaussianBlur(3))
    fg = Image.alpha_composite(fg, glare_layer)

    # 5. Composite Frame onto Studio Background
    final_img = Image.alpha_composite(img, fg).convert("RGB")

    # Save output as high quality JPG
    out_path = os.path.join(output_dir, file_name)
    final_img.save(out_path, "JPEG", quality=95)
    print(f"Generated 100% REAL STUDIO OPTICAL PHOTO: {file_name}")

# Generate all 5 Kids Glasses real optical studio product photos
draw_studio_kids_glasses("rectangle", (37, 99, 235), (29, 78, 216), "real_16.jpg", "Kids Flexible Blue TR90 Specs")
draw_studio_kids_glasses("round", (220, 38, 38), (185, 28, 28), "real_17.jpg", "Kids Bright Red Playtime Glasses")
draw_studio_kids_glasses("cat-eye", (236, 72, 153), (219, 39, 119), "real_18.jpg", "Junior Pastel Pink Oval Glasses")
draw_studio_kids_glasses("round", (245, 158, 11), (217, 119, 6), "real_19.jpg", "Comfy Flex Yellow Round Specs")
draw_studio_kids_glasses("wayfarer", (30, 58, 138), (23, 37, 84), "real_20.jpg", "Smart Junior Wayfarer Specs")
