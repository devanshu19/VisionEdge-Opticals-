let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    // Check if status is passed in URL
    const urlParams = new URLSearchParams(window.location.search);
    const statusParam = urlParams.get('status');
    if (statusParam && document.getElementById('statusFilter')) {
        document.getElementById('statusFilter').value = statusParam;
    }

    await loadBills();
    
    const searchInput = document.getElementById('searchBill');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                loadBills();
            }, 300);
        });
    }
    
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', loadBills);
    }
});

async function loadBills() {
    const search = document.getElementById('searchBill')?.value.trim() || '';
    const status = document.getElementById('statusFilter')?.value || '';
    
    try {
        let url = `${API_BASE_URL}/billing/?`;
        if (search) url += `search=${encodeURIComponent(search)}&`;
        if (status && status !== 'all') url += `status=${encodeURIComponent(status)}&`;
        
        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch bills');
        
        const bills = await response.json();
        const tbody = document.getElementById('billsTableBody');
        tbody.innerHTML = '';
        
        if (bills.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted">No invoices found.</td></tr>';
            return;
        }
        
        const role = typeof getUserRole === 'function' ? getUserRole() : 'staff';
        
        bills.forEach(b => {
            const dateStr = b.created_at ? b.created_at.split(' ')[0] : 'Today';
            const badgeClass = b.payment_status === 'Paid' ? 'success' : (b.payment_status === 'Partial' ? 'info' : 'warning');
            const adminToken = localStorage.getItem('token') || localStorage.getItem('jwtToken') || sessionStorage.getItem('token') || '';
            const pdfUrl = `${API_BASE_URL}/billing/${b.id}/pdf?token=${encodeURIComponent(adminToken)}`;
            const custName = b.customer_name || 'Customer';
            const total = (b.total_amount || 0).toFixed(2);
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-bold text-primary">${b.invoice_number}</td>
                <td>${dateStr}</td>
                <td>
                    <div class="fw-bold">${custName}</div>
                </td>
                <td><a href="view-order.html?id=${b.order_id}" class="text-decoration-none">#${b.order_id}</a></td>
                <td class="fw-bold">₹${total}</td>
                <td>
                    <span class="badge bg-${badgeClass} bg-opacity-10 text-${badgeClass} border border-${badgeClass} me-1">${b.payment_status || 'Pending'}</span>
                    <small class="text-muted">via ${b.payment_method || 'Cash'}</small>
                </td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary rounded-circle me-1" title="View PDF" onclick="previewPDF('${pdfUrl}', ${b.id})"><i class="bi bi-file-earmark-pdf"></i></button>
                    <a href="${pdfUrl}" download class="btn btn-sm btn-outline-success rounded-circle me-1" title="Download PDF" target="_blank"><i class="bi bi-download"></i></a>
                    ${role === 'admin' ? `
                    <button class="btn btn-sm btn-outline-danger rounded-circle" title="Delete Invoice" onclick="deleteBill(${b.id})"><i class="bi bi-trash"></i></button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading bills:", error);
        document.getElementById('billsTableBody').innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

function previewPDF(url, billId) {
    const frame = document.getElementById('pdfPreviewFrame');
    const downloadBtn = document.getElementById('btnDownloadFull');
    if (frame) frame.src = url;
    if (downloadBtn) downloadBtn.href = url;
    const modalEl = document.getElementById('previewModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    } else {
        window.open(url, '_blank');
    }
}

async function deleteBill(id) {
    if (!confirm('Are you sure you want to delete this invoice?')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/${id}`, { method: 'DELETE' });
        if (response.ok) {
            if(window.showToast) window.showToast('Deleted', 'Invoice deleted successfully');
            loadBills();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to delete invoice');
        }
    } catch(err) {
        alert('An error occurred');
    }
}
