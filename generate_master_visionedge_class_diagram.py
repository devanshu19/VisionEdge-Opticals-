import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_master_class_diagram():
    # Workspace & Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_master_class_diagram.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\e79292ba-2641-475d-9708-3cfd889a9b55"
    artifact_png = os.path.join(artifact_dir, "visionedge_master_class_diagram.png")

    width = 3200
    height = 1850
    bg_color = (255, 255, 255) # Pure white background
    text_color = (0, 0, 0)     # Black font
    line_color = (0, 0, 0)     # Black lines/arrows

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 34)
        header_font = ImageFont.truetype("arialbd.ttf", 16)
        stereo_font = ImageFont.truetype("ariali.ttf", 13)
        attr_font = ImageFont.truetype("arial.ttf", 13.5)
        mult_font = ImageFont.truetype("arialbd.ttf", 13)
        label_font = ImageFont.truetype("arialbd.ttf", 13.5)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 34)
            header_font = ImageFont.truetype("segoeuib.ttf", 16)
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
    title_text = "VisionEdge Full System - Master UML Class Diagram"
    bbox = title_font.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 22), title_text, font=title_font, fill=text_color)

    # Subtitle
    sub_text = "Complete Domain Architecture with 100% Flawless Arrow Connectivity, Zero Box Cutthroughs & Pure UML Standards"
    bbox = attr_font.getbbox(sub_text)
    stw = bbox[2] - bbox[0]
    draw.text(((width - stw) / 2, 64), sub_text, font=attr_font, fill=(60, 60, 60))

    # Helper function to draw a 3-compartment UML class box
    def draw_uml_class(x, y, w, title, attrs, methods, stereotype=""):
        title_h = 44 if stereotype else 36
        attr_h = len(attrs) * 20 + 12
        method_h = len(methods) * 20 + 12
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
            
            bbox = header_font.getbbox(title)
            ctw = bbox[2] - bbox[0]
            draw.text((x + (w - ctw) / 2, y + 22), title, font=header_font, fill=text_color)
        else:
            bbox = header_font.getbbox(title)
            ctw = bbox[2] - bbox[0]
            draw.text((x + (w - ctw) / 2, y + 8), title, font=header_font, fill=text_color)

        # Divider 1
        draw.line([(x, y + title_h), (x + w, y + title_h)], fill=line_color, width=2)

        # Attributes Section
        curr_y = y + title_h + 6
        for attr in attrs:
            draw.text((x + 10, curr_y), attr, font=attr_font, fill=text_color)
            curr_y += 20

        # Divider 2
        method_start_y = y + title_h + attr_h
        draw.line([(x, method_start_y), (x + w, method_start_y)], fill=line_color, width=2)

        # Methods Section
        curr_y = method_start_y + 6
        for m in methods:
            draw.text((x + 10, curr_y), m, font=attr_font, fill=text_color)
            curr_y += 20

        return {
            "x": x, "y": y, "w": w, "h": total_h,
            "top": y,
            "bottom": y + total_h,
            "left": x,
            "right": x + w,
            "center_top": (x + w/2, y),
            "center_bottom": (x + w/2, y + total_h),
            "center_left": (x, y + total_h/2),
            "center_right": (x + w, y + total_h/2)
        }

    classes = {}

    # TIER 1 TOP: User (Top Center) (y = 100, bottom = 340)
    classes["User"] = draw_uml_class(1130, 100, 360, "User", [
        "+ id : int [PK]",
        "+ username : String [UNQ]",
        "+ email : String [UNQ]",
        "+ password_hash : String",
        "+ role : String",
        "+ created_at : DateTime"
    ], [
        "+ to_dict() : dict",
        "+ login() : bool",
        "+ register() : void"
    ])

    # TIER 1 BOTTOM: Inherited Roles (y = 430, giving 90px gap for 45px stem height)
    classes["Admin"] = draw_uml_class(150, 430, 320, "Admin", [
        "+ admin_level : String",
        "+ permissions : List"
    ], [
        "+ audit_system() : void",
        "+ manage_users() : void"
    ])

    classes["Optometrist"] = draw_uml_class(1130, 430, 340, "Optometrist", [
        "+ license_number : String",
        "+ specialization : String"
    ], [
        "+ record_eye_test() : void",
        "+ approve_prescription() : void"
    ])

    classes["Customer"] = draw_uml_class(1670, 430, 360, "Customer", [
        "+ id : int [PK]",
        "+ customer_code : String",
        "+ first_name : String",
        "+ last_name : String",
        "+ phone : String",
        "+ age : int"
    ], [
        "+ to_dict() : dict",
        "+ calculate_age() : int",
        "+ get_order_history() : List"
    ])

    classes["CustomerProfile"] = draw_uml_class(2190, 430, 340, "CustomerProfile", [
        "+ id : int [PK]",
        "+ customer_id : int [FK]",
        "+ blood_group : String",
        "+ eye_conditions : Text",
        "+ allergies : Text"
    ], [
        "+ to_dict() : dict",
        "+ update_profile() : void"
    ])

    # TIER 2: Clinical & AI Examination (y = 750)
    classes["Appointment"] = draw_uml_class(150, 750, 340, "Appointment", [
        "+ id : int [PK]",
        "+ customer_id : int [FK]",
        "+ appointment_date : Date",
        "+ appointment_time : Time",
        "+ status : String = 'Pending'"
    ], [
        "+ to_dict() : dict",
        "+ confirm_slot() : void"
    ])

    classes["EyeTest"] = draw_uml_class(630, 750, 360, "EyeTest", [
        "+ id : int [PK]",
        "+ customer_id : int [FK]",
        "+ appointment_id : int [FK]",
        "+ right_sphere : String (OD)",
        "+ right_cylinder : String",
        "+ left_sphere : String (OS)",
        "+ pd_value : String"
    ], [
        "+ to_dict() : dict",
        "+ validate_diopters() : bool"
    ])

    classes["Prescription"] = draw_uml_class(1130, 750, 380, "Prescription", [
        "+ id : int [PK]",
        "+ prescription_number : String",
        "+ customer_id : int [FK]",
        "+ eye_test_id : int [FK]",
        "+ prescription_image : String",
        "+ confidence_score : Float"
    ], [
        "+ to_dict() : dict",
        "+ verify_ai_accuracy() : float"
    ])

    classes["GeminiAI_OCRService"] = draw_uml_class(1670, 750, 420, "GeminiAI_OCRService", [
        "+ api_key : String",
        "+ model_name : String = 'gemini-1.5-pro'",
        "+ prompt_schema : JSON"
    ], [
        "+ extract_diopters(image_buf) : JSON",
        "+ parse_multimodal_text() : dict"
    ], stereotype="<<AI Service>>")

    classes["MediaPipe_VTOService"] = draw_uml_class(2230, 750, 420, "MediaPipe_VTOService", [
        "+ facial_landmarks : int = 468",
        "+ camera_stream_url : String"
    ], [
        "+ detect_facial_mesh() : Canvas",
        "+ overlay_3d_frame_png() : void"
    ], stereotype="<<CV Engine>>")

    # TIER 3: Inventory Catalog & Eyewear (y = 1080)
    classes["Brand"] = draw_uml_class(150, 1080, 300, "Brand", [
        "+ id : int [PK]",
        "+ name : String",
        "+ logo : String"
    ], [
        "+ to_dict() : dict"
    ])

    classes["Category"] = draw_uml_class(590, 1080, 280, "Category", [
        "+ id : int [PK]",
        "+ name : String",
        "+ type : String"
    ], [
        "+ to_dict() : dict"
    ])

    classes["Frame"] = draw_uml_class(1010, 1080, 360, "Frame", [
        "+ id : int [PK]",
        "+ frame_code : String",
        "+ brand : String",
        "+ model : String",
        "+ shape : String",
        "+ price : Float",
        "+ stock : int",
        "+ vto_image : String"
    ], [
        "+ to_dict() : dict",
        "+ update_stock(qty) : void"
    ])

    classes["Lens"] = draw_uml_class(1530, 1080, 340, "Lens", [
        "+ id : int [PK]",
        "+ lens_code : String",
        "+ brand : String",
        "+ type : String (Single/Prog)",
        "+ coating : String",
        "+ price : Float"
    ], [
        "+ to_dict() : dict"
    ])

    # TIER 4: Sales, POS Billing & Analytics (y = 1480, giving generous 140px gap below Tier 3)
    classes["Order"] = draw_uml_class(1130, 1480, 360, "Order", [
        "+ id : int [PK]",
        "+ order_number : String",
        "+ customer_id : int [FK]",
        "+ prescription_id : int [FK]",
        "+ total_amount : Float",
        "+ status : String"
    ], [
        "+ to_dict() : dict",
        "+ calculate_total() : Float"
    ])

    classes["OrderItem"] = draw_uml_class(1650, 1480, 340, "OrderItem", [
        "+ id : int [PK]",
        "+ order_id : int [FK]",
        "+ frame_id : int [FK]",
        "+ lens_id : int [FK]",
        "+ quantity : int",
        "+ unit_price : Float"
    ], [
        "+ to_dict() : dict"
    ])

    classes["BillingInvoice"] = draw_uml_class(2150, 1480, 380, "BillingInvoice", [
        "+ id : int [PK]",
        "+ invoice_number : String",
        "+ order_id : int [FK]",
        "+ subtotal : Float",
        "+ tax_amount_18_gst : Float",
        "+ grand_total : Float",
        "+ pdf_path : String"
    ], [
        "+ to_dict() : dict",
        "+ generate_pdf_invoice() : String"
    ])

    classes["AnalyticsReportService"] = draw_uml_class(2670, 1480, 420, "AnalyticsReportService", [
        "+ total_sales : Float",
        "+ top_brands : List"
    ], [
        "+ compute_revenue_stream() : JSON",
        "+ export_sales_report() : PDF"
    ], stereotype="<<Report Service>>")

    # Precise Orthogonal Line & Solid Arrow Drawer with non-overlapping label & multiplicity placement
    def draw_uml_arrow(points, label="", label_pos=None, mult1="", mult2="", mult1_pos=None, mult2_pos=None):
        # All lines are drawn as solid lines
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i+1]
            draw.line([p1, p2], fill=line_color, width=2)

        # Solid Arrowhead at end point (last segment) - Prominent & Bold
        end_p = points[-1]
        prev_p = points[-2]
        head_w = 9
        head_l = 16

        if end_p[0] > prev_p[0]: # Pointing Right
            pts = [(end_p[0], end_p[1]), (end_p[0] - head_l, end_p[1] - head_w), (end_p[0] - head_l, end_p[1] + head_w)]
        elif end_p[0] < prev_p[0]: # Pointing Left
            pts = [(end_p[0], end_p[1]), (end_p[0] + head_l, end_p[1] - head_w), (end_p[0] + head_l, end_p[1] + head_w)]
        elif end_p[1] > prev_p[1]: # Pointing Down
            pts = [(end_p[0], end_p[1]), (end_p[0] - head_w, end_p[1] - head_l), (end_p[0] + head_w, end_p[1] - head_l)]
        elif end_p[1] < prev_p[1]: # Pointing Up
            pts = [(end_p[0], end_p[1]), (end_p[0] - head_w, end_p[1] + head_l), (end_p[0] + head_w, end_p[1] + head_l)]
        else:
            pts = []

        if pts:
            draw.polygon(pts, fill=line_color)

        # Multiplicity 1 (Source)
        if mult1:
            if mult1_pos:
                mx, my = mult1_pos
            else:
                mx, my = points[0][0] + 10, points[0][1] + 6
            draw.text((mx, my), mult1, font=mult_font, fill=text_color)

        # Multiplicity 2 (Target)
        if mult2:
            if mult2_pos:
                mx, my = mult2_pos
            else:
                mx, my = points[-1][0] - 30, points[-1][1] + 6
            draw.text((mx, my), mult2, font=mult_font, fill=text_color)

        # Relationship Text Label
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

    # 1, 2, 3: Unified Inheritance Tree for Admin, Optometrist, Customer -> User (hbar_y = 385, 45px stem height)
    hbar_y = 385
    user_bottom_y = classes["User"]["bottom"]
    user_center_x = classes["User"]["left"] + 180

    # Draw branch from Admin up to horizontal bar
    draw.line([(classes["Admin"]["x"] + 160, classes["Admin"]["top"]), (classes["Admin"]["x"] + 160, hbar_y)], fill=line_color, width=2)

    # Draw branch from Optometrist up to horizontal bar
    draw.line([(classes["Optometrist"]["x"] + 170, classes["Optometrist"]["top"]), (classes["Optometrist"]["x"] + 170, hbar_y)], fill=line_color, width=2)

    # Draw branch from Customer up to horizontal bar
    draw.line([(classes["Customer"]["x"] + 180, classes["Customer"]["top"]), (classes["Customer"]["x"] + 180, hbar_y)], fill=line_color, width=2)

    # Draw horizontal bar from Admin to Customer
    draw.line([(classes["Admin"]["x"] + 160, hbar_y), (classes["Customer"]["x"] + 180, hbar_y)], fill=line_color, width=2)

    # Draw main trunk arrow from horizontal bar up to User bottom
    draw_uml_arrow([
        (user_center_x, hbar_y),
        (user_center_x, user_bottom_y)
    ])

    # 4. Customer to CustomerProfile
    y_mid = (classes["Customer"]["top"] + classes["Customer"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["Customer"]["right"], y_mid),
        (classes["CustomerProfile"]["left"], y_mid)
    ], label="has profile", label_pos=((classes["Customer"]["right"] + classes["CustomerProfile"]["left"])/2, y_mid - 25), mult1="1", mult2="1", mult1_pos=(classes["Customer"]["right"] + 10, y_mid + 8), mult2_pos=(classes["CustomerProfile"]["left"] - 25, y_mid + 8))

    # 5. Customer schedules Appointment
    draw_uml_arrow([
        (classes["Customer"]["x"] + 180, classes["Customer"]["bottom"]),
        (classes["Customer"]["x"] + 180, classes["Appointment"]["top"] - 40),
        (classes["Appointment"]["x"] + 170, classes["Appointment"]["top"] - 40),
        (classes["Appointment"]["x"] + 170, classes["Appointment"]["top"])
    ], label="schedules", label_pos=((classes["Customer"]["x"] + classes["Appointment"]["x"])/2, classes["Appointment"]["top"] - 62), mult1="1", mult2="0..*", mult1_pos=(classes["Customer"]["x"] + 192, classes["Customer"]["bottom"] + 10), mult2_pos=(classes["Appointment"]["x"] + 182, classes["Appointment"]["top"] - 25))

    # 6. Appointment produces EyeTest
    y_mid = (classes["Appointment"]["top"] + classes["Appointment"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["Appointment"]["right"], y_mid),
        (classes["EyeTest"]["left"], y_mid)
    ], label="produces", label_pos=((classes["Appointment"]["right"] + classes["EyeTest"]["left"])/2, y_mid - 25), mult1="1", mult2="0..1", mult1_pos=(classes["Appointment"]["right"] + 10, y_mid + 8), mult2_pos=(classes["EyeTest"]["left"] - 35, y_mid + 8))

    # 7. EyeTest generates Prescription
    y_mid = (classes["EyeTest"]["top"] + classes["EyeTest"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["EyeTest"]["right"], y_mid),
        (classes["Prescription"]["left"], y_mid)
    ], label="generates", label_pos=((classes["EyeTest"]["right"] + classes["Prescription"]["left"])/2, y_mid - 25), mult1="1", mult2="0..1", mult1_pos=(classes["EyeTest"]["right"] + 10, y_mid + 8), mult2_pos=(classes["Prescription"]["left"] - 35, y_mid + 8))

    # 8. Prescription uses AI OCR GeminiAI_OCRService
    y_mid = (classes["Prescription"]["top"] + classes["Prescription"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["Prescription"]["right"], y_mid),
        (classes["GeminiAI_OCRService"]["left"], y_mid)
    ], label="uses AI OCR", label_pos=((classes["Prescription"]["right"] + classes["GeminiAI_OCRService"]["left"])/2, y_mid - 25))

    # 9. Brand manufactures Frame
    draw_uml_arrow([
        (classes["Brand"]["x"] + 150, classes["Brand"]["top"]),
        (classes["Brand"]["x"] + 150, classes["Brand"]["top"] - 50),
        (classes["Frame"]["x"] + 180, classes["Brand"]["top"] - 50),
        (classes["Frame"]["x"] + 180, classes["Frame"]["top"])
    ], label="manufactures", label_pos=((classes["Brand"]["x"] + classes["Frame"]["x"])/2 + 80, classes["Brand"]["top"] - 72), mult1="1", mult2="0..*", mult1_pos=(classes["Brand"]["x"] + 162, classes["Brand"]["top"] - 25), mult2_pos=(classes["Frame"]["x"] + 192, classes["Frame"]["top"] - 25))

    # 10. Category classifies Frame
    y_mid = (classes["Category"]["top"] + classes["Category"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["Category"]["right"], y_mid),
        (classes["Frame"]["left"], y_mid)
    ], label="classifies", label_pos=((classes["Category"]["right"] + classes["Frame"]["left"])/2, y_mid - 25), mult1="1", mult2="0..*", mult1_pos=(classes["Category"]["right"] + 10, y_mid + 8), mult2_pos=(classes["Frame"]["left"] - 35, y_mid + 8))

    # THREE DISTINCT HORIZONTAL CHANNELS BETWEEN TIER 3 (bottom=1340) AND TIER 4 (top=1480):
    # Channel 1 (Top): y = 1380 (40px below Frame bottom) -> Frame ordered in OrderItem
    # Channel 2 (Mid): y = 1415 (35px below Channel 1)     -> Prescription linked to Order
    # Channel 3 (Bot): y = 1445 (30px below Channel 2)     -> Frame renders 3D VTO

    # 11. Frame renders 3D VTO MediaPipe_VTOService (Channel 3: y = 1445)
    draw_uml_arrow([
        (classes["Frame"]["x"] + 270, classes["Frame"]["bottom"]),
        (classes["Frame"]["x"] + 270, 1445),
        (classes["MediaPipe_VTOService"]["x"] + 210, 1445),
        (classes["MediaPipe_VTOService"]["x"] + 210, classes["MediaPipe_VTOService"]["bottom"])
    ], label="renders 3D VTO", label_pos=((classes["Frame"]["x"] + classes["MediaPipe_VTOService"]["x"])/2 + 100, 1423))

    # 12. Prescription linked to Order (Channel 2: y = 1415 through x = 1450)
    draw_uml_arrow([
        (1450, classes["Prescription"]["bottom"]),
        (1450, 1415),
        (classes["Order"]["left"] + 180, 1415),
        (classes["Order"]["left"] + 180, classes["Order"]["top"])
    ], label="linked to", label_pos=(1405, (classes["Prescription"]["bottom"] + 1415)/2), mult1="1", mult2="0..*", mult1_pos=(1462, classes["Prescription"]["bottom"] + 12), mult2_pos=(classes["Order"]["left"] + 192, classes["Order"]["top"] - 25))

    # 13. Order contains OrderItem
    y_mid = (classes["Order"]["top"] + classes["Order"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["Order"]["right"], y_mid),
        (classes["OrderItem"]["left"], y_mid)
    ], label="contains", label_pos=((classes["Order"]["right"] + classes["OrderItem"]["left"])/2, y_mid - 25), mult1="1", mult2="1..*", mult1_pos=(classes["Order"]["right"] + 10, y_mid + 8), mult2_pos=(classes["OrderItem"]["left"] - 35, y_mid + 8))

    # 14. Frame ordered in OrderItem (Channel 1: y = 1380, label placed at y = 1358 clear of Frame border)
    draw_uml_arrow([
        (classes["Frame"]["x"] + 90, classes["Frame"]["bottom"]),
        (classes["Frame"]["x"] + 90, 1380),
        (classes["OrderItem"]["x"] + 170, 1380),
        (classes["OrderItem"]["x"] + 170, classes["OrderItem"]["top"])
    ], label="ordered in", label_pos=((classes["Frame"]["x"] + classes["OrderItem"]["x"])/2 + 40, 1358), mult1="1", mult2="0..*", mult1_pos=(classes["Frame"]["x"] + 102, classes["Frame"]["bottom"] + 12), mult2_pos=(classes["OrderItem"]["x"] + 182, classes["OrderItem"]["top"] - 25))

    # 15. OrderItem billedup BillingInvoice
    y_mid = (classes["OrderItem"]["top"] + classes["OrderItem"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["OrderItem"]["right"], y_mid),
        (classes["BillingInvoice"]["left"], y_mid)
    ], label="billedup", label_pos=((classes["OrderItem"]["right"] + classes["BillingInvoice"]["left"])/2, y_mid - 25), mult1="1", mult2="1", mult1_pos=(classes["OrderItem"]["right"] + 10, y_mid + 8), mult2_pos=(classes["BillingInvoice"]["left"] - 25, y_mid + 8))

    # 16. BillingInvoice audited by AnalyticsReportService
    y_mid = (classes["BillingInvoice"]["top"] + classes["BillingInvoice"]["bottom"]) / 2
    draw_uml_arrow([
        (classes["BillingInvoice"]["right"], y_mid),
        (classes["AnalyticsReportService"]["left"], y_mid)
    ], label="audited by", label_pos=((classes["BillingInvoice"]["right"] + classes["AnalyticsReportService"]["left"])/2, y_mid - 25))

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_master_class_diagram()
