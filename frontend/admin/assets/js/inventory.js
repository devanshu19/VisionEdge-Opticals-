// inventory.js - Live Real-Time CRUD Inventory Management for VisionEdge Admin

let liveInventory = [];

document.addEventListener("DOMContentLoaded", async () => {
    await loadInventoryData();

    // Setup Search Input
    const searchInput = document.getElementById('searchInventory');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            filterAndRender();
        });
    }

    // Setup Category Filter
    const filterCategory = document.getElementById('filterCategory');
    if (filterCategory) {
        filterCategory.addEventListener('change', () => {
            filterAndRender();
        });
    }
});

function toggleFormFields(prefix) {
    const isFrame = document.querySelector(`input[name="itemType"]:checked`).value === 'Frame';
    const frameGroup = document.getElementById(`${prefix}FrameSpecsGroup`);
    const lensGroup = document.getElementById(`${prefix}LensSpecsGroup`);
    const vtoGroup = document.getElementById(`${prefix}VtoGroup`);
    const catSelect = document.getElementById(`${prefix}Category`);

    if (frameGroup) frameGroup.style.display = isFrame ? 'flex' : 'none';
    if (lensGroup) lensGroup.style.display = isFrame ? 'none' : 'flex';
    if (vtoGroup) vtoGroup.style.display = isFrame ? 'block' : 'none';

    if (catSelect && isFrame && catSelect.value === 'Contact & Optical Lenses') {
        catSelect.value = 'Eyeglasses';
    } else if (catSelect && !isFrame) {
        catSelect.value = 'Contact & Optical Lenses';
    }
}

function autoGenerateCode(prefix) {
    const isFrame = document.querySelector(`input[name="itemType"]:checked`) 
        ? document.querySelector(`input[name="itemType"]:checked`).value === 'Frame' 
        : true;
    const rnd = Math.floor(1000 + Math.random() * 9000);
    const code = (isFrame ? 'FRM-' : 'LNS-') + rnd;
    const input = document.getElementById(`${prefix}Code`);
    if (input) input.value = code;
}

// ==============================================================
// 1. READ: Fetch and Display Live Inventory from Supabase
// ==============================================================
async function loadInventoryData() {
    const tbody = document.getElementById('inventoryTableBody');
    if (tbody) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4 text-muted"><div class="spinner-border text-primary spinner-border-sm me-2"></div> Fetching live inventory from Supabase...</td></tr>`;
    }

    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');
        const token = typeof getToken === 'function' ? getToken() : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token'));
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        // 1. Fetch Stats
        try {
            const statsRes = await fetch(`${apiUrl}/inventory/stats`, { headers });
            if (statsRes.ok) {
                const stats = await statsRes.json();
                const totalEl = document.getElementById('totalItemsCount');
                const lowEl = document.getElementById('lowStockCount');
                const valEl = document.getElementById('valueOfStock');

                const totalItems = (stats.total_frames || 0) + (stats.total_lenses || 0);
                if (totalEl) totalEl.textContent = totalItems.toLocaleString('en-IN');
                if (lowEl) lowEl.textContent = (stats.low_stock_items || 0).toLocaleString('en-IN');
                if (valEl) valEl.textContent = `₹${(stats.total_value || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
            }
        } catch (err) {
            console.warn('Could not load inventory stats:', err);
        }

        // 2. Fetch Frames & Lenses
        let frames = [];
        let lenses = [];

        try {
            const itemsRes = await fetch(`${apiUrl}/inventory/items`, { credentials: 'omit' });
            if (itemsRes.ok) {
                const data = await itemsRes.json();
                frames = data.frames || [];
                lenses = data.lenses || [];
            } else {
                throw new Error("Items endpoint fallback");
            }
        } catch(e) {
            const [framesRes, lensesRes] = await Promise.all([
                fetch(`${apiUrl}/inventory/frames`, { credentials: 'omit' }),
                fetch(`${apiUrl}/inventory/lenses`, { credentials: 'omit' })
            ]);
            if (framesRes.ok) frames = await framesRes.json();
            if (lensesRes.ok) lenses = await lensesRes.json();
        }

        // 3. Normalize into unified live inventory list
        liveInventory = [];

        frames.forEach(f => {
            liveInventory.push({
                id: f.id,
                item_type: 'Frame',
                code: f.frame_code || `FR-${String(f.id).padStart(3, '0')}`,
                name: f.name || f.model || 'Optical Frame',
                category: f.category || 'Eyeglasses',
                brand: f.brand || f.brand_name || 'VisionEdge',
                shape: f.shape || 'Rectangle',
                material: f.material || 'Acetate',
                size: f.size || 'Medium',
                color: f.color || 'Black',
                gender: f.gender || 'Unisex',
                stock: f.stock ?? 0,
                min_stock: f.min_stock ?? 5,
                price: f.selling_price || f.price || 0,
                mrp: f.price || f.selling_price || 0,
                status: f.status || 'Available',
                image: f.image || '',
                vto_image: f.vto_image || '',
                raw: f
            });
        });

        lenses.forEach(l => {
            liveInventory.push({
                id: l.id,
                item_type: 'Lens',
                code: l.lens_code || `LN-${String(l.id).padStart(3, '0')}`,
                name: l.name || `${l.brand || ''} ${l.type || 'Lens'}`.trim(),
                category: l.category || 'Contact & Optical Lenses',
                brand: l.brand || 'VisionEdge',
                shape: '-',
                material: l.material || '-',
                size: '-',
                color: '-',
                gender: 'Unisex',
                lens_type: l.type || l.lens_type || 'Single Vision',
                coating: l.coating || 'Anti-Reflective',
                stock: l.stock ?? 0,
                min_stock: l.min_stock ?? 10,
                price: l.selling_price || l.price || 0,
                mrp: l.price || l.selling_price || 0,
                status: l.status || 'Available',
                image: l.image || '',
                raw: l
            });
        });

        // Update local KPI if stats endpoint failed
        const totalEl = document.getElementById('totalItemsCount');
        if (totalEl && totalEl.textContent === '0') {
            totalEl.textContent = liveInventory.length.toLocaleString('en-IN');
            const lowCount = liveInventory.filter(i => i.stock <= i.min_stock).length;
            const lowEl = document.getElementById('lowStockCount');
            if (lowEl) lowEl.textContent = lowCount.toString();
            const totalVal = liveInventory.reduce((acc, i) => acc + (i.stock * i.price), 0);
            const valEl = document.getElementById('valueOfStock');
            if (valEl) valEl.textContent = `₹${totalVal.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
        }

        filterAndRender();

    } catch (error) {
        console.error('Error fetching live inventory:', error);
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4"><i class="bi bi-exclamation-triangle me-2"></i>Failed to load inventory data from server.</td></tr>`;
        }
    }
}

// ==============================================================
// 2. FILTER & RENDER TABLE
// ==============================================================
function filterAndRender() {
    const searchInput = document.getElementById('searchInventory');
    const filterCategory = document.getElementById('filterCategory');

    const term = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const cat = filterCategory ? filterCategory.value : 'all';

    const filtered = liveInventory.filter(item => {
        let matchesCat = true;
        if (cat === 'Low Stock') {
            matchesCat = item.stock <= item.min_stock;
        } else if (cat !== 'all') {
            matchesCat = (item.category || '').toLowerCase().includes(cat.toLowerCase());
        }

        const matchesTerm = !term ||
            item.code.toLowerCase().includes(term) ||
            item.name.toLowerCase().includes(term) ||
            item.brand.toLowerCase().includes(term) ||
            (item.shape && item.shape.toLowerCase().includes(term));

        return matchesCat && matchesTerm;
    });

    renderInventoryTable(filtered);
}

function renderInventoryTable(items) {
    const tbody = document.getElementById('inventoryTableBody');
    if (!tbody) return;

    if (!items || items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-5"><i class="bi bi-inbox fs-2 d-block mb-2 text-secondary"></i>No inventory items match the selected filter.</td></tr>`;
        return;
    }

    let html = '';
    items.forEach((item, index) => {
        let stockBadge = 'success';
        if (item.stock <= (item.min_stock || 5)) stockBadge = 'warning';
        if (item.stock === 0) stockBadge = 'danger';

        let catBadgeColor = 'primary';
        if (item.category === 'Sunglasses') catBadgeColor = 'warning text-dark';
        else if (item.category === 'Computer Glasses') catBadgeColor = 'info text-dark';
        else if (item.category === 'Kids Glasses') catBadgeColor = 'danger';
        else if (item.category.includes('Lenses')) catBadgeColor = 'secondary';

        let imgSrc = item.image || '';
        if (imgSrc && imgSrc.startsWith('assets/')) imgSrc = '../' + imgSrc;

        const imgTag = (imgSrc && imgSrc.trim())
            ? `<img src="${imgSrc}" class="product-thumb me-2" alt="${item.name}" onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\\'product-thumb-placeholder me-2\\'><i class=\\'bi bi-eyeglasses\\'></i></div>';">`
            : `<div class="product-thumb-placeholder me-2"><i class="bi ${item.item_type === 'Frame' ? 'bi-eyeglasses' : 'bi-record-circle'}"></i></div>`;

        const specsSummary = item.item_type === 'Frame' 
            ? `${item.shape || 'Standard'} • ${item.material || 'Acetate'}`
            : `${item.lens_type || 'Single Vision'}`;

        html += `
            <tr>
                <td class="ps-4">
                    <div class="d-flex align-items-center">
                        ${imgTag}
                        <div>
                            <div class="fw-bold text-dark text-truncate" style="max-width: 220px;" title="${item.name}">${item.name}</div>
                            <small class="text-muted">${item.item_type}</small>
                        </div>
                    </div>
                </td>
                <td class="font-monospace fw-semibold text-primary">${item.code}</td>
                <td><span class="badge bg-${catBadgeColor} px-2 py-1 rounded-pill">${item.category}</span></td>
                <td class="fw-medium">${item.brand}</td>
                <td><small class="text-muted">${specsSummary}</small></td>
                <td class="fw-bold text-success">₹${item.price.toLocaleString('en-IN')}</td>
                <td>
                    <span class="badge bg-${stockBadge} badge-stock rounded-pill">
                        ${item.stock} in stock
                    </span>
                    ${item.stock <= (item.min_stock || 5) && item.stock > 0 ? '<small class="text-danger d-block fw-bold" style="font-size:0.7rem;">Low Stock!</small>' : ''}
                    ${item.stock === 0 ? '<small class="text-danger d-block fw-bold" style="font-size:0.7rem;">Out of Stock</small>' : ''}
                </td>
                <td class="text-end pe-4">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-info" onclick="viewProduct('${item.code}')" title="View Full Specifications"><i class="bi bi-eye"></i></button>
                        <button class="btn btn-outline-secondary" onclick="openAdjustStock('${item.item_type}', ${item.id}, '${escapeHtml(item.name)}')" title="Quick Adjust Stock"><i class="bi bi-box-seam"></i></button>
                        <button class="btn btn-outline-primary" onclick="openEditItem('${item.code}')" title="Edit Item Specifications"><i class="bi bi-pencil"></i></button>
                        <button class="btn btn-outline-danger" onclick="deleteProduct('${item.item_type}', ${item.id}, '${escapeHtml(item.name)}')" title="Delete from Supabase"><i class="bi bi-trash"></i></button>
                    </div>
                </td>
            </tr>
        `;
    });

    tbody.innerHTML = html;
}

// ==============================================================
// 3. CREATE: Add New Item to Supabase in Real-Time
// ==============================================================
async function submitNewItem() {
    const isFrame = document.querySelector(`input[name="itemType"]:checked`).value === 'Frame';
    const name = document.getElementById('addName').value.trim();
    const code = document.getElementById('addCode').value.trim();
    const brand = document.getElementById('addBrand').value.trim();
    const category = document.getElementById('addCategory').value;
    const price = parseFloat(document.getElementById('addPrice').value);
    const stock = parseInt(document.getElementById('addStock').value) || 0;
    const min_stock = parseInt(document.getElementById('addMinStock').value) || 5;
    const image = document.getElementById('addImage').value.trim();
    const status = document.getElementById('addStatus').value;

    if (!name || !brand || isNaN(price) || price <= 0) {
        alert("Please provide Product Name, Brand, and a valid Selling Price.");
        return;
    }

    const btn = document.getElementById('btnSaveNewItem');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Saving to Supabase...`;
    btn.disabled = true;

    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');
        
        let endpoint = isFrame ? `${apiUrl}/inventory/frames` : `${apiUrl}/inventory/lenses`;
        let payload = {};

        if (isFrame) {
            payload = {
                frame_code: code || undefined,
                name: name,
                model: name,
                brand: brand,
                category: category,
                shape: document.getElementById('addShape').value,
                material: document.getElementById('addMaterial').value,
                size: document.getElementById('addSize').value,
                color: document.getElementById('addColor').value.trim() || 'Classic',
                gender: document.getElementById('addGender').value,
                price: price,
                selling_price: price,
                stock: stock,
                min_stock: min_stock,
                image: image,
                vto_image: document.getElementById('addVtoImage').value.trim(),
                status: status
            };
        } else {
            payload = {
                lens_code: code || undefined,
                name: name,
                brand: brand,
                category: category,
                type: document.getElementById('addLensType').value.trim() || 'Single Vision',
                lens_type: document.getElementById('addLensType').value.trim() || 'Single Vision',
                coating: document.getElementById('addLensCoating').value.trim() || 'Anti-Reflective',
                price: price,
                selling_price: price,
                stock: stock,
                min_stock: min_stock,
                image: image,
                status: status
            };
        }

        const res = await (typeof fetchWithAuth === 'function' 
            ? fetchWithAuth(endpoint, { method: 'POST', body: JSON.stringify(payload) }) 
            : fetch(endpoint, { 
                method: 'POST', 
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('jwtToken')}` 
                }, 
                body: JSON.stringify(payload) 
            }));

        const result = await res.json();

        if (res.ok) {
            // Close Modal
            const modalEl = document.getElementById('addItemModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }

            document.getElementById('addInventoryForm').reset();
            alert(`✅ ${isFrame ? 'Frame' : 'Lens'} "${name}" added successfully to Supabase!`);
            
            // Reload realtime list
            await loadInventoryData();
        } else {
            alert(`Error adding item: ${result.message || 'Please check input fields.'}`);
        }
    } catch (err) {
        console.error("Save error:", err);
        alert(`Network error saving item: ${err.message}`);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// ==============================================================
// 4. UPDATE: Edit Item Specifications in Supabase in Real-Time
// ==============================================================
function openEditItem(code) {
    const item = liveInventory.find(i => i.code === code);
    if (!item) return;

    document.getElementById('editItemId').value = item.id;
    document.getElementById('editItemType').value = item.item_type;
    document.getElementById('editName').value = item.name;
    document.getElementById('editCode').value = item.code;
    document.getElementById('editBrand').value = item.brand;
    document.getElementById('editCategory').value = item.category;
    document.getElementById('editPrice').value = item.price;
    document.getElementById('editStock').value = item.stock;
    document.getElementById('editStatus').value = item.status;
    document.getElementById('editImage').value = item.image || '';

    const isFrame = item.item_type === 'Frame';
    document.getElementById('editFrameSpecsGroup').style.display = isFrame ? 'flex' : 'none';
    document.getElementById('editLensSpecsGroup').style.display = isFrame ? 'none' : 'flex';

    if (isFrame) {
        document.getElementById('editShape').value = item.shape || 'Rectangle';
        document.getElementById('editMaterial').value = item.material || 'Acetate';
        document.getElementById('editSize').value = item.size || 'Medium';
        document.getElementById('editColor').value = item.color || '';
        document.getElementById('editGender').value = item.gender || 'Unisex';
    } else {
        document.getElementById('editLensType').value = item.lens_type || '';
        document.getElementById('editLensCoating').value = item.coating || '';
    }

    const modalEl = document.getElementById('editItemModal');
    if (modalEl) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    }
}

async function submitEditItem() {
    const id = document.getElementById('editItemId').value;
    const itemType = document.getElementById('editItemType').value;
    const isFrame = itemType === 'Frame';

    const name = document.getElementById('editName').value.trim();
    const brand = document.getElementById('editBrand').value.trim();
    const category = document.getElementById('editCategory').value;
    const price = parseFloat(document.getElementById('editPrice').value);
    const stock = parseInt(document.getElementById('editStock').value) || 0;
    const status = document.getElementById('editStatus').value;
    const image = document.getElementById('editImage').value.trim();

    if (!name || !brand || isNaN(price)) {
        alert("Please ensure Name, Brand and Price are provided.");
        return;
    }

    const btn = document.getElementById('btnUpdateItem');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Updating in Supabase...`;
    btn.disabled = true;

    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');
        
        const endpoint = isFrame ? `${apiUrl}/inventory/frames/${id}` : `${apiUrl}/inventory/lenses/${id}`;
        let payload = {
            name: name,
            brand: brand,
            category: category,
            price: price,
            selling_price: price,
            stock: stock,
            status: status,
            image: image
        };

        if (isFrame) {
            payload.shape = document.getElementById('editShape').value;
            payload.material = document.getElementById('editMaterial').value.trim();
            payload.size = document.getElementById('editSize').value;
            payload.color = document.getElementById('editColor').value.trim();
            payload.gender = document.getElementById('editGender').value;
        } else {
            payload.type = document.getElementById('editLensType').value.trim();
            payload.coating = document.getElementById('editLensCoating').value.trim();
        }

        const res = await (typeof fetchWithAuth === 'function' 
            ? fetchWithAuth(endpoint, { method: 'PUT', body: JSON.stringify(payload) }) 
            : fetch(endpoint, { 
                method: 'PUT', 
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('jwtToken')}` 
                }, 
                body: JSON.stringify(payload) 
            }));

        const result = await res.json();

        if (res.ok) {
            const modalEl = document.getElementById('editItemModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }

            alert(`✅ "${name}" updated successfully in Supabase!`);
            await loadInventoryData();
        } else {
            alert(`Error updating item: ${result.message || 'Please check fields.'}`);
        }
    } catch (err) {
        console.error("Update error:", err);
        alert(`Network error updating item: ${err.message}`);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// ==============================================================
// 5. DELETE: Remove Item from Supabase in Real-Time
// ==============================================================
async function deleteProduct(itemType, id, name) {
    if (!confirm(`Are you sure you want to permanently delete "${name}" from Supabase database?`)) {
        return;
    }

    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');
        
        const endpoint = itemType === 'Frame' 
            ? `${apiUrl}/inventory/frames/${id}` 
            : `${apiUrl}/inventory/lenses/${id}`;

        const res = await (typeof fetchWithAuth === 'function' 
            ? fetchWithAuth(endpoint, { method: 'DELETE' }) 
            : fetch(endpoint, { 
                method: 'DELETE', 
                headers: { 
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('jwtToken')}` 
                } 
            }));

        if (res.ok) {
            // Remove locally and re-render instantly
            liveInventory = liveInventory.filter(i => !(i.item_type === itemType && i.id === id));
            filterAndRender();

            // Refresh stats
            const totalEl = document.getElementById('totalItemsCount');
            if (totalEl) totalEl.textContent = liveInventory.length.toLocaleString('en-IN');
            alert(`🗑️ Product "${name}" was deleted from Supabase.`);
        } else {
            const err = await res.json();
            alert(`Failed to delete: ${err.message || 'Server error'}`);
        }
    } catch (err) {
        console.error("Delete error:", err);
        alert(`Error deleting item: ${err.message}`);
    }
}

// ==============================================================
// 6. QUICK ADJUST STOCK
// ==============================================================
function openAdjustStock(itemType, id, name) {
    document.getElementById('adjustId').value = id;
    document.getElementById('adjustType').value = itemType;
    document.getElementById('adjustItemName').textContent = name;
    document.getElementById('adjustQty').value = 10;
    document.getElementById('adjustReason').value = 'Stock replenishment';

    const modalEl = document.getElementById('adjustStockModal');
    if (modalEl) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    }
}

async function submitStockAdjustment() {
    const id = parseInt(document.getElementById('adjustId').value);
    const itemType = document.getElementById('adjustType').value;
    const txType = document.getElementById('adjustTxType').value;
    const qty = parseInt(document.getElementById('adjustQty').value);
    const reason = document.getElementById('adjustReason').value.trim();

    if (!qty || qty < 1) {
        alert("Please enter a valid quantity of 1 or more.");
        return;
    }

    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');

        const res = await (typeof fetchWithAuth === 'function' 
            ? fetchWithAuth(`${apiUrl}/inventory/transactions`, {
                method: 'POST',
                body: JSON.stringify({
                    item_type: itemType,
                    item_id: id,
                    transaction_type: txType,
                    quantity: qty,
                    reason: reason || 'Inventory manual adjustment'
                })
            })
            : fetch(`${apiUrl}/inventory/transactions`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('jwtToken')}` 
                },
                body: JSON.stringify({
                    item_type: itemType,
                    item_id: id,
                    transaction_type: txType,
                    quantity: qty,
                    reason: reason || 'Inventory manual adjustment'
                })
            }));

        const data = await res.json();
        if (res.ok) {
            const modalEl = document.getElementById('adjustStockModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }

            alert(`✅ Stock adjusted successfully! New stock: ${data.new_stock}`);
            await loadInventoryData();
        } else {
            alert(`Error adjusting stock: ${data.message || 'Operation failed'}`);
        }
    } catch (err) {
        console.error("Adjustment error:", err);
        alert(`Error: ${err.message}`);
    }
}

// ==============================================================
// 7. VIEW PRODUCT DETAILS MODAL
// ==============================================================
function viewProduct(code) {
    const product = liveInventory.find(p => p.code === code);
    if (!product) return;

    const modalBody = document.getElementById('modalBodyContent');
    if (!modalBody) return;

    let imgSrc = product.image || '';
    if (imgSrc && imgSrc.startsWith('assets/')) imgSrc = '../' + imgSrc;

    const imgTag = (imgSrc && imgSrc.trim())
        ? `<img src="${imgSrc}" class="img-fluid rounded mb-3 border" style="max-height: 180px; object-fit: contain;" alt="${product.name}">`
        : `<div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;"><i class="bi ${product.item_type === 'Frame' ? 'bi-eyeglasses' : 'bi-record-circle'} fs-1 text-primary"></i></div>`;

    let extraSpecs = '';
    if (product.item_type === 'Frame') {
        extraSpecs = `
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Frame Shape</span>
                <span class="fw-semibold">${product.shape || 'Rectangle'}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Material</span>
                <span class="fw-semibold">${product.material || 'Acetate'}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Size & Gender</span>
                <span class="fw-semibold">${product.size || 'Medium'} • ${product.gender || 'Unisex'}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Color</span>
                <span class="fw-semibold">${product.color || 'Standard'}</span>
            </li>
        `;
    } else {
        extraSpecs = `
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Lens Type</span>
                <span class="fw-semibold">${product.lens_type || 'Single Vision'}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Coating</span>
                <span class="fw-semibold">${product.coating || 'Anti-Reflective'}</span>
            </li>
        `;
    }

    modalBody.innerHTML = `
        <div class="text-center mb-3">
            ${imgTag}
            <h5 class="fw-bold mb-1">${product.name}</h5>
            <p class="text-muted small mb-0">${product.brand} • <span class="badge bg-primary rounded-pill">${product.category}</span></p>
        </div>
        <ul class="list-group list-group-flush small">
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Item Code</span>
                <span class="font-monospace fw-bold text-primary">${product.code}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Selling Price</span>
                <span class="fw-bold text-success fs-6">₹${product.price.toLocaleString('en-IN')}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Current Stock</span>
                <span class="fw-bold ${product.stock <= product.min_stock ? 'text-danger' : 'text-success'}">${product.stock} units</span>
            </li>
            ${extraSpecs}
            <li class="list-group-item d-flex justify-content-between px-0">
                <span class="text-muted">Status</span>
                <span class="badge bg-light text-dark border">${product.status}</span>
            </li>
        </ul>
    `;

    const editBtn = document.getElementById('btnModalEditTarget');
    if (editBtn) {
        editBtn.onclick = () => {
            const viewModal = bootstrap.Modal.getInstance(document.getElementById('productDetailsModal'));
            if (viewModal) viewModal.hide();
            openEditItem(product.code);
        };
    }

    const modalEl = document.getElementById('productDetailsModal');
    if (modalEl) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

window.loadInventoryData = loadInventoryData;
window.submitNewItem = submitNewItem;
window.openEditItem = openEditItem;
window.submitEditItem = submitEditItem;
window.deleteProduct = deleteProduct;
window.openAdjustStock = openAdjustStock;
window.submitStockAdjustment = submitStockAdjustment;
window.viewProduct = viewProduct;
window.toggleFormFields = toggleFormFields;
window.autoGenerateCode = autoGenerateCode;
