let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    await loadLenses();
    
    document.getElementById('searchLens').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadLenses(e.target.value.trim());
        }, 300);
    });
});

async function loadLenses(search = '') {
    try {
        let url = `${API_BASE_URL}/inventory/lenses`;
        if (search) url += `?search=${encodeURIComponent(search)}`;
        
        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch lenses');
        
        const lenses = await response.json();
        const tbody = document.getElementById('lensesTableBody');
        tbody.innerHTML = '';
        
        if (lenses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4 text-muted">No lenses found.</td></tr>';
            return;
        }
        
        const role = typeof getUserRole === 'function' ? getUserRole() : 'staff';
        const baseUrl = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL.replace(/\/api$/, '') : '';
        
        lenses.forEach(l => {
            let stockBadge = l.stock > l.min_stock ? 'success' : (l.stock > 0 ? 'warning' : 'danger');
            const imgTag = l.image 
                ? `<img src="${(l.image.startsWith('http') || l.image.startsWith('data:')) ? l.image : (baseUrl + (l.image.startsWith('/') ? '' : '/') + l.image)}" class="rounded me-2" style="width:36px; height:36px; object-fit:cover;">`
                : `<div class="rounded me-2 d-inline-flex align-items-center justify-content-center bg-light border text-muted" style="width:36px; height:36px;"><i class="bi bi-disc"></i></div>`;
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-medium text-primary align-middle">${l.lens_code}</td>
                <td class="fw-bold align-middle"><div class="d-flex align-items-center">${imgTag}<span>${l.name}</span></div></td>
                <td class="align-middle">${l.lens_type || '-'}</td>
                <td class="align-middle">${l.index || '-'}</td>
                <td class="align-middle">${l.coating || '-'}</td>
                <td class="align-middle"><span class="badge bg-${stockBadge}">${l.stock}</span></td>
                <td class="align-middle">₹${l.selling_price}</td>
                <td class="text-end pe-4 align-middle">
                    <a href="product-details.html?type=lens&id=${l.id}" class="btn btn-sm btn-outline-info rounded-circle me-1" title="View"><i class="bi bi-eye"></i></a>
                    ${role === 'admin' ? `
                    <button class="btn btn-sm btn-outline-secondary rounded-circle me-1" title="Adjust Stock" onclick="openAdjustStock(${l.id})"><i class="bi bi-box-seam"></i></button>
                    <a href="add-lens.html?id=${l.id}" class="btn btn-sm btn-outline-primary rounded-circle me-1" title="Edit"><i class="bi bi-pencil"></i></a>
                    <button class="btn btn-sm btn-outline-danger rounded-circle" title="Delete" onclick="deleteLens(${l.id})"><i class="bi bi-trash"></i></button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading lenses:", error);
        document.getElementById('lensesTableBody').innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function deleteLens(id) {
    if (!confirm('Are you sure you want to delete this lens?')) return;
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/lenses/${id}`, { method: 'DELETE' });
        if (response.ok) {
            if(window.showToast) window.showToast('Deleted', 'Lens deleted successfully');
            loadLenses();
        } else {
            alert('Failed to delete lens');
        }
    } catch(err) {
        alert('An error occurred');
    }
}

function openAdjustStock(id) {
    document.getElementById('adjustLensId').value = id;
    const modal = new bootstrap.Modal(document.getElementById('adjustStockModal'));
    modal.show();
}

async function submitStockAdjustment() {
    const id = document.getElementById('adjustLensId').value;
    const data = {
        item_type: 'Lens',
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
            loadLenses();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to adjust stock');
        }
    } catch (error) {
        alert('Error adjusting stock');
    }
}
