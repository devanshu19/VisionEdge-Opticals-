document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type'); // 'frame' or 'lens'
    const id = urlParams.get('id');
    
    if (!type || !id) {
        alert('Invalid product link');
        window.location.href = 'inventory-dashboard.html';
        return;
    }
    
    document.getElementById('breadcrumbType').textContent = type.charAt(0).toUpperCase() + type.slice(1);
    
    if (typeof getUserRole === 'function' && getUserRole() === 'admin') {
        document.getElementById('actionButtons').innerHTML = `
            <a href="add-${type}.html?id=${id}" class="btn btn-outline-primary shadow-sm"><i class="bi bi-pencil me-2"></i>Edit Product</a>
        `;
    }
    
    await loadProductDetails(type, id);
    await loadTransactions(type, id);
});

async function loadProductDetails(type, id) {
    try {
        const endpoint = type === 'frame' ? 'frames' : 'lenses';
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/${endpoint}/${id}`);
        if (!response.ok) throw new Error('Failed to load product details');
        
        const p = await response.json();
        
        document.getElementById('pName').textContent = p.name;
        document.getElementById('pCode').textContent = p.frame_code || p.lens_code;
        document.getElementById('pStatus').textContent = p.status;
        document.getElementById('pStock').textContent = p.stock;
        document.getElementById('pStock').className = p.stock > p.min_stock ? 'fw-bold fs-5 text-success' : (p.stock > 0 ? 'fw-bold fs-5 text-warning' : 'fw-bold fs-5 text-danger');
        document.getElementById('pMinStock').textContent = p.min_stock;
        document.getElementById('pLocation').textContent = p.location || 'Not Set';
        document.getElementById('pPurchasePrice').textContent = `₹${p.purchase_price}`;
        document.getElementById('pSellingPrice').textContent = `₹${p.selling_price}`;
        
        const specContainer = document.getElementById('specContainer');
        specContainer.innerHTML = '';
        
        const imgWrapper = document.getElementById('productIcon').parentElement;
        if (p.image && p.image.trim()) {
            const baseUrl = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL.replace(/\/api$/, '') : '';
            const fullImgUrl = (p.image.startsWith('http') || p.image.startsWith('data:')) ? p.image : (baseUrl + (p.image.startsWith('/') ? '' : '/') + p.image);
            imgWrapper.className = 'mb-3 text-center';
            imgWrapper.style.width = 'auto';
            imgWrapper.style.height = 'auto';
            imgWrapper.innerHTML = `<img src="${fullImgUrl}" class="rounded border shadow-sm" style="max-height:140px; max-width:100%; object-fit:contain;">`;
        } else {
            if (type === 'frame') {
                document.getElementById('productIcon').className = 'bi bi-eyeglasses text-primary fs-1';
            } else {
                document.getElementById('productIcon').className = 'bi bi-circle text-primary fs-1';
            }
        }
        
        // Render common specs
        addSpecItem(specContainer, 'Brand', p.brand_name || '-');
        addSpecItem(specContainer, 'Category', p.category_name || '-');
        addSpecItem(specContainer, 'Supplier', p.supplier_name || '-');
        
        if (type === 'frame') {
            addSpecItem(specContainer, 'Shape', p.shape || '-');
            addSpecItem(specContainer, 'Material', p.material || '-');
            addSpecItem(specContainer, 'Size', p.size || '-');
            addSpecItem(specContainer, 'Color', p.color || '-');
            addSpecItem(specContainer, 'Gender', p.gender || '-');
        } else {
            addSpecItem(specContainer, 'Lens Type', p.lens_type || '-');
            addSpecItem(specContainer, 'Material', p.material || '-');
            addSpecItem(specContainer, 'Index', p.index || '-');
            addSpecItem(specContainer, 'Coating', p.coating || '-');
            addSpecItem(specContainer, 'Power Range', p.power_range || '-');
        }
        
    } catch (e) {
        console.error(e);
        alert('Error loading product details.');
    }
}

function addSpecItem(container, label, value) {
    container.innerHTML += `
        <div class="col-sm-6 col-md-4">
            <div class="p-3 border rounded bg-light">
                <small class="text-muted d-block mb-1">${label}</small>
                <span class="fw-medium">${value}</span>
            </div>
        </div>
    `;
}

async function loadTransactions(type, id) {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/transactions/${type}/${id}`);
        if (!response.ok) throw new Error('Failed to fetch transactions');
        
        const txs = await response.json();
        const tbody = document.getElementById('txHistoryBody');
        tbody.innerHTML = '';
        
        if (txs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-muted">No transactions found.</td></tr>';
            return;
        }
        
        txs.forEach(tx => {
            const tr = document.createElement('tr');
            let color = 'secondary';
            if (tx.transaction_type === 'Stock In') color = 'success';
            if (tx.transaction_type === 'Stock Out') color = 'danger';
            if (tx.transaction_type === 'Sale') color = 'primary';
            
            const d = new Date(tx.date);
            const dateStr = d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            tr.innerHTML = `
                <td class="ps-4 text-muted small">${dateStr}</td>
                <td><span class="badge bg-${color} bg-opacity-10 text-${color}">${tx.transaction_type}</span></td>
                <td class="fw-bold">${tx.transaction_type === 'Stock Out' || tx.transaction_type === 'Sale' ? '-' : '+'}${tx.quantity}</td>
                <td>${tx.reason || '-'}</td>
                <td>${tx.username || '-'}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        document.getElementById('txHistoryBody').innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading history.</td></tr>';
    }
}
