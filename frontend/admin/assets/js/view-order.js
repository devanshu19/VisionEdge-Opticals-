let currentOrder = null;

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('id');
    
    if (!orderId) {
        window.location.href = 'orders.html';
        return;
    }
    
    await loadOrderDetails(orderId);
    
    document.getElementById('newStatus').addEventListener('change', function() {
        document.getElementById('cancelWarning').style.display = this.value === 'Cancelled' ? 'block' : 'none';
    });
});

function getStatusColor(status) {
    switch (status) {
        case 'Pending': return 'warning';
        case 'Confirmed': return 'info';
        case 'Assembly': return 'primary';
        case 'Quality Check': return 'secondary';
        case 'Ready for Pickup': return 'success';
        case 'Delivered': return 'dark';
        case 'Cancelled': return 'danger';
        default: return 'light';
    }
}

async function loadOrderDetails(id) {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/${id}`);
        if (!response.ok) throw new Error('Failed to load order');
        
        const order = await response.json();
        currentOrder = order;
        
        // Header
        document.getElementById('oNumber').textContent = order.order_number;
        const badgeColor = getStatusColor(order.status);
        document.getElementById('oStatusBadge').className = `badge bg-${badgeColor} bg-opacity-10 text-${badgeColor} border border-${badgeColor} d-flex align-items-center fs-6 px-3`;
        document.getElementById('oStatusBadge').textContent = order.status;
        
        // Info
        document.getElementById('oDate').textContent = new Date(order.order_date).toLocaleDateString();
        document.getElementById('oDelivery').textContent = order.expected_delivery_date ? new Date(order.expected_delivery_date).toLocaleDateString() : 'TBD';
        document.getElementById('oPriority').textContent = order.priority;
        document.getElementById('oSalesPerson').textContent = order.sales_person_name;
        
        // Customer
        document.getElementById('oCustName').textContent = order.customer_name;
        document.getElementById('oCustPhone').textContent = order.customer_details.phone;
        document.getElementById('oCustEmail').textContent = order.customer_details.email || 'N/A';
        document.getElementById('oCustAddress').textContent = order.customer_details.address ? `${order.customer_details.address}, ${order.customer_details.city || ''}` : 'No address provided';
        
        // Prescription
        if (order.prescription_details) {
            document.getElementById('rxCard').style.display = 'block';
            const rx = order.prescription_details;
            document.getElementById('rxNumber').textContent = `(#${rx.prescription_number})`;
            document.getElementById('rxOdSph').textContent = rx.od.sph || '-';
            document.getElementById('rxOdCyl').textContent = rx.od.cyl || '-';
            document.getElementById('rxOdAxis').textContent = rx.od.axis || '-';
            document.getElementById('rxOdAdd').textContent = rx.od.add || '-';
            document.getElementById('rxOsSph').textContent = rx.os.sph || '-';
            document.getElementById('rxOsCyl').textContent = rx.os.cyl || '-';
            document.getElementById('rxOsAxis').textContent = rx.os.axis || '-';
            document.getElementById('rxOsAdd').textContent = rx.os.add || '-';
        }
        
        // Items
        const tbody = document.getElementById('oItemsBody');
        tbody.innerHTML = '';
        order.items.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4">
                    <div class="fw-bold">${item.product_code}</div>
                    <small class="text-muted">${item.product_name}</small>
                </td>
                <td><span class="badge bg-secondary">${item.item_type}</span></td>
                <td>${item.quantity}</td>
                <td>₹${item.unit_price.toFixed(2)}</td>
                <td>₹${item.discount.toFixed(2)}</td>
                <td class="text-end pe-4 fw-bold">₹${item.total_price.toFixed(2)}</td>
            `;
            tbody.appendChild(tr);
        });
        
        // Financials
        document.getElementById('oSubtotal').textContent = `₹${order.subtotal.toFixed(2)}`;
        document.getElementById('oDiscount').textContent = `- ₹${order.discount.toFixed(2)}`;
        document.getElementById('oGst').textContent = `₹${order.gst.toFixed(2)}`;
        document.getElementById('oTotal').textContent = `₹${order.total_amount.toFixed(2)}`;
        
        // Timeline
        const timeline = document.getElementById('oTimeline');
        timeline.innerHTML = '';
        order.history.reverse().forEach(h => {
            const dateStr = new Date(h.timestamp).toLocaleString();
            const div = document.createElement('div');
            div.className = 'timeline-item';
            div.innerHTML = `
                <div class="fw-bold text-${getStatusColor(h.status)}">${h.status}</div>
                <div class="small text-muted mb-1">${dateStr} • By ${h.username}</div>
                ${h.remarks ? `<div class="bg-light p-2 rounded small border">${h.remarks}</div>` : ''}
            `;
            timeline.appendChild(div);
        });
        
    } catch (e) {
        console.error(e);
        alert('Failed to load order details');
    }
}

function openUpdateStatus() {
    if (!currentOrder) return;
    document.getElementById('newStatus').value = currentOrder.status;
    document.getElementById('statusRemarks').value = '';
    document.getElementById('cancelWarning').style.display = currentOrder.status === 'Cancelled' ? 'block' : 'none';
    
    const modal = new bootstrap.Modal(document.getElementById('updateStatusModal'));
    modal.show();
}

async function submitStatusUpdate() {
    const status = document.getElementById('newStatus').value;
    const remarks = document.getElementById('statusRemarks').value;
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/${currentOrder.id}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status, remarks })
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('updateStatusModal')).hide();
            if(window.showToast) window.showToast('Updated', 'Order status updated successfully');
            await loadOrderDetails(currentOrder.id);
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to update status');
        }
    } catch (e) {
        alert('Network Error');
    }
}
