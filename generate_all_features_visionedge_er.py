import os
import shutil
import subprocess

def generate_all_features_er():
    canvas_w = 2200
    canvas_h = 2800
    cx = 1100 # Center spine X

    ew, eh = 240, 52
    rw, rh = 140, 50
    aw, ah = 120, 36

    # 1. Main Spine Entities (Central Vertical Flow)
    spine_entities = [
        ("user", 120, [("id", True), ("username", False), ("email", False)], [("phone", False), ("role", False), ("created_at", False)]),
        ("customer", 400, [("id", True), ("customer_code", False), ("first_name", False), ("last_name", False)], [("phone", False), ("email", False), ("status", False), ("created_at", False)]),
        ("appointment", 680, [("id", True), ("appointment_date", False), ("appointment_time", False)], [("type", False), ("doctor_name", False), ("status", False)]),
        ("eye_test", 960, [("id", True), ("right_sphere", False), ("right_cylinder", False)], [("left_sphere", False), ("left_cylinder", False), ("pd_value", False)]),
        ("prescription", 1240, [("id", True), ("prescription_no", False), ("sph_od", False), ("cyl_od", False)], [("sph_os", False), ("cyl_os", False), ("add_power", False), ("doctor_name", False)]),
        ("order", 1520, [("id", True), ("order_number", False), ("total_amount", False)], [("status", False), ("order_date", False), ("created_at", False)]),
        ("order_item", 1800, [("id", True), ("product_type", False), ("quantity", False)], [("price", False), ("subtotal", False)]),
        ("billing", 2080, [("id", True), ("invoice_number", False), ("subtotal", False)], [("gst_amount", False), ("grand_total", False), ("payment_status", False)]),
        ("payment", 2360, [("id", True), ("amount", False), ("payment_method", False)], [("transaction_id", False), ("payment_date", False)])
    ]

    spine_relationships = [
        ("registers", 260, "user", "customer", "1", "M"),
        ("schedules", 540, "customer", "appointment", "1", "M"),
        ("leads_to", 820, "appointment", "eye_test", "1", "1"),
        ("generates", 1100, "eye_test", "prescription", "1", "1"),
        ("applied_to", 1380, "prescription", "order", "1", "M"),
        ("contains", 1660, "order", "order_item", "1", "M"),
        ("billed_via", 1940, "order_item", "billing", "1", "1"),
        ("settled_by", 2220, "billing", "payment", "1", "M")
    ]

    # 2. Side Feature Subsystem Entities (Left & Right Branches)
    side_entities = [
        # Left Branch (CRM Extensions, AI VTO & Suppliers)
        ("audit_log", 400, 120, [("id", True), ("action", False), ("module", False), ("timestamp", False)]),
        ("customer_profile", 400, 400, [("id", True), ("blood_group", False), ("eye_conditions", False), ("allergies", False)]),
        ("virtual_try_on_history", 400, 960, [("id", True), ("original_image", False), ("tryon_image", False)]),
        ("frame_recommendation", 400, 1240, [("id", True), ("face_shape", False), ("selected_frame", False)]),
        ("frame", 400, 1800, [("id", True), ("brand", False), ("model", False), ("price", False), ("vto_image", False)]),
        ("supplier", 400, 2080, [("id", True), ("name", False), ("phone", False), ("email", False)]),

        # Right Branch (AI Assistant, Inventory & Order Status)
        ("chat_history", 1800, 120, [("id", True), ("question", False), ("answer", False), ("created_at", False)]),
        ("notification", 1800, 400, [("id", True), ("title", False), ("message", False), ("status", False)]),
        ("lens_recommendation", 1800, 1240, [("id", True), ("recommended_lens", False), ("reason", False)]),
        ("order_status_history", 1800, 1520, [("id", True), ("status", False), ("notes", False), ("created_at", False)]),
        ("lens", 1800, 1800, [("id", True), ("lens_type", False), ("coating", False), ("price", False)]),
        ("inventory_transaction", 1800, 2080, [("id", True), ("transaction_type", False), ("quantity", False), ("notes", False)])
    ]

    side_relationships = [
        ("logs_action", 750, 120, "user", "audit_log", "1", "M"),
        ("has_profile", 750, 400, "customer", "customer_profile", "1", "1"),
        ("saves_vto", 750, 960, "customer", "virtual_try_on_history", "1", "M"),
        ("recommends", 750, 1240, "customer", "frame_recommendation", "1", "M"),
        ("inc_frame", 750, 1800, "frame", "order_item", "1", "M"),
        ("supplies", 400, 1940, "supplier", "frame", "1", "M"),

        ("sends_chat", 1450, 120, "user", "chat_history", "1", "M"),
        ("receives_alert", 1450, 400, "customer", "notification", "1", "M"),
        ("drives_rec", 1450, 1240, "prescription", "lens_recommendation", "1", "M"),
        ("tracks_status", 1450, 1520, "order", "order_status_history", "1", "M"),
        ("inc_lens", 1450, 1800, "lens", "order_item", "1", "M"),
        ("tracks_stock", 1800, 1940, "lens", "inventory_transaction", "1", "M")
    ]

    # Assembly Draw.io XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<mxfile host="app.diagrams.net" modified="2026-08-20T15:30:00.000Z" agent="VisionEdge" version="21.0.0" type="device">',
        '  <diagram id="visionedge_all_features_er" name="VisionEdge All Features Chen ER Diagram">',
        f'    <mxGraphModel dx="{canvas_w}" dy="{canvas_h}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{canvas_w}" pageHeight="{canvas_h}" background="#FFFFFF" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />'
    ]

    # Central Spine Entities & Attributes XML
    for name, ey, left_attrs, right_attrs in spine_entities:
        ex = cx - ew // 2
        ent_id = f"ent_{name}"
        xml_lines.append(f'        <!-- Spine Entity: {name} -->')
        xml_lines.append(f'        <mxCell id="{ent_id}" value="{name}" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{ex}" y="{ey}" width="{ew}" height="{eh}" as="geometry" />')
        xml_lines.append('        </mxCell>')

        for i, (aname, is_pk) in enumerate(left_attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = ex - 180 - (i % 2) * 110
            ay = ey - 10 + i * 32
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

        for i, (aname, is_pk) in enumerate(right_attrs):
            att_id = f"att_{name}_{aname}".replace(" ", "_")
            ax = ex + ew + 60 + (i % 2) * 110
            ay = ey - 10 + i * 32
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;{'fontStyle=4;' if is_pk else ''}fontSize=12;"
            xml_lines.append(f'        <mxCell id="{att_id}" value="{aname}" style="{style}" vertex="1" parent="1">')
            xml_lines.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry" />')
            xml_lines.append('        </mxCell>')
            xml_lines.append(f'        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="{ent_id}" target="{att_id}" />')

    # Central Spine Relationships XML
    for rname, ry, src, tgt, c1, c2 in spine_relationships:
        rx = cx - rw // 2
        rel_id = f"rel_{rname}"
        xml_lines.append(f'        <mxCell id="{rel_id}" value="{rname}" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{rx}" y="{ry}" width="{rw}" height="{rh}" as="geometry" />')
        xml_lines.append('        </mxCell>')
        xml_lines.append(f'        <mxCell value="{c1}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_{src}" target="{rel_id}" />')
        xml_lines.append(f'        <mxCell value="{c2}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{rel_id}" target="ent_{tgt}" />')

    # Side Feature Entities XML
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

    # Side Relationships XML
    for rname, rx, ry, src_name, tgt_name, c1, c2 in side_relationships:
        rel_id = f"rel_{rname}"
        xml_lines.append(f'        <mxCell id="{rel_id}" value="{rname}" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=12;" vertex="1" parent="1">')
        xml_lines.append(f'          <mxGeometry x="{rx - rw//2}" y="{ry - rh//2}" width="{rw}" height="{rh}" as="geometry" />')
        xml_lines.append('        </mxCell>')
        src_id = f"ent_{src_name}"
        tgt_id = f"ent_{tgt_name}"
        xml_lines.append(f'        <mxCell value="{c1}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{src_id}" target="{rel_id}" />')
        xml_lines.append(f'        <mxCell value="{c2}" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{rel_id}" target="{tgt_id}" />')

    xml_lines.extend([
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>'
    ])

    xml_content = "\n".join(xml_lines)
    for p in [r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', r'c:\projects\VisionEdge\visionedge_chen_er_diagram.drawio']:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"Saved All Features Draw.io file to: {p}")


    # High-Resolution SVG & PNG Assembly
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
        '    .sub-title { font-family: Arial, sans-serif; font-size: 16px; fill: #333333; text-anchor: middle; }',
        '  </style>',
        f'  <text x="{cx}" y="45" class="diagram-title">VISIONEDGE SYSTEM - ALL 21 FEATURES RELATIONAL ER DIAGRAM</text>',
        f'  <text x="{cx}" y="75" class="sub-title">Complete Architecture: Auth, CRM, Eye Examinations, Prescriptions, Orders, Inventory, Suppliers, AI Vision VTO &amp; Payments</text>'
    ]

    # Spine Entities in SVG
    for name, ey, left_attrs, right_attrs in spine_entities:
        ex = cx - ew // 2
        svg_elements.append(f'  <!-- Spine Entity: {name} -->')
        svg_elements.append(f'  <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" class="entity-rect" />')
        svg_elements.append(f'  <text x="{cx}" y="{ey + eh//2}" class="entity-text">{name}</text>')

        for i, (aname, is_pk) in enumerate(left_attrs):
            ax = ex - 180 - (i % 2) * 110
            ay = ey - 10 + i * 30
            svg_elements.append(f'  <line x1="{ex}" y1="{ey + eh//2}" x2="{ax + aw//2}" y2="{ay + ah//2}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax + aw//2}" cy="{ay + ah//2}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax + aw//2}" y="{ay + ah//2}" class="{cls}">{aname}</text>')

        for i, (aname, is_pk) in enumerate(right_attrs):
            ax = ex + ew + 60 + (i % 2) * 110
            ay = ey - 10 + i * 30
            svg_elements.append(f'  <line x1="{ex + ew}" y1="{ey + eh//2}" x2="{ax + aw//2}" y2="{ay + ah//2}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax + aw//2}" cy="{ay + ah//2}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax + aw//2}" y="{ay + ah//2}" class="{cls}">{aname}</text>')

    # Spine Relationships in SVG
    for rname, ry, src, tgt, c1, c2 in spine_relationships:
        y_src = [ey for n, ey, _, _ in spine_entities if n == src][0] + eh
        y_tgt = [ey for n, ey, _, _ in spine_entities if n == tgt][0]

        svg_elements.append(f'  <line x1="{cx}" y1="{y_src}" x2="{cx}" y2="{ry}" class="connector" />')
        svg_elements.append(f'  <rect x="{cx - 12}" y="{(y_src + ry)//2 - 10}" width="24" height="20" class="card-box" />')
        svg_elements.append(f'  <text x="{cx}" y="{(y_src + ry)//2}" class="card-text">{c1}</text>')

        pts = f"{cx},{ry} {cx + rw//2},{ry + rh//2} {cx},{ry + rh} {cx - rw//2},{ry + rh//2}"
        svg_elements.append(f'  <polygon points="{pts}" class="rel-diamond" />')
        svg_elements.append(f'  <text x="{cx}" y="{ry + rh//2}" class="rel-text">{rname}</text>')

        svg_elements.append(f'  <line x1="{cx}" y1="{ry + rh}" x2="{cx}" y2="{y_tgt}" class="connector" />')
        svg_elements.append(f'  <rect x="{cx - 12}" y="{(ry + rh + y_tgt)//2 - 10}" width="24" height="20" class="card-box" />')
        svg_elements.append(f'  <text x="{cx}" y="{(ry + rh + y_tgt)//2}" class="card-text">{c2}</text>')

    # Side Feature Entities in SVG
    for name, sx, sy, attrs in side_entities:
        ex = sx - ew // 2
        ey = sy - eh // 2
        svg_elements.append(f'  <!-- Side Entity: {name} -->')
        svg_elements.append(f'  <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" class="entity-rect" />')
        svg_elements.append(f'  <text x="{sx}" y="{sy}" class="entity-text">{name}</text>')

        for i, (aname, is_pk) in enumerate(attrs):
            ax = sx - 130 + (i % 2) * 140
            ay = sy + 45 + (i // 2) * 45
            svg_elements.append(f'  <line x1="{sx}" y1="{sy + eh//2}" x2="{ax}" y2="{ay}" class="connector" />')
            svg_elements.append(f'  <ellipse cx="{ax}" cy="{ay}" rx="{aw//2}" ry="{ah//2}" class="attr-ellipse" />')
            cls = "attr-text-pk" if is_pk else "attr-text"
            svg_elements.append(f'  <text x="{ax}" y="{ay}" class="{cls}">{aname}</text>')

    # Side Relationships & Connectors in SVG
    for rname, rx, ry, src_name, tgt_name, c1, c2 in side_relationships:
        pts = f"{rx},{ry - rh//2} {rx + rw//2},{ry} {rx},{ry + rh//2} {rx - rw//2},{ry}"
        svg_elements.append(f'  <polygon points="{pts}" class="rel-diamond" />')
        svg_elements.append(f'  <text x="{rx}" y="{ry}" class="rel-text">{rname}</text>')

        # Direct Orthogonal Lines
        if rx < cx: # Left Branch
            svg_elements.append(f'  <line x1="{cx - ew//2}" y1="{ry}" x2="{rx + rw//2}" y2="{ry}" class="connector" />')
            svg_elements.append(f'  <line x1="{rx - rw//2}" y1="{ry}" x2="520" y2="{ry}" class="connector" />')
        else: # Right Branch
            svg_elements.append(f'  <line x1="{cx + ew//2}" y1="{ry}" x2="{rx - rw//2}" y2="{ry}" class="connector" />')
            svg_elements.append(f'  <line x1="{rx + rw//2}" y1="{ry}" x2="1680" y2="{ry}" class="connector" />')

    svg_elements.append('</svg>')
    svg_content = "\n".join(svg_elements)

    svg_path = r'c:\projects\VisionEdge\visionedge_er_diagram.svg'
    html_path = r'c:\projects\VisionEdge\render_all_features_er.html'
    output_png_dir = r'c:\projects\VisionEdge\diagrams\png'
    os.makedirs(output_png_dir, exist_ok=True)
    png_path = os.path.join(output_png_dir, 'visionedge_er_diagram.png')

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

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
        shutil.copy(png_path, os.path.join(artifact_dir, 'visionedge_er_diagram.png'))
        shutil.copy(r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', os.path.join(artifact_dir, 'visionedge_er_diagram.drawio'))
        shutil.copy(svg_path, os.path.join(artifact_dir, 'visionedge_er_diagram.svg'))
        print("Successfully updated all artifact files with all 21 features!")

if __name__ == '__main__':
    generate_all_features_er()
