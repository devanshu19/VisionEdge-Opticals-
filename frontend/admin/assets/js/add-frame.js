document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([
        loadDropdown('brands', 'fBrand'),
        loadDropdown('categories?type=Frame', 'fCategory'),
        loadDropdown('suppliers', 'fSupplier')
    ]);
    
    // Image listeners
    const fileInput = document.getElementById('fImageFile');
    const urlInput = document.getElementById('fImageUrl');
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
    const frameId = urlParams.get('id');
    
    if (frameId) {
        document.getElementById('pageTitle').textContent = 'Edit Frame';
        document.getElementById('breadcrumbActive').textContent = 'Edit Frame';
        document.getElementById('stockGroup').style.display = 'none'; // Stock updated via ledger
        await loadFrameForEdit(frameId);
    }
    
    document.getElementById('frameForm').addEventListener('submit', handleFormSubmit);
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

async function loadFrameForEdit(id) {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/inventory/frames/${id}`);
        if (!response.ok) throw new Error('Failed');
        const f = await response.json();
        
        document.getElementById('fCode').value = f.frame_code;
        document.getElementById('fCode').readOnly = true; // Don't change code
        document.getElementById('fName').value = f.name;
        document.getElementById('fBrand').value = f.brand_id || '';
        document.getElementById('fCategory').value = f.category_id || '';
        document.getElementById('fGender').value = f.gender || 'Unisex';
        document.getElementById('fShape').value = f.shape || '';
        document.getElementById('fMaterial').value = f.material || '';
        document.getElementById('fSize').value = f.size || 'Medium';
        document.getElementById('fColor').value = f.color || '';
        document.getElementById('fPurchasePrice').value = f.purchase_price;
        document.getElementById('fSellingPrice').value = f.selling_price;
        document.getElementById('fMinStock').value = f.min_stock;
        document.getElementById('fSupplier').value = f.supplier_id || '';
        document.getElementById('fLocation').value = f.location || '';
        document.getElementById('fStatus').value = f.status || 'Available';
        document.getElementById('fNotes').value = f.notes || '';
        
        if (document.getElementById('fImageUrl')) {
            document.getElementById('fImageUrl').value = f.image || '';
            updateImagePreview(f.image);
        }
        if (document.getElementById('fVtoImageUrl')) {
            document.getElementById('fVtoImageUrl').value = f.vto_image || '';
        }
        
    } catch (e) {
        alert('Failed to load frame data');
        window.location.href = 'frames.html';
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const urlParams = new URLSearchParams(window.location.search);
    const frameId = urlParams.get('id');
    const method = frameId ? 'PUT' : 'POST';
    const url = frameId ? `${API_BASE_URL}/inventory/frames/${frameId}` : `${API_BASE_URL}/inventory/frames`;
    
    const data = {
        frame_code: document.getElementById('fCode').value.trim(),
        name: document.getElementById('fName').value.trim(),
        brand_id: document.getElementById('fBrand').value || null,
        category_id: document.getElementById('fCategory').value || null,
        gender: document.getElementById('fGender').value,
        shape: document.getElementById('fShape').value,
        material: document.getElementById('fMaterial').value,
        size: document.getElementById('fSize').value,
        color: document.getElementById('fColor').value.trim(),
        purchase_price: parseFloat(document.getElementById('fPurchasePrice').value) || 0,
        price: parseFloat(document.getElementById('fSellingPrice').value) || 0,
        selling_price: parseFloat(document.getElementById('fSellingPrice').value) || 0,
        min_stock: parseInt(document.getElementById('fMinStock').value) || 5,
        supplier_id: document.getElementById('fSupplier').value || null,
        location: document.getElementById('fLocation').value.trim(),
        status: document.getElementById('fStatus').value,
        image: document.getElementById('fImageUrl') ? document.getElementById('fImageUrl').value.trim() : null,
        vto_image: document.getElementById('fVtoImageUrl') ? document.getElementById('fVtoImageUrl').value.trim() : null,
        notes: document.getElementById('fNotes').value.trim()
    };
    
    if (!frameId) {
        data.stock = parseInt(document.getElementById('fStock').value) || 0;
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
            window.location.href = 'frames.html';
        } else {
            const err = await response.json();
            alert(err.message || 'Error saving frame');
        }
    } catch (e) {
        alert('Network Error');
    }
}
