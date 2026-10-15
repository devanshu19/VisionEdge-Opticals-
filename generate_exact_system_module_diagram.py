import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def create_system_module_diagram_light():
    # Workspace & Artifact paths
    workspace_dir = r'c:\projects\VisionEdge'
    output_dir = os.path.join(workspace_dir, 'diagrams', 'png')
    os.makedirs(output_dir, exist_ok=True)
    artifact_dir = r'C:\Users\user\.gemini\antigravity-ide\brain\840dd819-d289-4997-bf94-57a1415606c7'
    
    png_filename = 'visionedge_system_module_diagram.png'
    svg_filename = 'visionedge_system_module_diagram.svg'

    workspace_png = os.path.join(output_dir, png_filename)
    workspace_svg = os.path.join(workspace_dir, svg_filename)
    artifact_png = os.path.join(artifact_dir, png_filename)
    artifact_svg = os.path.join(artifact_dir, svg_filename)

    width = 1200
    height = 1480

    # White Canvas background
    bg_color = "#FFFFFF"
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Load system font
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 22)
        module_title_font = ImageFont.truetype("arialbd.ttf", 17)
        box_font = ImageFont.truetype("arialbd.ttf", 14)
    except IOError:
        title_font = ImageFont.load_default()
        module_title_font = ImageFont.load_default()
        box_font = ImageFont.load_default()

    def draw_text_centered(box, text, font, fill="#000000"):
        x1, y1, x2, y2 = box
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        cx = (x1 + x2) / 2 - w / 2
        cy = (y1 + y2) / 2 - h / 2
        draw.text((cx, cy), text, font=font, fill=fill)

    # 1. Main Header Title Banner (White box, black border, black text)
    banner_box = [60, 35, 1140, 105]
    draw.rectangle(banner_box, fill="#FFFFFF", outline="#000000", width=2)
    draw_text_centered(banner_box, "VISIONEDGE - SYSTEM MODULE ARCHITECTURE DIAGRAM", title_font, fill="#000000")

    # Module definitions (Top to Bottom: Module 6 down to Module 1)
    modules_data = [
        {
            "title": "Module 6: Analytics & Financial Reporting",
            "boxes": ["Revenue & Sales Stream", "Top Brand Analytics", "Inventory Audit Logs"]
        },
        {
            "title": "Module 5: Billing & GST PDF Invoicing",
            "boxes": ["GST & Tax Calculator", "Payment Log & Gateway", "ReportLab PDF Streamer"]
        },
        {
            "title": "Module 4: Order & Inventory Management Engine",
            "boxes": ["Listing Catalog Stream", "Dual Inventory Matrix", "Fulfillment Pipeline"]
        },
        {
            "title": "Module 3: AI Vision & Virtual Try-On Suite",
            "boxes": ["Gemini 1.5 OCR Scanner", "Face Shape Classifier", "VTO Canvas Overlay Engine"]
        },
        {
            "title": "Module 2: Customer CRM & Clinical Eye Test",
            "boxes": ["Customer Profile CRUD", "Clinical Diopter Entry", "Patient History Lookup"]
        },
        {
            "title": "Module 1: Identity & Authentication (RBAC)",
            "boxes": ["User Registration", "Session JWT Caching", "Role Authorization State"]
        }
    ]

    start_y = 135
    module_height = 200
    module_gap = 20

    # Clean light-mode colors: White module container with light grey inner boxes
    container_fill = "#FFFFFF"     # Pure White
    container_border = "#000000"   # Solid Black Outline
    inner_fill = "#EFEFEF"         # Light Grey Sub-Box Fill
    inner_border = "#555555"       # Crisp Border Outline

    box_w = 320
    box_h = 120
    start_x = 90
    gap_x = 30

    for i, mod in enumerate(modules_data):
        m_y1 = start_y + i * (module_height + module_gap)
        m_y2 = m_y1 + module_height
        m_box = [60, m_y1, 1140, m_y2]

        # Draw Module Container
        draw.rectangle(m_box, fill=container_fill, outline=container_border, width=2)

        # Module Header Text (Black Font)
        header_box = [60, m_y1 + 12, 1140, m_y1 + 45]
        draw_text_centered(header_box, mod["title"], module_title_font, fill="#000000")

        # 3 Sub-Boxes
        box_y1 = m_y1 + 55
        box_y2 = box_y1 + box_h

        for j, b_text in enumerate(mod["boxes"]):
            b_x1 = start_x + j * (box_w + gap_x)
            b_x2 = b_x1 + box_w
            sub_box = [b_x1, box_y1, b_x2, box_y2]

            draw.rectangle(sub_box, fill=inner_fill, outline=inner_border, width=1)
            draw_text_centered(sub_box, b_text, box_font, fill="#000000")

    # Save PNG
    img.save(workspace_png)
    os.makedirs(artifact_dir, exist_ok=True)
    shutil.copy(workspace_png, artifact_png)
    print(f"PNG generated successfully: {workspace_png}")

    # SVG version
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'  <rect width="100%" height="100%" fill="{bg_color}"/>',
        f'  <rect x="60" y="35" width="1080" height="70" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>',
        '  <text x="600" y="78" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="#000000" text-anchor="middle">VISIONEDGE - SYSTEM MODULE ARCHITECTURE DIAGRAM</text>'
    ]

    for i, mod in enumerate(modules_data):
        m_y1 = start_y + i * (module_height + module_gap)
        
        svg_lines.append(f'  <!-- {mod["title"]} -->')
        svg_lines.append(f'  <rect x="60" y="{m_y1}" width="1080" height="{module_height}" fill="{container_fill}" stroke="{container_border}" stroke-width="2"/>')
        svg_lines.append(f'  <text x="600" y="{m_y1 + 32}" font-family="Arial, sans-serif" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">{mod["title"]}</text>')

        box_y1 = m_y1 + 55

        for j, b_text in enumerate(mod["boxes"]):
            b_x1 = start_x + j * (box_w + gap_x)
            svg_lines.append(f'  <rect x="{b_x1}" y="{box_y1}" width="{box_w}" height="{box_h}" fill="{inner_fill}" stroke="{inner_border}" stroke-width="1.5"/>')
            svg_lines.append(f'  <text x="{b_x1 + box_w/2}" y="{box_y1 + box_h/2 + 5}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">{b_text}</text>')

    svg_lines.append('</svg>')
    
    with open(workspace_svg, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))
    
    shutil.copy(workspace_svg, artifact_svg)
    print(f"SVG generated successfully: {workspace_svg}")

if __name__ == "__main__":
    create_system_module_diagram_light()
