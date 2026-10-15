import os
import shutil
import subprocess

def generate_visionedge_features_er():
    # Canvas Dimensions (Tall Portrait, exactly matching the user's reference diagram structure)
    canvas_w = 1500
    canvas_h = 2700
    cx = 750

    # Draw.io XML for VisionEdge Features Chen ER Diagram
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-08-20T15:30:00.000Z" agent="VisionEdge" version="21.0.0" type="device">
  <diagram id="visionedge_features_er" name="VisionEdge Features Chen ER Diagram">
    <mxGraphModel dx="1500" dy="2700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="2700" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ======================================================== -->
        <!-- 1. USERS ENTITY (Auth & System Roles) -->
        <!-- ======================================================== -->
        <mxCell id="ent_users" value="users" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="630" y="80" width="240" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for USERS -->
        <mxCell id="att_u_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="45" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_uname" value="username" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="280" y="85" width="90" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_email" value="email" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="125" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_u_phone" value="phone" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1010" y="45" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_role" value="role" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1130" y="85" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_created" value="created_at" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1010" y="125" width="95" height="35" as="geometry" />
        </mxCell>

        <!-- Attribute Edges -->
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_uname" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_email" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_phone" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_role" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_created" />

        <!-- RELATIONSHIP: USERS -> CUSTOMERS (registers) -->
        <mxCell id="rel_registers" value="registers" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="685" y="190" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_users" target="rel_registers" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_registers" target="ent_customers" />


        <!-- ======================================================== -->
        <!-- 2. CUSTOMERS ENTITY (Store CRM & Demographics) -->
        <!-- ======================================================== -->
        <mxCell id="ent_customers" value="customers" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="620" y="300" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for CUSTOMERS -->
        <mxCell id="att_c_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="265" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_c_code" value="customer_code" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="250" y="300" width="120" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_c_fname" value="first_name" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="380" y="335" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_c_lname" value="last_name" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="510" y="355" width="90" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_c_phone" value="phone" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1020" y="355" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_c_email" value="email" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1140" y="320" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_c_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1020" y="265" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_code" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_fname" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_lname" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_phone" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_email" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_customers" target="att_c_stat" />

        <!-- RELATIONSHIP: CUSTOMERS -> APPOINTMENTS (schedules) -->
        <mxCell id="rel_schedules" value="schedules" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="675" y="410" width="150" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_customers" target="rel_schedules" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_schedules" target="ent_appointments" />


        <!-- ======================================================== -->
        <!-- 3. APPOINTMENTS ENTITY (Clinical Visit Scheduling) -->
        <!-- ======================================================== -->
        <mxCell id="ent_appointments" value="appointments" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="620" y="520" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for APPOINTMENTS -->
        <mxCell id="att_apt_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="485" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_apt_date" value="appointment_date" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="240" y="520" width="130" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_apt_type" value="type" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="555" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_apt_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1020" y="485" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_apt_doc" value="doctor_name" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1130" y="520" width="105" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_appointments" target="att_apt_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_appointments" target="att_apt_date" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_appointments" target="att_apt_type" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_appointments" target="att_apt_stat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_appointments" target="att_apt_doc" />

        <!-- RELATIONSHIP: APPOINTMENTS -> EYE_TESTS (leads_to) -->
        <mxCell id="rel_leads" value="leads_to" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="685" y="630" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_appointments" target="rel_leads" />
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_leads" target="ent_eyetests" />


        <!-- ======================================================== -->
        <!-- 4. EYE_TESTS ENTITY (Clinical OD/OS Examination) -->
        <!-- ======================================================== -->
        <mxCell id="ent_eyetests" value="eye_tests" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="620" y="740" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for EYE_TESTS -->
        <mxCell id="att_et_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="705" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_et_sphr" value="right_sphere" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="270" y="740" width="100" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_et_cylr" value="right_cylinder" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="390" y="775" width="110" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_et_sphl" value="left_sphere" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1020" y="705" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_et_pd" value="pd_value" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1140" y="740" width="85" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_eyetests" target="att_et_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_eyetests" target="att_et_sphr" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_eyetests" target="att_et_cylr" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_eyetests" target="att_et_sphl" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_eyetests" target="att_et_pd" />

        <!-- RELATIONSHIP: EYE_TESTS -> PRESCRIPTIONS (generates) -->
        <mxCell id="rel_generates" value="generates" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="685" y="850" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_eyetests" target="rel_generates" />
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_generates" target="ent_prescriptions" />


        <!-- ======================================================== -->
        <!-- 5. PRESCRIPTIONS ENTITY (AI Gemini Scanned Rx) -->
        <!-- ======================================================== -->
        <mxCell id="ent_prescriptions" value="prescriptions" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="610" y="960" width="280" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for PRESCRIPTIONS -->
        <mxCell id="att_rx_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="890" y="930" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_rx_no" value="prescription_no" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1010" y="960" width="120" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_rx_add" value="add_power" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1150" y="960" width="90" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_rx_doc" value="doctor_name" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1260" y="930" width="100" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_prescriptions" target="att_rx_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_prescriptions" target="att_rx_no" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_prescriptions" target="att_rx_add" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_prescriptions" target="att_rx_doc" />

        <!-- RELATIONSHIP: PRESCRIPTIONS -> ORDERS (applied_to) -->
        <mxCell id="rel_applied" value="applied_to" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="685" y="1070" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_prescriptions" target="rel_applied" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_applied" target="ent_orders" />


        <!-- ======================================================== -->
        <!-- 6. ORDERS ENTITY (Retail Optical Orders) -->
        <!-- ======================================================== -->
        <mxCell id="ent_orders" value="orders" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="610" y="1180" width="280" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for ORDERS -->
        <mxCell id="att_o_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="390" y="1150" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_o_no" value="order_number" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="250" y="1180" width="115" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_o_tot" value="total_amount" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1010" y="1150" width="105" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_o_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1135" y="1180" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_orders" target="att_o_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_orders" target="att_o_no" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_orders" target="att_o_tot" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_orders" target="att_o_stat" />

        <!-- RELATIONSHIP: ORDERS -> BILLINGS (billed_via) -->
        <mxCell id="rel_billed" value="billed_via" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="675" y="1290" width="150" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_orders" target="rel_billed" />
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_billed" target="ent_billings" />


        <!-- ======================================================== -->
        <!-- 7. BILLINGS ENTITY (GST Invoices & Receipts) -->
        <!-- ======================================================== -->
        <mxCell id="ent_billings" value="billings" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="600" y="1400" width="300" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for BILLINGS -->
        <mxCell id="att_b_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="390" y="1370" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_b_inv" value="invoice_number" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="250" y="1400" width="120" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_b_tot" value="grand_total" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="370" y="1435" width="95" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_b_stat" value="payment_status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1020" y="1370" width="115" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_b_gst" value="gst_amount" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1150" y="1400" width="100" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_billings" target="att_b_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_billings" target="att_b_inv" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_billings" target="att_b_tot" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_billings" target="att_b_stat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_billings" target="att_b_gst" />

        <!-- RELATIONSHIP: BILLINGS -> PAYMENTS (settled_by) -->
        <mxCell id="rel_settled" value="settled_by" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="685" y="1510" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_billings" target="rel_settled" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_settled" target="ent_payments" />


        <!-- ======================================================== -->
        <!-- 8. PAYMENTS ENTITY (Transactions) -->
        <!-- ======================================================== -->
        <mxCell id="ent_payments" value="payments" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="620" y="1620" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for PAYMENTS -->
        <mxCell id="att_p_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="1585" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_p_amt" value="amount" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="270" y="1620" width="85" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_p_tx" value="transaction_id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="380" y="1655" width="115" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_p_meth" value="payment_method" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="1020" y="1585" width="125" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_p_date" value="payment_date" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1150" y="1620" width="115" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_amt" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_tx" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_meth" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_date" />


        <!-- ======================================================== -->
        <!-- 9. AI VIRTUAL TRY-ON (VTO Feature Side Module) -->
        <!-- ======================================================== -->
        <mxCell id="ent_vto" value="virtual_try_on_history" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=15;" vertex="1" parent="1">
          <mxGeometry x="120" y="960" width="240" height="50" as="geometry" />
        </mxCell>

        <mxCell id="att_vto_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="110" y="1030" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_vto_face" value="face_shape" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="200" y="1040" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_vto_img" value="tryon_image" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="310" y="1020" width="95" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_vto" target="att_vto_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_vto" target="att_vto_face" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_vto" target="att_vto_img" />

        <!-- RELATIONSHIP: CUSTOMERS -> VTO (saves) -->
        <mxCell id="rel_saves" value="saves" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="175" y="870" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_customers" target="rel_saves">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="240" y="325" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_saves" target="ent_vto" />


        <!-- ======================================================== -->
        <!-- 10. FRAMES & LENSES (Inventory Features Side Module) -->
        <!-- ======================================================== -->
        <mxCell id="ent_frames" value="frames" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="320" y="1620" width="220" height="50" as="geometry" />
        </mxCell>

        <mxCell id="att_frm_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="190" y="1590" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_frm_brand" value="brand" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="190" y="1630" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_frm_price" value="price" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="1670" width="70" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_frames" target="att_frm_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_frames" target="att_frm_brand" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_frames" target="att_frm_price" />

        <mxCell id="ent_lenses" value="lenses" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="960" y="1620" width="220" height="50" as="geometry" />
        </mxCell>

        <mxCell id="att_l_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1220" y="1590" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_l_type" value="lens_type" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1230" y="1630" width="90" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_l_coat" value="coating" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1190" y="1670" width="85" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_lenses" target="att_l_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_lenses" target="att_l_type" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_lenses" target="att_l_coat" />

        <!-- DASHED CONNECTIONS FOR FRAMES & LENSES TO ORDERS -->
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;dashed=1;dashPattern=4 4;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_orders" target="ent_frames" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;dashed=1;dashPattern=4 4;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_orders" target="ent_lenses" />

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

    for p in [r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', r'c:\projects\VisionEdge\visionedge_chen_er_diagram.drawio']:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"Saved true features Draw.io file to: {p}")


    # High-Resolution SVG & PNG Generation
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 2000" width="1500" height="2000" style="background-color: #ffffff;">
  <style>
    .entity-rect { fill: #ffffff; stroke: #000000; stroke-width: 2.5; rx: 6; ry: 6; }
    .entity-text { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }
    
    .attr-ellipse { fill: #ffffff; stroke: #000000; stroke-width: 1.8; }
    .attr-text { font-family: Arial, sans-serif; font-size: 13px; fill: #000000; text-anchor: middle; dominant-baseline: central; }
    .attr-text-pk { font-family: Arial, sans-serif; font-size: 13px; fill: #000000; font-weight: bold; text-decoration: underline; text-anchor: middle; dominant-baseline: central; }
    
    .rel-diamond { fill: #ffffff; stroke: #000000; stroke-width: 2.0; }
    .rel-text { font-family: Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }
    
    .connector { stroke: #000000; stroke-width: 1.8; fill: none; }
    .dashed-connector { stroke: #000000; stroke-width: 1.8; stroke-dasharray: 6,6; fill: none; }
    
    .card-box { fill: #ffffff; stroke: none; }
    .card-text { font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; fill: #000000; text-anchor: middle; dominant-baseline: central; }
    .diagram-title { font-family: Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #000000; text-anchor: middle; }
  </style>

  <text x="750" y="40" class="diagram-title">VisionEdge System - System Architecture &amp; Feature ER Diagram</text>

  <!-- ======================================================== -->
  <!-- 1. USERS -->
  <!-- ======================================================== -->
  <line x1="750" y1="105" x2="415" y2="65" class="connector" />
  <line x1="750" y1="105" x2="325" y2="105" class="connector" />
  <line x1="750" y1="105" x2="415" y2="145" class="connector" />

  <line x1="750" y1="105" x2="1085" y2="65" class="connector" />
  <line x1="750" y1="105" x2="1205" y2="105" class="connector" />
  <line x1="750" y1="105" x2="1085" y2="145" class="connector" />

  <ellipse cx="415" cy="65" rx="40" ry="20" class="attr-ellipse" />
  <text x="415" y="65" class="attr-text-pk">id</text>

  <ellipse cx="325" cy="105" rx="55" ry="20" class="attr-ellipse" />
  <text x="325" y="105" class="attr-text">username</text>

  <ellipse cx="415" cy="145" rx="45" ry="20" class="attr-ellipse" />
  <text x="415" y="145" class="attr-text">email</text>

  <ellipse cx="1085" cy="65" rx="45" ry="20" class="attr-ellipse" />
  <text x="1085" y="65" class="attr-text">phone</text>

  <ellipse cx="1205" cy="105" rx="45" ry="20" class="attr-ellipse" />
  <text x="1205" y="105" class="attr-text">role</text>

  <ellipse cx="1085" cy="145" rx="55" ry="20" class="attr-ellipse" />
  <text x="1085" y="145" class="attr-text">created_at</text>

  <rect x="630" y="80" width="240" height="50" class="entity-rect" />
  <text x="750" y="105" class="entity-text">users</text>

  <!-- USERS -> [registers] -> CUSTOMERS -->
  <line x1="750" y1="130" x2="750" y2="190" class="connector" />
  <rect x="738" y="150" width="24" height="20" class="card-box" />
  <text x="750" y="160" class="card-text">1</text>

  <polygon points="750,190 820,215 750,240 680,215" class="rel-diamond" />
  <text x="750" y="215" class="rel-text">registers</text>

  <line x1="750" y1="240" x2="750" y2="300" class="connector" />
  <rect x="738" y="260" width="24" height="20" class="card-box" />
  <text x="750" y="270" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 2. CUSTOMERS -->
  <!-- ======================================================== -->
  <line x1="750" y1="325" x2="415" y2="285" class="connector" />
  <line x1="750" y1="325" x2="285" y2="325" class="connector" />
  <line x1="750" y1="325" x2="415" y2="360" class="connector" />
  <line x1="750" y1="325" x2="545" y2="375" class="connector" />

  <line x1="750" y1="325" x2="1085" y2="375" class="connector" />
  <line x1="750" y1="325" x2="1205" y2="335" class="connector" />
  <line x1="750" y1="325" x2="1085" y2="285" class="connector" />

  <ellipse cx="415" cy="285" rx="40" ry="20" class="attr-ellipse" />
  <text x="415" y="285" class="attr-text-pk">id</text>

  <ellipse cx="285" cy="325" rx="65" ry="20" class="attr-ellipse" />
  <text x="285" y="325" class="attr-text">customer_code</text>

  <ellipse cx="415" cy="360" rx="55" ry="20" class="attr-ellipse" />
  <text x="415" y="360" class="attr-text">first_name</text>

  <ellipse cx="545" cy="375" rx="50" ry="20" class="attr-ellipse" />
  <text x="545" y="375" class="attr-text">last_name</text>

  <ellipse cx="1085" cy="375" rx="45" ry="20" class="attr-ellipse" />
  <text x="1085" y="375" class="attr-text">phone</text>

  <ellipse cx="1205" cy="335" rx="45" ry="20" class="attr-ellipse" />
  <text x="1205" y="335" class="attr-text">email</text>

  <ellipse cx="1085" cy="285" rx="45" ry="20" class="attr-ellipse" />
  <text x="1085" y="285" class="attr-text">status</text>

  <rect x="620" y="300" width="260" height="50" class="entity-rect" />
  <text x="750" y="325" class="entity-text">customers</text>

  <!-- CUSTOMERS -> [schedules] -> APPOINTMENTS -->
  <line x1="750" y1="350" x2="750" y2="410" class="connector" />
  <rect x="738" y="370" width="24" height="20" class="card-box" />
  <text x="750" y="380" class="card-text">1</text>

  <polygon points="750,410 830,435 750,460 670,435" class="rel-diamond" />
  <text x="750" y="435" class="rel-text">schedules</text>

  <line x1="750" y1="460" x2="750" y2="520" class="connector" />
  <rect x="738" y="480" width="24" height="20" class="card-box" />
  <text x="750" y="490" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 3. APPOINTMENTS -->
  <!-- ======================================================== -->
  <line x1="750" y1="545" x2="415" y2="505" class="connector" />
  <line x1="750" y1="545" x2="275" y2="545" class="connector" />
  <line x1="750" y1="545" x2="415" y2="580" class="connector" />

  <line x1="750" y1="545" x2="1085" y2="505" class="connector" />
  <line x1="750" y1="545" x2="1205" y2="545" class="connector" />

  <ellipse cx="415" cy="505" rx="40" ry="20" class="attr-ellipse" />
  <text x="415" y="505" class="attr-text-pk">id</text>

  <ellipse cx="275" cy="545" rx="75" ry="20" class="attr-ellipse" />
  <text x="275" y="545" class="attr-text">appointment_date</text>

  <ellipse cx="415" cy="580" rx="45" ry="20" class="attr-ellipse" />
  <text x="415" y="580" class="attr-text">type</text>

  <ellipse cx="1085" cy="505" rx="45" ry="20" class="attr-ellipse" />
  <text x="1085" y="505" class="attr-text">status</text>

  <ellipse cx="1205" cy="545" rx="60" ry="20" class="attr-ellipse" />
  <text x="1205" y="545" class="attr-text">doctor_name</text>

  <rect x="620" y="520" width="260" height="50" class="entity-rect" />
  <text x="750" y="545" class="entity-text">appointments</text>

  <!-- APPOINTMENTS -> [leads_to] -> EYE_TESTS -->
  <line x1="750" y1="570" x2="750" y2="630" class="connector" />
  <rect x="738" y="590" width="24" height="20" class="card-box" />
  <text x="750" y="600" class="card-text">1</text>

  <polygon points="750,630 820,655 750,680 680,655" class="rel-diamond" />
  <text x="750" y="655" class="rel-text">leads_to</text>

  <line x1="750" y1="680" x2="750" y2="740" class="connector" />
  <rect x="738" y="700" width="24" height="20" class="card-box" />
  <text x="750" y="710" class="card-text">1</text>


  <!-- ======================================================== -->
  <!-- 4. EYE_TESTS -->
  <!-- ======================================================== -->
  <line x1="750" y1="765" x2="415" y2="725" class="connector" />
  <line x1="750" y1="765" x2="295" y2="765" class="connector" />
  <line x1="750" y1="765" x2="415" y2="800" class="connector" />

  <line x1="750" y1="765" x2="1085" y2="725" class="connector" />
  <line x1="750" y1="765" x2="1205" y2="765" class="connector" />

  <ellipse cx="415" cy="725" rx="40" ry="20" class="attr-ellipse" />
  <text x="415" y="725" class="attr-text-pk">id</text>

  <ellipse cx="295" cy="765" rx="60" ry="20" class="attr-ellipse" />
  <text x="295" y="765" class="attr-text">right_sphere</text>

  <ellipse cx="415" cy="800" rx="60" ry="20" class="attr-ellipse" />
  <text x="415" y="800" class="attr-text">right_cylinder</text>

  <ellipse cx="1085" cy="725" rx="55" ry="20" class="attr-ellipse" />
  <text x="1085" y="725" class="attr-text">left_sphere</text>

  <ellipse cx="1205" cy="765" rx="50" ry="20" class="attr-ellipse" />
  <text x="1205" y="765" class="attr-text">pd_value</text>

  <rect x="620" y="740" width="260" height="50" class="entity-rect" />
  <text x="750" y="765" class="entity-text">eye_tests</text>

  <!-- EYE_TESTS -> [generates] -> PRESCRIPTIONS -->
  <line x1="750" y1="790" x2="750" y2="850" class="connector" />
  <rect x="738" y="810" width="24" height="20" class="card-box" />
  <text x="750" y="820" class="card-text">1</text>

  <polygon points="750,850 820,875 750,900 680,875" class="rel-diamond" />
  <text x="750" y="875" class="rel-text">generates</text>

  <line x1="750" y1="900" x2="750" y2="960" class="connector" />
  <rect x="738" y="920" width="24" height="20" class="card-box" />
  <text x="750" y="930" class="card-text">1</text>


  <!-- ======================================================== -->
  <!-- 5. PRESCRIPTIONS -->
  <!-- ======================================================== -->
  <line x1="750" y1="985" x2="905" y2="945" class="connector" />
  <line x1="750" y1="985" x2="1035" y2="985" class="connector" />
  <line x1="750" y1="985" x2="1165" y2="985" class="connector" />
  <line x1="750" y1="985" x2="1275" y2="945" class="connector" />

  <ellipse cx="905" cy="945" rx="40" ry="20" class="attr-ellipse" />
  <text x="905" y="945" class="attr-text-pk">id</text>

  <ellipse cx="1035" cy="985" rx="70" ry="20" class="attr-ellipse" />
  <text x="1035" y="985" class="attr-text">prescription_no</text>

  <ellipse cx="1165" cy="985" rx="55" ry="20" class="attr-ellipse" />
  <text x="1165" y="985" class="attr-text">add_power</text>

  <ellipse cx="1275" cy="945" rx="60" ry="20" class="attr-ellipse" />
  <text x="1275" y="945" class="attr-text">doctor_name</text>

  <rect x="610" y="960" width="280" height="50" class="entity-rect" />
  <text x="750" y="985" class="entity-text">prescriptions</text>

  <!-- PRESCRIPTIONS -> [applied_to] -> ORDERS -->
  <line x1="750" y1="1010" x2="750" y2="1070" class="connector" />
  <rect x="738" y="1030" width="24" height="20" class="card-box" />
  <text x="750" y="1040" class="card-text">1</text>

  <polygon points="750,1070 820,1095 750,1120 680,1095" class="rel-diamond" />
  <text x="750" y="1095" class="rel-text">applied_to</text>

  <line x1="750" y1="1120" x2="750" y2="1180" class="connector" />
  <rect x="738" y="1140" width="24" height="20" class="card-box" />
  <text x="750" y="1150" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 6. ORDERS -->
  <!-- ======================================================== -->
  <line x1="750" y1="1205" x2="415" y2="1165" class="connector" />
  <line x1="750" y1="1205" x2="285" y2="1205" class="connector" />

  <line x1="750" y1="1205" x2="1085" y2="1165" class="connector" />
  <line x1="750" y1="1205" x2="1205" y2="1205" class="connector" />

  <ellipse cx="415" cy="1165" rx="40" ry="20" class="attr-ellipse" />
  <text x="415" y="1165" class="attr-text-pk">id</text>

  <ellipse cx="285" cy="1205" rx="65" ry="20" class="attr-ellipse" />
  <text x="285" y="1205" class="attr-text">order_number</text>

  <ellipse cx="1085" cy="1165" rx="60" ry="20" class="attr-ellipse" />
  <text x="1085" y="1165" class="attr-text">total_amount</text>

  <ellipse cx="1205" cy="1205" rx="45" ry="20" class="attr-ellipse" />
  <text x="1205" y="1205" class="attr-text">status</text>

  <rect x="610" y="1180" width="280" height="50" class="entity-rect" />
  <text x="750" y="1205" class="entity-text">orders</text>

  <!-- ORDERS -> [billed_via] -> BILLINGS -->
  <line x1="750" y1="1230" x2="750" y2="1290" class="connector" />
  <rect x="738" y="1250" width="24" height="20" class="card-box" />
  <text x="750" y="1260" class="card-text">1</text>

  <polygon points="750,1290 830,1315 750,1340 670,1315" class="rel-diamond" />
  <text x="750" y="1315" class="rel-text">billed_via</text>

  <line x1="750" y1="1340" x2="750" y2="1400" class="connector" />
  <rect x="738" y="1360" width="24" height="20" class="card-box" />
  <text x="750" y="1370" class="card-text">1</text>


  <!-- ======================================================== -->
  <!-- 7. BILLINGS -->
  <!-- ======================================================== -->
  <line x1="750" y1="1425" x2="415" y2="1385" class="connector" />
  <line x1="750" y1="1425" x2="285" y2="1425" class="connector" />
  <line x1="750" y1="1425" x2="405" y2="1460" class="connector" />

  <line x1="750" y1="1425" x2="1085" y2="1385" class="connector" />
  <line x1="750" y1="1425" x2="1205" y2="1425" class="connector" />

  <ellipse cx="415" cy="1385" rx="40" ry="20" class="attr-ellipse" />
  <text x="415" y="1385" class="attr-text-pk">id</text>

  <ellipse cx="285" cy="1425" rx="65" ry="20" class="attr-ellipse" />
  <text x="285" y="1425" class="attr-text">invoice_number</text>

  <ellipse cx="405" cy="1460" rx="55" ry="20" class="attr-ellipse" />
  <text x="405" y="1460" class="attr-text">grand_total</text>

  <ellipse cx="1085" cy="1385" rx="65" ry="20" class="attr-ellipse" />
  <text x="1085" y="1385" class="attr-text">payment_status</text>

  <ellipse cx="1205" cy="1425" rx="55" ry="20" class="attr-ellipse" />
  <text x="1205" y="1425" class="attr-text">gst_amount</text>

  <rect x="600" y="1400" width="300" height="50" class="entity-rect" />
  <text x="750" y="1425" class="entity-text">billings</text>

  <!-- BILLINGS -> [settled_by] -> PAYMENTS -->
  <line x1="750" y1="1450" x2="750" y2="1510" class="connector" />
  <rect x="738" y="1470" width="24" height="20" class="card-box" />
  <text x="750" y="1480" class="card-text">1</text>

  <polygon points="750,1510 820,1535 750,1560 680,1535" class="rel-diamond" />
  <text x="750" y="1535" class="rel-text">settled_by</text>

  <line x1="750" y1="1560" x2="750" y2="1620" class="connector" />
  <rect x="738" y="1580" width="24" height="20" class="card-box" />
  <text x="750" y="1590" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 8. PAYMENTS -->
  <!-- ======================================================== -->
  <line x1="750" y1="1645" x2="445" y2="1605" class="connector" />
  <line x1="750" y1="1645" x2="305" y2="1645" class="connector" />
  <line x1="750" y1="1645" x2="415" y2="1680" class="connector" />

  <line x1="750" y1="1645" x2="1085" y2="1605" class="connector" />
  <line x1="750" y1="1645" x2="1205" y2="1645" class="connector" />

  <ellipse cx="445" cy="1605" rx="40" ry="20" class="attr-ellipse" />
  <text x="445" y="1605" class="attr-text-pk">id</text>

  <ellipse cx="305" cy="1645" rx="50" ry="20" class="attr-ellipse" />
  <text x="305" y="1645" class="attr-text">amount</text>

  <ellipse cx="415" cy="1680" rx="65" ry="20" class="attr-ellipse" />
  <text x="415" y="1680" class="attr-text">transaction_id</text>

  <ellipse cx="1085" cy="1605" rx="70" ry="20" class="attr-ellipse" />
  <text x="1085" y="1605" class="attr-text">payment_method</text>

  <ellipse cx="1205" cy="1645" rx="65" ry="20" class="attr-ellipse" />
  <text x="1205" y="1645" class="attr-text">payment_date</text>

  <rect x="620" y="1620" width="260" height="50" class="entity-rect" />
  <text x="750" y="1645" class="entity-text">payments</text>


  <!-- ======================================================== -->
  <!-- 9. AI VIRTUAL TRY-ON (Side Left) -->
  <!-- ======================================================== -->
  <polyline points="620,325 240,325 240,895" class="connector" />
  <rect x="228" y="580" width="24" height="20" class="card-box" />
  <text x="240" y="590" class="card-text">1</text>

  <polygon points="240,870 305,895 240,920 175,895" class="rel-diamond" />
  <text x="240" y="895" class="rel-text">saves</text>

  <line x1="240" y1="920" x2="240" y2="960" class="connector" />
  <rect x="228" y="930" width="24" height="20" class="card-box" />
  <text x="240" y="940" class="card-text">M</text>

  <ellipse cx="145" cy="1047" rx="38" ry="20" class="attr-ellipse" />
  <text x="145" y="1047" class="attr-text-pk">id</text>

  <ellipse cx="247" cy="1057" rx="55" ry="20" class="attr-ellipse" />
  <text x="247" y="1057" class="attr-text">face_shape</text>

  <ellipse cx="357" cy="1037" rx="55" ry="20" class="attr-ellipse" />
  <text x="357" y="1037" class="attr-text">tryon_image</text>

  <line x1="240" y1="985" x2="145" y2="1047" class="connector" />
  <line x1="240" y1="985" x2="247" y2="1057" class="connector" />
  <line x1="240" y1="985" x2="357" y2="1037" class="connector" />

  <rect x="120" y="960" width="240" height="50" class="entity-rect" />
  <text x="240" y="985" class="entity-text">virtual_try_on_history</text>


  <!-- ======================================================== -->
  <!-- 10. FRAMES & LENSES (Bottom Side Entities) -->
  <!-- ======================================================== -->
  <line x1="220" y1="1645" x2="110" y2="1610" class="connector" />
  <line x1="220" y1="1645" x2="110" y2="1650" class="connector" />
  <line x1="220" y1="1645" x2="170" y2="1690" class="connector" />

  <ellipse cx="110" cy="1610" rx="38" ry="20" class="attr-ellipse" />
  <text x="110" y="1610" class="attr-text-pk">id</text>

  <ellipse cx="110" cy="1650" rx="40" ry="20" class="attr-ellipse" />
  <text x="110" y="1650" class="attr-text">brand</text>

  <ellipse cx="170" cy="1690" rx="40" ry="20" class="attr-ellipse" />
  <text x="170" y="1690" class="attr-text">price</text>

  <rect x="220" y="1620" width="220" height="50" class="entity-rect" />
  <text x="330" y="1645" class="entity-text">frames</text>

  <line x1="1070" y1="1645" x2="1270" y2="1610" class="connector" />
  <line x1="1070" y1="1645" x2="1285" y2="1650" class="connector" />
  <line x1="1070" y1="1645" x2="1245" y2="1690" class="connector" />

  <ellipse cx="1270" cy="1610" rx="38" ry="20" class="attr-ellipse" />
  <text x="1270" y="1610" class="attr-text-pk">id</text>

  <ellipse cx="1285" cy="1650" rx="50" ry="20" class="attr-ellipse" />
  <text x="1285" y="1650" class="attr-text">lens_type</text>

  <ellipse cx="1245" cy="1690" rx="48" ry="20" class="attr-ellipse" />
  <text x="1245" y="1690" class="attr-text">coating</text>

  <rect x="960" y="1620" width="220" height="50" class="entity-rect" />
  <text x="1070" y="1645" class="entity-text">lenses</text>

  <!-- Dashed connections to orders -->
  <line x1="610" y1="1205" x2="330" y2="1620" class="dashed-connector" />
  <line x1="890" y1="1205" x2="1070" y2="1620" class="dashed-connector" />

</svg>
"""

    svg_path = r'c:\projects\VisionEdge\visionedge_er_diagram.svg'
    html_path = r'c:\projects\VisionEdge\render_features_er.html'
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
        '--window-size=1550,2050',
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Chrome exit code:", res.returncode)

    artifact_dir = r'C:\Users\user\.gemini\antigravity-ide\brain\e6764f65-6bff-4c78-a176-990deb180a57'
    if os.path.exists(artifact_dir):
        shutil.copy(png_path, os.path.join(artifact_dir, 'visionedge_er_diagram.png'))
        shutil.copy(r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', os.path.join(artifact_dir, 'visionedge_er_diagram.drawio'))
        shutil.copy(svg_path, os.path.join(artifact_dir, 'visionedge_er_diagram.svg'))
        print("Updated artifacts with VisionEdge features ER diagram!")

if __name__ == '__main__':
    generate_visionedge_features_er()
