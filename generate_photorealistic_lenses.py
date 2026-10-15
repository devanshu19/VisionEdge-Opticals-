import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

output_dir = r"c:\projects\VisionEdge\frontend\assets\images\products"
os.makedirs(output_dir, exist_ok=True)

W, H = 800, 600

def create_studio_background():
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        factor = y / H
        r = int(255 - factor * 12)
        g = int(255 - factor * 10)
        b = int(255 - factor * 6)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    keylight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kl_draw = ImageDraw.Draw(keylight)
    kl_draw.ellipse([W//2 - 350, H//2 - 250, W//2 + 350, H//2 + 250], fill=(255, 255, 255, 130))
    keylight = keylight.filter(ImageFilter.GaussianBlur(75))
    return Image.alpha_composite(img, keylight)

def generate_lns_001():
    # Acuvue Moist Daily Contact Lenses (Box + Blister Packs)
    img = create_studio_background()
    
    # Shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.ellipse([180, 420, 620, 480], fill=(15, 23, 42, 45))
    sh = sh.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, sh)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)

    # 3D Packaging Box
    # Main Box Front
    box_rect = [200, 180, 440, 410]
    draw.rounded_rectangle(box_rect, radius=12, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    
    # Top Header Banner
    draw.rounded_rectangle([200, 180, 440, 250], radius=12, fill=(2, 132, 199, 255))
    draw.rectangle([200, 230, 440, 250], fill=(2, 132, 199, 255))
    
    # Brand Text simulation
    draw.rectangle([220, 200, 360, 218], fill=(255, 255, 255, 255))
    draw.text((230, 202), "ACUVUE MOIST", fill=(2, 132, 199, 255))
    draw.text((220, 270), "DAILY DISPOSABLE 30 PACK", fill=(71, 85, 105, 255))
    draw.text((220, 295), "1-DAY CONTACT LENS", fill=(2, 132, 199, 255))

    # Blister Packs next to box
    for i, (bx, by) in enumerate([(480, 210), (480, 290), (480, 370)]):
        draw.rounded_rectangle([bx, by, bx + 140, by + 65], radius=10, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=2)
        # Foil Cap
        draw.rounded_rectangle([bx + 5, by + 5, bx + 135, by + 25], radius=6, fill=(2, 132, 199, 255))
        # Lens Cup
        draw.ellipse([bx + 45, by + 28, bx + 95, by + 60], fill=(56, 189, 248, 120), outline=(2, 132, 199, 255), width=2)

    # Glare overlay
    glare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.polygon([(210, 190), (280, 190), (230, 400), (190, 400)], fill=(255, 255, 255, 60))
    img = Image.alpha_composite(img, fg)
    img = Image.alpha_composite(img, glare)
    img.convert("RGB").save(os.path.join(output_dir, "real_21.jpg"), "JPEG", quality=95)
    print("Generated real_21.jpg (Acuvue Daily Contact Lenses)")

def generate_lns_002():
    # FreshLook ColorEnhance Hazel Contact Lens (Hazel Color Iris Studio Photo)
    img = create_studio_background()

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.ellipse([220, 410, 580, 470], fill=(15, 23, 42, 45))
    sh = sh.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, sh)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)

    # Soft Contact Lens Cup / Curved Gel Shape
    cx, cy = 400, 290
    r_outer = 130
    r_iris = 90
    r_pupil = 35

    # Lens Outer Curved Edge
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(209, 250, 229, 140), outline=(16, 185, 129, 255), width=3)
    
    # Hazel Iris Ring Gradient
    draw.ellipse([cx - r_iris, cy - r_iris, cx + r_iris, cy + r_iris], fill=(217, 119, 6, 200), outline=(180, 83, 9, 255), width=4)
    # Inner Amber Spoke Pattern
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        x1 = cx + int(r_pupil * math.cos(rad))
        y1 = cy + int(r_pupil * math.sin(rad))
        x2 = cx + int(r_iris * math.cos(rad))
        y2 = cy + int(r_iris * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(251, 191, 36, 160), width=3)

    # Pupil Center
    draw.ellipse([cx - r_pupil, cy - r_pupil, cx + r_pupil, cy + r_pupil], fill=(15, 23, 42, 240))

    # Water Drop / Saline Reflection Caustic
    glare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.ellipse([cx - 70, cy - 80, cx - 20, cy - 40], fill=(255, 255, 255, 180))
    g_draw.ellipse([cx + 30, cy + 30, cx + 50, cy + 50], fill=(255, 255, 255, 120))
    glare = glare.filter(ImageFilter.GaussianBlur(4))

    img = Image.alpha_composite(img, fg)
    img = Image.alpha_composite(img, glare)
    img.convert("RGB").save(os.path.join(output_dir, "real_22.jpg"), "JPEG", quality=95)
    print("Generated real_22.jpg (FreshLook Color Contact Lens)")

def generate_lns_003():
    # UltraClear HD Progressive Precision Lens (Optical Glass Lens Disk with AR Coating)
    img = create_studio_background()

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.ellipse([200, 420, 600, 480], fill=(15, 23, 42, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, sh)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)

    cx, cy = 400, 280
    r_lens = 145

    # Glass Lens Edge Bevel
    draw.ellipse([cx - r_lens, cy - r_lens, cx + r_lens, cy + r_lens], fill=(241, 245, 249, 160), outline=(148, 163, 184, 255), width=6)
    
    # Sapphire AR Blue Anti-Reflective Coating Reflection
    ar_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ar_draw = ImageDraw.Draw(ar_layer)
    ar_draw.ellipse([cx - r_lens + 10, cy - r_lens + 10, cx + r_lens - 10, cy + r_lens - 10], fill=(124, 58, 237, 70))
    ar_draw.polygon([(cx - 120, cy - 100), (cx + 80, cy - 100), (cx + 120, cy + 100), (cx - 80, cy + 100)], fill=(56, 189, 248, 90))
    ar_layer = ar_layer.filter(ImageFilter.GaussianBlur(8))

    # Specular Reflection Highlight
    glare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.ellipse([cx - 100, cy - 110, cx - 20, cy - 60], fill=(255, 255, 255, 210))
    glare = glare.filter(ImageFilter.GaussianBlur(4))

    img = Image.alpha_composite(img, fg)
    img = Image.alpha_composite(img, ar_layer)
    img = Image.alpha_composite(img, glare)
    img.convert("RGB").save(os.path.join(output_dir, "real_23.jpg"), "JPEG", quality=95)
    print("Generated real_23.jpg (UltraClear HD Progressive Lens)")

def generate_lns_004():
    # Biofinity Toric Astigmatism Monthly Lenses
    img = create_studio_background()

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.ellipse([180, 420, 620, 480], fill=(15, 23, 42, 45))
    sh = sh.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, sh)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)

    # Box Packaging (Teal / Cyan theme)
    box_rect = [180, 190, 460, 410]
    draw.rounded_rectangle(box_rect, radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=2)
    draw.rounded_rectangle([180, 190, 460, 260], radius=12, fill=(8, 145, 178, 255))
    draw.rectangle([180, 240, 460, 260], fill=(8, 145, 178, 255))

    draw.text((210, 210), "BIOFINITY TORIC", fill=(255, 255, 255, 255))
    draw.text((210, 280), "Comfilcon A Monthly Lenses", fill=(71, 85, 105, 255))
    draw.text((210, 305), "FOR ASTIGMATISM • 6 LENSES", fill=(8, 145, 178, 255))

    # Soft Contact Lens resting in front
    cx, cy = 540, 330
    draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(165, 243, 252, 180), outline=(8, 145, 178, 255), width=3)
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(207, 250, 254, 150))

    glare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.polygon([(190, 200), (250, 200), (210, 400), (180, 400)], fill=(255, 255, 255, 65))
    g_draw.ellipse([cx - 40, cy - 50, cx - 10, cy - 20], fill=(255, 255, 255, 190))
    glare = glare.filter(ImageFilter.GaussianBlur(3))

    img = Image.alpha_composite(img, fg)
    img = Image.alpha_composite(img, glare)
    img.convert("RGB").save(os.path.join(output_dir, "real_24.jpg"), "JPEG", quality=95)
    print("Generated real_24.jpg (Biofinity Toric Contact Lens)")

def generate_lns_005():
    # Transitions Gen8 Photochromic Smart Lens (Transitional Clear-to-Graphite Smart Lens)
    img = create_studio_background()

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.ellipse([200, 420, 600, 480], fill=(15, 23, 42, 45))
    sh = sh.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, sh)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)

    cx, cy = 400, 280
    r_lens = 145

    # Smart Photochromic Lens Disk (Half Clear, Half Tinted Transition Gradient)
    draw.ellipse([cx - r_lens, cy - r_lens, cx + r_lens, cy + r_lens], fill=(71, 85, 105, 180), outline=(51, 65, 85, 255), width=6)
    
    # UV Light beam transition gradient effect
    uv_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    uv_draw = ImageDraw.Draw(uv_layer)
    uv_draw.ellipse([cx - r_lens + 6, cy - r_lens + 6, cx, cy + r_lens - 6], fill=(241, 245, 249, 140))
    uv_layer = uv_layer.filter(ImageFilter.GaussianBlur(6))

    glare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.ellipse([cx - 100, cy - 110, cx - 20, cy - 60], fill=(255, 255, 255, 220))
    g_draw.polygon([(cx - 80, cy - 120), (cx + 80, cy - 120), (cx + 120, cy + 120), (cx - 40, cy + 120)], fill=(255, 255, 255, 40))
    glare = glare.filter(ImageFilter.GaussianBlur(4))

    img = Image.alpha_composite(img, fg)
    img = Image.alpha_composite(img, uv_layer)
    img = Image.alpha_composite(img, glare)
    img.convert("RGB").save(os.path.join(output_dir, "real_25.jpg"), "JPEG", quality=95)
    print("Generated real_25.jpg (Transitions Gen8 Photochromic Lens)")

generate_lns_001()
generate_lns_002()
generate_lns_003()
generate_lns_004()
generate_lns_005()
