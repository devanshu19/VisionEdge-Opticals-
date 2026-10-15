import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_class_diagram():
    # Workspace & Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_class_diagram.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\5afeff16-181e-4c5f-9331-54cb5f42d790"
    artifact_png = os.path.join(artifact_dir, "visionedge_class_diagram.png")

    width = 2400
    height = 1800
    bg_color = (255, 255, 255) # Pure white background
    text_color = (0, 0, 0)     # Black font
    line_color = (0, 0, 0)     # Black lines/arrows

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 32)
        class_name_font = ImageFont.truetype("arialbd.ttf", 16)
        stereo_font = ImageFont.truetype("ariali.ttf", 13)
        attr_font = ImageFont.truetype("arial.ttf", 13)
        mult_font = ImageFont.truetype("arialbd.ttf", 12.5)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 32)
            class_name_font = ImageFont.truetype("segoeuib.ttf", 16)
            stereo_font = ImageFont.truetype("segoeuii.ttf", 13)
            attr_font = ImageFont.truetype("segoeui.ttf", 13)
            mult_font = ImageFont.truetype("segoeuib.ttf", 12.5)
        except IOError:
            title_font = ImageFont.load_default()
            class_name_font = ImageFont.load_default()
            stereo_font = ImageFont.load_default()
            attr_font = ImageFont.load_default()
            mult_font = ImageFont.load_default()

    # Draw Header Title
    title_text = "VisionEdge System - UML Class Diagram"
    bbox = title_font.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 25), title_text, font=title_font, fill=text_color)

    # Subtitle
    sub_text = "White Background Theme with Crisp Black Typography & Standard UML Relationship Notation"
    bbox = attr_font.getbbox(sub_text)
    stw = bbox[2] - bbox[0]
    draw.text(((width - stw) / 2, 65), sub_text, font=attr_font, fill=(60, 60, 60))

    # Helper function to draw a UML Class Box
    def draw_uml_class(x, y, w, title, attrs, methods, stereotype=""):
        title_h = 44 if stereotype else 36
        attr_h = len(attrs) * 19 + 12
        method_h = len(methods) * 19 + 12
        total_h = title_h + attr_h + method_h

        # Outer Box
        draw.rectangle([x, y, x + w, y + total_h], fill=(255, 255, 255), outline=line_color, width=2)

        # Title Section Background
        draw.rectangle([x, y, x + w, y + title_h], fill=(245, 245, 245), outline=line_color, width=1)

        # Stereotype & Title
        if stereotype:
            bbox = stereo_font.getbbox(stereotype)
            stw = bbox[2] - bbox[0]
            draw.text((x + (w - stw) / 2, y + 5), stereotype, font=stereo_font, fill=text_color)
            
            bbox = class_name_font.getbbox(title)
            ctw = bbox[2] - bbox[0]
            draw.text((x + (w - ctw) / 2, y + 22), title, font=class_name_font, fill=text_color)
        else:
            bbox = class_name_font.getbbox(title)
            ctw = bbox[2] - bbox[0]
            draw.text((x + (w - ctw) / 2, y + 8), title, font=class_name_font, fill=text_color)

        # Divider 1
        draw.line([(x, y + title_h), (x + w, y + title_h)], fill=line_color, width=2)

        # Attributes Section
        curr_y = y + title_h + 6
        for attr in attrs:
            draw.text((x + 10, curr_y), attr, font=attr_font, fill=text_color)
            curr_y += 19

        # Divider 2
        method_start_y = y + title_h + attr_h
        draw.line([(x, method_start_y), (x + w, method_start_y)], fill=line_color, width=2)

        # Methods Section
        curr_y = method_start_y + 6
        for m in methods:
            draw.text((x + 10, curr_y), m, font=attr_font, fill=text_color)
            curr_y += 19

        return {
            "x": x, "y": y, "w": w, "h": total_h,
            "center_top": (x + w/2, y),
            "center_bottom": (x + w/2, y + total_h),
            "center_left": (x, y + total_h/2),
            "center_right": (x + w, y + total_h/2)
        }

    classes = {}

    # ROW 1 (y = 110)
    classes["User"] = draw_uml_class(80, 110, 320, "User", [
        "+ id : int [PK]",
        "+ username : String",
        "+ first_name : String",
        "+ last_name : String",
        "+ email : String",
        "+ phone : String",
        "+ password_hash : String",
        "+ role : String = 'Customer'"
    ], [
        "+ to_dict() : dict",
        "+ check_password(pwd) : bool",
        "+ get_full_name() : String"
    ])

    classes["Customer"] = draw_uml_class(500, 110, 360, "Customer", [
        "+ id : int [PK]",
        "+ customer_code : String [UNQ]",
        "+ first_name : String",
        "+ last_name : String",
        "+ phone : String",
        "+ email : String",
        "+ age : int",
        "+ created_by : int [FK]"
    ], [
        "+ to_dict() : dict",
        "+ calculate_age() : int",
        "+ get_clinical_history() : List"
    ])

    classes["CustomerProfile"] = draw_uml_class(960, 110, 340, "CustomerProfile", [
        "+ id : int [PK]",
        "+ customer_id : int [FK, UNQ]",
        "+ blood_group : String",
        "+ eye_conditions : Text",
        "+ allergies : Text",
        "+ notes : Text"
    ], [
        "+ to_dict() : dict",
        "+ update_allergies(text) : void"
    ])

    classes["Appointment"] = draw_uml_class(1400, 110, 360, "Appointment", [
        "+ id : int [PK]",
        "+ customer_id : int [FK]",
        "+ appointment_date : Date",
        "+ appointment_time : Time",
        "+ appointment_type : String",
        "+ doctor_name : String",
        "+ status : String = 'Pending'"
    ], [
        "+ to_dict() : dict",
        "+ confirm_slot() : bool",
        "+ cancel_appointment() : void"
    ])

    classes["Supplier"] = draw_uml_class(1860, 110, 340, "Supplier", [
        "+ id : int [PK]",
        "+ name : String",
        "+ phone : String",
        "+ email : String",
        "+ address : Text"
    ], [
        "+ to_dict() : dict",
        "+ get_supplied_frames() : List"
    ])

    # ROW 2 (y = 620)
    classes["EyeTest"] = draw_uml_class(80, 620, 360, "EyeTest", [
        "+ id : int [PK]",
        "+ customer_id : int [FK]",
        "+ appointment_id : int [FK]",
        "+ right_sphere : String (OD)",
        "+ right_cylinder : String",
        "+ right_axis : String",
        "+ left_sphere : String (OS)",
        "+ left_cylinder : String",
        "+ pd_value : String"
    ], [
        "+ to_dict() : dict",
        "+ validate_diopters() : bool"
    ])

    classes["Prescription"] = draw_uml_class(520, 620, 380, "Prescription", [
        "+ id : int [PK]",
        "+ prescription_number : String",
        "+ customer_id : int [FK]",
        "+ eye_test_id : int [FK]",
        "+ add_power : String",
        "+ prescription_image : String",
        "+ ai_extracted_text : Text",
        "+ confidence_score : Float"
    ], [
        "+ to_dict() : dict",
        "+ verify_ai_accuracy() : float"
    ])

    classes["GeminiAI_OCRService"] = draw_uml_class(1000, 620, 420, "GeminiAI_OCRService", [
        "+ api_key : String",
        "+ model_name : String = 'gemini-1.5-pro'",
        "+ prompt_schema : JSON"
    ], [
        "+ extract_diopters(image_buf) : JSON",
        "+ parse_multimodal_text() : dict",
        "+ calculate_confidence() : float"
    ], stereotype="<<Service>>")

    # ROW 3 (y = 1180)
    classes["Frame"] = draw_uml_class(80, 1180, 360, "Frame", [
        "+ id : int [PK]",
        "+ frame_code : String [UNQ]",
        "+ brand : String",
        "+ model : String",
        "+ shape : String",
        "+ price : Float",
        "+ stock : int",
        "+ vto_image : String"
    ], [
        "+ to_dict() : dict",
        "+ update_stock(qty) : void",
        "+ check_low_inventory() : bool"
    ])

    classes["Lens"] = draw_uml_class(500, 1180, 340, "Lens", [
        "+ id : int [PK]",
        "+ lens_code : String [UNQ]",
        "+ brand : String",
        "+ type : String (Single/Progressive)",
        "+ coating : String",
        "+ price : Float",
        "+ stock : int"
    ], [
        "+ to_dict() : dict",
        "+ update_stock(qty) : void"
    ])

    classes["Order"] = draw_uml_class(940, 1180, 380, "Order", [
        "+ id : int [PK]",
        "+ order_number : String [UNQ]",
        "+ customer_id : int [FK]",
        "+ prescription_id : int [FK]",
        "+ status : String = 'Pending'",
        "+ total_amount : Float",
        "+ created_at : DateTime"
    ], [
        "+ to_dict() : dict",
        "+ calculate_total() : Float",
        "+ update_status(new_status) : void"
    ])

    classes["OrderItem"] = draw_uml_class(1420, 1180, 340, "OrderItem", [
        "+ id : int [PK]",
        "+ order_id : int [FK]",
        "+ frame_id : int [FK]",
        "+ lens_id : int [FK]",
        "+ item_type : String",
        "+ quantity : int",
        "+ unit_price : Float"
    ], [
        "+ to_dict() : dict",
        "+ get_item_subtotal() : Float"
    ])

    classes["BillingInvoice"] = draw_uml_class(1860, 1180, 380, "BillingInvoice", [
        "+ id : int [PK]",
        "+ invoice_number : String [UNQ]",
        "+ order_id : int [FK, UNQ]",
        "+ subtotal : Float",
        "+ tax_amount_18_gst : Float",
        "+ discount_amount : Float",
        "+ grand_total : Float",
        "+ pdf_path : String"
    ], [
        "+ to_dict() : dict",
        "+ generate_pdf_invoice() : String",
        "+ process_payment() : bool"
    ])

    # Orthogonal Line & Arrowhead Drawer
    def draw_orthogonal_arrow(points, arrow_type="association", label="", mult1="", mult2=""):
        # points is a list of (x,y) tuples defining the polyline path
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]
            if arrow_type == "dependency":
                d_len, g_len = 6, 5
                if p1[0] == p2[0]: # Vertical
                    step = 1 if p2[1] > p1[1] else -1
                    cy = p1[1]
                    while (cy < p2[1] if step > 0 else cy > p2[1]):
                        draw.line([(p1[0], cy), (p1[0], min(cy + step * d_len, p2[1]) if step > 0 else max(cy + step * d_len, p2[1]))], fill=line_color, width=2)
                        cy += step * (d_len + g_len)
                else: # Horizontal
                    step = 1 if p2[0] > p1[0] else -1
                    cx = p1[0]
                    while (cx < p2[0] if step > 0 else cx > p2[0]):
                        draw.line([(cx, p1[1]), (min(cx + step * d_len, p2[0]) if step > 0 else max(cx + step * d_len, p2[0]), p1[1])], fill=line_color, width=2)
                        cx += step * (d_len + g_len)
            else:
                draw.line([p1, p2], fill=line_color, width=2)

        # Arrowhead at end point (last segment)
        end_p = points[-1]
        prev_p = points[-2]
        head_w = 7
        head_l = 12

        if arrow_type in ["association", "dependency"]:
            if end_p[0] > prev_p[0]: # Right
                draw.line([(end_p[0] - head_l, end_p[1] - head_w), (end_p[0], end_p[1])], fill=line_color, width=2)
                draw.line([(end_p[0] - head_l, end_p[1] + head_w), (end_p[0], end_p[1])], fill=line_color, width=2)
            elif end_p[0] < prev_p[0]: # Left
                draw.line([(end_p[0] + head_l, end_p[1] - head_w), (end_p[0], end_p[1])], fill=line_color, width=2)
                draw.line([(end_p[0] + head_l, end_p[1] + head_w), (end_p[0], end_p[1])], fill=line_color, width=2)
            elif end_p[1] > prev_p[1]: # Down
                draw.line([(end_p[0] - head_w, end_p[1] - head_l), (end_p[0], end_p[1])], fill=line_color, width=2)
                draw.line([(end_p[0] + head_w, end_p[1] - head_l), (end_p[0], end_p[1])], fill=line_color, width=2)
            elif end_p[1] < prev_p[1]: # Up
                draw.line([(end_p[0] - head_w, end_p[1] + head_l), (end_p[0], end_p[1])], fill=line_color, width=2)
                draw.line([(end_p[0] + head_w, end_p[1] + head_l), (end_p[0], end_p[1])], fill=line_color, width=2)

        elif arrow_type in ["composition", "aggregation"]:
            # Diamond at start point (first segment)
            start_p = points[0]
            next_p = points[1]
            dia_l = 14
            dia_w = 6
            x1, y1 = start_p[0], start_p[1]
            
            if next_p[0] > x1:
                pts = [(x1, y1), (x1 + dia_l/2, y1 - dia_w), (x1 + dia_l, y1), (x1 + dia_l/2, y1 + dia_w)]
            elif next_p[0] < x1:
                pts = [(x1, y1), (x1 - dia_l/2, y1 - dia_w), (x1 - dia_l, y1), (x1 - dia_l/2, y1 + dia_w)]
            elif next_p[1] > y1:
                pts = [(x1, y1), (x1 - dia_w, y1 + dia_l/2), (x1, y1 + dia_l), (x1 + dia_w, y1 + dia_l/2)]
            else:
                pts = [(x1, y1), (x1 - dia_w, y1 - dia_l/2), (x1, y1 - dia_l), (x1 + dia_w, y1 - dia_l/2)]

            fill_c = line_color if arrow_type == "composition" else (255, 255, 255)
            draw.polygon(pts, fill=fill_c, outline=line_color)

        # Labels
        if mult1:
            draw.text((points[0][0] + 8, points[0][1] - 18), mult1, font=mult_font, fill=text_color)
        if mult2:
            draw.text((points[-1][0] - 30, points[-1][1] - 18), mult2, font=mult_font, fill=text_color)
        if label:
            mid_idx = len(points) // 2
            mid_p = points[mid_idx]
            draw.text((mid_p[0] - 25, mid_p[1] - 18), label, font=attr_font, fill=text_color)

    # 1. User 1 ── 0..* Customer
    draw_orthogonal_arrow([(400, 250), (500, 250)], arrow_type="association", label="creates", mult1="1", mult2="0..*")

    # 2. Customer 1 ── 1 CustomerProfile
    draw_orthogonal_arrow([(860, 250), (960, 250)], arrow_type="composition", label="has profile", mult1="1", mult2="1")

    # 3. CustomerProfile 1 ── 0..* Appointment
    draw_orthogonal_arrow([(1300, 250), (1400, 250)], arrow_type="association", label="books", mult1="1", mult2="0..*")

    # 4. Customer 1 ── 0..* EyeTest (Orthogonal loop down)
    draw_orthogonal_arrow([(680, 395), (680, 520), (260, 520), (260, 620)], arrow_type="association", label="undergoes", mult1="1", mult2="0..*")

    # 5. EyeTest 1 ── 0..1 Prescription
    draw_orthogonal_arrow([(440, 780), (520, 780)], arrow_type="association", label="generates", mult1="1", mult2="0..1")

    # 6. Prescription dependency on GeminiAI_OCRService
    draw_orthogonal_arrow([(900, 780), (1000, 780)], arrow_type="dependency", label="uses OCR", mult1="", mult2="")

    # 7. Prescription 1 ── 0..* Order (Orthogonal loop down)
    draw_orthogonal_arrow([(710, 935), (710, 1060), (1130, 1060), (1130, 1180)], arrow_type="association", label="linked to", mult1="1", mult2="0..*")

    # 8. Order 1 ── 1..* OrderItem
    draw_orthogonal_arrow([(1320, 1340), (1420, 1340)], arrow_type="composition", label="contains", mult1="1", mult2="1..*")

    # 9. Frame 1 ── 0..* OrderItem (Orthogonal bottom path)
    draw_orthogonal_arrow([(260, 1495), (260, 1580), (1590, 1580), (1590, 1495)], arrow_type="association", label="ordered in", mult1="1", mult2="0..*")

    # 10. Lens 1 ── 0..* Order
    draw_orthogonal_arrow([(840, 1340), (940, 1340)], arrow_type="association", label="customizes", mult1="1", mult2="0..*")

    # 11. OrderItem 1 ── 1 BillingInvoice
    draw_orthogonal_arrow([(1760, 1340), (1860, 1340)], arrow_type="composition", label="billedup", mult1="1", mult2="1")

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_class_diagram()
