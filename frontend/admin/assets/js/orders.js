let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    // Check if status is passed in URL
    const urlParams = new URLSearchParams(window.location.search);
    const statusParam = urlParams.get('status');
    if (statusParam) {
        document.getElementById('statusFilter').value = statusParam;
    }

    await loadOrders();
    
    document.getElementById('searchOrder').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadOrders();
        }, 300);
    });
    
    document.getElementById('statusFilter').addEventListener('change', loadOrders);
    
    document.getElementById('newStatus').addEventListener('change', function() {
        if(this.value === 'Cancelled') {
            document.getElementById('cancelWarning').style.display = 'block';
        } else {
            document.getElementById('cancelWarning').style.display = 'none';
        }
    });
});

function getStatusBadge(status) {
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

async function loadOrders() {
    const search = document.getElementById('searchOrder').value.trim();
    const status = document.getElementById('statusFilter').value;
    
    try {
        let url = `${API_BASE_URL}/orders?`;
        if (search) url += `search=${encodeURIComponent(search)}&`;
        if (status) url += `status=${encodeURIComponent(status)}&`;
        
        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch orders');
        
        const orders = await response.json();
        const tbody = document.getElementById('ordersTableBody');
        tbody.innerHTML = '';
        
        if (orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted">No orders found.</td></tr>';
            return;
        }
        
        const role = typeof getUserRole === 'function' ? getUserRole() : 'staff';
        
        orders.forEach(o => {
            const dateStr = new Date(o.order_date).toLocaleDateString();
            const badgeClass = getStatusBadge(o.status);
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-bold text-primary">${o.order_number}</td>
                <td>${dateStr}</td>
                <td>${o.customer_name}</td>
                <td>${o.items.length} items</td>
                <td class="fw-bold">₹${o.total_amount.toFixed(2)}</td>
                <td><span class="badge bg-${badgeClass} bg-opacity-10 text-${badgeClass} border border-${badgeClass}">${o.status}</span></td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-secondary rounded-circle me-1" title="Update Status" onclick="openUpdateStatus(${o.id}, '${o.status}')"><i class="bi bi-arrow-repeat"></i></button>
                    <a href="view-order.html?id=${o.id}" class="btn btn-sm btn-outline-info rounded-circle me-1" title="View"><i class="bi bi-eye"></i></a>
                    ${role === 'admin' ? `
                    <button class="btn btn-sm btn-outline-danger rounded-circle" title="Delete" onclick="deleteOrder(${o.id})"><i class="bi bi-trash"></i></button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading orders:", error);
        document.getElementById('ordersTableBody').innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

function openUpdateStatus(id, currentStatus) {
    document.getElementById('statusOrderId').value = id;
    document.getElementById('newStatus').value = currentStatus;
    document.getElementById('statusRemarks').value = '';
    document.getElementById('cancelWarning').style.display = currentStatus === 'Cancelled' ? 'block' : 'none';
    
    const modal = new bootstrap.Modal(document.getElementById('updateStatusModal'));
    modal.show();
}

async function submitStatusUpdate() {
    const id = document.getElementById('statusOrderId').value;
    const status = document.getElementById('newStatus').value;
    const remarks = document.getElementById('statusRemarks').value;
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/${id}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status, remarks })
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('updateStatusModal')).hide();
            if(window.showToast) window.showToast('Updated', 'Order status updated successfully');
            loadOrders();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to update status');
        }
    } catch (e) {
        alert('Network Error');
    }
}

async function deleteOrder(id) {
    if (!confirm('Are you sure you want to completely delete this order? This cannot be undone.')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/${id}`, { method: 'DELETE' });
        if (response.ok) {
            if(window.showToast) window.showToast('Deleted', 'Order deleted successfully');
            loadOrders();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to delete order');
        }
    } catch(err) {
        alert('An error occurred');
    }
}
