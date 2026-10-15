document.addEventListener('DOMContentLoaded', () => {
    loadPrescriptions();
    
    // Search event
    document.getElementById('searchRx').addEventListener('input', (e) => {
        clearTimeout(window.searchTimeout);
        window.searchTimeout = setTimeout(() => {
            loadPrescriptions();
        }, 500);
    });
    
    // Filter event
    document.getElementById('filterStatus').addEventListener('change', loadPrescriptions);
});

let currentRxId = null;

async function loadPrescriptions() {
    const search = document.getElementById('searchRx').value;
    const status = document.getElementById('filterStatus').value;
    
    let url = `${API_BASE_URL}/prescriptions/?status=${status}`;
    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }
    
    try {
        const response = await fetchWithAuth(url);
        if (response.ok) {
            const rxList = await response.json();
            renderPrescriptions(rxList);
        }
    } catch (error) {
        console.error("Error loading prescriptions:", error);
    }
}

function renderPrescriptions(rxList) {
    const tbody = document.getElementById('rxTableBody');
    tbody.innerHTML = '';
    
    const role = getUserRole();
    
    if (rxList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4">No prescriptions found</td></tr>';
        return;
    }
    
    rxList.forEach(rx => {
        let statusBadge = '';
        if (rx.status === 'Completed') statusBadge = '<span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 px-2 py-1">Completed</span>';
        else if (rx.status === 'Draft') statusBadge = '<span class="badge bg-warning bg-opacity-10 text-warning border border-warning border-opacity-25 px-2 py-1">Draft</span>';
        else statusBadge = `<span class="badge bg-secondary bg-opacity-10 text-secondary border border-secondary border-opacity-25 px-2 py-1">${rx.status}</span>`;
        
        let actionBtns = `
            <a href="view-prescription.html?id=${rx.id}" class="btn btn-sm btn-outline-info rounded-circle me-1" title="View"><i class="bi bi-eye"></i></a>
            <a href="edit-prescription.html?id=${rx.id}" class="btn btn-sm btn-outline-primary rounded-circle me-1" title="Edit"><i class="bi bi-pencil"></i></a>
            <button class="btn btn-sm btn-outline-secondary rounded-circle me-1" onclick="downloadPDF(${rx.id})" title="Download PDF"><i class="bi bi-file-pdf"></i></button>
        `;
        
        if (role === 'admin') {
            actionBtns += `<button class="btn btn-sm btn-outline-danger rounded-circle" onclick="showDeleteModal(${rx.id})" title="Delete"><i class="bi bi-trash"></i></button>`;
        }
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="ps-4 fw-medium text-primary">${rx.prescription_number || '-'}</td>
            <td><div class="fw-bold">${rx.customer_name}</div></td>
            <td>${rx.doctor_name || '-'}</td>
            <td>${rx.date}</td>
            <td>${rx.expiry_date || '-'}</td>
            <td>${statusBadge}</td>
            <td class="text-end pe-4">${actionBtns}</td>
        `;
        tbody.appendChild(tr);
    });
}

function showDeleteModal(id) {
    currentRxId = id;
    const modal = new bootstrap.Modal(document.getElementById('deleteRxModal'));
    modal.show();
}

async function confirmDelete() {
    if (!currentRxId) return;
    
    const btn = document.getElementById('confirmDeleteBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...';
    btn.disabled = true;
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/${currentRxId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteRxModal'));
            modal.hide();
            loadPrescriptions();
            showToast('Success', 'Prescription deleted successfully');
        } else {
            const data = await response.json();
            alert(data.message || 'Failed to delete prescription');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error while deleting prescription');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
        currentRxId = null;
    }
}

function downloadPDF(id) {
    // Generate a secure URL by appending JWT (since it's a direct download in browser, standard fetch doesn't trigger file save easily without blobs)
    // Wait, the API requires a Bearer token. We can fetch it as a blob.
    
    showToast('Info', 'Generating PDF...');
    
    fetchWithAuth(`${API_BASE_URL}/prescriptions/${id}/pdf`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to generate PDF');
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Prescription_${id}.pdf`; // Fallback name
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showToast('Success', 'PDF downloaded successfully');
        })
        .catch(err => {
            console.error('Error downloading PDF:', err);
            showToast('Error', 'Could not download PDF');
        });
}

// Helper for toast
function showToast(title, message) {
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
