import os
from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.set_text_color(13, 110, 253) # Bootstrap primary blue
        self.cell(0, 10, 'VisionEdge Opticals', 0, 1, 'L')
        
        self.set_font('Arial', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, 'AI-Powered Smart Optical Management System', 0, 1, 'L')
        
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, 'Opp. Sardar Patel Stadium, Navrangpura, Ahmedabad, Gujarat 380009', 0, 1, 'L')
        self.cell(0, 5, 'Phone: +91 82382 40028', 0, 1, 'L')
        self.cell(0, 5, 'Email: chaudharidevanshu1912@gmail.com', 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Thank you for choosing VisionEdge Opticals', 0, 0, 'C')


def generate_invoice_pdf(billing, order_items, customer):
    """
    Generate a professional PDF invoice using fpdf.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_dir = os.path.join(base_dir, 'media', 'invoices')
    os.makedirs(media_dir, exist_ok=True)
    
    filename = f"{billing.invoice_number}.pdf"
    filepath = os.path.join(media_dir, filename)
    
    pdf = InvoicePDF()
    pdf.add_page()
    
    # 2. Invoice Details & Customer Info
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(95, 8, 'INVOICE DETAILS', 0, 0)
    pdf.cell(95, 8, 'BILL TO', 0, 1)
    
    pdf.set_font('Arial', '', 10)
    
    pdf.cell(95, 6, f'Invoice Number: {billing.invoice_number}', 0, 0)
    pdf.cell(95, 6, f'Name: {customer.name}', 0, 1)
    
    pdf.cell(95, 6, f'Date: {billing.created_at.strftime("%Y-%m-%d %H:%M")}', 0, 0)
    pdf.cell(95, 6, f'Phone: {customer.phone}', 0, 1)
    
    pdf.cell(95, 6, f'Order ID: {billing.order_id}', 0, 0)
    pdf.cell(95, 6, f'Address: {customer.address or "N/A"}', 0, 1)
    
    pdf.cell(95, 6, f'Status: {billing.payment_status}', 0, 1)
    pdf.ln(10)
    
    # 3. Order Items Table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'ORDER ITEMS', 0, 1)
    
    pdf.set_fill_color(248, 249, 250)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(70, 8, 'Item', 1, 0, 'L', fill=True)
    pdf.cell(25, 8, 'Type', 1, 0, 'C', fill=True)
    pdf.cell(15, 8, 'Qty', 1, 0, 'C', fill=True)
    pdf.cell(25, 8, 'Unit Price', 1, 0, 'R', fill=True)
    pdf.cell(25, 8, 'Discount', 1, 0, 'R', fill=True)
    pdf.cell(30, 8, 'Total', 1, 1, 'R', fill=True)
    
    pdf.set_font('Arial', '', 10)
    for item in order_items:
        pdf.cell(70, 8, item['product_name'][:35], 1, 0, 'L')
        pdf.cell(25, 8, item['item_type'], 1, 0, 'C')
        pdf.cell(15, 8, str(item['quantity']), 1, 0, 'C')
        pdf.cell(25, 8, f"Rs. {item['unit_price']:.2f}", 1, 0, 'R')
        pdf.cell(25, 8, f"Rs. {item['discount']:.2f}", 1, 0, 'R')
        pdf.cell(30, 8, f"Rs. {item['total_price']:.2f}", 1, 1, 'R')
        
    pdf.ln(5)
    
    # 4. Summary Table
    pdf.set_font('Arial', '', 10)
    
    pdf.set_x(120)
    pdf.cell(40, 6, 'Subtotal:', 0, 0, 'R')
    pdf.cell(30, 6, f"Rs. {billing.subtotal:.2f}", 0, 1, 'R')
    
    total_item_disc = sum(item['discount'] for item in order_items)
    pdf.set_x(120)
    pdf.cell(40, 6, 'Item Discounts:', 0, 0, 'R')
    pdf.cell(30, 6, f"- Rs. {total_item_disc:.2f}", 0, 1, 'R')
    
    pdf.set_x(120)
    pdf.cell(40, 6, 'Extra Discount:', 0, 0, 'R')
    pdf.cell(30, 6, f"- Rs. {billing.discount:.2f}", 0, 1, 'R')
    
    pdf.set_x(120)
    pdf.cell(40, 6, f'GST ({billing.gst_percentage}%):', 0, 0, 'R')
    pdf.cell(30, 6, f"Rs. {billing.gst_amount:.2f}", 0, 1, 'R')
    
    pdf.ln(2)
    pdf.set_x(120)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 8, 'GRAND TOTAL:', 'T', 0, 'R')
    pdf.cell(30, 8, f"Rs. {billing.total_amount:.2f}", 'T', 1, 'R')
    
    pdf.ln(10)
    
    # 5. Payment Details
    pdf.set_x(10)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Payment Method: {billing.payment_method}", 0, 1)
    pdf.cell(0, 6, f"Payment Status: {billing.payment_status}", 0, 1)
    
    pdf.output(filepath)
    
    return f"media/invoices/{filename}"
