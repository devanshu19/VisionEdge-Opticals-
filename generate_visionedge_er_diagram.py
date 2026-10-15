import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_er_diagram():
    # Workspace & Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_er_diagram.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\5afeff16-181e-4c5f-9331-54cb5f42d790"
    artifact_png = os.path.join(artifact_dir, "visionedge_er_diagram.png")

    width = 2800
    height = 1950
    bg_color = (255, 255, 255) # Pure white background
    text_color = (0, 0, 0)     # Black font
    line_color = (0, 0, 0)     # Black lines/arrows

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 34)
        header_font = ImageFont.truetype("arialbd.ttf", 17)
        stereo_font = ImageFont.truetype("ariali.ttf", 13)
        attr_font = ImageFont.truetype("arial.ttf", 13.5)
        mult_font = ImageFont.truetype("arialbd.ttf", 13)
        label_font = ImageFont.truetype("arialbd.ttf", 13.5)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 34)
            header_font = ImageFont.truetype("segoeuib.ttf", 17)
            stereo_font = ImageFont.truetype("segoeuii.ttf", 13)
            attr_font = ImageFont.truetype("segoeui.ttf", 13.5)
            mult_font = ImageFont.truetype("segoeuib.ttf", 13)
            label_font = ImageFont.truetype("segoeuib.ttf", 13.5)
        except IOError:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            stereo_font = ImageFont.load_default()
            attr_font = ImageFont.load_default()
            mult_font = ImageFont.load_default()
            label_font = ImageFont.load_default()

    # Draw Header Title
    title_text = "VisionEdge System - Entity-Relationship (ER) Diagram"
    bbox = title_font.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 18), title_text, font=title_font, fill=text_color)

    # Subtitle
    sub_text = "Relational Database Architecture: Primary Keys [PK], Foreign Keys [FK], Unique Constraints [UNQ] & Zero Box Cutthroughs"
    bbox = attr_font.getbbox(sub_text)
    stw = bbox[2] - bbox[0]
    draw.text(((width - stw) / 2, 58), sub_text, font=attr_font, fill=(60, 60, 60))

    # Helper function to draw an ER Entity Table Box
    def draw_er_table(x, y, w, table_name, attrs):
        title_h = 44
        attr_h = len(attrs) * 21 + 14
        total_h = title_h + attr_h

        # Outer Box
        draw.rectangle([x, y, x + w, y + total_h], fill=(255, 255, 255), outline=line_color, width=2)

        # Title Section Background
        draw.rectangle([x, y, x + w, y + title_h], fill=(240, 240, 240), outline=line_color, width=1)

        # Stereotype <<Table>>
        bbox = stereo_font.getbbox("<<Table>>")
        stw = bbox[2] - bbox[0]
        draw.text((x + (w - stw) / 2, y + 4), "<<Table>>", font=stereo_font, fill=text_color)

        # Entity Name
        bbox = header_font.getbbox(table_name)
        ctw = bbox[2] - bbox[0]
        draw.text((x + (w - ctw) / 2, y + 21), table_name, font=header_font, fill=text_color)

        # Divider Line
        draw.line([(x, y + title_h), (x + w, y + title_h)], fill=line_color, width=2)

        # Attributes List
        curr_y = y + title_h + 8
        for attr in attrs:
            if "[PK]" in attr or "[FK]" in attr:
                draw.text((x + 12, curr_y), attr, font=label_font, fill=text_color)
            else:
                draw.text((x + 12, curr_y), attr, font=attr_font, fill=text_color)
            curr_y += 21

        return {
            "x": x, "y": y, "w": w, "h": total_h,
            "center_top": (x + w/2, y),
            "center_bottom": (x + w/2, y + total_h),
            "center_left": (x, y + total_h/2),
            "center_right": (x + w, y + total_h/2)
        }

    tables = {}

    # ROW 1 (y = 120): Identity & Customer CRM
    tables["users"] = draw_er_table(100, 120, 360, "users", [
        "id : INTEGER [PK]",
        "username : VARCHAR(80) [UNQ]",
        "email : VARCHAR(120) [UNQ]",
        "password_hash : VARCHAR(255)",
        "role : VARCHAR(20) = 'Customer'",
        "first_name : VARCHAR(50)",
        "last_name : VARCHAR(50)",
        "phone : VARCHAR(20)",
        "created_at : DATETIME"
    ])

    tables["customers"] = draw_er_table(700, 120, 380, "customers", [
        "id : INTEGER [PK]",
        "customer_code : VARCHAR(20) [UNQ]",
        "first_name : VARCHAR(50)",
        "last_name : VARCHAR(50)",
        "phone : VARCHAR(20)",
        "email : VARCHAR(120)",
        "age : INTEGER",
        "created_by : INTEGER [FK -> users.id]",
        "created_at : DATETIME"
    ])

    tables["customer_profiles"] = draw_er_table(1300, 120, 380, "customer_profiles", [
        "id : INTEGER [PK]",
        "customer_id : INTEGER [FK, UNQ]",
        "blood_group : VARCHAR(5)",
        "eye_conditions : TEXT",
        "allergies : TEXT",
        "notes : TEXT",
        "updated_at : DATETIME"
    ])

    tables["appointments"] = draw_er_table(1900, 120, 400, "appointments", [
        "id : INTEGER [PK]",
        "customer_id : INTEGER [FK -> customers.id]",
        "appointment_date : DATE",
        "appointment_time : TIME",
        "appointment_type : VARCHAR(50)",
        "doctor_name : VARCHAR(100)",
        "status : VARCHAR(20) = 'Pending'",
        "created_at : DATETIME"
    ])

    # ROW 2 (y = 580): Clinical Examinations & Prescriptions
    tables["eye_tests"] = draw_er_table(700, 580, 400, "eye_tests", [
        "id : INTEGER [PK]",
        "customer_id : INTEGER [FK -> customers.id]",
        "appointment_id : INTEGER [FK]",
        "right_sphere : VARCHAR(10) (OD)",
        "right_cylinder : VARCHAR(10)",
        "right_axis : VARCHAR(10)",
        "left_sphere : VARCHAR(10) (OS)",
        "left_cylinder : VARCHAR(10)",
        "pd_value : VARCHAR(10)",
        "test_date : DATETIME"
    ])

    tables["prescriptions"] = draw_er_table(1300, 580, 420, "prescriptions", [
        "id : INTEGER [PK]",
        "prescription_number : VARCHAR(30) [UNQ]",
        "customer_id : INTEGER [FK -> customers.id]",
        "eye_test_id : INTEGER [FK -> eye_tests.id]",
        "add_power : VARCHAR(10)",
        "prescription_image : VARCHAR(255)",
        "ai_extracted_text : TEXT",
        "confidence_score : FLOAT",
        "issued_date : DATETIME"
    ])

    # ROW 3 (y = 1050): Inventory Catalog & Eyewear
    tables["suppliers"] = draw_er_table(100, 1050, 360, "suppliers", [
        "id : INTEGER [PK]",
        "name : VARCHAR(100)",
        "phone : VARCHAR(20)",
        "email : VARCHAR(120)",
        "address : TEXT",
        "created_at : DATETIME"
    ])

    tables["frames"] = draw_er_table(700, 1050, 400, "frames", [
        "id : INTEGER [PK]",
        "frame_code : VARCHAR(30) [UNQ]",
        "brand : VARCHAR(50)",
        "model : VARCHAR(50)",
        "shape : VARCHAR(30)",
        "color : VARCHAR(30)",
        "price : FLOAT",
        "stock : INTEGER",
        "vto_image : VARCHAR(255)",
        "supplier_id : INTEGER [FK -> suppliers.id]"
    ])

    tables["lenses"] = draw_er_table(1300, 1050, 380, "lenses", [
        "id : INTEGER [PK]",
        "lens_code : VARCHAR(30) [UNQ]",
        "brand : VARCHAR(50)",
        "type : VARCHAR(50)",
        "coating : VARCHAR(50)",
        "price : FLOAT",
        "stock : INTEGER"
    ])

    # ROW 4 (y = 1520): Sales Orders & Billing Invoices
    tables["orders"] = draw_er_table(700, 1520, 420, "orders", [
        "id : INTEGER [PK]",
        "order_number : VARCHAR(30) [UNQ]",
        "customer_id : INTEGER [FK -> customers.id]",
        "prescription_id : INTEGER [FK]",
        "status : VARCHAR(20) = 'Pending'",
        "subtotal : FLOAT",
        "tax_amount : FLOAT",
        "total_amount : FLOAT",
        "created_at : DATETIME"
    ])

    tables["order_items"] = draw_er_table(1300, 1520, 400, "order_items", [
        "id : INTEGER [PK]",
        "order_id : INTEGER [FK -> orders.id]",
        "frame_id : INTEGER [FK -> frames.id]",
        "lens_id : INTEGER [FK -> lenses.id]",
        "item_type : VARCHAR(20)",
        "quantity : INTEGER",
        "unit_price : FLOAT",
        "subtotal : FLOAT"
    ])

    tables["billing_invoices"] = draw_er_table(1900, 1520, 440, "billing_invoices", [
        "id : INTEGER [PK]",
        "invoice_number : VARCHAR(30) [UNQ]",
        "order_id : INTEGER [FK -> orders.id, UNQ]",
        "subtotal : FLOAT",
        "tax_amount_18_gst : FLOAT",
        "discount_amount : FLOAT",
        "grand_total : FLOAT",
        "pdf_path : VARCHAR(255)",
        "payment_status : VARCHAR(20)"
    ])

    # Smart ER Relationship Line Drawer with direction-aware non-overlapping multiplicity placement
    def draw_er_relationship(points, label="", label_pos=None, mult1="1", mult2="N", mult1_pos=None, mult2_pos=None):
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i+1]
            draw.line([p1, p2], fill=line_color, width=2)

        start_p = points[0]
        end_p = points[-1]
        prev_p = points[-2]
        crow_w = 7
        crow_l = 13

        # Arrowhead at target
        if end_p[0] > prev_p[0]: # Entering from LEFT -> pointing Right
            draw.line([(end_p[0] - crow_l, end_p[1] - crow_w), (end_p[0], end_p[1])], fill=line_color, width=2)
            draw.line([(end_p[0] - crow_l, end_p[1] + crow_w), (end_p[0], end_p[1])], fill=line_color, width=2)
            if not mult2_pos:
                mult2_pos = (end_p[0] - 38, end_p[1] + 6)
        elif end_p[0] < prev_p[0]: # Entering from RIGHT -> pointing Left
            draw.line([(end_p[0] + crow_l, end_p[1] - crow_w), (end_p[0], end_p[1])], fill=line_color, width=2)
            draw.line([(end_p[0] + crow_l, end_p[1] + crow_w), (end_p[0], end_p[1])], fill=line_color, width=2)
            if not mult2_pos:
                mult2_pos = (end_p[0] + 10, end_p[1] + 6)
        elif end_p[1] > prev_p[1]: # Entering from ABOVE -> pointing Down
            draw.line([(end_p[0] - crow_w, end_p[1] - crow_l), (end_p[0], end_p[1])], fill=line_color, width=2)
            draw.line([(end_p[0] + crow_w, end_p[1] - crow_l), (end_p[0], end_p[1])], fill=line_color, width=2)
            if not mult2_pos:
                mult2_pos = (end_p[0] + 10, end_p[1] - 22)
        elif end_p[1] < prev_p[1]: # Entering from BELOW -> pointing Up
            draw.line([(end_p[0] - crow_w, end_p[1] + crow_l), (end_p[0], end_p[1])], fill=line_color, width=2)
            draw.line([(end_p[0] + crow_w, end_p[1] + crow_l), (end_p[0], end_p[1])], fill=line_color, width=2)
            if not mult2_pos:
                mult2_pos = (end_p[0] + 10, end_p[1] + 6)

        if not mult1_pos:
            mult1_pos = (start_p[0] + 10, start_p[1] + 6)

        # Multiplicities
        if mult1:
            draw.text(mult1_pos, mult1, font=mult_font, fill=text_color)
        if mult2:
            draw.text(mult2_pos, mult2, font=mult_font, fill=text_color)

        # Relationship Label
        if label:
            if label_pos:
                lx, ly = label_pos
            else:
                mid_idx = len(points) // 2
                mid_p = points[mid_idx]
                lx, ly = mid_p[0], mid_p[1] - 22
            bbox = label_font.getbbox(label)
            tw = bbox[2] - bbox[0]
            draw.text((lx - tw / 2, ly), label, font=label_font, fill=text_color)

    # 1. users 1 ── 0..N customers (created_by)
    draw_er_relationship([(460, 240), (700, 240)], label="registers", label_pos=(580, 215), mult1="1", mult2="0..N")

    # 2. customers 1 ── 1 customer_profiles (customer_id)
    draw_er_relationship([(1080, 220), (1300, 220)], label="has profile", label_pos=(1190, 195), mult1="1", mult2="1")

    # 3. customers 1 ── 0..N appointments (customer_id) (Routed OVER customer_profiles at y=80!)
    draw_er_relationship([(890, 120), (890, 80), (2100, 80), (2100, 120)], label="books slots", label_pos=(1490, 58), mult1="1", mult2="0..N", mult1_pos=(900, 90), mult2_pos=(2110, 90))

    # 4. customers 1 ── 0..N eye_tests (customer_id)
    draw_er_relationship([(890, 370), (890, 580)], label="undergoes", label_pos=(830, 460), mult1="1", mult2="0..N", mult1_pos=(900, 385), mult2_pos=(900, 555))

    # 5. appointments 1 ── 0..1 eye_tests (appointment_id)
    draw_er_relationship([(1900, 280), (1800, 280), (1800, 520), (1100, 520), (1100, 580)], label="yields test", label_pos=(1450, 495), mult1="1", mult2="0..1", mult2_pos=(1110, 555))

    # 6. eye_tests 1 ── 0..1 prescriptions (eye_test_id)
    draw_er_relationship([(1100, 720), (1300, 720)], label="generates", label_pos=(1200, 695), mult1="1", mult2="0..1")

    # 7. customers 1 ── 0..N prescriptions (customer_id)
    draw_er_relationship([(1080, 340), (1240, 340), (1240, 640), (1300, 640)], label="owns diopters", label_pos=(1240, 480), mult1="1", mult2="0..N", mult1_pos=(1090, 345))

    # 8. suppliers 1 ── 0..N frames (supplier_id)
    draw_er_relationship([(460, 1150), (700, 1150)], label="supplies frames", label_pos=(580, 1125), mult1="1", mult2="0..N")

    # 9. prescriptions 1 ── 0..N orders (prescription_id)
    draw_er_relationship([(1320, 860), (1320, 970), (880, 970), (880, 1520)], label="diopters for", label_pos=(1100, 945), mult1="1", mult2="0..N", mult2_pos=(890, 1495))

    # 10. customers 1 ── 0..N orders (customer_id)
    draw_er_relationship([(730, 370), (600, 370), (600, 1420), (700, 1420), (700, 1520)], label="places orders", label_pos=(660, 1395), mult1="1", mult2="0..N", mult2_pos=(660, 1495))

    # 11. orders 1 ── 1..N order_items (order_id)
    draw_er_relationship([(1120, 1660), (1300, 1660)], label="contains items", label_pos=(1210, 1635), mult1="1", mult2="1..N")

    # 12. frames 1 ── 0..N order_items (frame_id)
    draw_er_relationship([(900, 1350), (900, 1440), (1500, 1440), (1500, 1520)], label="ordered frame", label_pos=(1200, 1415), mult1="1", mult2="0..N", mult2_pos=(1510, 1495))

    # 13. lenses 1 ── 0..N order_items (lens_id)
    draw_er_relationship([(1550, 1290), (1550, 1520)], label="custom lens", label_pos=(1610, 1405), mult1="1", mult2="0..N", mult2_pos=(1560, 1495))

    # 14. orders 1 ── 1 billing_invoices (order_id) (Routed BELOW order_items at y=1830 into billing_invoices.bottom)
    draw_er_relationship([(1120, 1750), (1120, 1830), (2120, 1830), (2120, 1800)], label="billed in GST invoice", label_pos=(1620, 1805), mult1="1", mult2="1", mult2_pos=(2130, 1775))

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_er_diagram()
