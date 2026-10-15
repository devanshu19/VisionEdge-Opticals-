document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([
        loadDropdown('brands', 'lBrand'),
        loadDropdown('categories?type=Lens', 'lCategory'),
        loadDropdown('suppliers', 'lSupplier')
    ]);
    
    // Image listeners
    const fileInput = document.getElementById('lImageFile');
    const urlInput = document.getElementById('lImageUrl');
    const removeBtn = document.getElementById('removeImgBtn');
    
    if (fileInput) {
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                const res = await fetch(`${API_BASE_URL}/inventory/upload-image`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${token}` },
                    body: formData
                });
                
                if (res.ok) {
                    const data = await res.json();
                    if (urlInput) urlInput.value = data.image_url;
                    updateImagePreview(data.image_url);
                } else {
                    const err = await res.json();
                    alert(err.message || 'Image upload failed');
                }
            } catch (err) {
                console.error('Image upload error:', err);
                alert('Failed to upload image file');
            }
        });
    }
    
    if (urlInput) {
        urlInput.addEventListener('input', (e) => {
            updateImagePreview(e.target.value);
        });
    }
    
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            if (urlInput) urlInput.value = '';
            if (fileInput) fileInput.value = '';
            updateImagePreview('');
        });
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const lensId = urlParams.get('id');
    
    if (lensId) {
        document.getElementById('pageTitle').textContent = 'Edit Lens';
        document.getElementById('breadcrumbActive').textContent = 'Edit Lens';
        document.getElementById('stockGroup').style.display = 'none'; // Stock updated via ledger
        await loadLensForEdit(lensId);
    }
    
    document.getElementById('lensForm').addEventListener('submit', handleFormSubmit);
});

function updateImagePreview(url) {
    const wrapper = document.getElementById('imgPreviewWrapper');
    const img = document.getElementById('imgPreview');
    if (!wrapper || !img) return;
    
    if (url && url.trim()) {
        const fullUrl = (url.startsWith('http') || url.startsWith('data:')) 
            ? url 
            : (API_BASE_URL.replace(/\/api$/, '') + (url.startsWith('/') ? '' : '/') + url);
        img.src = fullUrl;
        wrapper.style.display = 'block';
    } else {
        img.src = '';
        wrapper.style.display = 'none';
    }
}

async function loadDropdown(endpoint, selectId) {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/${endpoint}`);
        if (response.ok) {
            const data = await response.json();
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Select Option...</option>';
            data.forEach(item => {
                select.innerHTML += `<option value="${item.id}">${item.name}</option>`;
            });
        }
    } catch (e) { console.error(`Error loading ${endpoint}:`, e); }
}

async function loadLensForEdit(id) {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/lenses/${id}`);
        if (!response.ok) throw new Error('Failed');
        const l = await response.json();
        
        document.getElementById('lCode').value = l.lens_code;
        document.getElementById('lCode').readOnly = true; 
        document.getElementById('lName').value = l.name;
        document.getElementById('lBrand').value = l.brand_id || '';
        document.getElementById('lCategory').value = l.category_id || '';
        document.getElementById('lType').value = l.lens_type || '';
        document.getElementById('lMaterial').value = l.material || '';
        document.getElementById('lIndex').value = l.index || '';
        document.getElementById('lCoating').value = l.coating || '';
        document.getElementById('lPowerRange').value = l.power_range || '';
        document.getElementById('lPurchasePrice').value = l.purchase_price;
        document.getElementById('lSellingPrice').value = l.selling_price;
        document.getElementById('lMinStock').value = l.min_stock;
        document.getElementById('lSupplier').value = l.supplier_id || '';
        document.getElementById('lLocation').value = l.location || '';
        document.getElementById('lStatus').value = l.status || 'Available';
        document.getElementById('lNotes').value = l.notes || '';
        
        if (document.getElementById('lImageUrl')) {
            document.getElementById('lImageUrl').value = l.image || '';
            updateImagePreview(l.image);
        }
        
    } catch (e) {
        alert('Failed to load lens data');
        window.location.href = 'lenses.html';
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const urlParams = new URLSearchParams(window.location.search);
    const lensId = urlParams.get('id');
    const method = lensId ? 'PUT' : 'POST';
    const url = lensId ? `${API_BASE_URL}/inventory/lenses/${lensId}` : `${API_BASE_URL}/inventory/lenses`;
    
    const data = {
        lens_code: document.getElementById('lCode').value.trim(),
        name: document.getElementById('lName').value.trim(),
        brand_id: document.getElementById('lBrand').value || null,
        category_id: document.getElementById('lCategory').value || null,
        lens_type: document.getElementById('lType').value,
        material: document.getElementById('lMaterial').value,
        index: document.getElementById('lIndex').value,
        coating: document.getElementById('lCoating').value.trim(),
        power_range: document.getElementById('lPowerRange').value.trim(),
        purchase_price: parseFloat(document.getElementById('lPurchasePrice').value) || 0,
        price: parseFloat(document.getElementById('lSellingPrice').value) || 0,
        selling_price: parseFloat(document.getElementById('lSellingPrice').value) || 0,
        min_stock: parseInt(document.getElementById('lMinStock').value) || 10,
        supplier_id: document.getElementById('lSupplier').value || null,
        location: document.getElementById('lLocation').value.trim(),
        status: document.getElementById('lStatus').value,
        image: document.getElementById('lImageUrl') ? document.getElementById('lImageUrl').value.trim() : null,
        notes: document.getElementById('lNotes').value.trim()
    };
    
    if (!lensId) {
        data.stock = parseInt(document.getElementById('lStock').value) || 0;
    }
    
    if (data.selling_price < data.purchase_price) {
        if (!confirm('Selling price is lower than purchase price. Proceed?')) return;
    }
    
    try {
        const response = await fetchWithAuth(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            window.location.href = 'lenses.html';
        } else {
            const err = await response.json();
            alert(err.message || 'Error saving lens');
        }
    } catch (e) {
        alert('Network Error');
    }
}
