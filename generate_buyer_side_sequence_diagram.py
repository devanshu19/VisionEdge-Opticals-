import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_buyer_side_diagram():
    # Workspace & Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_buyer_side_sequence_diagram.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\e79292ba-2641-475d-9708-3cfd889a9b55"
    artifact_png = os.path.join(artifact_dir, "visionedge_buyer_side_sequence_diagram.png")

    width = 1850
    height = 1400
    
    # Pure White background with Black font and borders
    bg_color = (255, 255, 255)   # White background
    box_fill = (255, 255, 255)   # White fill for boxes
    box_border = (0, 0, 0)       # Black border
    text_color = (0, 0, 0)       # Pure Black font
    arrow_color = (0, 0, 0)      # Pure Black arrows
    lifeline_color = (80, 80, 80) # Charcoal gray lifelines

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 24)
        header_font = ImageFont.truetype("arialbd.ttf", 15)
        label_font = ImageFont.truetype("arialbd.ttf", 12.5)
        badge_font = ImageFont.truetype("arialbd.ttf", 11)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 24)
            header_font = ImageFont.truetype("segoeuib.ttf", 15)
            label_font = ImageFont.truetype("segoeuib.ttf", 12.5)
            badge_font = ImageFont.truetype("segoeuib.ttf", 11)
        except IOError:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            badge_font = ImageFont.load_default()

    # Draw Top Header Banner
    draw.rectangle([0, 0, width, 52], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    title_text = "VisionEdge - Buyer Side Sequence Diagram (Marketplace Browsing, VTO & Checkout Flow)"
    bbox = title_font.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 12), title_text, font=title_font, fill=(0, 0, 0))

    # Participants configuration (MySQL Database in LAST position)
    columns = [
        {"name": "Resident Buyer", "x": 110, "is_actor": True},
        {"name": "Marketplace Feed UI", "x": 370, "is_actor": False},
        {"name": "VTO & Detail Canvas", "x": 670, "is_actor": False},
        {"name": "Flask Backend API", "x": 980, "is_actor": False},
        {"name": "POS & Billing Engine", "x": 1290, "is_actor": False},
        {"name": "MySQL Database", "x": 1650, "is_actor": False}
    ]

    top_box_y1 = 65
    top_box_y2 = 115
    bot_box_y1 = 1290
    bot_box_y2 = 1340
    box_w = 170
    box_h = 50

    def draw_stick_figure(cx, cy):
        # Head
        draw.ellipse([cx - 13, cy - 35, cx + 13, cy - 9], outline=box_border, width=3)
        # Body
        draw.line([(cx, cy - 9), (cx, cy + 18)], fill=box_border, width=3)
        # Arms
        draw.line([(cx - 18, cy + 2), (cx + 18, cy + 2)], fill=box_border, width=3)
        # Legs
        draw.line([(cx, cy + 18), (cx - 14, cy + 40)], fill=box_border, width=3)
        draw.line([(cx, cy + 18), (cx + 14, cy + 40)], fill=box_border, width=3)

    # Lifelines & Header Boxes
    for col in columns:
        cx = col["x"]

        # Dashed Lifeline Line
        dash_len = 6
        gap_len = 6
        curr_y = top_box_y2 + (15 if col["is_actor"] else 0)
        end_y = bot_box_y1 - (45 if col["is_actor"] else 0)

        while curr_y < end_y:
            draw.line([(cx, curr_y), (cx, min(curr_y + dash_len, end_y))], fill=lifeline_color, width=2)
            curr_y += dash_len + gap_len

        if col["is_actor"]:
            # Top Actor
            draw_stick_figure(cx, top_box_y1 + 25)
            bbox = header_font.getbbox(col["name"])
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw/2, top_box_y1 + 48), col["name"], font=header_font, fill=text_color)

            # Bottom Actor
            draw_stick_figure(cx, bot_box_y1 - 10)
            draw.text((cx - tw/2, bot_box_y1 + 32), col["name"], font=header_font, fill=text_color)

        else:
            # Top Header Box
            rx1, ry1, rx2, ry2 = cx - box_w//2, top_box_y1, cx + box_w//2, top_box_y2
            draw.rectangle([rx1, ry1, rx2, ry2], fill=box_fill, outline=box_border, width=2)
            lines = col["name"].split('\n')
            for l_i, l_t in enumerate(lines):
                bbox = header_font.getbbox(l_t)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((cx - tw/2, ry1 + (box_h - len(lines)*18)/2 + l_i*18), l_t, font=header_font, fill=text_color)

            # Bottom Header Box
            rx1, ry1, rx2, ry2 = cx - box_w//2, bot_box_y1, cx + box_w//2, bot_box_y2
            draw.rectangle([rx1, ry1, rx2, ry2], fill=box_fill, outline=box_border, width=2)
            for l_i, l_t in enumerate(lines):
                bbox = header_font.getbbox(l_t)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((cx - tw/2, ry1 + (box_h - len(lines)*18)/2 + l_i*18), l_t, font=header_font, fill=text_color)

    # 15 Step Definitions for Buyer Side Flow
    # (step_num, from_col, to_col, label, is_dashed, is_self)
    steps = [
        (1, 0, 1, "Browse Product Catalog & Filter Frames", False, False),
        (2, 1, 3, "fetchCatalogItems(category, brand)", False, False),
        (3, 3, 5, "SELECT * FROM frames WHERE stock > 0", False, False),
        (4, 5, 1, "Return Available Frames & Lens Catalog Data", True, False),
        (5, 0, 1, "Select Frame & Tap \"View Details & Try-On\"", False, False),
        (6, 1, 2, "Launch 3D VTO Engine & Load Frame Mesh", False, False),
        (7, 2, 2, "MediaPipe: Detect Facial Landmarks & Overlay Frame", False, True),
        (8, 0, 2, "Select Lens Type (Single/Bifocal) & Tap \"Checkout\"", False, False),
        (9, 2, 3, "createOrderCheckout(frame_id, lens_id, prescription_id)", False, False),
        (10, 3, 4, "processBillingAndTax(orderDetails)", False, False),
        (11, 4, 4, "Calculate 18% GST Tax & Generate PDF Invoice", False, True),
        (12, 4, 5, "UPDATE frame SET stock = stock - 1, INSERT INTO orders", False, False),
        (13, 5, 4, "Transaction Committed & Order Saved (Order ID)", True, False),
        (14, 4, 3, "Return Order Status & PDF Invoice Download URL", True, False),
        (15, 3, 0, "Show Order Confirmation & Download Printable Receipt", True, False)
    ]

    start_y = 200
    step_h = 70.0

    def draw_arrow_head(x, y, direction="right", is_open=False):
        head_len = 10
        head_w = 5
        if direction == "right":
            pts = [(x - head_len, y - head_w), (x, y), (x - head_len, y + head_w)]
            if is_open:
                draw.line([pts[0], pts[1]], fill=arrow_color, width=2)
                draw.line([pts[2], pts[1]], fill=arrow_color, width=2)
            else:
                draw.polygon(pts, fill=arrow_color)
        elif direction == "left":
            pts = [(x + head_len, y - head_w), (x, y), (x + head_len, y + head_w)]
            if is_open:
                draw.line([pts[0], pts[1]], fill=arrow_color, width=2)
                draw.line([pts[2], pts[1]], fill=arrow_color, width=2)
            else:
                draw.polygon(pts, fill=arrow_color)

    for idx, (s_num, from_idx, to_idx, label, is_dashed, is_self) in enumerate(steps):
        y = start_y + idx * step_h
        x_from = columns[from_idx]["x"]
        x_to = columns[to_idx]["x"]

        if is_self:
            # Self loop box on the right of x_from
            loop_w = 42
            loop_h = 24
            y_top = y - 8
            y_bot = y_top + loop_h
            
            draw.line([(x_from + 7, y_top), (x_from + loop_w, y_top)], fill=arrow_color, width=2)
            draw.line([(x_from + loop_w, y_top), (x_from + loop_w, y_bot)], fill=arrow_color, width=2)
            draw.line([(x_from + loop_w, y_bot), (x_from + 7, y_bot)], fill=arrow_color, width=2)
            draw_arrow_head(x_from + 7, y_bot, direction="left", is_open=False)

            # Badge for self loop
            badge_x = x_from + 20
            badge_y = y_top
            badge_r = 10
            draw.ellipse([badge_x - badge_r, badge_y - badge_r, badge_x + badge_r, badge_y + badge_r], fill=(0, 0, 0), outline=(0, 0, 0), width=1)
            b_str = str(s_num)
            bbox = badge_font.getbbox(b_str)
            bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((badge_x - bw/2, badge_y - bh/2 - 1), b_str, font=badge_font, fill=(255, 255, 255))

            # Label text
            draw.text((x_from + loop_w + 8, y_top + 2), label, font=label_font, fill=text_color)

        else:
            dir_str = "right" if x_to > x_from else "left"
            margin = 10
            if dir_str == "right":
                ax1 = x_from + margin
                ax2 = x_to - margin
                badge_x = ax1 + 16
            else:
                ax1 = x_from - margin
                ax2 = x_to + margin
                badge_x = ax2 + 16

            # Line
            if is_dashed:
                d_len = 6
                g_len = 5
                cx = ax1
                if dir_str == "right":
                    while cx < ax2:
                        draw.line([(cx, y), (min(cx + d_len, ax2), y)], fill=arrow_color, width=2)
                        cx += d_len + g_len
                else:
                    while cx > ax2:
                        draw.line([(cx, y), (max(cx - d_len, ax2), y)], fill=arrow_color, width=2)
                        cx -= d_len + g_len
                draw_arrow_head(ax2, y, direction=dir_str, is_open=True)
            else:
                draw.line([(ax1, y), (ax2, y)], fill=arrow_color, width=2)
                draw_arrow_head(ax2, y, direction=dir_str, is_open=False)

            # Draw Numbered Badge (Circle with step number)
            badge_r = 11
            draw.ellipse([badge_x - badge_r, y - badge_r, badge_x + badge_r, y + badge_r], fill=(0, 0, 0), outline=(0, 0, 0), width=1)
            b_str = str(s_num)
            bbox = badge_font.getbbox(b_str)
            bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((badge_x - bw/2, y - bh/2 - 1), b_str, font=badge_font, fill=(255, 255, 255))

            # Label text positioned right after badge above the line
            text_x = badge_x + badge_r + 6
            draw.text((text_x, y - 18), label, font=label_font, fill=text_color)

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_buyer_side_diagram()
