// inventory.js - Live Inventory Management for VisionEdge Admin

let liveInventory = [];

document.addEventListener("DOMContentLoaded", async () => {
    await loadInventoryData();

    // Setup Search
    const searchInput = document.getElementById('searchInventory');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
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

async function loadInventoryData() {
    try {
        const token = localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        // 1. Fetch Inventory Stats
        try {
            const statsRes = await fetch('http://localhost:5000/api/inventory/stats', { headers });
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

        // 2. Fetch Frames & Lenses in Parallel
        const [framesRes, lensesRes] = await Promise.all([
            fetch('http://localhost:5000/api/inventory/frames', { credentials: 'omit' }),
            fetch('http://localhost:5000/api/inventory/lenses', { credentials: 'omit' })
        ]);

        const frames = framesRes.ok ? await framesRes.json() : [];
        const lenses = lensesRes.ok ? await lensesRes.json() : [];

        // 3. Normalize into unified inventory list
        liveInventory = [];

        frames.forEach(f => {
            liveInventory.push({
                id: f.id,
                code: f.frame_code || `FR-${String(f.id).padStart(3, '0')}`,
                name: f.name || f.model || 'Optical Frame',
                category: 'Frames',
                brand: f.brand || f.brand_name || 'Generic',
                stock: f.stock ?? 0,
                min_stock: f.min_stock ?? 5,
                price: f.price || f.selling_price || 0,
                priceFormatted: `₹${(f.price || f.selling_price || 0).toLocaleString('en-IN')}`,
                image: f.image || f.vto_image || '',
                raw: f
            });
        });

        lenses.forEach(l => {
            liveInventory.push({
                id: l.id,
                code: l.lens_code || `LN-${String(l.id).padStart(3, '0')}`,
                name: l.name || `${l.brand || ''} ${l.type || 'Lens'}`.trim(),
                category: 'Lenses',
                brand: l.brand || 'Generic',
                stock: l.stock ?? 0,
                min_stock: l.min_stock ?? 10,
                price: l.price || l.selling_price || 0,
                priceFormatted: `₹${(l.price || l.selling_price || 0).toLocaleString('en-IN')}`,
                image: l.image || '',
                raw: l
            });
        });

        filterAndRender();

        const productsGrid = document.getElementById('productsGrid');
        if (productsGrid) {
            populateProductsGrid(liveInventory);
        }

    } catch (error) {
        console.error('Error fetching live inventory:', error);
        const tbody = document.getElementById('inventoryTableBody');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger py-4"><i class="bi bi-exclamation-triangle me-2"></i>Failed to load inventory data from server.</td></tr>`;
        }
    }
}

function filterAndRender() {
    const searchInput = document.getElementById('searchInventory');
    const filterCategory = document.getElementById('filterCategory');

    const term = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const cat = filterCategory ? filterCategory.value : 'all';

    const filtered = liveInventory.filter(item => {
        const matchesCat = (cat === 'all' || item.category === cat);
        const matchesTerm = !term ||
            item.code.toLowerCase().includes(term) ||
            item.name.toLowerCase().includes(term) ||
            item.brand.toLowerCase().includes(term);
        return matchesCat && matchesTerm;
    });

    renderInventoryTable(filtered);
}

function renderInventoryTable(items) {
    const tbody = document.getElementById('inventoryTableBody');
    if (!tbody) return;

    if (!items || items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-5"><i class="bi bi-inbox fs-3 d-block mb-2"></i>No inventory items match the criteria.</td></tr>`;
        return;
    }

    let html = '';
    items.forEach((item, index) => {
        let stockBadge = 'success';
        if (item.stock <= (item.min_stock || 5)) stockBadge = 'warning';
        if (item.stock <= 3) stockBadge = 'danger';

        const delay = Math.min(index * 30, 300);

        let catColor = 'primary';
        if (item.category === 'Lenses') catColor = 'info';

        html += `
            <tr data-aos="fade-up" data-aos-delay="${delay}">
                <td class="fw-medium text-secondary ps-4">${item.code}</td>
                <td class="fw-bold">${item.name}</td>
                <td><span class="badge category-badge bg-${catColor} bg-opacity-10 text-${catColor} border border-${catColor}">${item.category}</span></td>
                <td class="text-muted">${item.brand}</td>
                <td>
                    <span class="badge bg-${stockBadge} px-2 py-1 rounded-pill">${item.stock} in stock</span>
                    ${item.stock <= (item.min_stock || 5) ? '<i class="bi bi-exclamation-circle-fill text-danger ms-1" title="Low Stock"></i>' : ''}
                </td>
                <td class="fw-bold text-success">${item.priceFormatted}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="viewProduct('${item.code}')" title="View Details"><i class="bi bi-eye"></i></button>
                    <a href="${item.category === 'Frames' ? 'frames.html' : 'lenses.html'}" class="btn btn-sm btn-outline-secondary" title="Manage"><i class="bi bi-pencil"></i></a>
                </td>
            </tr>
        `;
    });

    tbody.innerHTML = html;
}

function viewProduct(code) {
    const product = liveInventory.find(p => p.code === code);
    if (product) {
        const modalBody = document.getElementById('modalBodyContent');
        if (!modalBody) return;

        const icon = product.category === 'Frames' ? 'bi-eyeglasses' : 'bi-record-circle';

        modalBody.innerHTML = `
            <div class="text-center mb-4">
                <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <i class="bi ${icon} fs-1 text-primary"></i>
                </div>
                <h4 class="fw-bold">${product.name}</h4>
                <p class="text-muted mb-0">${product.brand}</p>
            </div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                    <span class="text-muted">Item Code</span>
                    <span class="fw-medium">${product.code}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                    <span class="text-muted">Category</span>
                    <span class="badge bg-primary">${product.category}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                    <span class="text-muted">Current Stock</span>
                    <span class="fw-bold ${product.stock <= product.min_stock ? 'text-danger' : 'text-success'}">${product.stock} units</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                    <span class="text-muted">Unit Price</span>
                    <span class="fw-bold text-success">${product.priceFormatted}</span>
                </li>
            </ul>
        `;
        const modalEl = document.getElementById('productDetailsModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
            modal.show();
        }
    }
}

function populateProductsGrid(items) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;

    let html = '';
    items.forEach((item, index) => {
        const delay = Math.min(index * 30, 300);
        const icon = item.category === 'Frames' ? 'bi-eyeglasses' : 'bi-record-circle';

        html += `
            <div class="col-12 col-sm-6 col-lg-4 col-xl-3" data-aos="fade-up" data-aos-delay="${delay}">
                <div class="card product-card h-100">
                    <div class="product-img-wrapper position-relative text-center p-3">
                        <i class="bi ${icon} text-primary" style="font-size: 4rem; opacity: 0.3"></i>
                        <span class="badge bg-primary position-absolute top-0 end-0 m-3">${item.category}</span>
                    </div>
                    <div class="card-body">
                        <h6 class="fw-bold text-truncate" title="${item.name}">${item.name}</h6>
                        <small class="text-muted d-block mb-3">${item.brand}</small>
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <h5 class="fw-bold text-success mb-0">${item.priceFormatted}</h5>
                            <button class="btn btn-sm btn-outline-primary" onclick="viewProduct('${item.code}')"><i class="bi bi-eye"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    grid.innerHTML = html;
}
