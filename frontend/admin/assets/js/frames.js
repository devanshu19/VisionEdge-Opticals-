let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    await loadFrames();
    
    document.getElementById('searchFrame').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadFrames(e.target.value.trim());
        }, 300);
    });
});

async function loadFrames(search = '') {
    try {
        let url = `${API_BASE_URL}/inventory/frames`;
        if (search) url += `?search=${encodeURIComponent(search)}`;
        
        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch frames');
        
        const frames = await response.json();
        const tbody = document.getElementById('framesTableBody');
        tbody.innerHTML = '';
        
        if (frames.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4 text-muted">No frames found.</td></tr>';
            return;
        }
        
        const role = typeof getUserRole === 'function' ? getUserRole() : 'staff';
        const baseUrl = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL.replace(/\/api$/, '') : '';
        
        frames.forEach(f => {
            let stockBadge = f.stock > f.min_stock ? 'success' : (f.stock > 0 ? 'warning' : 'danger');
            let imgSrc = f.image || '';
            if (imgSrc && imgSrc.startsWith('assets/')) imgSrc = '../' + imgSrc;
            const imgTag = imgSrc 
                ? `<img src="${(imgSrc.startsWith('http') || imgSrc.startsWith('data:') || imgSrc.startsWith('../')) ? imgSrc : (baseUrl + (imgSrc.startsWith('/') ? '' : '/') + imgSrc)}" class="rounded me-2" style="width:36px; height:36px; object-fit:cover;">`
                : `<div class="rounded me-2 d-inline-flex align-items-center justify-content-center bg-light border text-muted" style="width:36px; height:36px;"><i class="bi bi-eyeglasses"></i></div>`;
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-medium text-primary align-middle">${f.frame_code}</td>
                <td class="fw-bold align-middle"><div class="d-flex align-items-center">${imgTag}<span>${f.name}</span></div></td>
                <td class="align-middle">${f.brand_name || '-'}</td>
                <td class="align-middle">${f.shape || '-'}</td>
                <td class="align-middle"><span class="badge bg-${stockBadge}">${f.stock}</span></td>
                <td class="align-middle">₹${f.selling_price}</td>
                <td class="align-middle"><span class="badge bg-light text-dark border">${f.status}</span></td>
                <td class="text-end pe-4 align-middle">
                    <a href="product-details.html?type=frame&id=${f.id}" class="btn btn-sm btn-outline-info rounded-circle me-1" title="View"><i class="bi bi-eye"></i></a>
                    ${role === 'admin' ? `
                    <button class="btn btn-sm btn-outline-secondary rounded-circle me-1" title="Adjust Stock" onclick="openAdjustStock(${f.id})"><i class="bi bi-box-seam"></i></button>
                    <a href="add-frame.html?id=${f.id}" class="btn btn-sm btn-outline-primary rounded-circle me-1" title="Edit"><i class="bi bi-pencil"></i></a>
                    <button class="btn btn-sm btn-outline-danger rounded-circle" title="Delete" onclick="deleteFrame(${f.id})"><i class="bi bi-trash"></i></button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading frames:", error);
        document.getElementById('framesTableBody').innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function deleteFrame(id) {
    if (!confirm('Are you sure you want to delete this frame?')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/frames/${id}`, { method: 'DELETE' });
        if (response.ok) {
            if(window.showToast) window.showToast('Deleted', 'Frame deleted successfully');
            loadFrames();
        } else {
            alert('Failed to delete frame');
        }
    } catch(err) {
        alert('An error occurred');
    }
}

function openAdjustStock(id) {
    document.getElementById('adjustFrameId').value = id;
    const modal = new bootstrap.Modal(document.getElementById('adjustStockModal'));
    modal.show();
}

async function submitStockAdjustment() {
    const id = document.getElementById('adjustFrameId').value;
    const data = {
        item_type: 'Frame',
        item_id: id,
        transaction_type: document.getElementById('txType').value,
        quantity: document.getElementById('txQty').value,
        reason: document.getElementById('txReason').value
    };
    
    if (!data.quantity || data.quantity < 1) return alert('Valid quantity required');
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/transactions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('adjustStockModal')).hide();
            document.getElementById('adjustStockForm').reset();
            if(window.showToast) window.showToast('Success', 'Stock adjusted successfully');
            loadFrames();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to adjust stock');
        }
    } catch (error) {
        alert('Error adjusting stock');
    }
}
