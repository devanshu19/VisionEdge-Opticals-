import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_sequence_diagram():
    # Workspace and Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_sequence_diagram_exact.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\5afeff16-181e-4c5f-9331-54cb5f42d790"
    artifact_png = os.path.join(artifact_dir, "visionedge_sequence_diagram_exact.png")

    width = 1800
    height = 1960
    bg_color = (255, 255, 255) # Pure white background

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts setup
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 30)
        header_font = ImageFont.truetype("arialbd.ttf", 16)
        label_font = ImageFont.truetype("arialbd.ttf", 13)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 30)
            header_font = ImageFont.truetype("segoeuib.ttf", 16)
            label_font = ImageFont.truetype("segoeuib.ttf", 13)
            small_font = ImageFont.truetype("segoeui.ttf", 12)
        except IOError:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

    # Draw Title
    title_text = "VisionEdge or UML Sequence Diagram"
    bbox = title_font.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 25), title_text, font=title_font, fill=(0, 0, 0))

    # Participants configuration (MySQL Database is LAST in position 5)
    columns = [
        {"name": "Customer", "x": 130},
        {"name": "System Interface", "x": 400},
        {"name": "Flask API", "x": 700},
        {"name": "Gemini AI OCR", "x": 1000},
        {"name": "POS Billing", "x": 1290},
        {"name": "MySQL Database", "x": 1580}
    ]

    top_box_y1 = 80
    top_box_y2 = 128
    bot_box_y1 = 1840
    bot_box_y2 = 1888

    box_w = 160
    box_h = 48

    # Draw Lifelines & Header Boxes
    for col in columns:
        cx = col["x"]
        
        # Dashed Lifeline Line
        dash_len = 6
        gap_len = 6
        curr_y = top_box_y2
        while curr_y < bot_box_y1:
            draw.line([(cx, curr_y), (cx, min(curr_y + dash_len, bot_box_y1))], fill=(0, 0, 0), width=1)
            curr_y += dash_len + gap_len

        # Top Box
        rx1, ry1, rx2, ry2 = cx - box_w//2, top_box_y1, cx + box_w//2, top_box_y2
        draw.rectangle([rx1, ry1, rx2, ry2], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        bbox = header_font.getbbox(col["name"])
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw/2, ry1 + (box_h - th)/2 - 2), col["name"], font=header_font, fill=(0, 0, 0))

        # Bottom Box
        rx1, ry1, rx2, ry2 = cx - box_w//2, bot_box_y1, cx + box_w//2, bot_box_y2
        draw.rectangle([rx1, ry1, rx2, ry2], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        bbox = header_font.getbbox(col["name"])
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw/2, ry1 + (box_h - th)/2 - 2), col["name"], font=header_font, fill=(0, 0, 0))

    # Activation bars definition
    start_y = 170
    step_h = 68.0

    activations = [
        # System Interface (col 1)
        {"col": 1, "y1": start_y - 8, "y2": start_y + 23 * step_h + 12},
        # Flask API (col 2)
        {"col": 2, "y1": start_y + 1 * step_h - 8, "y2": start_y + 12 * step_h + 10},
        {"col": 2, "y1": start_y + 14 * step_h - 8, "y2": start_y + 22 * step_h + 10},
        # Gemini AI OCR (col 3)
        {"col": 3, "y1": start_y + 3 * step_h - 8, "y2": start_y + 6 * step_h + 10},
        # POS Billing (col 4)
        {"col": 4, "y1": start_y + 17 * step_h - 8, "y2": start_y + 19 * step_h + 10},
        # MySQL Database (col 5 - LAST)
        {"col": 5, "y1": start_y + 8 * step_h - 8, "y2": start_y + 9 * step_h + 10},
        {"col": 5, "y1": start_y + 10 * step_h - 8, "y2": start_y + 11 * step_h + 10},
        {"col": 5, "y1": start_y + 15 * step_h - 8, "y2": start_y + 16 * step_h + 10},
        {"col": 5, "y1": start_y + 20 * step_h - 8, "y2": start_y + 21 * step_h + 10}
    ]

    for act in activations:
        cx = columns[act["col"]]["x"]
        bar_w = 14
        rx1 = cx - bar_w // 2
        rx2 = cx + bar_w // 2
        draw.rectangle([rx1, act["y1"], rx2, act["y2"]], fill=(255, 255, 255), outline=(0, 0, 0), width=1)

    # 24 Step Definitions with MySQL Database in position 5 (last)
    # (step_num, from_col, to_col, label, is_dashed, is_self)
    steps = [
        (1, 0, 1, "1. Upload receipt photo\n(Mobile App)", False, False),
        (2, 1, 2, "2. POST /api/upload_receipt\n(Photo data)", False, False),
        (3, 2, 2, "3. Validate user & request", False, True),
        (4, 2, 3, "4. POST /analyze_receipt\n(Image URL/Base64)", False, False),
        (5, 3, 3, "5. Process image &\nextract text (OCR)", False, True),
        (6, 3, 3, "6. Identify receipt fields\n(Date, Vendor, Items, Totals)", False, True),
        (7, 3, 2, "7. Return structured JSON\n(Extracted Data)", True, False),
        (8, 2, 2, "8. Process JSON,\ncalculate taxes/discounts", False, True),
        (9, 2, 5, "9. SELECT existing customer records", False, False),
        (10, 5, 2, "10. Customer data (e.g., membership)", True, False),
        (11, 2, 5, "11. INSERT new expense record (Pending)", False, False),
        (12, 5, 2, "12. Success confirmation", True, False),
        (13, 2, 1, "13. Display extracted expense summary", True, False),
        (14, 0, 1, "14. Review & confirm details", False, False),
        (15, 1, 2, "15. POST /api/confirm_expense\n(Confirmed data)", False, False),
        (16, 2, 5, "16. UPDATE expense status to 'Confirmed'", False, False),
        (17, 5, 2, "17. Success", True, False),
        (18, 2, 4, "18. POST /api/integrate_billing\n(Transaction details)", False, False),
        (19, 4, 4, "19. Generate billing record,\nprocess payment", False, True),
        (20, 4, 2, "20. Transaction status (Success/Failure)", True, False),
        (21, 2, 5, "21. UPDATE expense with POS reference", False, False),
        (22, 5, 2, "22. Success", True, False),
        (23, 2, 1, "23. Show \"Expense Recorded\n& Billed\"", True, False),
        (24, 1, 0, "24. Confirm transaction\ncompletion", True, False)
    ]

    def draw_arrow_head(x, y, direction="right", is_open=False):
        head_len = 10
        head_w = 5
        if direction == "right":
            pts = [(x - head_len, y - head_w), (x, y), (x - head_len, y + head_w)]
            if is_open:
                draw.line([pts[0], pts[1]], fill=(0, 0, 0), width=2)
                draw.line([pts[2], pts[1]], fill=(0, 0, 0), width=2)
            else:
                draw.polygon(pts, fill=(0, 0, 0))
        elif direction == "left":
            pts = [(x + head_len, y - head_w), (x, y), (x + head_len, y + head_w)]
            if is_open:
                draw.line([pts[0], pts[1]], fill=(0, 0, 0), width=2)
                draw.line([pts[2], pts[1]], fill=(0, 0, 0), width=2)
            else:
                draw.polygon(pts, fill=(0, 0, 0))

    for idx, (s_num, from_idx, to_idx, label, is_dashed, is_self) in enumerate(steps):
        y = start_y + idx * step_h
        x_from = columns[from_idx]["x"]
        x_to = columns[to_idx]["x"]

        if is_self:
            # Self loop box on the right of x_from
            loop_w = 42
            loop_h = 26
            y_top = y - 8
            y_bot = y_top + loop_h
            
            draw.line([(x_from + 7, y_top), (x_from + loop_w, y_top)], fill=(0, 0, 0), width=2)
            draw.line([(x_from + loop_w, y_top), (x_from + loop_w, y_bot)], fill=(0, 0, 0), width=2)
            draw.line([(x_from + loop_w, y_bot), (x_from + 7, y_bot)], fill=(0, 0, 0), width=2)
            draw_arrow_head(x_from + 7, y_bot, direction="left", is_open=False)

            # Label text
            lines = label.split('\n')
            for l_i, l_text in enumerate(lines):
                draw.text((x_from + loop_w + 8, y_top + l_i * 15 - 2), l_text, font=label_font, fill=(0, 0, 0))

        else:
            dir_str = "right" if x_to > x_from else "left"
            margin = 7
            ax1 = x_from + (margin if dir_str == "right" else -margin)
            ax2 = x_to + (-margin if dir_str == "right" else margin)

            # Line
            if is_dashed:
                d_len = 5
                g_len = 4
                cx = ax1
                if dir_str == "right":
                    while cx < ax2:
                        draw.line([(cx, y), (min(cx + d_len, ax2), y)], fill=(0, 0, 0), width=2)
                        cx += d_len + g_len
                else:
                    while cx > ax2:
                        draw.line([(cx, y), (max(cx - d_len, ax2), y)], fill=(0, 0, 0), width=2)
                        cx -= d_len + g_len
                draw_arrow_head(ax2, y, direction=dir_str, is_open=True)
            else:
                draw.line([(ax1, y), (ax2, y)], fill=(0, 0, 0), width=2)
                draw_arrow_head(ax2, y, direction=dir_str, is_open=False)

            # Label text centered above line
            lines = label.split('\n')
            mid_x = (x_from + x_to) / 2
            
            # Position label
            total_text_h = len(lines) * 15
            start_text_y = y - total_text_h - 4
            
            for l_i, l_text in enumerate(lines):
                bbox = label_font.getbbox(l_text)
                tw = bbox[2] - bbox[0]
                draw.text((mid_x - tw / 2, start_text_y + l_i * 15), l_text, font=label_font, fill=(0, 0, 0))

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_sequence_diagram()
