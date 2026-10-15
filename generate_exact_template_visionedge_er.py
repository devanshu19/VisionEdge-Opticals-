import os
import shutil
import subprocess

def generate_exact_template_er():
    # Canvas Size (Tall Portrait, exactly matching the reference image layout)
    canvas_w = 1400
    canvas_h = 2400
    cx = 700

    # Draw.io XML generation matching exact reference structure
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-08-20T15:25:00.000Z" agent="VisionEdge" version="21.0.0" type="device">
  <diagram id="visionedge_template_er" name="VisionEdge System Chen ER Diagram">
    <mxGraphModel dx="1400" dy="2400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="2400" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ======================================================== -->
        <!-- 1. USERS ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_users" value="users" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="580" y="80" width="240" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for USERS -->
        <mxCell id="att_u_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="360" y="45" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_fname" value="full_name" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="230" y="85" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_email" value="email" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="360" y="125" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_u_phone" value="phone" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="960" y="45" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_role" value="role" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1080" y="85" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_pwd" value="password" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="960" y="125" width="90" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_u_created" value="created_at" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1080" y="155" width="95" height="35" as="geometry" />
        </mxCell>

        <!-- Attribute Edges -->
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_fname" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_email" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_phone" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_role" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_pwd" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_users" target="att_u_created" />

        <!-- RELATIONSHIP: USERS -> ROOMS (makes) -->
        <mxCell id="rel_makes" value="makes" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="635" y="190" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_users" target="rel_makes" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_makes" target="ent_rooms" />


        <!-- ======================================================== -->
        <!-- 2. ROOMS ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_rooms" value="rooms" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="570" y="300" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for ROOMS -->
        <mxCell id="att_r_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="360" y="265" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_r_stype" value="sharing_type" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="210" y="300" width="110" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_r_rname" value="room_name" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="330" y="335" width="100" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_r_cat" value="category" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="460" y="355" width="90" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_r_rent" value="monthly_rent" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="970" y="355" width="115" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_r_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1100" y="320" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_r_rno" value="room_no" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="970" y="265" width="90" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_stype" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_rname" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_cat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_rent" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_stat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_rooms" target="att_r_rno" />

        <!-- RELATIONSHIP: ROOMS -> BOOKINGS (reserved via) -->
        <mxCell id="rel_reserved" value="reserved via" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="620" y="410" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_rooms" target="rel_reserved" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_reserved" target="ent_bookings" />


        <!-- ======================================================== -->
        <!-- 3. BOOKINGS ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_bookings" value="bookings" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="570" y="520" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for BOOKINGS -->
        <mxCell id="att_b_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="360" y="485" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_b_sdate" value="start_date" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="230" y="520" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_b_dur" value="duration" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="360" y="555" width="85" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_b_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="970" y="485" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_b_created" value="created_at" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1080" y="520" width="95" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_bookings" target="att_b_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_bookings" target="att_b_sdate" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_bookings" target="att_b_dur" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_bookings" target="att_b_stat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_bookings" target="att_b_created" />

        <!-- RELATIONSHIP: BOOKINGS -> PAYMENTS (settled by) -->
        <mxCell id="rel_settled" value="settled by" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="630" y="630" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_bookings" target="rel_settled" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_settled" target="ent_payments" />


        <!-- ======================================================== -->
        <!-- 4. PAYMENTS ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_payments" value="payments" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="570" y="740" width="260" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for PAYMENTS -->
        <mxCell id="att_p_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="360" y="705" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_p_amt" value="amount" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="230" y="740" width="85" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_p_tx" value="transaction_id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="340" y="775" width="115" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_p_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="970" y="705" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_p_date" value="payment_date" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1080" y="740" width="115" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_amt" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_tx" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_stat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_payments" target="att_p_date" />

        <!-- RELATIONSHIP: PAYMENTS -> NOTIFICATIONS (receives) -->
        <mxCell id="rel_receives" value="receives" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="630" y="850" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_payments" target="rel_receives" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_receives" target="ent_notifications" />


        <!-- ======================================================== -->
        <!-- 5. NOTIFICATIONS ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_notifications" value="notifications" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="560" y="960" width="280" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for NOTIFICATIONS -->
        <mxCell id="att_n_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="840" y="930" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_n_msg" value="message" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="960" y="960" width="90" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_n_type" value="type" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1080" y="960" width="75" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_n_seen" value="is_seen" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1190" y="930" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_notifications" target="att_n_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_notifications" target="att_n_msg" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_notifications" target="att_n_type" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_notifications" target="att_n_seen" />

        <!-- RELATIONSHIP: NOTIFICATIONS -> CHAT_MESSAGES (sends) -->
        <mxCell id="rel_sends" value="sends" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="630" y="1070" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_notifications" target="rel_sends" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_sends" target="ent_chat" />


        <!-- ======================================================== -->
        <!-- 6. CHAT_MESSAGES ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_chat" value="chat_messages" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="560" y="1180" width="280" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for CHAT_MESSAGES -->
        <mxCell id="att_chat_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="340" y="1150" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_chat_send" value="sender_id FK" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="210" y="1180" width="110" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_chat_recv" value="receiver_id FK" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="320" y="1215" width="115" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_chat_msg" value="message" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="960" y="1150" width="90" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_chat_time" value="sent_at" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1080" y="1180" width="80" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_chat" target="att_chat_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_chat" target="att_chat_send" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_chat" target="att_chat_recv" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_chat" target="att_chat_msg" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_chat" target="att_chat_time" />

        <!-- RELATIONSHIP: CHAT_MESSAGES -> PASSWORD_RESETS (requests) -->
        <mxCell id="rel_requests" value="requests" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="620" y="1290" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_chat" target="rel_requests" />
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_requests" target="ent_passresets" />


        <!-- ======================================================== -->
        <!-- 7. PASSWORD_RESETS ENTITY -->
        <!-- ======================================================== -->
        <mxCell id="ent_passresets" value="password_resets" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="550" y="1400" width="300" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for PASSWORD_RESETS -->
        <mxCell id="att_pr_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="340" y="1370" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_pr_tok" value="token" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="230" y="1400" width="75" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_pr_otp" value="otp" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="330" y="1435" width="65" height="35" as="geometry" />
        </mxCell>

        <mxCell id="att_pr_exp" value="expires_at" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="970" y="1370" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_pr_used" value="used" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1080" y="1400" width="70" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_passresets" target="att_pr_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_passresets" target="att_pr_tok" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_passresets" target="att_pr_otp" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_passresets" target="att_pr_exp" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_passresets" target="att_pr_used" />


        <!-- ======================================================== -->
        <!-- 8. COMPLAINTS ENTITY (Left Branch) -->
        <!-- ======================================================== -->
        <mxCell id="ent_complaints" value="complaints" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="50" y="960" width="220" height="50" as="geometry" />
        </mxCell>

        <!-- Attributes for COMPLAINTS -->
        <mxCell id="att_cmp_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="40" y="1030" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_cmp_sub" value="subject" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="135" y="1040" width="80" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_cmp_det" value="detail" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="235" y="1040" width="75" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_cmp_stat" value="status" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="325" y="1020" width="75" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_cmp_reply" value="admin_reply" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="345" y="970" width="95" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_complaints" target="att_cmp_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_complaints" target="att_cmp_sub" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_complaints" target="att_cmp_det" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_complaints" target="att_cmp_stat" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_complaints" target="att_cmp_reply" />

        <!-- RELATIONSHIP: USERS -> COMPLAINTS (raises) -->
        <mxCell id="rel_raises" value="raises" style="shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="90" y="870" width="120" height="50" as="geometry" />
        </mxCell>
        <mxCell value="1" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_users" target="rel_raises">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="150" y="105" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="rel_raises" target="ent_complaints" />


        <!-- ======================================================== -->
        <!-- 9. ADMIN_ROOMS & ADMIN (Bottom Entities) -->
        <!-- ======================================================== -->
        <mxCell id="ent_admin_rooms" value="admin_rooms" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="250" y="1650" width="220" height="50" as="geometry" />
        </mxCell>
        <!-- Attributes for ADMIN_ROOMS -->
        <mxCell id="att_ar_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="110" y="1620" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_ar_lbl" value="label" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="110" y="1660" width="70" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_ar_val" value="value" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="180" y="1700" width="70" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin_rooms" target="att_ar_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin_rooms" target="att_ar_lbl" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin_rooms" target="att_ar_val" />

        <mxCell id="ent_admin" value="admin" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2.5;fontColor=#000000;fontStyle=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="780" y="1650" width="220" height="50" as="geometry" />
        </mxCell>
        <!-- Attributes for ADMIN -->
        <mxCell id="att_adm_rfk" value="room_id FK" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="660" y="1700" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_adm_id" value="id" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontStyle=4;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1040" y="1620" width="65" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_adm_usr" value="username" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1050" y="1660" width="95" height="35" as="geometry" />
        </mxCell>
        <mxCell id="att_adm_pwd" value="password" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.8;fontColor=#000000;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="1010" y="1700" width="90" height="35" as="geometry" />
        </mxCell>

        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin" target="att_adm_rfk" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin" target="att_adm_id" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin" target="att_adm_usr" />
        <mxCell style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;" edge="1" parent="1" source="ent_admin" target="att_adm_pwd" />

        <!-- DASHED CONNECTIONS FOR HAS DETAILS & ADMIN_ROOMS LINK -->
        <mxCell id="e_has_details" value="has details" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;dashed=1;dashPattern=4 4;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_passresets" target="ent_admin">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="700" y="1560" />
              <mxPoint x="890" y="1560" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell value="M" style="endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.8;dashed=1;dashPattern=4 4;fontColor=#000000;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="ent_admin" target="ent_admin_rooms" />

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

    for p in [r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', r'c:\projects\VisionEdge\visionedge_chen_er_diagram.drawio']:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"Saved template Draw.io file to: {p}")


    # High Resolution SVG & PNG rendering
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1350 1850" width="1350" height="1850" style="background-color: #ffffff;">
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
  </style>

  <!-- ======================================================== -->
  <!-- 1. USERS -->
  <!-- ======================================================== -->
  <line x1="675" y1="95" x2="365" y2="55" class="connector" />
  <line x1="675" y1="95" x2="265" y2="95" class="connector" />
  <line x1="675" y1="95" x2="365" y2="135" class="connector" />

  <line x1="675" y1="95" x2="985" y2="55" class="connector" />
  <line x1="675" y1="95" x2="1105" y2="95" class="connector" />
  <line x1="675" y1="95" x2="985" y2="135" class="connector" />
  <line x1="675" y1="95" x2="1105" y2="165" class="connector" />

  <ellipse cx="365" cy="55" rx="40" ry="20" class="attr-ellipse" />
  <text x="365" y="55" class="attr-text-pk">id</text>

  <ellipse cx="265" cy="95" rx="55" ry="20" class="attr-ellipse" />
  <text x="265" y="95" class="attr-text">full_name</text>

  <ellipse cx="365" cy="135" rx="45" ry="20" class="attr-ellipse" />
  <text x="365" y="135" class="attr-text">email</text>

  <ellipse cx="985" cy="55" rx="45" ry="20" class="attr-ellipse" />
  <text x="985" y="55" class="attr-text">phone</text>

  <ellipse cx="1105" cy="95" rx="45" ry="20" class="attr-ellipse" />
  <text x="1105" y="95" class="attr-text">role</text>

  <ellipse cx="985" cy="135" rx="50" ry="20" class="attr-ellipse" />
  <text x="985" y="135" class="attr-text">password</text>

  <ellipse cx="1105" cy="165" rx="55" ry="20" class="attr-ellipse" />
  <text x="1105" y="165" class="attr-text">created_at</text>

  <rect x="555" y="70" width="240" height="50" class="entity-rect" />
  <text x="675" y="95" class="entity-text">users</text>

  <!-- USERS -> [makes] -> ROOMS -->
  <line x1="675" y1="120" x2="675" y2="185" class="connector" />
  <rect x="663" y="140" width="24" height="20" class="card-box" />
  <text x="675" y="150" class="card-text">1</text>

  <polygon points="675,185 745,210 675,235 605,210" class="rel-diamond" />
  <text x="675" y="210" class="rel-text">makes</text>

  <line x1="675" y1="235" x2="675" y2="295" class="connector" />
  <rect x="663" y="255" width="24" height="20" class="card-box" />
  <text x="675" y="265" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 2. ROOMS -->
  <!-- ======================================================== -->
  <line x1="675" y1="320" x2="365" y2="280" class="connector" />
  <line x1="675" y1="320" x2="235" y2="320" class="connector" />
  <line x1="675" y1="320" x2="355" y2="355" class="connector" />
  <line x1="675" y1="320" x2="485" y2="375" class="connector" />

  <line x1="675" y1="320" x2="1005" y2="375" class="connector" />
  <line x1="675" y1="320" x2="1125" y2="335" class="connector" />
  <line x1="675" y1="320" x2="1005" y2="280" class="connector" />

  <ellipse cx="365" cy="280" rx="40" ry="20" class="attr-ellipse" />
  <text x="365" y="280" class="attr-text-pk">id</text>

  <ellipse cx="235" cy="320" rx="65" ry="20" class="attr-ellipse" />
  <text x="235" y="320" class="attr-text">sharing_type</text>

  <ellipse cx="355" cy="355" rx="60" ry="20" class="attr-ellipse" />
  <text x="355" y="355" class="attr-text">room_name</text>

  <ellipse cx="485" cy="375" rx="55" ry="20" class="attr-ellipse" />
  <text x="485" y="375" class="attr-text">category</text>

  <ellipse cx="1005" cy="375" rx="65" ry="20" class="attr-ellipse" />
  <text x="1005" y="375" class="attr-text">monthly_rent</text>

  <ellipse cx="1125" cy="335" rx="45" ry="20" class="attr-ellipse" />
  <text x="1125" y="335" class="attr-text">status</text>

  <ellipse cx="1005" cy="280" rx="55" ry="20" class="attr-ellipse" />
  <text x="1005" y="280" class="attr-text">room_no</text>

  <rect x="545" y="295" width="260" height="50" class="entity-rect" />
  <text x="675" y="320" class="entity-text">rooms</text>

  <!-- ROOMS -> [reserved via] -> BOOKINGS -->
  <line x1="675" y1="345" x2="675" y2="405" class="connector" />
  <rect x="663" y="365" width="24" height="20" class="card-box" />
  <text x="675" y="375" class="card-text">1</text>

  <polygon points="675,405 765,430 675,455 585,430" class="rel-diamond" />
  <text x="675" y="430" class="rel-text">reserved via</text>

  <line x1="675" y1="455" x2="675" y2="515" class="connector" />
  <rect x="663" y="475" width="24" height="20" class="card-box" />
  <text x="675" y="485" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 3. BOOKINGS -->
  <!-- ======================================================== -->
  <line x1="675" y1="540" x2="365" y2="500" class="connector" />
  <line x1="675" y1="540" x2="255" y2="540" class="connector" />
  <line x1="675" y1="540" x2="375" y2="575" class="connector" />

  <line x1="675" y1="540" x2="985" y2="500" class="connector" />
  <line x1="675" y1="540" x2="1115" y2="540" class="connector" />

  <ellipse cx="365" cy="500" rx="40" ry="20" class="attr-ellipse" />
  <text x="365" y="500" class="attr-text-pk">id</text>

  <ellipse cx="255" cy="540" rx="55" ry="20" class="attr-ellipse" />
  <text x="255" y="540" class="attr-text">start_date</text>

  <ellipse cx="375" cy="575" rx="50" ry="20" class="attr-ellipse" />
  <text x="375" y="575" class="attr-text">duration</text>

  <ellipse cx="985" cy="500" rx="45" ry="20" class="attr-ellipse" />
  <text x="985" y="500" class="attr-text">status</text>

  <ellipse cx="1115" cy="540" rx="55" ry="20" class="attr-ellipse" />
  <text x="1115" y="540" class="attr-text">created_at</text>

  <rect x="545" y="515" width="260" height="50" class="entity-rect" />
  <text x="675" y="540" class="entity-text">bookings</text>

  <!-- BOOKINGS -> [settled by] -> PAYMENTS -->
  <line x1="675" y1="565" x2="675" y2="625" class="connector" />
  <rect x="663" y="585" width="24" height="20" class="card-box" />
  <text x="675" y="595" class="card-text">1</text>

  <polygon points="675,625 755,650 675,675 595,650" class="rel-diamond" />
  <text x="675" y="650" class="rel-text">settled by</text>

  <line x1="675" y1="675" x2="675" y2="735" class="connector" />
  <rect x="663" y="695" width="24" height="20" class="card-box" />
  <text x="675" y="705" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 4. PAYMENTS -->
  <!-- ======================================================== -->
  <line x1="675" y1="760" x2="365" y2="720" class="connector" />
  <line x1="675" y1="760" x2="255" y2="760" class="connector" />
  <line x1="675" y1="760" x2="365" y2="795" class="connector" />

  <line x1="675" y1="760" x2="985" y2="720" class="connector" />
  <line x1="675" y1="760" x2="1115" y2="760" class="connector" />

  <ellipse cx="365" cy="720" rx="40" ry="20" class="attr-ellipse" />
  <text x="365" y="720" class="attr-text-pk">id</text>

  <ellipse cx="255" cy="760" rx="50" ry="20" class="attr-ellipse" />
  <text x="255" y="760" class="attr-text">amount</text>

  <ellipse cx="365" cy="795" rx="65" ry="20" class="attr-ellipse" />
  <text x="365" y="795" class="attr-text">transaction_id</text>

  <ellipse cx="985" cy="720" rx="45" ry="20" class="attr-ellipse" />
  <text x="985" y="720" class="attr-text">status</text>

  <ellipse cx="1115" cy="760" rx="65" ry="20" class="attr-ellipse" />
  <text x="1115" y="760" class="attr-text">payment_date</text>

  <rect x="545" y="735" width="260" height="50" class="entity-rect" />
  <text x="675" y="760" class="entity-text">payments</text>

  <!-- PAYMENTS -> [receives] -> NOTIFICATIONS -->
  <line x1="675" y1="785" x2="675" y2="845" class="connector" />

  <polygon points="675,845 745,870 675,895 605,870" class="rel-diamond" />
  <text x="675" y="870" class="rel-text">receives</text>

  <line x1="675" y1="895" x2="675" y2="955" class="connector" />


  <!-- ======================================================== -->
  <!-- 5. NOTIFICATIONS -->
  <!-- ======================================================== -->
  <line x1="675" y1="980" x2="845" y2="945" class="connector" />
  <line x1="675" y1="980" x2="985" y2="980" class="connector" />
  <line x1="675" y1="980" x2="1105" y2="980" class="connector" />
  <line x1="675" y1="980" x2="1215" y2="945" class="connector" />

  <ellipse cx="845" cy="945" rx="40" ry="20" class="attr-ellipse" />
  <text x="845" y="945" class="attr-text-pk">id</text>

  <ellipse cx="985" cy="980" rx="55" ry="20" class="attr-ellipse" />
  <text x="985" y="980" class="attr-text">message</text>

  <ellipse cx="1105" cy="980" rx="45" ry="20" class="attr-ellipse" />
  <text x="1105" y="980" class="attr-text">type</text>

  <ellipse cx="1215" cy="945" rx="45" ry="20" class="attr-ellipse" />
  <text x="1215" y="945" class="attr-text">is_seen</text>

  <rect x="535" y="955" width="280" height="50" class="entity-rect" />
  <text x="675" y="980" class="entity-text">notifications</text>

  <!-- NOTIFICATIONS -> [sends] -> CHAT_MESSAGES -->
  <line x1="675" y1="1005" x2="675" y2="1065" class="connector" />

  <polygon points="675,1065 745,1090 675,1115 605,1090" class="rel-diamond" />
  <text x="675" y="1090" class="rel-text">sends</text>

  <line x1="675" y1="1115" x2="675" y2="1175" class="connector" />


  <!-- ======================================================== -->
  <!-- 6. CHAT_MESSAGES -->
  <!-- ======================================================== -->
  <line x1="675" y1="1200" x2="345" y2="1165" class="connector" />
  <line x1="675" y1="1200" x2="225" y2="1200" class="connector" />
  <line x1="675" y1="1200" x2="345" y2="1235" class="connector" />

  <line x1="675" y1="1200" x2="985" y2="1165" class="connector" />
  <line x1="675" y1="1200" x2="1105" y2="1200" class="connector" />

  <ellipse cx="345" cy="1165" rx="40" ry="20" class="attr-ellipse" />
  <text x="345" y="1165" class="attr-text-pk">id</text>

  <ellipse cx="225" cy="1200" rx="65" ry="20" class="attr-ellipse" />
  <text x="225" y="1200" class="attr-text">sender_id FK</text>

  <ellipse cx="345" cy="1235" rx="70" ry="20" class="attr-ellipse" />
  <text x="345" y="1235" class="attr-text">receiver_id FK</text>

  <ellipse cx="985" cy="1165" rx="55" ry="20" class="attr-ellipse" />
  <text x="985" y="1165" class="attr-text">message</text>

  <ellipse cx="1105" cy="1200" rx="50" ry="20" class="attr-ellipse" />
  <text x="1105" y="1200" class="attr-text">sent_at</text>

  <rect x="535" y="1175" width="280" height="50" class="entity-rect" />
  <text x="675" y="1200" class="entity-text">chat_messages</text>

  <!-- CHAT_MESSAGES -> [requests] -> PASSWORD_RESETS -->
  <line x1="675" y1="1225" x2="675" y2="1285" class="connector" />
  <rect x="663" y="1245" width="24" height="20" class="card-box" />
  <text x="675" y="1255" class="card-text">1</text>

  <polygon points="675,1285 755,1310 675,1335 595,1310" class="rel-diamond" />
  <text x="675" y="1310" class="rel-text">requests</text>

  <line x1="675" y1="1335" x2="675" y2="1395" class="connector" />
  <rect x="663" y="1355" width="24" height="20" class="card-box" />
  <text x="675" y="1365" class="card-text">M</text>


  <!-- ======================================================== -->
  <!-- 7. PASSWORD_RESETS -->
  <!-- ======================================================== -->
  <line x1="675" y1="1420" x2="345" y2="1385" class="connector" />
  <line x1="675" y1="1420" x2="235" y2="1420" class="connector" />
  <line x1="675" y1="1420" x2="335" y2="1455" class="connector" />

  <line x1="675" y1="1420" x2="985" y2="1385" class="connector" />
  <line x1="675" y1="1420" x2="1105" y2="1420" class="connector" />

  <ellipse cx="345" cy="1385" rx="40" ry="20" class="attr-ellipse" />
  <text x="345" y="1385" class="attr-text-pk">id</text>

  <ellipse cx="235" cy="1420" rx="45" ry="20" class="attr-ellipse" />
  <text x="235" y="1420" class="attr-text">token</text>

  <ellipse cx="335" cy="1455" rx="40" ry="20" class="attr-ellipse" />
  <text x="335" y="1455" class="attr-text">otp</text>

  <ellipse cx="985" cy="1385" rx="55" ry="20" class="attr-ellipse" />
  <text x="985" y="1385" class="attr-text">expires_at</text>

  <ellipse cx="1105" cy="1420" rx="40" ry="20" class="attr-ellipse" />
  <text x="1105" y="1420" class="attr-text">used</text>

  <rect x="525" y="1395" width="300" height="50" class="entity-rect" />
  <text x="675" y="1420" class="entity-text">password_resets</text>

  <!-- Dashed Line to ADMIN -->
  <polyline points="675,1445 675,1580 890,1580 890,1650" class="dashed-connector" />
  <rect x="740" y="1570" width="90" height="20" class="card-box" />
  <text x="785" y="1580" class="card-text">has details</text>


  <!-- ======================================================== -->
  <!-- 8. COMPLAINTS (Side Left) -->
  <!-- ======================================================== -->
  <polyline points="555,95 120,95 120,845 160,845" class="connector" />
  <rect x="108" y="470" width="24" height="20" class="card-box" />
  <text x="120" y="480" class="card-text">1</text>

  <polygon points="160,845 220,870 160,895 100,870" class="rel-diamond" />
  <text x="160" y="870" class="rel-text">raises</text>

  <line x1="160" y1="895" x2="160" y2="955" class="connector" />
  <rect x="148" y="915" width="24" height="20" class="card-box" />
  <text x="160" y="925" class="card-text">M</text>

  <line x1="160" y1="980" x2="45" y2="1035" class="connector" />
  <line x1="160" y1="980" x2="140" y2="1050" class="connector" />
  <line x1="160" y1="980" x2="240" y2="1050" class="connector" />
  <line x1="160" y1="980" x2="330" y2="1030" class="connector" />
  <line x1="160" y1="980" x2="370" y2="980" class="connector" />

  <ellipse cx="45" cy="1035" rx="40" ry="20" class="attr-ellipse" />
  <text x="45" y="1035" class="attr-text-pk">id</text>

  <ellipse cx="140" cy="1050" rx="50" ry="20" class="attr-ellipse" />
  <text x="140" y="1050" class="attr-text">subject</text>

  <ellipse cx="240" cy="1050" rx="45" ry="20" class="attr-ellipse" />
  <text x="240" y="1050" class="attr-text">detail</text>

  <ellipse cx="330" cy="1030" rx="45" ry="20" class="attr-ellipse" />
  <text x="330" y="1030" class="attr-text">status</text>

  <ellipse cx="370" cy="980" rx="55" ry="20" class="attr-ellipse" />
  <text x="370" y="980" class="attr-text">admin_reply</text>

  <rect x="50" y="955" width="220" height="50" class="entity-rect" />
  <text x="160" y="980" class="entity-text">complaints</text>


  <!-- ======================================================== -->
  <!-- 9. ADMIN_ROOMS & ADMIN (Bottom Entities) -->
  <!-- ======================================================== -->
  <line x1="360" y1="1675" x2="160" y2="1640" class="connector" />
  <line x1="360" y1="1675" x2="180" y2="1705" class="connector" />
  <line x1="360" y1="1675" x2="260" y2="1740" class="connector" />

  <ellipse cx="160" cy="1640" rx="40" ry="20" class="attr-ellipse" />
  <text x="160" y="1640" class="attr-text-pk">id</text>

  <ellipse cx="180" cy="1705" rx="45" ry="20" class="attr-ellipse" />
  <text x="180" y="1705" class="attr-text">label</text>

  <ellipse cx="260" cy="1740" rx="45" ry="20" class="attr-ellipse" />
  <text x="260" y="1740" class="attr-text">value</text>

  <rect x="250" y="1650" width="220" height="50" class="entity-rect" />
  <text x="360" y="1675" class="entity-text">admin_rooms</text>

  <line x1="470" y1="1675" x2="780" y2="1675" class="connector" />
  <rect x="613" y="1665" width="24" height="20" class="card-box" />
  <text x="625" y="1675" class="card-text">M</text>

  <line x1="890" y1="1675" x2="630" y2="1740" class="connector" />
  <line x1="890" y1="1675" x2="1020" y2="1640" class="connector" />
  <line x1="890" y1="1675" x2="1080" y2="1695" class="connector" />
  <line x1="890" y1="1675" x2="1050" y2="1745" class="connector" />

  <ellipse cx="630" cy="1740" rx="65" ry="20" class="attr-ellipse" />
  <text x="630" y="1740" class="attr-text">room_id FK</text>

  <ellipse cx="1020" cy="1640" rx="40" ry="20" class="attr-ellipse" />
  <text x="1020" y="1640" class="attr-text-pk">id</text>

  <ellipse cx="1080" cy="1695" rx="55" ry="20" class="attr-ellipse" />
  <text x="1080" y="1695" class="attr-text">username</text>

  <ellipse cx="1050" cy="1745" rx="55" ry="20" class="attr-ellipse" />
  <text x="1050" y="1745" class="attr-text">password</text>

  <rect x="780" y="1650" width="220" height="50" class="entity-rect" />
  <text x="890" y="1675" class="entity-text">admin</text>

</svg>
"""

    svg_path = r'c:\projects\VisionEdge\visionedge_er_diagram.svg'
    html_path = r'c:\projects\VisionEdge\render_exact_template.html'
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
        '--window-size=1400,1900',
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Chrome exit code:", res.returncode)

    artifact_dir = r'C:\Users\user\.gemini\antigravity-ide\brain\e6764f65-6bff-4c78-a176-990deb180a57'
    if os.path.exists(artifact_dir):
        shutil.copy(png_path, os.path.join(artifact_dir, 'visionedge_er_diagram.png'))
        shutil.copy(r'c:\projects\VisionEdge\visionedge_er_diagram.drawio', os.path.join(artifact_dir, 'visionedge_er_diagram.drawio'))
        shutil.copy(svg_path, os.path.join(artifact_dir, 'visionedge_er_diagram.svg'))
        print("Updated artifact files with exact template structure!")

if __name__ == '__main__':
    generate_exact_template_er()
