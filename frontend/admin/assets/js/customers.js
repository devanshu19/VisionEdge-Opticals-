document.addEventListener('DOMContentLoaded', () => {
    loadCustomers();
    
    // Search event
    document.getElementById('searchCustomer').addEventListener('input', (e) => {
        // debounce search
        clearTimeout(window.searchTimeout);
        window.searchTimeout = setTimeout(() => {
            loadCustomers();
        }, 500);
    });
    
    // Filter event
    document.getElementById('filterStatus').addEventListener('change', loadCustomers);
    
    // Hide Export and Delete buttons if staff
    if (getUserRole() === 'staff') {
        const exportBtns = document.querySelectorAll('.admin-only');
        exportBtns.forEach(btn => btn.style.display = 'none');
    }
});

let currentCustomerId = null;

async function loadCustomers() {
    const search = document.getElementById('searchCustomer').value;
    const status = document.getElementById('filterStatus').value;
    
    let url = `${API_BASE_URL}/customers/?status=${status}`;
    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }
    
    try {
        const response = await fetchWithAuth(url);
        if (response.ok) {
            const customers = await response.json();
            renderCustomers(customers);
        }
    } catch (error) {
        console.error("Error loading customers:", error);
    }
}

function renderCustomers(customers) {
    const tbody = document.getElementById('customersTableBody');
    tbody.innerHTML = '';
    
    const role = getUserRole();
    
    if (customers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center py-4">No customers found</td></tr>';
        return;
    }
    
    customers.forEach(c => {
        const age = c.age ? `${c.age} yrs` : '-';
        const photoUrl = c.photo || 'https://via.placeholder.com/40';
        
        let statusBadge = '';
        if (c.status === 'Active') statusBadge = '<span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 px-2 py-1">Active</span>';
        else if (c.status === 'Inactive') statusBadge = '<span class="badge bg-warning bg-opacity-10 text-warning border border-warning border-opacity-25 px-2 py-1">Inactive</span>';
        else statusBadge = '<span class="badge bg-danger bg-opacity-10 text-danger border border-danger border-opacity-25 px-2 py-1">Blocked</span>';
        
        let actionBtns = `
            <a href="customer-details.html?id=${c.id}" class="btn btn-sm btn-outline-info rounded-circle me-1" title="View"><i class="bi bi-eye"></i></a>
            <a href="edit-customer.html?id=${c.id}" class="btn btn-sm btn-outline-primary rounded-circle me-1" title="Edit"><i class="bi bi-pencil"></i></a>
        `;
        
        if (role === 'admin') {
            actionBtns += `<button class="btn btn-sm btn-outline-danger rounded-circle" onclick="showDeleteModal(${c.id})" title="Delete"><i class="bi bi-trash"></i></button>`;
        }
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="ps-4 fw-medium text-muted">${c.customer_code || '-'}</td>
            <td><img src="${photoUrl}" class="rounded-circle" width="40" height="40" alt="Photo"></td>
            <td>
                <div class="fw-bold">${c.name}</div>
                <small class="text-muted">${c.email || ''}</small>
            </td>
            <td>${c.phone}</td>
            <td>${c.gender || '-'}</td>
            <td>${age}</td>
            <td>${c.city || '-'}</td>
            <td>${statusBadge}</td>
            <td class="text-end pe-4">${actionBtns}</td>
        `;
        tbody.appendChild(tr);
    });
}

function showDeleteModal(id) {
    currentCustomerId = id;
    const modal = new bootstrap.Modal(document.getElementById('deleteCustomerModal'));
    modal.show();
}

async function confirmDelete() {
    if (!currentCustomerId) return;
    
    const btn = document.getElementById('confirmDeleteBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...';
    btn.disabled = true;
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/${currentCustomerId}`, {
            method: 'DELETE'
        });
        
        const modalEl = document.getElementById('deleteCustomerModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();

        if (response.ok) {
            loadCustomers();
            showToast('Success', 'Customer deleted successfully');
        } else {
            const data = await response.json();
            alert(data.message || 'Failed to delete customer');
        }
    } catch (error) {
        console.error('Error deleting customer:', error);
        alert(error.message || 'Failed to delete customer');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
        currentCustomerId = null;
    }
}

// Basic CSV Export
async function exportCSV() {
    const status = document.getElementById('filterStatus').value;
    const response = await fetchWithAuth(`${API_BASE_URL}/customers/?status=${status}`);
    const data = await response.json();
    
    if (data.length === 0) return alert('No data to export');
    
    const headers = ['Code', 'Name', 'Phone', 'Email', 'Gender', 'Age', 'City', 'Status', 'Created At'];
    const rows = data.map(c => [
        c.customer_code, c.name, c.phone, c.email, c.gender, c.age, c.city, c.status, c.created_at
    ]);
    
    let csvContent = "data:text/csv;charset=utf-8," 
        + headers.join(",") + "\n"
        + rows.map(e => e.join(",")).join("\n");
        
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "customers.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function exportPDF() {
    window.print();
}

// Helper for toast
function showToast(title, message) {
    // Check if toast container exists
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toastHtml = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-primary text-white">
                <i class="bi bi-info-circle me-2"></i>
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', toastHtml);
    const toastEl = container.lastElementChild;
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}
