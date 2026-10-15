import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def draw_png_diagram():
    # Workspace and Artifact paths
    output_dir = r'c:\projects\VisionEdge\diagrams\png'
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, 'visionedge_module_planning.png')
    workspace_svg = r'c:\projects\VisionEdge\visionedge_module_planning.svg'
    artifact_dir = r'C:\Users\user\.gemini\antigravity-ide\brain\8c313650-a06a-4d9c-80a8-75b0619ca764'
    
    artifact_png = os.path.join(artifact_dir, 'visionedge_module_planning.png')
    artifact_svg = os.path.join(artifact_dir, 'visionedge_module_planning.svg')

    width = 2000
    height = 1350

    # Create RGB white canvas
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Load system font or default
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        heading_font = ImageFont.truetype("arial.ttf", 18)
        box_title_font = ImageFont.truetype("arialbd.ttf", 16)
        box_body_font = ImageFont.truetype("arial.ttf", 13)
    except IOError:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        box_title_font = ImageFont.load_default()
        box_body_font = ImageFont.load_default()

    # Draw Helper Functions
    def draw_rounded_rect(xy, outline="#000000", fill="#FFFFFF", width=2, radius=8):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

    def draw_text_centered(box, text, font, fill="#000000"):
        x1, y1, x2, y2 = box
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        cx = (x1 + x2) / 2 - w / 2
        cy = (y1 + y2) / 2 - h / 2
        draw.text((cx, cy), text, font=font, fill=fill)

    def draw_arrow_down(x, y1, y2):
        draw.line([(x, y1), (x, y2)], fill="#000000", width=2)
        # Arrowhead
        draw.polygon([(x - 6, y2 - 10), (x + 6, y2 - 10), (x, y2)], fill="#000000")

    # 1. Main Header Box
    draw_rounded_rect([450, 25, 1550, 85], outline="#000000", fill="#FFFFFF", width=2, radius=8)
    draw_text_centered([450, 25, 1550, 85], "VISIONEDGE: SYSTEM MODULE ARCHITECTURE & PLANNING", title_font, fill="#000000")

    # ================= LAYER 1: FRONTEND PRESENTATION =================
    draw_rounded_rect([50, 110, 1950, 310], outline="#000000", fill="#FFFFFF", width=2, radius=8)
    draw.text((75, 125), "1. FRONTEND PRESENTATION LAYER (Web Clients & Portals)", font=heading_font, fill="#000000")

    portals = [
        ("Customer Storefront & Portal", "Catalog, Product Virtual Try-On, Wishlist, Checkout, Prescription History", 80),
        ("Staff & Optometrist Portal", "Customer CRM, Clinical Eye Test, AI OCR Scanner, POS Checkout", 730),
        ("Admin Management Portal", "Inventory Control, Role Access (RBAC), Analytics & Financial Reports", 1380)
    ]
    for title, sub, x in portals:
        draw_rounded_rect([x, 160, x + 540, 280], outline="#000000", fill="#F8FAFC", width=2, radius=6)
        draw.text((x + 20, 185), title, font=box_title_font, fill="#000000")
        
        # Word wrap sub
        words = sub.split()
        l1 = " ".join(words[:len(words)//2 + 1])
        l2 = " ".join(words[len(words)//2 + 1:])
        draw.text((x + 20, 220), l1, font=box_body_font, fill="#333333")
        draw.text((x + 20, 242), l2, font=box_body_font, fill="#333333")

    # Downward Connectors
    for cx in [350, 1000, 1650]:
        draw_arrow_down(cx, 310, 340)

    # ================= LAYER 2: BACKEND API CONTROLLERS =================
    draw_rounded_rect([50, 340, 1950, 730], outline="#000000", fill="#FFFFFF", width=2, radius=8)
    draw.text((75, 355), "2. BACKEND API CONTROLLER LAYER (Python Flask RESTful API)", font=heading_font, fill="#000000")

    modules_r1 = [
        ("MOD-01: Auth & RBAC", "JWT Tokens & Permissions", 80, 395),
        ("MOD-02: Customer CRM", "Profiles & Medical Logs", 390, 395),
        ("MOD-03: Clinical Eye Test", "OD/OS SPH, CYL, AXIS, PD", 700, 395),
        ("MOD-08: Inventory Control", "Frames & Lens Stock Alert", 1010, 395),
        ("MOD-09: Order Processing", "Fulfillment Pipeline", 1320, 395),
        ("MOD-10: Billing & Invoicing", "GST & PDF Receipts", 1630, 395)
    ]
    for code, desc, x, y in modules_r1:
        draw_rounded_rect([x, y, x + 290, y + 90], outline="#000000", fill="#F8FAFC", width=2, radius=6)
        draw.text((x + 15, y + 18), code, font=box_title_font, fill="#000000")
        draw.text((x + 15, y + 50), desc, font=box_body_font, fill="#333333")

    modules_r2 = [
        ("MOD-11: Analytics Dashboard", "Revenue & Sales Trends", 80, 510),
        ("MOD-12: Chatbot & Alerts", "AI Assistant & Notifications", 390, 510)
    ]
    for code, desc, x, y in modules_r2:
        draw_rounded_rect([x, y, x + 290, y + 90], outline="#000000", fill="#F8FAFC", width=2, radius=6)
        draw.text((x + 15, y + 18), code, font=box_title_font, fill="#000000")
        draw.text((x + 15, y + 50), desc, font=box_body_font, fill="#333333")

    # Core Hub Box
    draw_rounded_rect([700, 510, 1920, 700], outline="#000000", fill="#F1F5F9", width=2, radius=6)
    draw.text((730, 535), "Flask Application Dispatcher & Middleware Engine", font=box_title_font, fill="#000000")
    draw.text((730, 580), "• RESTful JSON Route Blueprints  • JWT Authorization Middleware  • CORS & Static Media Handler", font=box_body_font, fill="#1E293B")
    draw.text((730, 620), "• Coordinates request routing across Auth, CRM, Prescriptions, Inventory, Billing & AI Microservices", font=box_body_font, fill="#475569")

    # Downward Connector to AI
    draw_arrow_down(1000, 730, 760)

    # ================= LAYER 3: AI & COMPUTER VISION =================
    draw_rounded_rect([50, 760, 1950, 1000], outline="#000000", fill="#FFFFFF", width=2, radius=8)
    draw.text((75, 775), "3. AI & COMPUTER VISION INTELLIGENCE LAYER", font=heading_font, fill="#000000")

    ai_mods = [
        ("MOD-04: AI Prescription OCR", "Google Gemini 1.5 Pro Vision API parsing paper prescription diopters", 80),
        ("MOD-05: AI Frame Recommendation", "Facial structure geometry analysis matching Oval, Round, Square shapes", 540),
        ("MOD-06: AI Lens & Coating Rec.", "Prescription diopter power analysis for High-Index & Blue-Cut coatings", 1000),
        ("MOD-07: Virtual Try-On (VTO)", "HTML5 Canvas & MediaPipe FaceMesh overlaying frames live on webcam (24+ FPS)", 1460)
    ]
    for code, desc, x in ai_mods:
        draw_rounded_rect([x, 810, x + 440, 960], outline="#000000", fill="#F8FAFC", width=2, radius=6)
        draw.text((x + 20, 835), code, font=box_title_font, fill="#000000")
        
        words = desc.split()
        l1 = " ".join(words[:len(words)//2 + 1])
        l2 = " ".join(words[len(words)//2 + 1:])
        draw.text((x + 20, 880), l1, font=box_body_font, fill="#333333")
        draw.text((x + 20, 910), l2, font=box_body_font, fill="#333333")

    # Downward Connector to Persistence
    draw_arrow_down(1000, 1000, 1030)

    # ================= LAYER 4: PERSISTENCE & EXTERNAL SERVICES =================
    draw_rounded_rect([50, 1030, 1950, 1280], outline="#000000", fill="#FFFFFF", width=2, radius=8)
    draw.text((75, 1045), "4. PERSISTENCE & EXTERNAL SERVICES LAYER", font=heading_font, fill="#000000")

    pers_services = [
        ("Relational Database (SQLAlchemy)", "MySQL / SQLite: User, Customer, EyeTest, Frame, Lens, Order, Invoice Tables", 80),
        ("Google Gemini 1.5 Pro AI Service", "Multimodal REST Cloud API Endpoint for OCR Prescription Image Extraction", 730),
        ("PDF Engine & Static Media Storage", "ReportLab Invoice Generator & File Storage (/uploads/ Prescriptions & Snapshots)", 1380)
    ]
    for title, sub, x in pers_services:
        draw_rounded_rect([x, 1085, x + 540, 1240], outline="#000000", fill="#F8FAFC", width=2, radius=6)
        draw.text((x + 20, 1115), title, font=box_title_font, fill="#000000")
        
        words = sub.split()
        l1 = " ".join(words[:len(words)//2 + 1])
        l2 = " ".join(words[len(words)//2 + 1:])
        draw.text((x + 20, 1160), l1, font=box_body_font, fill="#333333")
        draw.text((x + 20, 1190), l2, font=box_body_font, fill="#333333")

    # Save to Workspace
    img.save(workspace_png, 'PNG')
    print(f"Saved PNG to workspace: {workspace_png}")

    # Copy to Artifacts directory so IDE image preview displays it natively!
    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts directory: {artifact_png}")
        if os.path.exists(workspace_svg):
            shutil.copy(workspace_svg, artifact_svg)
            print(f"Copied SVG to artifacts directory: {artifact_svg}")

if __name__ == '__main__':
    draw_png_diagram()
