import os
import math
from PIL import Image, ImageDraw

def create_frames():
    backend_frames_dir = os.path.join(os.path.dirname(__file__), 'media', 'frames')
    frontend_frames_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'images', 'frames'))
    os.makedirs(backend_frames_dir, exist_ok=True)
    os.makedirs(frontend_frames_dir, exist_ok=True)

    W, H = 800, 300
    cx_l, cx_r = 270, 530
    cy = 145

    def save_dual(img, name):
        p1 = os.path.join(backend_frames_dir, f"{name}.png")
        p2 = os.path.join(frontend_frames_dir, f"{name}.png")
        img.save(p1, "PNG")
        img.save(p2, "PNG")
        print(f"Generated: {name}.png -> {p1}")

    # 1. WAYFARER / RAYBAN CLASSIC (Bold Acetate Black)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Left & Right lens polygons (classic trapezoidal wayfarer)
    def wayfarer_pts(cx, cy, flip=False):
        pts = [
            (cx - 105, cy - 55),
            (cx + 85, cy - 55),
            (cx + 65, cy + 60),
            (cx - 85, cy + 50)
        ]
        if flip:
            pts = [(2 * cx - x, y) for (x, y) in pts]
            pts = list(reversed(pts))
        return pts

    # Lens tint (clear anti-reflective light blue)
    l_pts = wayfarer_pts(cx_l, cy)
    r_pts = wayfarer_pts(cx_r, cy, flip=True)
    draw.polygon(l_pts, fill=(180, 220, 255, 45))
    draw.polygon(r_pts, fill=(180, 220, 255, 45))

    # Thick rims
    draw.line(l_pts + [l_pts[0]], fill=(25, 25, 28, 250), width=14, joint="curve")
    draw.line(r_pts + [r_pts[0]], fill=(25, 25, 28, 250), width=14, joint="curve")

    # Bridge
    draw.line([(cx_l + 75, cy - 40), (cx_r - 75, cy - 40)], fill=(25, 25, 28, 250), width=12)
    # Temples / Hinges
    draw.line([(cx_l - 100, cy - 48), (cx_l - 150, cy - 52)], fill=(25, 25, 28, 250), width=14)
    draw.line([(cx_r + 100, cy - 48), (cx_r + 150, cy - 52)], fill=(25, 25, 28, 250), width=14)
    # Silver rivets
    draw.ellipse([cx_l - 110, cy - 53, cx_l - 98, cy - 45], fill=(210, 215, 220, 255))
    draw.ellipse([cx_r + 98, cy - 53, cx_r + 110, cy - 45], fill=(210, 215, 220, 255))
    save_dual(im, "rayban_vto")
    save_dual(im, "wayfarer_vto")

    # 2. AVIATOR (Double Bridge Metal Teardrop)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    def aviator_pts(cx, cy, flip=False):
        pts = []
        for a in range(0, 360, 10):
            rad = math.radians(a)
            rx = 98 * math.cos(rad)
            # Teardrop shape: elongate bottom outer corner
            ry = 70 * math.sin(rad)
            if math.sin(rad) > 0: # bottom half
                ry += 15 * math.sin(rad)
                rx -= 8 * math.sin(rad) * (-1 if flip else 1)
            pts.append((cx + rx, cy + ry))
        return pts

    l_av = aviator_pts(cx_l, cy)
    r_av = aviator_pts(cx_r, cy, flip=True)
    # Dark gradient sunglass tint
    draw.polygon(l_av, fill=(35, 55, 45, 175))
    draw.polygon(r_av, fill=(35, 55, 45, 175))
    # Golden rims
    draw.line(l_av + [l_av[0]], fill=(212, 175, 55, 255), width=7, joint="curve")
    draw.line(r_av + [r_av[0]], fill=(212, 175, 55, 255), width=7, joint="curve")
    # Double bridge: top brow bar & lower nose bridge
    draw.line([(cx_l + 70, cy - 42), (cx_r - 70, cy - 42)], fill=(212, 175, 55, 255), width=6)
    draw.arc([cx_l + 65, cy - 25, cx_r - 65, cy + 5], 180, 360, fill=(212, 175, 55, 255), width=5)
    # Temples
    draw.line([(cx_l - 96, cy - 20), (cx_l - 145, cy - 25)], fill=(212, 175, 55, 255), width=6)
    draw.line([(cx_r + 96, cy - 20), (cx_r + 145, cy - 25)], fill=(212, 175, 55, 255), width=6)
    save_dual(im, "aviator_vto")

    # 3. ROUND VINTAGE WIREFRAME (Gunmetal / Classic Gold)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    r_radius = 72
    # Lens tints
    draw.ellipse([cx_l - r_radius, cy - r_radius, cx_l + r_radius, cy + r_radius], fill=(200, 230, 255, 40), outline=(50, 50, 55, 255), width=6)
    draw.ellipse([cx_r - r_radius, cy - r_radius, cx_r + r_radius, cy + r_radius], fill=(200, 230, 255, 40), outline=(50, 50, 55, 255), width=6)
    # Arched Keyhole Bridge
    draw.arc([cx_l + r_radius - 8, cy - 35, cx_r - r_radius + 8, cy + 5], 180, 360, fill=(50, 50, 55, 255), width=6)
    # Temple hinges
    draw.line([(cx_l - r_radius, cy), (cx_l - r_radius - 40, cy - 5)], fill=(50, 50, 55, 255), width=6)
    draw.line([(cx_r + r_radius, cy), (cx_r + r_radius + 40, cy - 5)], fill=(50, 50, 55, 255), width=6)
    save_dual(im, "round_vto")

    # 4. RECTANGLE EXECUTIVE (Modern Matte Midnight Blue)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    rw, rh = 100, 52
    draw.rounded_rectangle([cx_l - rw, cy - rh, cx_l + rw, cy + rh], radius=16, fill=(190, 225, 255, 35), outline=(20, 30, 50, 255), width=8)
    draw.rounded_rectangle([cx_r - rw, cy - rh, cx_r + rw, cy + rh], radius=16, fill=(190, 225, 255, 35), outline=(20, 30, 50, 255), width=8)
    # Bridge
    draw.line([(cx_l + rw - 2, cy - 10), (cx_r - rw + 2, cy - 10)], fill=(20, 30, 50, 255), width=7)
    # Temples
    draw.line([(cx_l - rw, cy - 25), (cx_l - rw - 45, cy - 30)], fill=(20, 30, 50, 255), width=8)
    draw.line([(cx_r + rw, cy - 25), (cx_r + rw + 45, cy - 30)], fill=(20, 30, 50, 255), width=8)
    save_dual(im, "rectangle_vto")

    # 5. CAT-EYE DESIGNER (Chic Burgundy / Rose Gold)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    def cateye_pts(cx, cy, flip=False):
        pts = [
            (cx - 105, cy - 65), # Winged top corner
            (cx + 70, cy - 40),
            (cx + 60, cy + 45),
            (cx - 65, cy + 50)
        ]
        if flip:
            pts = [(2 * cx - x, y) for (x, y) in pts]
            pts = list(reversed(pts))
        return pts
    l_cat = cateye_pts(cx_l, cy)
    r_cat = cateye_pts(cx_r, cy, flip=True)
    draw.polygon(l_cat, fill=(230, 200, 220, 45))
    draw.polygon(r_cat, fill=(230, 200, 220, 45))
    draw.line(l_cat + [l_cat[0]], fill=(140, 20, 60, 255), width=10, joint="curve")
    draw.line(r_cat + [r_cat[0]], fill=(140, 20, 60, 255), width=10, joint="curve")
    # Bridge
    draw.line([(cx_l + 65, cy - 28), (cx_r - 65, cy - 28)], fill=(140, 20, 60, 255), width=7)
    # Wing extensions
    draw.line([(cx_l - 105, cy - 65), (cx_l - 145, cy - 68)], fill=(140, 20, 60, 255), width=8)
    draw.line([(cx_r + 105, cy - 65), (cx_r + 145, cy - 68)], fill=(140, 20, 60, 255), width=8)
    save_dual(im, "cateye_vto")

    # 6. RIMLESS TITANIUM (Minimalist Wire Bridge & Nose Pads)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    rw, rh = 90, 48
    # Subtle clear lens edges
    draw.rounded_rectangle([cx_l - rw, cy - rh, cx_l + rw, cy + rh], radius=12, fill=(210, 235, 255, 30), outline=(180, 200, 220, 160), width=3)
    draw.rounded_rectangle([cx_r - rw, cy - rh, cx_r + rw, cy + rh], radius=12, fill=(210, 235, 255, 30), outline=(180, 200, 220, 160), width=3)
    # Titanium Bridge
    draw.arc([cx_l + rw - 5, cy - 25, cx_r - rw + 5, cy + 5], 180, 360, fill=(160, 165, 175, 255), width=4)
    # Screws
    draw.ellipse([cx_l + rw - 10, cy - 14, cx_l + rw - 2, cy - 6], fill=(120, 125, 135, 255))
    draw.ellipse([cx_r - rw + 2, cy - 14, cx_r - rw + 10, cy - 6], fill=(120, 125, 135, 255))
    # Temples
    draw.line([(cx_l - rw, cy - 10), (cx_l - rw - 40, cy - 15)], fill=(160, 165, 175, 255), width=4)
    draw.line([(cx_r + rw, cy - 10), (cx_r + rw + 40, cy - 15)], fill=(160, 165, 175, 255), width=4)
    save_dual(im, "rimless_vto")

    print("All VTO Frame PNG Cutouts successfully generated!")

if __name__ == '__main__':
    create_frames()
