import math, os
from PIL import Image, ImageDraw, ImageFilter

output_dir = r"c:\projects\VisionEdge\frontend\assets\images\products"
os.makedirs(output_dir, exist_ok=True)

W, H = 800, 600

def generate_eye_004():
    # Base Studio Background
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    bg_draw = ImageDraw.Draw(img)
    for y in range(H):
        factor = y / H
        r = int(255 - factor * 14)
        g = int(255 - factor * 10)
        b = int(255 - factor * 6)
        bg_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    keylight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kl_draw = ImageDraw.Draw(keylight)
    kl_draw.ellipse([W//2 - 350, H//2 - 250, W//2 + 350, H//2 + 250], fill=(255, 255, 255, 130))
    keylight = keylight.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, keylight)

    # Floor Shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.ellipse([180, 420, 620, 480], fill=(15, 23, 42, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, sh)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fg)

    cx_left, cx_right = 280, 520
    cy = 280
    rw, rh = 95, 70

    # Temples (Transparent Clear Acetate with Silver Wire Core inside)
    # Wire Core
    draw.line([(cx_left - rw, cy - 15), (140, cy - 60)], fill=(148, 163, 184, 255), width=6)
    draw.line([(140, cy - 60), (100, cy + 30)], fill=(148, 163, 184, 255), width=5)
    draw.line([(cx_right + rw, cy - 15), (660, cy - 60)], fill=(148, 163, 184, 255), width=6)
    draw.line([(660, cy - 60), (700, cy + 30)], fill=(148, 163, 184, 255), width=5)

    # Transparent Acetate Outer Sleeve
    draw.line([(cx_left - rw, cy - 15), (140, cy - 60)], fill=(226, 232, 240, 180), width=16)
    draw.line([(140, cy - 60), (100, cy + 30)], fill=(226, 232, 240, 180), width=14)
    draw.line([(cx_right + rw, cy - 15), (660, cy - 60)], fill=(226, 232, 240, 180), width=16)
    draw.line([(660, cy - 60), (700, cy + 30)], fill=(226, 232, 240, 180), width=14)

    # Bridge (Transparent Clear Center Curve)
    draw.arc([cx_left + rw - 12, cy - 30, cx_right - rw + 12, cy + 5], start=190, end=350, fill=(203, 213, 225, 220), width=14)
    draw.arc([cx_left + rw - 12, cy - 30, cx_right - rw + 12, cy + 5], start=190, end=350, fill=(255, 255, 255, 255), width=4)

    # Crystal Clear Oval Rims & Lenses
    for cx in [cx_left, cx_right]:
        bbox_outer = [cx - rw, cy - rh, cx + rw, cy + rh]
        bbox_inner = [cx - rw + 14, cy - rh + 14, cx + rw - 14, cy + rh - 14]

        # Transparent Rim Body
        draw.ellipse(bbox_outer, fill=(226, 232, 240, 150), outline=(148, 163, 184, 220), width=4)
        
        # Clear Glass Lens Fill
        draw.ellipse(bbox_inner, fill=(240, 249, 255, 190), outline=(203, 213, 225, 200), width=2)
        
        # Rim Edge Specular Highlight
        draw.ellipse(bbox_outer, outline=(255, 255, 255, 255), width=2)

        # Metallic Silver Hinge Pins
        pin_x = cx - rw + 6 if cx == cx_left else cx + rw - 6
        draw.ellipse([pin_x - 3, cy - rh + 10, pin_x + 3, cy - rh + 16], fill=(148, 163, 184, 255))

    # Glass Lens Specular Reflections
    glare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    for cx in [cx_left, cx_right]:
        g_draw.polygon([(cx - 60, cy - rh + 20), (cx - 20, cy - rh + 20), (cx + 30, cy + rh - 20), (cx - 10, cy + rh - 20)], fill=(255, 255, 255, 90))
        g_draw.polygon([(cx - 10, cy - rh + 20), (cx + 15, cy - rh + 20), (cx + 55, cy + rh - 20), (cx + 30, cy + rh - 20)], fill=(255, 255, 255, 50))

    glare = glare.filter(ImageFilter.GaussianBlur(3))
    fg = Image.alpha_composite(fg, glare)

    final_img = Image.alpha_composite(img, fg).convert("RGB")
    out_path = os.path.join(output_dir, "real_4.jpg")
    final_img.save(out_path, "JPEG", quality=95)
    print("Generated real_4.jpg (Crystal Clear Oval Eyeglasses)")

generate_eye_004()
