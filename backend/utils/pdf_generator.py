import os
from datetime import datetime
from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        # Company Header
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(13, 110, 253) # Bootstrap primary blue
        self.cell(120, 9, 'VisionEdge Opticals', 0, 0, 'L')
        
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(40, 40, 40)
        self.cell(70, 9, 'TAX INVOICE', 0, 1, 'R')
        
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 100, 100)
        self.cell(120, 5, 'AI-Powered Smart Optical Management System', 0, 0, 'L')
        self.set_font('Helvetica', 'I', 8)
        self.cell(70, 5, '(Original for Recipient)', 0, 1, 'R')
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(70, 70, 70)
        self.cell(0, 4, 'Opp. Sardar Patel Stadium, Navrangpura, Ahmedabad, Gujarat 380009', 0, 1, 'L')
        self.cell(0, 4, 'Phone: +91 82382 40028 | Email: chaudharidevanshu1912@gmail.com', 0, 1, 'L')
        self.cell(0, 4, 'GSTIN: 24AAACV1234F1Z5 | State: Gujarat (Code: 24) | HSN/SAC: 9004', 0, 1, 'L')
        self.ln(2)
        self.set_draw_color(210, 220, 230)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(210, 220, 230)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, 'Thank you for choosing VisionEdge Opticals! For customer care call +91 82382 40028', 0, 1, 'C')
        self.cell(0, 4, 'This is an authentic computer-generated GST tax invoice. No physical signature required.', 0, 0, 'C')


def generate_invoice_pdf(billing, order_items=None, customer=None):
    """
    Generate a professional GST PDF invoice using fpdf.
    Robust against any missing attributes or differing data structures.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_dir = os.path.join(base_dir, 'media', 'invoices')
    os.makedirs(media_dir, exist_ok=True)
    
    inv_num = getattr(billing, 'invoice_number', None) or f"INV-{getattr(billing, 'id', 1):05d}"
    filename = f"{inv_num}.pdf"
    filepath = os.path.join(media_dir, filename)
    
    # Resolve customer data safely
    cust_name = "Valued Customer"
    cust_phone = "N/A"
    cust_email = "N/A"
    cust_address = "N/A"
    
    if customer is None and hasattr(billing, 'order_rel') and billing.order_rel:
        customer = getattr(billing.order_rel, 'customer', None)
        
    if customer:
        first = getattr(customer, 'first_name', '') or ''
        last = getattr(customer, 'last_name', '') or ''
        full = f"{first} {last}".strip()
        if not full:
            full = getattr(customer, 'name', '') or getattr(customer, 'username', '')
        if full:
            cust_name = full
            
        cust_phone = getattr(customer, 'phone', None) or "N/A"
        cust_email = getattr(customer, 'email', None) or "N/A"
        cust_address = getattr(customer, 'address', None) or "N/A"
        if getattr(customer, 'city', None):
            cust_address += f", {customer.city}"

    # Resolve order details
    order_ref = getattr(billing, 'order_id', 'N/A')
    order_num = order_ref
    if hasattr(billing, 'order_rel') and billing.order_rel:
        order_num = getattr(billing.order_rel, 'order_number', None) or order_ref
        
    created_dt = getattr(billing, 'created_at', None)
    if not created_dt:
        created_dt = datetime.utcnow()
    date_str = created_dt.strftime("%d-%b-%Y %I:%M %p")

    # Resolve items safely
    if order_items is None:
        order_items = []
        if hasattr(billing, 'order_rel') and billing.order_rel and hasattr(billing.order_rel, 'items'):
            for oi in billing.order_rel.items:
                pname = getattr(oi, 'product_name', None) or f"Eyewear Item #{getattr(oi, 'item_id', 1)}"
                itype = getattr(oi, 'item_type', 'Frame')
                qty = int(getattr(oi, 'quantity', 1) or 1)
                uprice = float(getattr(oi, 'unit_price', 0.0) or 0.0)
                disc = float(getattr(oi, 'discount', 0.0) or 0.0)
                tprice = float(getattr(oi, 'total_price', uprice * qty) or (uprice * qty))
                order_items.append({
                    "product_name": pname,
                    "item_type": itype,
                    "quantity": qty,
                    "unit_price": uprice,
                    "discount": disc,
                    "total_price": tprice
                })

    # Calculations
    subtotal = float(getattr(billing, 'subtotal', 0.0) or 0.0)
    discount = float(getattr(billing, 'discount', 0.0) or 0.0)
    gst_val = float(getattr(billing, 'gst', 0.0) or 0.0)
    total_amt = float(getattr(billing, 'total_amount', 0.0) or (subtotal - discount + gst_val))
    
    cgst_val = round(gst_val / 2.0, 2)
    sgst_val = round(gst_val - cgst_val, 2)
    
    pay_method = getattr(billing, 'payment_method', 'Razorpay Online') or 'Razorpay Online'
    pay_status = getattr(billing, 'payment_status', 'Paid') or 'Paid'

    # Build PDF
    pdf = InvoicePDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # 2-Column Info Block
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(245, 247, 250)
    pdf.cell(95, 6, '  INVOICE DETAILS', 1, 0, 'L', fill=True)
    pdf.cell(95, 6, '  BILLED TO', 1, 1, 'L', fill=True)
    
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    
    col1_lines = [
        f"Invoice No : {inv_num}",
        f"Invoice Date: {date_str}",
        f"Order Ref   : #{order_num}",
        f"Payment Mode: {pay_method}",
        f"Payment Stat: {pay_status.upper()}"
    ]
    
    col2_lines = [
        f"Name   : {cust_name[:36]}",
        f"Phone  : {cust_phone}",
        f"Email  : {cust_email[:36]}",
        f"Address: {cust_address[:42]}",
        "Place  : Gujarat, India (State Code: 24)"
    ]
    
    for c1, c2 in zip(col1_lines, col2_lines):
        pdf.cell(95, 5, f"  {c1}", 'LR', 0, 'L')
        pdf.cell(95, 5, f"  {c2}", 'LR', 1, 'L')
        
    pdf.cell(95, 1, '', 'LBR', 0)
    pdf.cell(95, 1, '', 'LBR', 1)
    pdf.ln(5)
    
    # Itemized Table
    pdf.set_fill_color(13, 110, 253)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 8.5)
    
    pdf.cell(10, 7, '#', 1, 0, 'C', fill=True)
    pdf.cell(75, 7, 'Description / Product', 1, 0, 'L', fill=True)
    pdf.cell(25, 7, 'Category', 1, 0, 'C', fill=True)
    pdf.cell(15, 7, 'Qty', 1, 0, 'C', fill=True)
    pdf.cell(30, 7, 'Unit Rate (INR)', 1, 0, 'R', fill=True)
    pdf.cell(35, 7, 'Amount (INR)', 1, 1, 'R', fill=True)
    
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(40, 40, 40)
    
    item_idx = 1
    if not order_items:
        # Fallback line item
        pdf.cell(10, 6, "1", 1, 0, 'C')
        pdf.cell(75, 6, "VisionEdge Eyewear Product", 1, 0, 'L')
        pdf.cell(25, 6, "Optical", 1, 0, 'C')
        pdf.cell(15, 6, "1", 1, 0, 'C')
        pdf.cell(30, 6, f"{subtotal:.2f}", 1, 0, 'R')
        pdf.cell(35, 6, f"{subtotal:.2f}", 1, 1, 'R')
    else:
        for it in order_items:
            pdf.cell(10, 6, str(item_idx), 1, 0, 'C')
            pname = str(it.get('product_name', 'Eyewear Item'))[:38]
            pdf.cell(75, 6, pname, 1, 0, 'L')
            pdf.cell(25, 6, str(it.get('item_type', 'Frame'))[:14], 1, 0, 'C')
            pdf.cell(15, 6, str(it.get('quantity', 1)), 1, 0, 'C')
            pdf.cell(30, 6, f"{float(it.get('unit_price', 0.0)):.2f}", 1, 0, 'R')
            pdf.cell(35, 6, f"{float(it.get('total_price', 0.0)):.2f}", 1, 1, 'R')
            item_idx += 1
            
    pdf.ln(3)
    
    # Financial Summary Table
    pdf.set_x(110)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(45, 5, 'Taxable Subtotal:', 0, 0, 'R')
    pdf.cell(35, 5, f"INR {subtotal:.2f}", 0, 1, 'R')
    
    if discount > 0:
        pdf.set_x(110)
        pdf.set_text_color(220, 53, 69)
        pdf.cell(45, 5, 'Discount Applied:', 0, 0, 'R')
        pdf.cell(35, 5, f"- INR {discount:.2f}", 0, 1, 'R')
        pdf.set_text_color(40, 40, 40)
        
    pdf.set_x(110)
    pdf.cell(45, 5, 'CGST @ 9%:', 0, 0, 'R')
    pdf.cell(35, 5, f"INR {cgst_val:.2f}", 0, 1, 'R')
    
    pdf.set_x(110)
    pdf.cell(45, 5, 'SGST @ 9%:', 0, 0, 'R')
    pdf.cell(35, 5, f"INR {sgst_val:.2f}", 0, 1, 'R')
    
    pdf.set_x(110)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(13, 110, 253)
    pdf.cell(45, 7, 'TOTAL AMOUNT:', 'T', 0, 'R')
    pdf.cell(35, 7, f"INR {total_amt:.2f}", 'T', 1, 'R')
    
    # Terms & Authorized Signatory Block
    pdf.ln(8)
    pdf.set_x(10)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(100, 4, 'TERMS & CONDITIONS:', 0, 0, 'L')
    pdf.cell(80, 4, 'FOR VISIONEDGE OPTICALS', 0, 1, 'R')
    
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(100, 3.5, '1. 1-Year Limited Warranty against manufacturer defects on all frames.', 0, 0, 'L')
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(13, 110, 253)
    pdf.cell(80, 3.5, 'Authorized Signatory', 0, 1, 'R')
    
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(100, 3.5, '2. Prescription lenses custom fabricated are non-returnable once cut.', 0, 0, 'L')
    pdf.cell(80, 3.5, '(Digitally verified by VisionEdge ERP)', 0, 1, 'R')
    pdf.cell(100, 3.5, '3. Subject to Ahmedabad jurisdiction.', 0, 1, 'L')
    
    # Save output
    pdf.output(filepath)
    
    return f"media/invoices/{filename}"
