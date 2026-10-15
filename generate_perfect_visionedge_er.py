import os
import shutil
import subprocess

def generate_perfect_er():
    # Geometry Definitions
    cx = 1000 # Center X
    ew, eh = 220, 50 # Entity Width, Height
    rw, rh = 140, 55 # Relationship Diamond Width, Height
    aw, ah = 120, 38 # Attribute Ellipse Width, Height

    # Entities and their Y coordinates along central spine
    spine_entities = [
        ("users", 120, [("id", True), ("username", False), ("email", False)], [("phone", False), ("role", False), ("created_at", False)]),
        ("customers", 340, [("id", True), ("customer_code", False), ("first_name", False), ("last_name", False)], [("phone", False), ("email", False), ("address", False), ("status", False)]),
        ("appointments", 560, [("id", True), ("start_date", False), ("duration", False)], [("type", False), ("status", False), ("created_at", False)]),
        ("eye_tests", 780, [("id", True), ("sph_right", False), ("cyl_right", False)], [("sph_left", False), ("cyl_left", False), ("pd_value", False)]),
        ("prescriptions", 1000, [("id", True), ("prescription_no", False), ("sph_od", False), ("cyl_od", False)], [("sph_os", False), ("cyl_os", False), ("add_power", False), ("doctor_name", False)]),
        ("orders", 1220, [("id", True), ("order_number", False), ("order_date", False)], [("total_amount", False), ("status", False), ("created_at", False)]),
        ("billings", 1440, [("id", True), ("invoice_number", False), ("subtotal", False)], [("tax_amount", False), ("grand_total", False), ("payment_status", False)]),
        ("payments", 1660, [("id", True), ("amount", False), ("payment_method", False)], [("transaction_id", False), ("status", False), ("payment_date", False)]),
        ("chat_messages", 1880, [("id", True), ("sender_id FK", False), ("receiver_id FK", False)], [("message", False), ("sent_at", False)]),
        ("password_resets", 2100, [("id", True), ("token", False), ("otp", False)], [("expires_at", False), ("used", False)])
    ]

    relationships = [
        ("makes", 230, "users", "customers", "1", "M"),
        ("schedules", 450, "customers", "appointments", "1", "M"),
        ("leads_to", 670, "appointments", "eye_tests", "1", "1"),
        ("generates", 890, "eye_tests", "prescriptions", "1", "1"),
        ("applied_to", 1110, "prescriptions", "orders", "1", "M"),
        ("billed_via", 1330, "orders", "billings", "1", "1"),
        ("settled_by", 1550, "billings", "payments", "1", "M"),
        ("sends", 1770, "payments", "chat_messages", "1", "M"),
        ("requests", 1990, "chat_messages", "password_resets", "1", "M")
    ]

    # Generate Draw.io XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<mxfile host="app.diagrams.net" modified="2026-08-20T14:15:00.000Z" agent="VisionEdge" version="21.0.0" type="device">',
        '  <diagram id="visionedge_perfect_er" name="VisionEdge System ER Diagram">',
        '    <mxGraphModel dx="2000" dy="2400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2000" pageHeight="2400" background="#FFFFFF" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />'
    ]

    # Draw Central Entities & Attributes in Draw.io XML
    for name, ey, left_attrs, right_attrs in spine_entities:
        ex = cx - ew // 2
        ent_id = f"ent_{name}"
        xml_lines.append(f'        <!-- Entity: {name} -->')
        xml_lines.append(f'        <mxCell id="{ent_id}" value="{name}" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=15;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{ex}" y="{ey}" width="{ew}" height="{eh}" as="geometry" />')
        xml_lines.append('        </mxCell>')

        # Left Attributes
        n_left = len(left_attrs)
        for i, (aname, is_pk) in enumerate(left_attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = ex - 180 - (i % 2) * 110
            ay = ey - 20 + i * 28
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

        # Right Attributes
        for i, (aname, is_pk) in enumerate(right_attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = ex + ew + 60 + (i % 2) * 110
            ay = ey - 20 + i * 28
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

    # Draw Central Relationships in Draw.io XML
    for rname, ry, src, tgt, c1, c2 in relationships:
        rx = cx - rw // 2
        rel_id = f"rel_{rname}"
        xml_lines.append(f'        <!-- Relationship: {rname} -->')
        xml_lines.append(f'        <mxCell id="{rel_id}" value="{rname}" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{rx}" y="{ry}" width="{rw}" height="{rh}" as="geometry" />')
        xml_lines.append('        </mxCell>')
        
        # Edge src -> rel
        xml_lines.append(f'        <mxCell value="{c1}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_{src}" target="{rel_id}" />')
        # Edge rel -> tgt
        xml_lines.append(f'        <mxCell value="{c2}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{rel_id}" target="ent_{tgt}" />')

    # Add Side Module Entities (Notifications, Complaints, VTO, Frames/Lenses/OrderItems)
    side_entities = [
        ("notifications", 1550, 1660, [("id", True), ("message", False), ("type", False), ("is_seen", False)]),
        ("complaints", 300, 340, [("id", True), ("subject", False), ("detail", False), ("status", False), ("admin_reply", False)]),
        ("virtual_try_on_history", 280, 780, [("id", True), ("face_shape", False), ("snapshot_url", False), ("fit_score", False)]),
        ("frames", 280, 1220, [("id", True), ("frame_name", False), ("brand", False), ("price", False)]),
        ("lenses", 1720, 1220, [("id", True), ("lens_name", False), ("type", False), ("price", False)]),
        ("order_items", 550, 1220, [("id", True), ("quantity", False), ("subtotal", False)])
    ]

    for name, sx, sy, attrs in side_entities:
        ent_id = f"ent_{name}"
        xml_lines.append(f'        <!-- Side Entity: {name} -->')
        xml_lines.append(f'        <mxCell id="{ent_id}" value="{name}" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=15;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{sx - ew//2}" y="{sy - eh//2}" width="{ew}" height="{eh}" as="geometry" />')
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

    # Side Module Relationships
    side_rels = [
        ("receives", 1320, 1660, "ent_payments", "ent_notifications", "1", "M"),
        ("raises", 550, 230, "ent_users", "ent_complaints", "1", "M"),
        ("saves", 550, 560, "ent_customers", "ent_virtual_try_on_history", "1", "M"),
        ("contains", 770, 1220, "ent_orders", "ent_order_items", "1", "M"),
        ("included_in", 415, 1220, "ent_frames", "ent_order_items", "1", "M"),
        ("inc_in", 1350, 1220, "ent_lenses", "ent_order_items", "1", "M")
    ]
    for rname, rx, ry, src_id, tgt_id, c1, c2 in side_rels:
        rel_id = f"rel_{rname}"
        xml_lines.append(f'        <mxCell id="{rel_id}" value="{rname}" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=12;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{rx - rw//2}" y="{ry - rh//2}" width="{rw}" height="{rh}" as="geometry" />')
        xml_lines.append('        </mxCell>')
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
        print(f"Saved formatted Draw.io file to: {p}")


    # ========================================================
    # SVG GENERATION FOR CRISP PERFECT PNG RENDERING
    # ========================================================
    svg_elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 2300" width="2000" height="2300" style="background-color: #ffffff;">',
        '  <style>',
        '    .entity-rect { fill: #ffffff; stroke: #000000; stroke-width: 2.5; rx: 6; ry: 6; }',
        '    .entity-text { font-family: Arial, sans-serif; font-size: 17px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .attr-ellipse { fill: #ffffff; stroke: #000000; stroke-width: 1.8; }',
        '    .attr-text { font-family: Arial, sans-serif; font-size: 13px; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .attr-text-pk { font-family: Arial, sans-serif; font-size: 13px; fill: #000000; font-weight: bold; text-decoration: underline; text-anchor: middle; dominant-baseline: central; }',
        '    .rel-diamond { fill: #ffffff; stroke: #000000; stroke-width: 2.0; }',
        '    .rel-text { font-family: Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .connector { stroke: #000000; stroke-width: 1.8; fill: none; }',
        '    .card-box { fill: #ffffff; stroke: none; }',
        '    .card-text { font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }',
        '    .diagram-title { font-family: Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #000000; text-anchor: middle; }',
        '  </style>',
        '  <text x="1000" y="45" class="diagram-title">VisionEdge Optical Store Management - Entity Relationship (ER) Diagram</text>'
    ]

    # Draw SVG Central Entities & Attributes
    for name, ey, left_attrs, right_attrs in spine_entities:
        ex = cx - ew // 2
        # Entity Box
        svg_elements.append(f'  <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" class="entity-rect" />')
        svg_elements.append(f'  <text x="{cx}" y="{ey + eh//2}" class="entity-text">{name}</text>')

        # Left Attributes
        for i, (aname, is_pk) in enumerate(left_attrs):
            ax = ex - 160 - (i % 2) * 110
            ay = ey - 10 + i * 30
            svg_elements.append(f'  <line x1="{ex}" y1="{ey + eh//2}" x2="{ax + aw//2}" y2="{ay + ah//2}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax + aw//2}" cy="{ay + ah//2}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls_name = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax + aw//2}" y="{ay + ah//2}" class="{cls_name}">{aname}</text>')

        # Right Attributes
        for i, (aname, is_pk) in enumerate(right_attrs):
            ax = ex + ew + 50 + (i % 2) * 110
            ay = ey - 10 + i * 30
            svg_elements.append(f'  <line x1="{ex + ew}" y1="{ey + eh//2}" x2="{ax + aw//2}" y2="{ay + ah//2}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax + aw//2}" cy="{ay + ah//2}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls_name = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax + aw//2}" y="{ay + ah//2}" class="{cls_name}">{aname}</text>')

    # Draw SVG Central Relationships
    for rname, ry, src, tgt, c1, c2 in relationships:
        rx = cx - rw // 2
        y_src = [ey for n, ey, _, _ in spine_entities if n == src][0] + eh
        y_tgt = [ey for n, ey, _, _ in spine_entities if n == tgt][0]

        # Top Connector
        svg_elements.append(f'  <line x1="{cx}" y1="{y_src}" x2="{cx}" y2="{ry}" class="connector" />')
        svg_elements.append(f'  <rect x="{cx - 12}" y="{(y_src + ry)//2 - 10}" width="24" height="20" class="card-box" />')
        svg_elements.append(f'  <text x="{cx}" y="{(y_src + ry)//2}" class="card-text">{c1}</text>')

        # Diamond Shape
        pts = f"{cx},{ry} {cx + rw//2},{ry + rh//2} {cx},{ry + rh} {cx - rw//2},{ry + rh//2}"
        svg_elements.append(f'  <polygon points="{pts}" class="rel-diamond" />')
        svg_elements.append(f'  <text x="{cx}" y="{ry + rh//2}" class="rel-text">{rname}</text>')

        # Bottom Connector
        svg_elements.append(f'  <line x1="{cx}" y1="{ry + rh}" x2="{cx}" y2="{y_tgt}" class="connector" />')
        svg_elements.append(f'  <rect x="{cx - 12}" y="{(ry + rh + y_tgt)//2 - 10}" width="24" height="20" class="card-box" />')
        svg_elements.append(f'  <text x="{cx}" y="{(ry + rh + y_tgt)//2}" class="card-text">{c2}</text>')

    # Draw SVG Side Entities & Relationships
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
            cls_name = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax}" y="{ay}" class="{cls_name}">{aname}</text>')

    for rname, rx, ry, src_id, tgt_id, c1, c2 in side_rels:
        # Diamond
        pts = f"{rx},{ry - rh//2} {rx + rw//2},{ry} {rx},{ry + rh//2} {rx - rw//2},{ry}"
        svg_elements.append(f'  <polygon points="{pts}" class="rel-diamond" />')
        svg_elements.append(f'  <text x="{rx}" y="{ry}" class="rel-text">{rname}</text>')

    svg_elements.append('</svg>')
    svg_content = "\n".join(svg_elements)

    svg_path = r'c:\projects\VisionEdge\visionedge_er_diagram.svg'
    html_path = r'c:\projects\VisionEdge\render_perfect_er.html'
    output_png_dir = r'c:\projects\VisionEdge\diagrams\png'
    os.makedirs(output_png_dir, exist_ok=True)
    png_path = os.path.join(output_png_dir, 'visionedge_er_diagram.png')

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Written formatted SVG to: {svg_path}")

    # Write HTML host file
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
        '--window-size=2050,2350',
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
        print("Updated artifacts successfully!")

if __name__ == '__main__':
    generate_perfect_er()
