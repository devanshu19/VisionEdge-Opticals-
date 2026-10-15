from flask import Blueprint, jsonify, request, send_file
from models import db, User, Customer, Prescription, Frame, Lens, Order, OrderItem, Billing, Appointment, InventoryTransaction
from auth_utils import roles_required
from datetime import datetime, timedelta
from sqlalchemy import func
import os

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@roles_required('admin', 'staff')
def get_dashboard_summary():
    # Summary Metrics
    total_customers = Customer.query.count()
    total_orders = Order.query.count()
    
    total_sales = db.session.query(func.sum(Billing.total_amount)).filter(Billing.payment_status == 'Paid').scalar() or 0.0
    total_appointments = Appointment.query.count()
    
    pending_orders = Order.query.filter(Order.status != 'Delivered', Order.status != 'Cancelled').count()
    
    low_stock_frames = Frame.query.filter(Frame.stock <= Frame.min_stock).count()
    low_stock_lenses = Lens.query.filter(Lens.stock <= Lens.min_stock).count()
    low_stock_items = low_stock_frames + low_stock_lenses

    # Monthly Revenue Chart Data
    current_year = datetime.utcnow().year
    monthly_sales = db.session.query(
        func.extract('month', Billing.created_at).label('month'),
        func.sum(Billing.total_amount).label('total')
    ).filter(
        func.extract('year', Billing.created_at) == current_year,
        Billing.payment_status == 'Paid'
    ).group_by('month').all()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    revenue_data = [0] * 12
    for item in monthly_sales:
        month_idx = int(item.month) - 1
        revenue_data[month_idx] = float(item.total)

    # Sales Distribution Pie Chart Data
    # Join Billing -> Order -> OrderItem
    distribution = db.session.query(
        OrderItem.item_type,
        func.sum(OrderItem.total_price)
    ).join(Order).join(Billing).filter(
        Billing.payment_status == 'Paid'
    ).group_by(OrderItem.item_type).all()
    
    dist_labels = [d[0] for d in distribution]
    dist_data = [float(d[1]) for d in distribution]

    # Real Inventory Distribution (Frames vs Lenses)
    frame_count = Frame.query.count()
    lens_count = Lens.query.count()
    inv_labels = ['Frames', 'Lenses']
    inv_counts = [frame_count, lens_count]

    # Real Payment Methods Distribution
    pmt_query = db.session.query(
        Billing.payment_method,
        func.count(Billing.id)
    ).filter(Billing.payment_status == 'Paid').group_by(Billing.payment_method).all()
    
    pmt_labels = [p[0].split('|')[0] if p[0] else 'Direct' for p in pmt_query]
    pmt_data = [int(p[1]) for p in pmt_query]
    if not pmt_labels:
        pmt_labels = ['Credit Card', 'Cash on Delivery']
        pmt_data = [0, 0]

    return jsonify({
        "summary": {
            "customers": total_customers,
            "orders": total_orders,
            "sales": total_sales,
            "appointments": total_appointments,
            "pending_orders": pending_orders,
            "low_stock_items": low_stock_items
        },
        "charts": {
            "revenue": {
                "labels": months,
                "data": revenue_data
            },
            "distribution": {
                "labels": inv_labels,
                "data": inv_counts
            },
            "inventory": {
                "labels": inv_labels,
                "data": inv_counts
            },
            "payment_methods": {
                "labels": pmt_labels,
                "data": pmt_data
            }
        }
    })

@reports_bp.route('/sales', methods=['GET'])
@roles_required('admin')
def get_sales_report():
    period = request.args.get('period', 'monthly') # daily, weekly, monthly, yearly
    
    # Calculate totals
    total_revenue = db.session.query(func.sum(Billing.total_amount)).filter_by(payment_status='Paid').scalar() or 0.0
    total_transactions = Billing.query.filter_by(payment_status='Paid').count()
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0.0
    
    # Time series data
    query = db.session.query(
        func.date(Billing.created_at).label('date'),
        func.sum(Billing.total_amount).label('revenue')
    ).filter_by(payment_status='Paid').group_by(func.date(Billing.created_at)).order_by(func.date(Billing.created_at).desc()).limit(30).all()
    
    timeline = [{"date": str(q.date), "revenue": float(q.revenue)} for q in query]

    return jsonify({
        "metrics": {
            "total_revenue": total_revenue,
            "total_transactions": total_transactions,
            "avg_order_value": avg_order_value
        },
        "timeline": timeline
    })

@reports_bp.route('/inventory', methods=['GET'])
@roles_required('admin', 'staff')
def get_inventory_report():
    total_frames = db.session.query(func.sum(Frame.stock)).scalar() or 0
    total_lenses = db.session.query(func.sum(Lens.stock)).scalar() or 0
    
    # Low stock
    low_frames = Frame.query.filter(Frame.stock <= Frame.min_stock).all()
    low_lenses = Lens.query.filter(Lens.stock <= Lens.min_stock).all()
    
    alerts = []
    for f in low_frames:
        alerts.append({"type": "Frame", "name": f.name, "stock": f.stock, "status": "Out of Stock" if f.stock == 0 else "Low Stock"})
    for l in low_lenses:
        alerts.append({"type": "Lens", "name": l.name, "stock": l.stock, "status": "Out of Stock" if l.stock == 0 else "Low Stock"})
        
    # Top selling frames (using order items)
    top_frames_query = db.session.query(
        Frame.name,
        func.sum(OrderItem.quantity).label('sold')
    ).join(OrderItem, OrderItem.item_id == Frame.id)\
     .filter(OrderItem.item_type == 'Frame')\
     .group_by(Frame.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
     
    top_frames = [{"name": f[0], "sold": int(f[1])} for f in top_frames_query]
    
    top_lenses_query = db.session.query(
        Lens.name,
        func.sum(OrderItem.quantity).label('sold')
    ).join(OrderItem, OrderItem.item_id == Lens.id)\
     .filter(OrderItem.item_type == 'Lens')\
     .group_by(Lens.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
     
    top_lenses = [{"name": l[0], "sold": int(l[1])} for l in top_lenses_query]

    return jsonify({
        "metrics": {
            "total_frames": int(total_frames),
            "total_lenses": int(total_lenses),
            "low_stock_count": len(alerts)
        },
        "alerts": alerts,
        "top_frames": top_frames,
        "top_lenses": top_lenses
    })

@reports_bp.route('/appointments', methods=['GET'])
@roles_required('admin', 'staff')
def get_appointment_report():
    total = Appointment.query.count()
    completed = Appointment.query.filter_by(status='Completed').count()
    cancelled = Appointment.query.filter_by(status='Cancelled').count()
    pending = Appointment.query.filter_by(status='Pending').count()
    
    return jsonify({
        "metrics": {
            "total": total,
            "completed": completed,
            "cancelled": cancelled,
            "pending": pending
        },
        "chart": {
            "labels": ["Completed", "Pending", "Cancelled"],
            "data": [completed, pending, cancelled]
        }
    })

@reports_bp.route('/customers', methods=['GET'])
@roles_required('admin', 'staff')
def get_customer_report():
    total = Customer.query.count()
    
    today = datetime.utcnow()
    first_day_month = today.replace(day=1, hour=0, minute=0, second=0)
    new_this_month = Customer.query.filter(Customer.created_at >= first_day_month).count()
    
    # Growth Chart
    growth = db.session.query(
        func.extract('month', Customer.created_at).label('month'),
        func.count(Customer.id).label('count')
    ).filter(func.extract('year', Customer.created_at) == today.year)\
     .group_by('month').all()
     
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    growth_data = [0] * 12
    for item in growth:
        month_idx = int(item.month) - 1
        growth_data[month_idx] = int(item.count)
        
    return jsonify({
        "metrics": {
            "total": total,
            "new_this_month": new_this_month
        },
        "chart": {
            "labels": months,
            "data": growth_data
        }
    })

@reports_bp.route('/export/excel', methods=['GET'])
@roles_required('admin', 'staff')
def export_excel():
    from openpyxl import Workbook
    import io
    
    report_type = request.args.get('type', 'sales')
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    
    if report_type == 'sales':
        ws.title = "Sales Report"
        headers = ["Invoice No", "Date", "Customer ID", "Order ID", "Subtotal", "Discount", "GST", "Total Amount", "Payment Method", "Payment Status"]
        ws.append(headers)
        
        bills = Billing.query.options(db.joinedload(Billing.order_rel)).order_by(Billing.created_at.desc()).all()
        for b in bills:
            ws.append([
                b.invoice_number,
                b.created_at.strftime("%Y-%m-%d"),
                b.order_rel.customer_id if b.order_rel else None,
                b.order_id,
                getattr(b, 'subtotal', b.total_amount),
                getattr(b, 'discount', 0),
                getattr(b, 'gst', 0),
                b.total_amount,
                b.payment_method,
                b.payment_status
            ])
        filename = "Sales_Report.xlsx"
        
    elif report_type == 'inventory':
        ws.title = "Inventory Report"
        headers = ["Item Type", "Code", "Name", "Stock", "Min Stock", "Price"]
        ws.append(headers)
        
        frames = Frame.query.all()
        for f in frames:
            ws.append(["Frame", f.frame_code, f.name, f.stock, f.min_stock, f.selling_price])
            
        lenses = Lens.query.all()
        for l in lenses:
            ws.append(["Lens", l.lens_code, l.name, l.stock, l.min_stock, l.selling_price])
            
        filename = "Inventory_Report.xlsx"
    else:
        return jsonify({"message": "Invalid report type"}), 400
        
    wb.save(output)
    output.seek(0)
    return send_file(output, download_name=filename, as_attachment=True)

@reports_bp.route('/export/pdf', methods=['GET'])
@roles_required('admin', 'staff')
def export_pdf():
    from fpdf import FPDF
    import io
    
    report_type = request.args.get('type', 'sales')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    if report_type == 'sales':
        pdf.cell(0, 10, 'Sales Report', 0, 1, 'C')
        pdf.set_font('Arial', 'B', 10)
        
        # Header
        pdf.cell(40, 10, 'Invoice No', 1)
        pdf.cell(40, 10, 'Date', 1)
        pdf.cell(40, 10, 'Total', 1)
        pdf.cell(40, 10, 'Status', 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 10)
        bills = Billing.query.order_by(Billing.created_at.desc()).limit(50).all()
        for b in bills:
            pdf.cell(40, 10, str(b.invoice_number), 1)
            pdf.cell(40, 10, str(b.created_at.strftime("%Y-%m-%d")), 1)
            pdf.cell(40, 10, f"Rs. {b.total_amount:.2f}", 1)
            pdf.cell(40, 10, str(b.payment_status), 1)
            pdf.ln()
            
        filename = "Sales_Report.pdf"
        
    else:
        return jsonify({"message": "Invalid report type"}), 400
        
    output = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
    return send_file(output, download_name=filename, as_attachment=True, mimetype='application/pdf')
