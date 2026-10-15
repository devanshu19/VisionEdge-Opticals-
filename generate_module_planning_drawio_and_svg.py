import os

def generate_drawio_xml():
    drawio_path = r'c:\projects\VisionEdge\visionedge_module_planning.drawio'
    
    # Clean White Background + Black Text / Dark Outlines Draw.io XML
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-08-18T13:55:00.000Z" agent="VisionEdge" version="21.0.0" type="device">
  <diagram id="visionedge_module_planning" name="VisionEdge Module Planning Architecture">
    <mxGraphModel dx="1800" dy="1800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2000" pageHeight="1500" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title_banner" value="VisionEdge: System Module Architecture &amp; Planning Diagram" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontStyle=1;fontSize=18;verticalAlign=middle;align=center;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="500" y="30" width="1000" height="50" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 1: USER PRESENTATION LAYER ================= -->
        <mxCell id="box_presentation" value="1. FRONTEND PRESENTATION LAYER (Web Clients &amp; Portals)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;verticalAlign=top;align=left;spacingLeft=15;spacingTop=10;fontStyle=1;fontSize=14;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="60" y="110" width="1880" height="190" as="geometry" />
        </mxCell>

        <mxCell id="node_cust_portal" value="&lt;b&gt;Customer Storefront &amp; Portal&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Catalog, Product Try-On, Wishlist, Checkout, Prescription History&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="100" y="160" width="540" height="110" as="geometry" />
        </mxCell>

        <mxCell id="node_staff_portal" value="&lt;b&gt;Staff &amp; Optometrist Portal&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;CRM Lookup, Eye Test Recording, AI OCR Scanner, POS Checkout&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="730" y="160" width="540" height="110" as="geometry" />
        </mxCell>

        <mxCell id="node_admin_portal" value="&lt;b&gt;Admin Management Portal&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Inventory Control, User RBAC, Analytics Dashboard, Financial Reports&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1360" y="160" width="540" height="110" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 2: CORE BACKEND CONTROLLERS ================= -->
        <mxCell id="box_backend" value="2. BACKEND API CONTROLLER LAYER (Flask RESTful Services)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;verticalAlign=top;align=left;spacingLeft=15;spacingTop=10;fontStyle=1;fontSize=14;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="60" y="340" width="1880" height="380" as="geometry" />
        </mxCell>

        <mxCell id="mod_01" value="&lt;b&gt;MOD-01: Auth &amp; RBAC&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;JWT Tokens, User Roles, Password Hashing&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="100" y="390" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_02" value="&lt;b&gt;MOD-02: Customer CRM&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Profiles, Eye Condition Logs, Medical Notes&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="420" y="390" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_03" value="&lt;b&gt;MOD-03: Clinical Eye Test&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;OD/OS SPH, CYL, AXIS, ADD &amp; PD Records&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="740" y="390" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_08" value="&lt;b&gt;MOD-08: Inventory Control&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Frames &amp; Lenses Stock, Alert Triggers&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1060" y="390" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_09" value="&lt;b&gt;MOD-09: Order Processing&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Sales Pipeline, Lab Fitting &amp; Fulfillment&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1380" y="390" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_10" value="&lt;b&gt;MOD-10: Billing &amp; Invoicing&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;GST Calculations, Payments, PDF Receipt&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="100" y="500" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_11" value="&lt;b&gt;MOD-11: Analytics Dashboard&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Revenue Metrics, Stock Trends, Reports&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="420" y="500" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="mod_12" value="&lt;b&gt;MOD-12: Chatbot &amp; Alerts&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;AI Optical Assistant &amp; Event Notifications&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="740" y="500" width="280" height="80" as="geometry" />
        </mxCell>

        <!-- Core App Engine Sub-box -->
        <mxCell id="app_core_hub" value="&lt;b&gt;Flask Application Core Hub&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Blueprint Routing, JWT Middleware, Request Dispatcher, Error Handlers&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;fontStyle=1;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1060" y="500" width="600" height="80" as="geometry" />
        </mxCell>

        <!-- Connectors -->
        <mxCell id="e_pres_app" style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" source="node_cust_portal" target="box_backend" />
        <mxCell id="e_staff_app" style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" source="node_staff_portal" target="box_backend" />
        <mxCell id="e_admin_app" style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" source="node_admin_portal" target="box_backend" />

        <!-- ================= CONTAINER 3: AI & COMPUTER VISION SERVICES ================= -->
        <mxCell id="box_ai_engine" value="3. AI &amp; COMPUTER VISION INTELLIGENCE LAYER" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;verticalAlign=top;align=left;spacingLeft=15;spacingTop=10;fontStyle=1;fontSize=14;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="60" y="760" width="1880" height="230" as="geometry" />
        </mxCell>

        <mxCell id="mod_04" value="&lt;b&gt;MOD-04: AI Prescription OCR&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Google Gemini 1.5 Pro Multimodal Vision API parsing Rx images to diopters&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="100" y="820" width="420" height="130" as="geometry" />
        </mxCell>

        <mxCell id="mod_05" value="&lt;b&gt;MOD-05: AI Face Frame Rec.&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Facial structure detection &amp; frame geometry compatibility algorithm&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="560" y="820" width="420" height="130" as="geometry" />
        </mxCell>

        <mxCell id="mod_06" value="&lt;b&gt;MOD-06: AI Lens &amp; Coating Rec.&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Diopter power analysis recommending High-Index, Blue-Cut &amp; Anti-Reflective&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1020" y="820" width="420" height="130" as="geometry" />
        </mxCell>

        <mxCell id="mod_07" value="&lt;b&gt;MOD-07: Virtual Try-On (VTO)&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;HTML5 Canvas &amp; MediaPipe FaceMesh overlaying frames live on webcam feed (&amp;ge;24 FPS)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1480" y="820" width="420" height="130" as="geometry" />
        </mxCell>

        <mxCell id="e_ai_back" style="endArrow=classic;startArrow=classic;html=1;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" source="box_backend" target="box_ai_engine" />

        <!-- ================= CONTAINER 4: PERSISTENCE & EXTERNAL INTEGRATIONS ================= -->
        <mxCell id="box_persistence" value="4. PERSISTENCE &amp; EXTERNAL SERVICES LAYER" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;verticalAlign=top;align=left;spacingLeft=15;spacingTop=10;fontStyle=1;fontSize=14;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="60" y="1030" width="1880" height="200" as="geometry" />
        </mxCell>

        <mxCell id="db_relational" value="&lt;b&gt;Relational Database (SQLAlchemy)&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;MySQL / SQLite: User, Customer, EyeTest, Frame, Lens, Order, Invoice Tables&lt;/font&gt;" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="100" y="1080" width="540" height="120" as="geometry" />
        </mxCell>

        <mxCell id="service_gemini" value="&lt;b&gt;Google Gemini 1.5 Pro AI Cloud API&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;Multimodal Vision OCR Service Endpoint for Optical Prescription Parsing&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="730" y="1080" width="540" height="120" as="geometry" />
        </mxCell>

        <mxCell id="service_pdf_media" value="&lt;b&gt;PDF Engine &amp; Media File Storage&lt;/b&gt;&lt;br/&gt;&lt;font color=&quot;#333333&quot;&gt;ReportLab PDF Receipt Builder &amp; Local Static Media Storage (/uploads/)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=12;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1360" y="1080" width="540" height="120" as="geometry" />
        </mxCell>

        <mxCell id="e_db_back" style="endArrow=classic;startArrow=classic;html=1;strokeColor=#000000;strokeWidth=1.5;" edge="1" parent="1" source="box_ai_engine" target="box_persistence" />

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(drawio_path, 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print(f"Successfully generated Draw.io file (White Background / Black Font): {drawio_path}")

def generate_svg_diagram():
    svg_path = r'c:\projects\VisionEdge\visionedge_module_planning.svg'
    width = 2000
    height = 1300
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: #FFFFFF; font-family: Arial, Helvetica, sans-serif;">')
    
    # Definitions / Arrows
    svg.append('''<defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#000000" />
        </marker>
        <filter id="light-shadow" x="-2%" y="-2%" width="104%" height="104%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.1"/>
        </filter>
    </defs>''')
    
    # Pure White Background
    svg.append(f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>')

    # Main Title Header (Black Text, White Fill, Black Border)
    svg.append('<rect x="450" y="25" width="1100" height="60" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2" filter="url(#light-shadow)"/>')
    svg.append('<text x="1000" y="63" font-size="22" font-weight="bold" fill="#000000" text-anchor="middle" letter-spacing="0.5">VISIONEDGE: SYSTEM MODULE ARCHITECTURE &amp; PLANNING</text>')

    # ================= 1. PRESENTATION LAYER =================
    svg.append('<rect x="50" y="110" width="1900" height="200" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2" filter="url(#light-shadow)"/>')
    svg.append('<text x="75" y="142" font-size="15" font-weight="bold" fill="#000000" letter-spacing="0.5">1. FRONTEND PRESENTATION LAYER (Web Clients &amp; Portals)</text>')

    portals = [
        ("Customer Storefront & Portal", "Catalog, Virtual Try-On, Wishlist, Checkout, Prescription History", 80),
        ("Staff & Optometrist Portal", "Customer CRM, Clinical Eye Test, AI OCR Scanner, POS Checkout", 730),
        ("Admin Management Portal", "Inventory Control, Role Access (RBAC), Analytics & Financial Reports", 1380)
    ]
    for title, sub, x in portals:
        svg.append(f'<rect x="{x}" y="160" width="540" height="120" rx="6" fill="#F8FAFC" stroke="#000000" stroke-width="1.5"/>')
        svg.append(f'<text x="{x + 270}" y="205" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">{title}</text>')
        svg.append(f'<text x="{x + 270}" y="238" font-size="12" fill="#333333" text-anchor="middle">{sub}</text>')

    # Connectors Down
    for cx in [350, 1000, 1650]:
        svg.append(f'<line x1="{cx}" y1="280" x2="{cx}" y2="340" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arrow)"/>')

    # ================= 2. BACKEND CONTROLLERS LAYER =================
    svg.append('<rect x="50" y="340" width="1900" height="380" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2" filter="url(#light-shadow)"/>')
    svg.append('<text x="75" y="372" font-size="15" font-weight="bold" fill="#000000" letter-spacing="0.5">2. BACKEND API CONTROLLER LAYER (Python Flask RESTful API)</text>')

    modules_r1 = [
        ("MOD-01: Auth & RBAC", "JWT Tokens & Permissions", 80, 400),
        ("MOD-02: Customer CRM", "Profiles & Medical Logs", 390, 400),
        ("MOD-03: Clinical Eye Test", "OD/OS SPH, CYL, AXIS, PD", 700, 400),
        ("MOD-08: Inventory Control", "Frames & Lens Stock Alert", 1010, 400),
        ("MOD-09: Order Processing", "Fulfillment Pipeline", 1320, 400),
        ("MOD-10: Billing & Invoicing", "GST & PDF Receipts", 1630, 400)
    ]
    for code, desc, x, y in modules_r1:
        svg.append(f'<rect x="{x}" y="{y}" width="290" height="85" rx="6" fill="#F8FAFC" stroke="#000000" stroke-width="1.5"/>')
        svg.append(f'<text x="{x + 145}" y="{y + 36}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">{code}</text>')
        svg.append(f'<text x="{x + 145}" y="{y + 60}" font-size="11" fill="#333333" text-anchor="middle">{desc}</text>')

    modules_r2 = [
        ("MOD-11: Analytics Dashboard", "Revenue & Sales Trends", 80, 510),
        ("MOD-12: Chatbot & Alerts", "AI Assistant & Notifications", 390, 510)
    ]
    for code, desc, x, y in modules_r2:
        svg.append(f'<rect x="{x}" y="{y}" width="290" height="85" rx="6" fill="#F8FAFC" stroke="#000000" stroke-width="1.5"/>')
        svg.append(f'<text x="{x + 145}" y="{y + 36}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">{code}</text>')
        svg.append(f'<text x="{x + 145}" y="{y + 60}" font-size="11" fill="#333333" text-anchor="middle">{desc}</text>')

    # Core Hub Box
    svg.append('<rect x="700" y="510" width="1220" height="170" rx="6" fill="#F1F5F9" stroke="#000000" stroke-width="2"/>')
    svg.append('<text x="1310" y="555" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">Flask Application Dispatcher &amp; Middleware Engine</text>')
    svg.append('<text x="1310" y="590" font-size="13" fill="#1E293B" text-anchor="middle">RESTful JSON Route Blueprints • JWT Authorization Middleware • CORS &amp; Static Media Handler</text>')
    svg.append('<text x="1310" y="625" font-size="12" font-style="italic" fill="#475569" text-anchor="middle">Coordinates requests across Auth, CRM, Prescriptions, Inventory, Billing &amp; AI Microservices</text>')

    # Connectors Down to AI
    svg.append('<line x1="1000" y1="720" x2="1000" y2="760" stroke="#000000" stroke-width="2" marker-end="url(#arrow)"/>')

    # ================= 3. AI & COMPUTER VISION LAYER =================
    svg.append('<rect x="50" y="760" width="1900" height="230" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2" filter="url(#light-shadow)"/>')
    svg.append('<text x="75" y="792" font-size="15" font-weight="bold" fill="#000000" letter-spacing="0.5">3. AI &amp; COMPUTER VISION INTELLIGENCE LAYER</text>')

    ai_mods = [
        ("MOD-04: AI Prescription OCR", "Google Gemini 1.5 Pro Vision API parsing paper prescription diopters", 80),
        ("MOD-05: AI Frame Recommendation", "Facial structure geometry analysis matching Oval, Round, Square shapes", 540),
        ("MOD-06: AI Lens & Coating Rec.", "Prescription diopter power analysis for High-Index & Blue-Cut coatings", 1000),
        ("MOD-07: Virtual Try-On (VTO)", "HTML5 Canvas & MediaPipe FaceMesh overlaying frames live on webcam (24+ FPS)", 1460)
    ]
    for code, desc, x in ai_mods:
        svg.append(f'<rect x="{x}" y="820" width="440" height="140" rx="6" fill="#F8FAFC" stroke="#000000" stroke-width="1.5"/>')
        svg.append(f'<text x="{x + 220}" y="865" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">{code}</text>')
        
        words = desc.split()
        l1 = " ".join(words[:len(words)//2])
        l2 = " ".join(words[len(words)//2:])
        svg.append(f'<text x="{x + 220}" y="900" font-size="12" fill="#333333" text-anchor="middle">{l1}</text>')
        svg.append(f'<text x="{x + 220}" y="925" font-size="12" fill="#333333" text-anchor="middle">{l2}</text>')

    # Connectors Down to Persistence
    svg.append('<line x1="1000" y1="990" x2="1000" y2="1030" stroke="#000000" stroke-width="2" marker-end="url(#arrow)"/>')

    # ================= 4. PERSISTENCE & EXTERNAL LAYER =================
    svg.append('<rect x="50" y="1030" width="1900" height="220" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2" filter="url(#light-shadow)"/>')
    svg.append('<text x="75" y="1062" font-size="15" font-weight="bold" fill="#000000" letter-spacing="0.5">4. PERSISTENCE &amp; EXTERNAL SERVICES LAYER</text>')

    pers_services = [
        ("Relational Database (SQLAlchemy)", "MySQL / SQLite: User, Customer, EyeTest, Frame, Lens, Order, Invoice Tables", 80),
        ("Google Gemini 1.5 Pro AI Service", "Multimodal REST Cloud API Endpoint for OCR Prescription Image Extraction", 730),
        ("PDF Engine & Static Media Storage", "ReportLab Invoice Generator & File Storage (/uploads/ Prescriptions & Snapshots)", 1380)
    ]
    for title, sub, x in pers_services:
        svg.append(f'<rect x="{x}" y="1085" width="540" height="130" rx="6" fill="#F8FAFC" stroke="#000000" stroke-width="1.5"/>')
        svg.append(f'<text x="{x + 270}" y="1135" font-size="17" font-weight="bold" fill="#000000" text-anchor="middle">{title}</text>')
        
        words = sub.split()
        l1 = " ".join(words[:len(words)//2])
        l2 = " ".join(words[len(words)//2:])
        svg.append(f'<text x="{x + 270}" y="1170" font-size="12" fill="#333333" text-anchor="middle">{l1}</text>')
        svg.append(f'<text x="{x + 270}" y="1192" font-size="12" fill="#333333" text-anchor="middle">{l2}</text>')

    svg.append('</svg>')

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print(f"Successfully generated SVG file (White Background / Black Font): {svg_path}")

if __name__ == '__main__':
    generate_drawio_xml()
    generate_svg_diagram()
