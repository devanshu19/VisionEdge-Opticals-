import os

def create_sequence_svg():
    svg_path = r'c:\projects\VisionEdge\visionedge_sequence_diagram.svg'
    
    width = 2200
    height = 1650
    
    columns = [
        ("Customer / Staff", 120),
        ("System Interface\n(Web UI)", 480),
        ("API Controller\n(Flask Backend)", 880),
        ("AI & CV Engine\n(Gemini / MediaPipe)", 1320),
        ("Database\n(MySQL / SQLAlchemy)", 1720),
        ("POS & Invoice Engine\n(PDF / Tax Generator)", 2060)
    ]
    
    steps = [
        (1, 0, 1, "Request available eye test slots & catalog", False),
        (2, 1, 2, "Fetch appointments & frame list (GET /api/appointments)", False),
        (3, 2, 4, "Query doctor schedules & frame inventory", False),
        (4, 4, 2, "Return slot availability & frame stock records", True),
        (5, 2, 1, "Send schedules & frame catalog JSON", True),
        (6, 1, 0, "Display appointment calendar & frame options", True),
        (7, 0, 1, "Upload physical prescription scan image", False),
        (8, 1, 2, "Initiate AI extraction (POST /api/ai/extract)", False),
        (9, 2, 3, "Transmit image payload to Google Gemini 1.5 Pro AI", False),
        (10, 3, 2, "Return parsed diopters JSON (OD/OS SPH, CYL, AXIS, PD)", True),
        (11, 2, 4, "Save EyeTest & Prescription records", False),
        (12, 4, 2, "Confirm record creation (Prescription ID)", True),
        (13, 2, 1, "Return auto-filled prescription & lens recommendations", True),
        (14, 0, 1, "Launch 3D Virtual Try-On & select frame", False),
        (15, 1, 3, "Detect facial landmarks via MediaPipe & position frame PNG", False),
        (16, 3, 1, "Render live 3D frame overlay on webcam canvas", True),
        (17, 0, 1, "Confirm frame & lens selection (Proceed to POS Checkout)", False),
        (18, 1, 2, "Initiate billing transaction (POST /api/billing/create-invoice)", False),
        (19, 2, 5, "Calculate 18% GST tax, discounts & compile PDF invoice", False),
        (20, 5, 4, "Deduct frame/lens inventory stock & store invoice record", False),
        (21, 4, 5, "Invoice transaction committed (Invoice ID)", True),
        (22, 5, 2, "Return PDF invoice URL & payment status", True),
        (23, 2, 1, "Send order completion payload", True),
        (24, 1, 0, "Display order success message & PDF invoice download button", True)
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: #ffffff; font-family: Arial, sans-serif;">')
    
    # Title
    svg.append('<text x="1100" y="45" font-size="22" font-weight="bold" fill="#000000" text-anchor="middle">VisionEdge: System Sequence Diagram (AI Exam, VTO &amp; POS Billing Flow)</text>')
    
    # Marker Definitions (Arrows)
    svg.append('''<defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#000000" />
        </marker>
        <marker id="arrow-open" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="#000000" stroke-width="1.5" />
        </marker>
    </defs>''')
    
    top_y = 80
    bottom_y = 1540
    
    # Draw Lifelines & Headers
    for name, x in columns:
        # Vertical Line
        svg.append(f'<line x1="{x}" y1="{top_y + 60}" x2="{x}" y2="{bottom_y}" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="6,6" />')
        
        # Header Box Top
        svg.append(f'<rect x="{x - 85}" y="{top_y}" width="170" height="55" rx="8" ry="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" />')
        lines_text = name.split('\n')
        if len(lines_text) == 1:
            svg.append(f'<text x="{x}" y="{top_y + 33}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">{lines_text[0]}</text>')
        else:
            svg.append(f'<text x="{x}" y="{top_y + 24}" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">{lines_text[0]}</text>')
            svg.append(f'<text x="{x}" y="{top_y + 42}" font-size="12" fill="#475569" text-anchor="middle">{lines_text[1]}</text>')

        # Header Box Bottom
        svg.append(f'<rect x="{x - 85}" y="{bottom_y}" width="170" height="55" rx="8" ry="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" />')
        if len(lines_text) == 1:
            svg.append(f'<text x="{x}" y="{bottom_y + 33}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">{lines_text[0]}</text>')
        else:
            svg.append(f'<text x="{x}" y="{bottom_y + 24}" font-size="13" font-weight="bold" fill="#000000" text-anchor="middle">{lines_text[0]}</text>')
            svg.append(f'<text x="{x}" y="{bottom_y + 42}" font-size="12" fill="#475569" text-anchor="middle">{lines_text[1]}</text>')

    # Draw Messages
    start_y = 170
    step_gap = 55
    
    for num, src_idx, tgt_idx, label, is_return in steps:
        y = start_y + (num - 1) * step_gap
        x1 = columns[src_idx][1]
        x2 = columns[tgt_idx][1]
        
        # Adjust endpoints so arrows don't collide with lifelines
        if x1 < x2:
            arr_x1 = x1 + 5
            arr_x2 = x2 - 5
            text_x = (x1 + x2) / 2
        else:
            arr_x1 = x1 - 5
            arr_x2 = x2 + 5
            text_x = (x1 + x2) / 2
            
        dash_attr = 'stroke-dasharray="5,5"' if is_return else ''
        marker_attr = 'marker-end="url(#arrow-open)"' if is_return else 'marker-end="url(#arrow)"'
        
        # Arrow line
        svg.append(f'<line x1="{arr_x1}" y1="{y}" x2="{arr_x2}" y2="{y}" stroke="#000000" stroke-width="1.8" {dash_attr} {marker_attr} />')
        
        # Step Number Badge
        circle_x = x1 + (18 if x1 < x2 else -18)
        svg.append(f'<circle cx="{circle_x}" cy="{y}" r="11" fill="#1e293b" />')
        svg.append(f'<text x="{circle_x}" y="{y + 4}" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">{num}</text>')
        
        # Label text
        svg.append(f'<text x="{text_x}" y="{y - 8}" font-size="12" font-weight="bold" fill="#000000" text-anchor="middle">{label}</text>')

    svg.append('</svg>')

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))
        
    print(f"Successfully created SVG Sequence Diagram at: {svg_path}")

if __name__ == '__main__':
    create_sequence_svg()
