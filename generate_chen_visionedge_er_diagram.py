import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def generate_chen_er_diagram():
    # Workspace & Artifact Paths
    output_dir = r"c:\projects\VisionEdge\diagrams\png"
    os.makedirs(output_dir, exist_ok=True)
    workspace_png = os.path.join(output_dir, "visionedge_chen_er_diagram.png")
    artifact_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\5afeff16-181e-4c5f-9331-54cb5f42d790"
    artifact_png = os.path.join(artifact_dir, "visionedge_chen_er_diagram.png")

    width = 2800
    height = 3100
    bg_color = (255, 255, 255) # Pure white background
    text_color = (0, 0, 0)     # Black font
    line_color = (0, 0, 0)     # Black lines/outlines

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 34)
        entity_font = ImageFont.truetype("arialbd.ttf", 17)
        diamond_font = ImageFont.truetype("ariali.ttf", 13.5)
        oval_font = ImageFont.truetype("arial.ttf", 13)
        mult_font = ImageFont.truetype("arialbd.ttf", 15)
        sub_font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        try:
            title_font = ImageFont.truetype("segoeui.ttf", 34)
            entity_font = ImageFont.truetype("segoeuib.ttf", 17)
            diamond_font = ImageFont.truetype("segoeuii.ttf", 13.5)
            oval_font = ImageFont.truetype("segoeui.ttf", 13)
            mult_font = ImageFont.truetype("segoeuib.ttf", 15)
            sub_font = ImageFont.truetype("segoeui.ttf", 14)
        except IOError:
            title_font = ImageFont.load_default()
            entity_font = ImageFont.load_default()
            diamond_font = ImageFont.load_default()
            oval_font = ImageFont.load_default()
            mult_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()

    # Draw Header Title
    title_text = "VISIONEDGE SYSTEM - COMPLETE RELATIONAL CONNECTIVITY & ER DIAGRAM"
    bbox = title_font.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 25), title_text, font=title_font, fill=text_color)

    # Subtitle
    sub_text = "Traditional Chen's ER Model Architecture: Entity Rectangles, Relationship Diamonds, Attribute Ovals & Cardinalities"
    bbox = sub_font.getbbox(sub_text)
    stw = bbox[2] - bbox[0]
    draw.text(((width - stw) / 2, 70), sub_text, font=sub_font, fill=(60, 60, 60))

    # Helper: Rounded Entity Box
    def draw_entity(cx, cy, w, h, text):
        x1, y1 = cx - w/2, cy - h/2
        x2, y2 = cx + w/2, cy + h/2
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(255, 255, 255), outline=line_color, width=2)
        bbox = entity_font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw/2, cy - th/2 - 2), text, font=entity_font, fill=text_color)
        return {"cx": cx, "cy": cy, "w": w, "h": h, "bounds": (x1, y1, x2, y2)}

    # Helper: Relationship Diamond
    def draw_diamond(cx, cy, w, h, text):
        pts = [(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)]
        draw.polygon(pts, fill=(255, 255, 255), outline=line_color)
        draw.line([pts[0], pts[1]], fill=line_color, width=2)
        draw.line([pts[1], pts[2]], fill=line_color, width=2)
        draw.line([pts[2], pts[3]], fill=line_color, width=2)
        draw.line([pts[3], pts[0]], fill=line_color, width=2)
        bbox = diamond_font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw/2, cy - th/2 - 2), text, font=diamond_font, fill=text_color)
        return {"cx": cx, "cy": cy, "w": w, "h": h, "top": pts[0], "right": pts[1], "bottom": pts[2], "left": pts[3]}

    # Helper: Attribute Oval
    def draw_oval(cx, cy, text, w=110, h=36):
        x1, y1 = cx - w/2, cy - h/2
        x2, y2 = cx + w/2, cy + h/2
        draw.ellipse([x1, y1, x2, y2], fill=(255, 255, 255), outline=line_color, width=2)
        bbox = oval_font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw/2, cy - th/2 - 2), text, font=oval_font, fill=text_color)
        return {"cx": cx, "cy": cy, "w": w, "h": h}

    # Helper: Perimeter-to-Perimeter connection between Entity Box and Oval
    def connect_entity_oval(entity_obj, oval_obj, width=1.5):
        (x1, y1, x2, y2) = entity_obj["bounds"]
        ox, oy = oval_obj["cx"], oval_obj["cy"]
        ow, oh = oval_obj["w"], oval_obj["h"]

        # Nearest point on rectangle boundary to oval center
        rx = max(x1, min(ox, x2))
        ry = max(y1, min(oy, y2))

        # Nearest point on oval boundary to (rx, ry)
        angle = math.atan2(ry - oy, rx - ox)
        opx = ox + (ow / 2.0) * math.cos(angle)
        opy = oy + (oh / 2.0) * math.sin(angle)

        draw.line([(rx, ry), (opx, opy)], fill=line_color, width=int(width))

    # Helper: Connect two points
    def connect(p1, p2, width=2):
        draw.line([p1, p2], fill=line_color, width=int(width))

    # =========================================================================
    # MASTER VERTICAL SPINE ENTITIES & DIAMONDS
    # =========================================================================

    # 1. USER (Tier 0)
    e_user = draw_entity(1400, 160, 280, 58, "user")
    connect_entity_oval(e_user, draw_oval(1250, 95, "id", w=80, h=32))
    connect_entity_oval(e_user, draw_oval(1100, 160, "username", w=110, h=34))
    connect_entity_oval(e_user, draw_oval(1250, 225, "email", w=95, h=32))
    connect_entity_oval(e_user, draw_oval(1550, 95, "phone", w=95, h=32))
    connect_entity_oval(e_user, draw_oval(1700, 160, "created_at", w=115, h=34))
    connect_entity_oval(e_user, draw_oval(1550, 225, "role", w=85, h=32))

    # Right Branch 0: audit_log
    d_audit = draw_diamond(1900, 160, 150, 52, "logs_action")
    connect((e_user["cx"] + e_user["w"]/2, 160), d_audit["left"])
    e_audit = draw_entity(2240, 160, 260, 58, "audit_log")
    connect(d_audit["right"], (e_audit["cx"] - e_audit["w"]/2, 160))
    connect_entity_oval(e_audit, draw_oval(2080, 240, "id", w=75, h=32))
    connect_entity_oval(e_audit, draw_oval(2240, 240, "action", w=95, h=32))
    connect_entity_oval(e_audit, draw_oval(2400, 240, "resource", w=105, h=32))
    connect_entity_oval(e_audit, draw_oval(2240, 290, "timestamp", w=110, h=34))

    # Diamond 1: registers (User -> Customer)
    d_reg = draw_diamond(1400, 310, 160, 56, "registers")
    connect((1400, e_user["cy"] + e_user["h"]/2), d_reg["top"])
    draw.text((1415, 215), "1", font=mult_font, fill=text_color)

    # 2. CUSTOMER (Tier 1)
    e_cust = draw_entity(1400, 460, 280, 58, "customer")
    connect(d_reg["bottom"], (1400, e_cust["cy"] - e_cust["h"]/2))
    draw.text((1415, 385), "M", font=mult_font, fill=text_color)

    connect_entity_oval(e_cust, draw_oval(1290, 535, "id", w=75, h=32))
    connect_entity_oval(e_cust, draw_oval(1150, 585, "customer_code", w=130, h=34))
    connect_entity_oval(e_cust, draw_oval(1320, 595, "first_name", w=110, h=34))
    connect_entity_oval(e_cust, draw_oval(1480, 595, "last_name", w=110, h=34))
    connect_entity_oval(e_cust, draw_oval(1530, 535, "phone", w=95, h=32))

    # Left Branch 1: customer_profile
    d_prof = draw_diamond(980, 460, 150, 52, "has_profile")
    connect((e_cust["cx"] - e_cust["w"]/2, 460), d_prof["right"])
    e_prof = draw_entity(580, 460, 280, 58, "customer_profile")
    connect(d_prof["left"], (e_prof["cx"] + e_prof["w"]/2, 460))
    connect_entity_oval(e_prof, draw_oval(430, 535, "id", w=75, h=32))
    connect_entity_oval(e_prof, draw_oval(560, 545, "blood_group", w=115, h=34))
    connect_entity_oval(e_prof, draw_oval(430, 595, "eye_conditions", w=130, h=34))
    connect_entity_oval(e_prof, draw_oval(580, 605, "allergies", w=105, h=32))

    # Right Branch 1: chat_history
    d_chat = draw_diamond(1820, 460, 150, 52, "sends_chat")
    connect((e_cust["cx"] + e_cust["w"]/2, 460), d_chat["left"])
    e_chat = draw_entity(2240, 460, 260, 58, "chat_history")
    connect(d_chat["right"], (e_chat["cx"] - e_chat["w"]/2, 460))
    connect_entity_oval(e_chat, draw_oval(2080, 535, "id", w=75, h=32))
    connect_entity_oval(e_chat, draw_oval(2240, 535, "question", w=105, h=32))
    connect_entity_oval(e_chat, draw_oval(2400, 535, "response", w=105, h=32))
    connect_entity_oval(e_chat, draw_oval(2240, 590, "created_at", w=115, h=34))

    # Diamond 2: schedules (Customer -> Appointment)
    d_sched = draw_diamond(1400, 690, 160, 56, "schedules")
    connect((1400, e_cust["cy"] + e_cust["h"]/2), d_sched["top"])
    draw.text((1415, 515), "1", font=mult_font, fill=text_color)

    # 3. APPOINTMENT (Tier 2)
    e_appt = draw_entity(1400, 840, 280, 58, "appointment")
    connect(d_sched["bottom"], (1400, e_appt["cy"] - e_appt["h"]/2))
    draw.text((1415, 765), "M", font=mult_font, fill=text_color)

    connect_entity_oval(e_appt, draw_oval(1290, 915, "id", w=75, h=32))
    connect_entity_oval(e_appt, draw_oval(1140, 965, "appointment_date", w=140, h=34))
    connect_entity_oval(e_appt, draw_oval(1320, 975, "appointment_time", w=140, h=34))
    connect_entity_oval(e_appt, draw_oval(1480, 975, "type", w=85, h=32))
    connect_entity_oval(e_appt, draw_oval(1550, 915, "doctor_name", w=115, h=34))

    # Left Branch 2: frame_recommendation
    d_frame_rec = draw_diamond(960, 840, 160, 52, "matches_face")
    connect((e_appt["cx"] - e_appt["w"]/2, 840), d_frame_rec["right"])
    e_frame_rec = draw_entity(560, 840, 300, 58, "frame_recommendation")
    connect(d_frame_rec["left"], (e_frame_rec["cx"] + e_frame_rec["w"]/2, 840))
    connect_entity_oval(e_frame_rec, draw_oval(410, 915, "id", w=75, h=32))
    connect_entity_oval(e_frame_rec, draw_oval(560, 935, "face_shape", w=115, h=34))
    connect_entity_oval(e_frame_rec, draw_oval(410, 975, "selected_frames", w=135, h=34))

    # Right Branch 2: notification
    d_notif = draw_diamond(1840, 840, 160, 52, "receives_alert")
    connect((e_appt["cx"] + e_appt["w"]/2, 840), d_notif["left"])
    e_notif = draw_entity(2240, 840, 260, 58, "notification")
    connect(d_notif["right"], (e_notif["cx"] - e_notif["w"]/2, 840))
    connect_entity_oval(e_notif, draw_oval(2080, 915, "id", w=75, h=32))
    connect_entity_oval(e_notif, draw_oval(2240, 915, "title", w=85, h=32))
    connect_entity_oval(e_notif, draw_oval(2400, 915, "message", w=95, h=32))
    connect_entity_oval(e_notif, draw_oval(2240, 970, "status", w=85, h=32))

    # Diamond 3: leads_to (Appointment -> EyeTest)
    d_leads = draw_diamond(1400, 1070, 160, 56, "leads_to")
    connect((1400, e_appt["cy"] + e_appt["h"]/2), d_leads["top"])
    draw.text((1415, 895), "1", font=mult_font, fill=text_color)

    # 4. EYE_TEST (Tier 3)
    e_eyetest = draw_entity(1400, 1220, 280, 58, "eye_test")
    connect(d_leads["bottom"], (1400, e_eyetest["cy"] - e_eyetest["h"]/2))
    draw.text((1415, 1145), "1", font=mult_font, fill=text_color)

    connect_entity_oval(e_eyetest, draw_oval(1290, 1295, "right_sphere", w=115, h=34))
    connect_entity_oval(e_eyetest, draw_oval(1150, 1345, "right_cylinder", w=125, h=34))
    connect_entity_oval(e_eyetest, draw_oval(1320, 1355, "left_sphere", w=115, h=34))
    connect_entity_oval(e_eyetest, draw_oval(1480, 1355, "left_cylinder", w=125, h=34))
    connect_entity_oval(e_eyetest, draw_oval(1550, 1295, "pd_value", w=95, h=32))

    # Diamond 4: generates (EyeTest -> Prescription)
    d_gen = draw_diamond(1400, 1470, 160, 56, "generates")
    connect((1400, e_eyetest["cy"] + e_eyetest["h"]/2), d_gen["top"])
    draw.text((1415, 1275), "1", font=mult_font, fill=text_color)

    # 5. PRESCRIPTION (Tier 4)
    e_presc = draw_entity(1400, 1620, 280, 58, "prescription")
    connect(d_gen["bottom"], (1400, e_presc["cy"] - e_presc["h"]/2))
    draw.text((1415, 1545), "1", font=mult_font, fill=text_color)

    connect_entity_oval(e_presc, draw_oval(1290, 1695, "id", w=75, h=32))
    connect_entity_oval(e_presc, draw_oval(1130, 1745, "prescription_number", w=150, h=34))
    connect_entity_oval(e_presc, draw_oval(1330, 1755, "camera_given_text", w=150, h=34))
    connect_entity_oval(e_presc, draw_oval(1510, 1755, "with_vto", w=95, h=32))
    connect_entity_oval(e_presc, draw_oval(1550, 1695, "add_val", w=85, h=32))

    # Left Branch 4: virtual_try_on_history
    d_vto = draw_diamond(960, 1620, 150, 52, "serves_vto")
    connect((e_presc["cx"] - e_presc["w"]/2, 1620), d_vto["right"])
    e_vto = draw_entity(560, 1620, 300, 58, "virtual_try_on_history")
    connect(d_vto["left"], (e_vto["cx"] + e_vto["w"]/2, 1620))
    connect_entity_oval(e_vto, draw_oval(410, 1695, "id", w=75, h=32))
    connect_entity_oval(e_vto, draw_oval(560, 1715, "original_image", w=130, h=34))
    connect_entity_oval(e_vto, draw_oval(410, 1755, "tryon_image", w=115, h=34))

    # Right Branch 4: lens_recommendation
    d_lens_rec = draw_diamond(1840, 1620, 160, 52, "drives_rec")
    connect((e_presc["cx"] + e_presc["w"]/2, 1620), d_lens_rec["left"])
    e_lens_rec = draw_entity(2240, 1620, 280, 58, "lens_recommendation")
    connect(d_lens_rec["right"], (e_lens_rec["cx"] - e_lens_rec["w"]/2, 1620))
    connect_entity_oval(e_lens_rec, draw_oval(2080, 1695, "id", w=75, h=32))
    connect_entity_oval(e_lens_rec, draw_oval(2260, 1715, "recommended_lens", w=150, h=34))
    connect_entity_oval(e_lens_rec, draw_oval(2080, 1755, "reason", w=95, h=32))

    # Diamond 5: applied_in (Prescription -> Order)
    d_app = draw_diamond(1400, 1850, 160, 56, "applied_in")
    connect((1400, e_presc["cy"] + e_presc["h"]/2), d_app["top"])
    draw.text((1415, 1675), "1", font=mult_font, fill=text_color)

    # 6. ORDER (Tier 5)
    e_order = draw_entity(1400, 2000, 280, 58, "order")
    connect(d_app["bottom"], (1400, e_order["cy"] - e_order["h"]/2))
    draw.text((1415, 1925), "M", font=mult_font, fill=text_color)

    connect_entity_oval(e_order, draw_oval(1290, 2075, "id", w=75, h=32))
    connect_entity_oval(e_order, draw_oval(1150, 2125, "order_number", w=130, h=34))
    connect_entity_oval(e_order, draw_oval(1320, 2135, "created_at", w=115, h=34))
    connect_entity_oval(e_order, draw_oval(1480, 2135, "order_date", w=115, h=34))

    # Left Branch 5: order_item
    d_item = draw_diamond(960, 2000, 160, 52, "contains_item")
    connect((e_order["cx"] - e_order["w"]/2, 2000), d_item["right"])
    e_item = draw_entity(580, 2000, 260, 58, "order_item")
    connect(d_item["left"], (e_item["cx"] + e_item["w"]/2, 2000))
    connect_entity_oval(e_item, draw_oval(430, 2075, "id", w=75, h=32))
    connect_entity_oval(e_item, draw_oval(560, 2095, "product_type", w=125, h=34))
    connect_entity_oval(e_item, draw_oval(430, 2135, "quantity", w=95, h=32))
    connect_entity_oval(e_item, draw_oval(560, 2145, "price", w=85, h=32))

    # Right Branch 5A: frame (supplies_frame)
    d_frame = draw_diamond(1820, 1960, 160, 52, "supplies_frame")
    connect((e_order["cx"] + e_order["w"]/2, 2000), d_frame["left"])
    e_frame = draw_entity(2240, 1960, 240, 58, "frame")
    connect(d_frame["right"], (e_frame["cx"] - e_frame["w"]/2, 1960))
    connect_entity_oval(e_frame, draw_oval(2080, 2035, "id", w=75, h=32))
    connect_entity_oval(e_frame, draw_oval(2240, 2035, "brand", w=85, h=32))
    connect_entity_oval(e_frame, draw_oval(2400, 2035, "model", w=85, h=32))
    connect_entity_oval(e_frame, draw_oval(2240, 2090, "vto_image", w=115, h=34))

    # Right Branch 5B: lens (supplies_lens)
    d_lens = draw_diamond(1720, 2180, 160, 52, "supplies_lens")
    connect((e_order["cx"] + e_order["w"]/2, 2000), d_lens["left"])
    e_lens = draw_entity(2240, 2220, 240, 58, "lens")
    connect(d_lens["right"], (e_lens["cx"] - e_lens["w"]/2, 2220))
    connect_entity_oval(e_lens, draw_oval(2080, 2295, "id", w=75, h=32))
    connect_entity_oval(e_lens, draw_oval(2240, 2295, "lens_type", w=105, h=32))
    connect_entity_oval(e_lens, draw_oval(2400, 2295, "coating", w=95, h=32))
    connect_entity_oval(e_lens, draw_oval(2240, 2350, "price", w=85, h=32))

    # Diamond 6: billed_via (Order -> Billing)
    d_bill = draw_diamond(1400, 2230, 160, 56, "billed_via")
    connect((1400, e_order["cy"] + e_order["h"]/2), d_bill["top"])
    draw.text((1415, 2055), "1", font=mult_font, fill=text_color)

    # 7. BILLING (Tier 6)
    e_billing = draw_entity(1400, 2380, 280, 58, "billing")
    connect(d_bill["bottom"], (1400, e_billing["cy"] - e_billing["h"]/2))
    draw.text((1415, 2305), "1", font=mult_font, fill=text_color)

    connect_entity_oval(e_billing, draw_oval(1250, 2455, "id", w=75, h=32))
    connect_entity_oval(e_billing, draw_oval(1120, 2505, "invoice_number", w=140, h=34))
    connect_entity_oval(e_billing, draw_oval(1310, 2515, "subtotal", w=95, h=32))
    connect_entity_oval(e_billing, draw_oval(1470, 2515, "gst_amount", w=115, h=34))
    connect_entity_oval(e_billing, draw_oval(1590, 2455, "grand_total", w=115, h=34))

    # Diamond 7: settled_by (Billing -> Payment)
    d_pay = draw_diamond(1400, 2610, 160, 56, "settled_by")
    connect((1400, e_billing["cy"] + e_billing["h"]/2), d_pay["top"])
    draw.text((1415, 2435), "1", font=mult_font, fill=text_color)

    # 8. PAYMENT (Tier 7)
    e_pay = draw_entity(1400, 2760, 280, 58, "payment")
    connect(d_pay["bottom"], (1400, e_pay["cy"] - e_pay["h"]/2))
    draw.text((1415, 2685), "M", font=mult_font, fill=text_color)

    connect_entity_oval(e_pay, draw_oval(1250, 2835, "id", w=75, h=32))
    connect_entity_oval(e_pay, draw_oval(1110, 2885, "amount", w=95, h=32))
    connect_entity_oval(e_pay, draw_oval(1290, 2895, "payment_method", w=145, h=34))
    connect_entity_oval(e_pay, draw_oval(1470, 2895, "transaction_id", w=135, h=34))
    connect_entity_oval(e_pay, draw_oval(1600, 2835, "payment_date", w=125, h=34))

    # Save PNG
    img.save(workspace_png, "PNG")
    print(f"Saved PNG to: {workspace_png}")

    if os.path.exists(artifact_dir):
        shutil.copy(workspace_png, artifact_png)
        print(f"Copied PNG to artifacts: {artifact_png}")

if __name__ == "__main__":
    generate_chen_er_diagram()
