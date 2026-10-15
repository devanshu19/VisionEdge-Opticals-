import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_exact_class_diagram():
    # Workspace & Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_exact_class_diagram.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\5afeff16-181e-4c5f-9331-54cb5f42d790"
    artifact_png = os.path.join(artifact_dir, "visionedge_exact_class_diagram.png")

    width = 1400
    height = 1450
    bg_color = (255, 255, 255) # Pure white background
    text_color = (0, 0, 0)     # Black font
    line_color = (0, 0, 0)     # Black lines/arrows

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts matching uploaded image styling
    try:
        class_name_font = ImageFont.truetype("arialbd.ttf", 22)
        attr_font = ImageFont.truetype("arial.ttf", 17)
        label_font = ImageFont.truetype("arial.ttf", 17)
    except IOError:
        try:
            class_name_font = ImageFont.truetype("segoeuib.ttf", 22)
            attr_font = ImageFont.truetype("segoeui.ttf", 17)
            label_font = ImageFont.truetype("segoeui.ttf", 17)
        except IOError:
            class_name_font = ImageFont.load_default()
            attr_font = ImageFont.load_default()
            label_font = ImageFont.load_default()

    # Helper function to draw UML class boxes
    def draw_class_box(x, y, w, title, attrs, methods):
        title_h = 42
        attr_h = max(24, len(attrs) * 26 + 10)
        method_h = max(24, len(methods) * 26 + 10)
        total_h = title_h + attr_h + method_h

        # Outer Rectangle
        draw.rectangle([x, y, x + w, y + total_h], fill=(255, 255, 255), outline=line_color, width=2)

        # Title
        bbox = class_name_font.getbbox(title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (w - tw) / 2, y + 8), title, font=class_name_font, fill=text_color)

        # Divider 1
        draw.line([(x, y + title_h), (x + w, y + title_h)], fill=line_color, width=2)

        # Attributes
        curr_y = y + title_h + 6
        for a in attrs:
            draw.text((x + 12, curr_y), a, font=attr_font, fill=text_color)
            curr_y += 26

        # Divider 2
        method_start_y = y + title_h + attr_h
        draw.line([(x, method_start_y), (x + w, method_start_y)], fill=line_color, width=2)

        # Methods
        curr_y = method_start_y + 6
        for m in methods:
            draw.text((x + 12, curr_y), m, font=attr_font, fill=text_color)
            curr_y += 26

        return {
            "x": x, "y": y, "w": w, "h": total_h,
            "center_top": (x + w/2, y),
            "center_bottom": (x + w/2, y + total_h)
        }

    boxes = {}

    # LEVEL 1: User (Top Center)
    boxes["User"] = draw_class_box(530, 40, 260, "User", [
        "- userId",
        "- username",
        "- email"
    ], [
        "+ login()",
        "+ register()"
    ])

    # LEVEL 2: Admin, Optician, Customer (Middle Row 1)
    boxes["Admin"] = draw_class_box(160, 310, 260, "Admin", [
        "- userId",
        "- username",
        "- email"
    ], [
        "+ login()",
        "+ register()"
    ])

    boxes["Optician"] = draw_class_box(530, 310, 260, "Optician", [
        "- userId",
        "- username",
        "- email"
    ], [
        "+ login()",
        "+ register()"
    ])

    boxes["Customer"] = draw_class_box(900, 310, 260, "Customer", [
        "- userId",
        "- username",
        "- email"
    ], [
        "+ login()",
        "+ register()"
    ])

    # LEVEL 3: SystemLog, Appointment, Prescription (Middle Row 2)
    boxes["SystemLog"] = draw_class_box(60, 600, 260, "SystemLog", [
        "- userId",
        "- username",
        "- email"
    ], [
        "+ generate()",
        "+ register()"
    ])

    boxes["Appointment"] = draw_class_box(410, 600, 260, "Appointment", [
        "- userId"
    ], [
        "+ login()",
        "+ register()"
    ])

    boxes["Prescription"] = draw_class_box(760, 600, 260, "Prescription", [
        "- prescription",
        "- prrscription"
    ], [
        "+ creates()"
    ])

    # LEVEL 4: ExamResults, Order, Invoice (Bottom Row)
    boxes["ExamResults"] = draw_class_box(410, 890, 260, "ExamResults", [], [])

    boxes["Order"] = draw_class_box(760, 890, 260, "Order", [
        "- userId",
        "- order"
    ], [
        "+ order ()"
    ])

    boxes["Invoice"] = draw_class_box(1100, 890, 260, "Invoice", [
        "- userId",
        "- invoice"
    ], [
        "+ pays()"
    ])

    # Drawing 3 Separate Inheritance Hollow Triangles at User bottom edge
    user_bot_y = boxes["User"]["center_bottom"][1]
    
    def draw_triangle(tx, ty):
        tri_h = 18
        tri_w = 12
        pts = [(tx, ty), (tx - tri_w, ty + tri_h), (tx + tri_w, ty + tri_h)]
        draw.polygon(pts, fill=(255, 255, 255), outline=line_color)
        draw.line([pts[0], pts[1]], fill=line_color, width=2)
        draw.line([pts[1], pts[2]], fill=line_color, width=2)
        draw.line([pts[2], pts[0]], fill=line_color, width=2)
        return ty + tri_h

    # 3 Triangles under User
    t1_y = draw_triangle(580, user_bot_y)
    t2_y = draw_triangle(660, user_bot_y)
    t3_y = draw_triangle(740, user_bot_y)

    # Admin inheritance line
    draw.line([(290, 310), (290, t1_y + 20), (580, t1_y + 20), (580, t1_y)], fill=line_color, width=2)

    # Optician inheritance line
    draw.line([(660, 310), (660, t2_y)], fill=line_color, width=2)

    # Customer inheritance line
    draw.line([(1030, 310), (1030, t3_y + 20), (740, t3_y + 20), (740, t3_y)], fill=line_color, width=2)

    # Drawing Association Arrows (Solid line with open arrowhead `-->`)
    def draw_association_arrow(start_pt, end_pt, label="", label_pos=None):
        draw.line([start_pt, end_pt], fill=line_color, width=2)

        x1, y1 = start_pt
        x2, y2 = end_pt
        head_l = 12
        head_w = 6

        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            ux = dx / length
            uy = dy / length
            px = -uy
            py = ux
            wing1 = (x2 - head_l * ux + head_w * px, y2 - head_l * uy + head_w * py)
            wing2 = (x2 - head_l * ux - head_w * px, y2 - head_l * uy - head_w * py)
            draw.line([wing1, (x2, y2)], fill=line_color, width=2)
            draw.line([wing2, (x2, y2)], fill=line_color, width=2)

        if label:
            if label_pos:
                lx, ly = label_pos
            else:
                lx = (x1 + x2) / 2
                ly = (y1 + y2) / 2
            bbox = label_font.getbbox(label)
            tw = bbox[2] - bbox[0]
            draw.text((lx - tw / 2, ly - 18), label, font=label_font, fill=text_color)

    # 1. Admin -> SystemLog ("generates")
    draw_association_arrow((230, 506), (190, 600), "generates", (190, 545))

    # 2. Optician -> Appointment ("schedules")
    draw_association_arrow((580, 506), (510, 600), "schedules", (510, 545))

    # 3. Optician -> Prescription ("creates")
    draw_association_arrow((730, 506), (840, 600), "creates", (810, 545))

    # 4. Customer -> Appointment ("undergoes")
    draw_association_arrow((950, 506), (620, 600), "undergoes", (690, 545))

    # 5. Customer -> Invoice ("pays")
    draw_association_arrow((1080, 506), (1220, 890), "pays", (1170, 680))

    # 6. Appointment -> ExamResults ("produces")
    draw_association_arrow((540, 750), (540, 890), "produces", (540, 810))

    # 7. Prescription -> Order ("generates")
    draw_association_arrow((890, 726), (890, 890), "generates", (890, 800))

    # 8. Order -> Invoice ("creates")
    draw_association_arrow((1020, 950), (1100, 950), "creates", (1060, 930))

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_exact_class_diagram()
