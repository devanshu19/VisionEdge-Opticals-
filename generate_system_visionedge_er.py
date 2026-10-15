import os
import shutil
import subprocess

def generate_full_system_er():
    # Canvas parameters
    canvas_w, canvas_h = 2400, 2600
    cx = 1200 # Main central axis
    ew, eh = 240, 55 # Entity width & height
    rw, rh = 140, 55 # Relationship diamond width & height
    aw, ah = 125, 40 # Attribute ellipse width & height

    # 1. Main Spine Entities & Attributes
    spine = [
        ("user", 120, [("id", True), ("username", False), ("email", False)], [("phone", False), ("role", False), ("created_at", False)]),
        ("customer", 350, [("id", True), ("customer_code", False), ("first_name", False), ("last_name", False)], [("phone", False), ("email", False), ("status", False), ("created_at", False)]),
        ("appointment", 580, [("id", True), ("appointment_date", False), ("appointment_time", False)], [("type", False), ("doctor_name", False), ("status", False)]),
        ("eye_test", 810, [("id", True), ("right_sphere", False), ("right_cylinder", False)], [("left_sphere", False), ("left_cylinder", False), ("pd_value", False)]),
        ("prescription", 1040, [("id", True), ("prescription_no", False), ("sph_od", False), ("cyl_od", False)], [("sph_os", False), ("cyl_os", False), ("add_power", False), ("doctor_name", False)]),
        ("order", 1290, [("id", True), ("order_number", False), ("total_amount", False)], [("status", False), ("order_date", False), ("created_at", False)]),
        ("billing", 1540, [("id", True), ("invoice_number", False), ("subtotal", False)], [("gst_amount", False), ("grand_total", False), ("payment_status", False)]),
        ("payment", 1790, [("id", True), ("amount", False), ("payment_method", False)], [("transaction_id", False), ("payment_date", False)])
    ]

    spine_rels = [
        ("registers", 235, "user", "customer", "1", "M"),
        ("schedules", 465, "customer", "appointment", "1", "M"),
        ("leads_to", 695, "appointment", "eye_test", "1", "1"),
        ("generates", 925, "eye_test", "prescription", "1", "1"),
        ("applied_to", 1165, "prescription", "order", "1", "M"),
        ("billed_via", 1415, "order", "billing", "1", "1"),
        ("settled_by", 1665, "billing", "payment", "1", "M")
    ]

    # 2. Left & Right Subsystem Modules (Real System Connectivity)
    side_entities = [
        # Left Side (CRM, Clinical & VTO AI)
        ("customer_profile", 500, 350, [("id", True), ("blood_group", False), ("eye_conditions", False), ("allergies", False)]),
        ("frame_recommendation", 480, 680, [("id", True), ("face_shape", False), ("selected_frame", False)]),
        ("virtual_try_on_history", 480, 1040, [("id", True), ("original_image", False), ("tryon_image", False)]),
        ("order_item", 720, 1290, [("id", True), ("product_type", False), ("quantity", False), ("price", False)]),

        # Right Side (Audit, AI Lens, Inventory & System Logs)
        ("audit_log", 1920, 120, [("id", True), ("action", False), ("module", False), ("timestamp", False)]),
        ("chat_history", 1920, 350, [("id", True), ("question", False), ("answer", False), ("created_at", False)]),
        ("notification", 1920, 580, [("id", True), ("title", False), ("message", False), ("status", False)]),
        ("lens_recommendation", 1920, 1040, [("id", True), ("recommended_lens", False), ("reason", False)]),
        ("frame", 1920, 1290, [("id", True), ("brand", False), ("model", False), ("price", False), ("vto_image", False)]),
        ("lens", 1920, 1540, [("id", True), ("lens_type", False), ("coating", False), ("price", False)])
    ]

    # Explicit Foreign Key System Connections
    system_connections = [
        # Customer Profile 1-to-1 with Customer
        ("has_profile", 850, 350, "customer", "customer_profile", "1", "1"),
        # User to Audit Log
        ("logs_action", 1560, 120, "user", "audit_log", "1", "M"),
        # User to Chat History
        ("sends_chat", 1560, 350, "user", "chat_history", "1", "M"),
        # Customer to Notifications
        ("receives_alert", 1560, 580, "customer", "notification", "1", "M"),
        # Customer to Frame Rec AI
        ("matches_face", 840, 680, "customer", "frame_recommendation", "1", "M"),
        # Customer & Frame to VTO History
        ("saves_vto", 840, 1040, "customer", "virtual_try_on_history", "1", "M"),
        ("previews_frame", 1200, 1040, "frame", "virtual_try_on_history", "1", "M"),
        # Prescription to Lens Recommendation AI
        ("drives_rec", 1560, 1040, "prescription", "lens_recommendation", "1", "M"),
        # Order to Order Item
        ("contains_item", 960, 1290, "order", "order_item", "1", "M"),
        # Frame & Lens to Order Item
        ("supplies_frame", 1320, 1290, "frame", "order_item", "1", "M"),
        ("supplies_lens", 1320, 1415, "lens", "order_item", "1", "M")
    ]

    # Build Draw.io XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<mxfile host="app.diagrams.net" modified="2026-08-20T14:20:00.000Z" agent="VisionEdge" version="21.0.0" type="device">',
        '  <diagram id="visionedge_full_system" name="VisionEdge System Full ER Connectivity Diagram">',
        f'    <mxGraphModel dx="{canvas_w}" dy="{canvas_h}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{canvas_w}" pageHeight="{canvas_h}" background="#FFFFFF" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />'
    ]

    # Draw Central Spine Entities & Attributes
    for name, ey, left_attrs, right_attrs in spine:
        ex = cx - ew // 2
        ent_id = f"ent_{name}"
        xml_lines.append(f'        <!-- Spine Entity: {name} -->')
        xml_lines.append(f'        <mxCell id="{ent_id}" value="{name}" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{ex}" y="{ey}" width="{ew}" height="{eh}" as="geometry" />')
        xml_lines.append('        </mxCell>')

        # Left Attributes
        for i, (aname, is_pk) in enumerate(left_attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = ex - 180 - (i % 2) * 120
            ay = ey - 15 + i * 28
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

        # Right Attributes
        for i, (aname, is_pk) in enumerate(right_attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = ex + ew + 60 + (i % 2) * 120
            ay = ey - 15 + i * 28
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

    # Draw Central Relationships
    for rname, ry, src, tgt, c1, c2 in spine_rels:
        rx = cx - rw // 2
        rel_id = f"rel_{rname}"
        xml_lines.append(f'        <mxCell id="{rel_id}" value="{rname}" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{rx}" y="{ry}" width="{rw}" height="{rh}" as="geometry" />')
        xml_lines.append('        </mxCell>')
        xml_lines.append(f'        <mxCell value="{c1}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_{src}" target="{rel_id}" />')
        xml_lines.append(f'        <mxCell value="{c2}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{rel_id}" target="ent_{tgt}" />')

    # Draw Side Entities & Attributes
    for name, sx, sy, attrs in side_entities:
        ex = sx - ew // 2
        ey = sy - eh // 2
        ent_id = f"ent_{name}"
        xml_lines.append(f'        <mxCell id="{ent_id}" value="{name}" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=15;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{ex}" y="{ey}" width="{ew}" height="{eh}" as="geometry" />')
        xml_lines.append('        </mxCell>')

        for i, (aname, is_pk) in enumerate(attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = sx - 130 + (i % 2) * 140
            ay = sy + 45 + (i // 2) * 45
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

    # Draw System Connections & Foreign Key Relationships
    for rname, rx, ry, src_name, tgt_name, c1, c2 in system_connections:
        rel_id = f"rel_{rname}"
        xml_lines.append(f'        <mxCell id="{rel_id}" value="{rname}" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=12;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{rx - rw//2}" y="{ry - rh//2}" width="{rw}" height="{rh}" as="geometry" />')
        xml_lines.append('        </mxCell>')
        
        src_id = f"ent_{src_name}" if not src_name.startswith("ent_") else src_name
        tgt_id = f"ent_{tgt_name}" if not tgt_name.startswith("ent_") else tgt_name
        
        xml_lines.append(f'        <mxCell value="{c1}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{src_id}" target="{rel_id}" />')
        xml_lines.append(f'        <mxCell value="{c2}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{rel_id}" target="{tgt_id}" />')

    xml_lines.extend([
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>'
    ])

    xml_content = "\n".join(xml_lines)
    paths = [
        r'c:\projects\VisionEdge\visionedge_er_diagram.drawio',
        r'c:\projects\VisionEdge\visionedge_chen_er_diagram.drawio'
    ]
    for p in paths:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"Saved system Draw.io to: {p}")


    # ========================================================
    # SVG & HIGH-RES PNG GENERATION
    # ========================================================
    svg_elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}" style="background-color: #ffffff;">',
        '  <style>',
        '    .entity-rect { fill: #ffffff; stroke: #000000; stroke-width: 2.5; rx: 6; ry: 6; }',
        '    .entity-text { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .attr-ellipse { fill: #ffffff; stroke: #000000; stroke-width: 1.8; }',
        '    .attr-text { font-family: Arial, sans-serif; font-size: 13px; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .attr-text-pk { font-family: Arial, sans-serif; font-size: 13px; fill: #000000; font-weight: bold; text-decoration: underline; text-anchor: middle; dominant-baseline: central; }',
        '    .rel-diamond { fill: #ffffff; stroke: #000000; stroke-width: 2.0; }',
        '    .rel-text { font-family: Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .connector { stroke: #000000; stroke-width: 1.8; fill: none; }',
        '    .card-box { fill: #ffffff; stroke: none; }',
        '    .card-text { font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .diagram-title { font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; fill: #000000; text-anchor: middle; }',
        '  </style>',
        f'  <text x="{cx}" y="50" class="diagram-title">VISIONEDGE SYSTEM - COMPLETE RELATIONAL CONNECTIVITY &amp; ER DIAGRAM</text>'
    ]

    # Draw Spine Entities & Attributes in SVG
    for name, ey, left_attrs, right_attrs in spine:
        ex = cx - ew // 2
        svg_elements.append(f'  <!-- Entity: {name} -->')
        svg_elements.append(f'  <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" class="entity-rect" />')
        svg_elements.append(f'  <text x="{cx}" y="{ey + eh//2}" class="entity-text">{name}</text>')

        # Left Attributes
        for i, (aname, is_pk) in enumerate(left_attrs):
            ax = ex - 180 - (i % 2) * 120
            ay = ey - 10 + i * 30
            svg_elements.append(f'  <line x1="{ex}" y1="{ey + eh//2}" x2="{ax + aw//2}" y2="{ay + ah//2}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax + aw//2}" cy="{ay + ah//2}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax + aw//2}" y="{ay + ah//2}" class="{cls}">{aname}</text>')

        # Right Attributes
        for i, (aname, is_pk) in enumerate(right_attrs):
            ax = ex + ew + 60 + (i % 2) * 120
            ay = ey - 10 + i * 30
            svg_elements.append(f'  <line x1="{ex + ew}" y1="{ey + eh//2}" x2="{ax + aw//2}" y2="{ay + ah//2}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax + aw//2}" cy="{ay + ah//2}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax + aw//2}" y="{ay + ah//2}" class="{cls}">{aname}</text>')

    # Draw Central Relationships in SVG
    for rname, ry, src, tgt, c1, c2 in spine_rels:
        y_src = [ey for n, ey, _, _ in spine if n == src][0] + eh
        y_tgt = [ey for n, ey, _, _ in spine if n == tgt][0]

        svg_elements.append(f'  <line x1="{cx}" y1="{y_src}" x2="{cx}" y2="{ry}" class="connector" />')
        svg_elements.append(f'  <rect x="{cx - 12}" y="{(y_src + ry)//2 - 10}" width="24" height="20" class="card-box" />')
        svg_elements.append(f'  <text x="{cx}" y="{(y_src + ry)//2}" class="card-text">{c1}</text>')

        pts = f"{cx},{ry} {cx + rw//2},{ry + rh//2} {cx},{ry + rh} {cx - rw//2},{ry + rh//2}"
        svg_elements.append(f'  <polygon points="{pts}" class="rel-diamond" />')
        svg_elements.append(f'  <text x="{cx}" y="{ry + rh//2}" class="rel-text">{rname}</text>')

        svg_elements.append(f'  <line x1="{cx}" y1="{ry + rh}" x2="{cx}" y2="{y_tgt}" class="connector" />')
        svg_elements.append(f'  <rect x="{cx - 12}" y="{(ry + rh + y_tgt)//2 - 10}" width="24" height="20" class="card-box" />')
        svg_elements.append(f'  <text x="{cx}" y="{(ry + rh + y_tgt)//2}" class="card-text">{c2}</text>')

    # Draw Side Entities in SVG
    for name, sx, sy, attrs in side_entities:
        ex = sx - ew // 2
        ey = sy - eh // 2
        svg_elements.append(f'  <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" class="entity-rect" />')
        svg_elements.append(f'  <text x="{sx}" y="{sy}" class="entity-text">{name}</text>')

        for i, (aname, is_pk) in enumerate(attrs):
            ax = sx - 130 + (i % 2) * 140
            ay = sy + 45 + (i // 2) * 45
            svg_elements.append(f'  <line x1="{sx}" y1="{sy + eh//2}" x2="{ax}" y2="{ay}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax}" cy="{ay}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax}" y="{ay}" class="{cls}">{aname}</text>')

    # Draw System Connections & Relationship Diamonds in SVG
    for rname, rx, ry, src_name, tgt_name, c1, c2 in system_connections:
        pts = f"{rx},{ry - rh//2} {rx + rw//2},{ry} {rx},{ry + rh//2} {rx - rw//2},{ry}"
        svg_elements.append(f'  <polygon points="{pts}" class="rel-diamond" />')
        svg_elements.append(f'  <text x="{rx}" y="{ry}" class="rel-text">{rname}</text>')

        # Helper line coords
        if src_name == "customer" and tgt_name == "customer_profile":
            svg_elements.append(f'  <line x1="1080" y1="350" x2="{rx + rw//2}" y2="350" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="350" x2="620" y2="350" class="connector" />')
        elif src_name == "user" and tgt_name == "audit_log":
            svg_elements.append(f'  <line x1="1320" y1="120" x2="{rx - rw//2}" y2="120" class="connector" />')
            svg_elements.append(f'  <line x1="{rx + rw//2}" y1="120" x2="1800" y2="120" class="connector" />')
        elif src_name == "user" and tgt_name == "chat_history":
            svg_elements.append(f'  <line x1="1320" y1="350" x2="{rx - rw//2}" y2="350" class="connector" />')
            svg_elements.append(f'  <line x1="{rx + rw//2}" y1="350" x2="1800" y2="350" class="connector" />')
        elif src_name == "customer" and tgt_name == "notification":
            svg_elements.append(f'  <line x1="1320" y1="580" x2="{rx - rw//2}" y2="580" class="connector" />')
            svg_elements.append(f'  <line x1="{rx + rw//2}" y1="580" x2="1800" y2="580" class="connector" />')
        elif src_name == "customer" and tgt_name == "frame_recommendation":
            svg_elements.append(f'  <line x1="1080" y1="680" x2="{rx + rw//2}" y2="680" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="680" x2="600" y2="680" class="connector" />')
        elif src_name == "customer" and tgt_name == "virtual_try_on_history":
            svg_elements.append(f'  <line x1="1080" y1="1040" x2="{rx + rw//2}" y2="1040" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="1040" x2="600" y2="1040" class="connector" />')
        elif src_name == "prescription" and tgt_name == "lens_recommendation":
            svg_elements.append(f'  <line x1="1320" y1="1040" x2="{rx - rw//2}" y2="1040" class="connector" />')
            svg_elements.append(f'  <line x1="{rx + rw//2}" y1="1040" x2="1800" y2="1040" class="connector" />')
        elif src_name == "order" and tgt_name == "order_item":
            svg_elements.append(f'  <line x1="1080" y1="1290" x2="{rx + rw//2}" y2="1290" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="1290" x2="840" y2="1290" class="connector" />')
        elif src_name == "frame" and tgt_name == "order_item":
            svg_elements.append(f'  <line x1="1800" y1="1290" x2="{rx + rw//2}" y2="1290" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="1290" x2="1390" y2="1290" class="connector" />')
        elif src_name == "lens" and tgt_name == "order_item":
            svg_elements.append(f'  <line x1="1800" y1="1540" x2="{rx + rw//2}" y2="1415" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="1415" x2="840" y2="1290" class="connector" />')

    svg_elements.append('</svg>')
    svg_content = "\n".join(svg_elements)

    svg_path = r'c:\projects\VisionEdge\visionedge_er_diagram.svg'
    html_path = r'c:\projects\VisionEdge\render_full_system_er.html'
    output_png_dir = r'c:\projects\VisionEdge\diagrams\png'
    os.makedirs(output_png_dir, exist_ok=True)
    png_path = os.path.join(output_png_dir, 'visionedge_er_diagram.png')

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Written system SVG to: {svg_path}")

    # HTML wrapper for Chrome Headless rendering
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 0; background: #ffffff; display: flex; justify-content: center; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if not os.path.exists(chrome_path):
        chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

    cmd = [
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--force-device-scale-factor=2',
        f'--screenshot={png_path}',
        f'--window-size={canvas_w + 50},{canvas_h + 50}',
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Chrome exit code:", res.returncode)

    artifact_dir = r'C:\Users\user\.gemini\antigravity-ide\brain\e6764f65-6bff-4c78-a176-990deb180a57'
    if os.path.exists(artifact_dir):
        artifact_png = os.path.join(artifact_dir, 'visionedge_er_diagram.png')
        artifact_drawio = os.path.join(artifact_dir, 'visionedge_er_diagram.drawio')
        artifact_svg = os.path.join(artifact_dir, 'visionedge_er_diagram.svg')
        
        shutil.copy(png_path, artifact_png)
        shutil.copy(r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', artifact_drawio)
        shutil.copy(svg_path, artifact_svg)
        print("Updated artifact directory with full system ER diagram!")

if __name__ == '__main__':
    generate_full_system_er()
