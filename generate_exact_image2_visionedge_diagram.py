import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_diagram():
    # Workspace & Artifact Paths
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\24af6b21-8af6-4312-8660-c477577db3bd"
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_module_block_diagram.png")
    artifact_png = os.path.join(artifact_dir, "visionedge_module_block_diagram.png")

    # Dimensions
    width = 1100
    height = 1350

    # Background color matching Image 2: Dark slate / dark navy gray
    bg_color = (26, 29, 38) # #1A1D26
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Font setup
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 22)
        mod_font = ImageFont.truetype("arialbd.ttf", 16)
        sub_font = ImageFont.truetype("arialbd.ttf", 14)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 22)
            mod_font = ImageFont.truetype("segoeuib.ttf", 16)
            sub_font = ImageFont.truetype("segoeuib.ttf", 14)
        except IOError:
            title_font = ImageFont.load_default()
            mod_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()

    # Draw Helper
    def draw_text_centered(box, text, font, fill=(0, 0, 0)):
        x1, y1, x2, y2 = box
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        cx = (x1 + x2) / 2 - w / 2
        cy = (y1 + y2) / 2 - h / 2
        draw.text((cx, cy), text, font=font, fill=fill)

    # Top Header Box
    header_rect = [50, 40, width - 50, 100]
    draw.rectangle(header_rect, fill=(255, 255, 255), outline=(100, 100, 100), width=2)
    draw_text_centered(header_rect, "VISIONEDGE - SYSTEM MODULE ARCHITECTURE DIAGRAM", title_font, fill=(15, 23, 42))

    # Modules configuration (matching Image 2 layout)
    # Light blue outer container: #9FE3F8 (159, 227, 248), border: #4092B0 (64, 146, 176)
    # Lavender inner boxes: #DBCFF7 (219, 207, 247), border: #8A75C9 (138, 117, 201)
    
    modules = [
        {
            "title": "Module 6: Analytics & Financial Reporting",
            "subs": ["Revenue & Sales Stream", "Top Brand Analytics", "Inventory Audit Logs"]
        },
        {
            "title": "Module 5: Billing & GST PDF Invoicing",
            "subs": ["GST & Tax Calculator", "Payment Log & Gateway", "ReportLab PDF Streamer"]
        },
        {
            "title": "Module 4: Order & Inventory Management Engine",
            "subs": ["Listing Catalog Stream", "Dual Inventory Matrix", "Fulfillment Pipeline"]
        },
        {
            "title": "Module 3: AI Vision & Virtual Try-On Suite",
            "subs": ["Gemini 1.5 OCR Scanner", "Face Shape Classifier", "VTO Canvas Overlay Engine"]
        },
        {
            "title": "Module 2: Customer CRM & Clinical Eye Test",
            "subs": ["Customer Profile CRUD", "Clinical Diopter Entry", "Patient History Lookup"]
        },
        {
            "title": "Module 1: Identity & Authentication (RBAC)",
            "subs": ["User Registration", "Session JWT Caching", "Role Authorization State"]
        }
    ]

    start_y = 130
    mod_height = 175
    gap = 25
    margin_x = 60

    outer_bg = (160, 225, 246)       # Light blue like Image 2
    outer_border = (50, 135, 170)
    inner_bg = (220, 210, 242)       # Soft lavender purple like Image 2
    inner_border = (135, 115, 195)
    text_color = (25, 25, 35)

    for i, mod in enumerate(modules):
        top_y = start_y + i * (mod_height + gap)
        bot_y = top_y + mod_height
        
        # Outer Module Box
        outer_rect = [margin_x, top_y, width - margin_x, bot_y]
        draw.rectangle(outer_rect, fill=outer_bg, outline=outer_border, width=2)

        # Module Title
        title_box = [margin_x, top_y + 12, width - margin_x, top_y + 42]
        draw_text_centered(title_box, mod["title"], mod_font, fill=text_color)

        # Inner Sub-component boxes (arranged side by side)
        subs = mod["subs"]
        num_subs = len(subs)
        sub_width = (width - 2 * margin_x - 40 - (num_subs - 1) * 20) / num_subs
        sub_top = top_y + 55
        sub_bot = bot_y - 25

        for j, sub in enumerate(subs):
            sub_x1 = margin_x + 20 + j * (sub_width + 20)
            sub_x2 = sub_x1 + sub_width
            sub_rect = [sub_x1, sub_top, sub_x2, sub_bot]
            
            draw.rectangle(sub_rect, fill=inner_bg, outline=inner_border, width=2)
            draw_text_centered(sub_rect, sub, sub_font, fill=text_color)

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved diagram image to workspace: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied diagram image to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_diagram()
