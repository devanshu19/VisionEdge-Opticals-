document.addEventListener("DOMContentLoaded", () => {
    
    // Check which page we are on
    const inventoryTable = document.getElementById('inventoryTableBody');
    if (inventoryTable) {
        populateInventoryTable();
        
        // Setup Search
        const searchInput = document.getElementById('searchInventory');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase();
                const rows = inventoryTable.querySelectorAll('tr');
                rows.forEach(row => {
                    row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
                });
            });
        }
        
        // Setup Filter
        const filterCategory = document.getElementById('filterCategory');
        if (filterCategory) {
            filterCategory.addEventListener('change', (e) => {
                const cat = e.target.value;
                const rows = inventoryTable.querySelectorAll('tr');
                rows.forEach(row => {
                    if (cat === 'all') {
                        row.style.display = '';
                    } else {
                        const rowCat = row.querySelector('.category-badge').textContent;
                        row.style.display = rowCat.includes(cat) ? '' : 'none';
                    }
                });
            });
        }
    }

    const productsGrid = document.getElementById('productsGrid');
    if (productsGrid) {
        populateProductsGrid();
    }
});

const dummyInventory = [
    { code: 'FR-001', name: 'Ray-Ban Aviator Classic', category: 'Frames', brand: 'Ray-Ban', stock: 15, price: '$150.00' },
    { code: 'FR-002', name: 'Oakley Holbrook', category: 'Frames', brand: 'Oakley', stock: 4, price: '$120.00' },
    { code: 'LN-001', name: 'Zeiss Progressive Classic', category: 'Lenses', brand: 'Zeiss', stock: 45, price: '$200.00' },
    { code: 'CL-001', name: 'Acuvue Oasys', category: 'Contact Lens', brand: 'Johnson & Johnson', stock: 120, price: '$45.00' },
    { code: 'AC-001', name: 'Microfiber Cleaning Cloth', category: 'Accessories', brand: 'Generic', stock: 2, price: '$5.00' },
    { code: 'FR-003', name: 'Gucci GG0036S', category: 'Frames', brand: 'Gucci', stock: 8, price: '$350.00' },
    { code: 'LN-002', name: 'Essilor Crizal Prevencia', category: 'Lenses', brand: 'Essilor', stock: 32, price: '$180.00' },
];

function populateInventoryTable() {
    const tbody = document.getElementById('inventoryTableBody');
    let html = '';
    
    dummyInventory.forEach((item, index) => {
        let stockBadge = 'success';
        if (item.stock < 10) stockBadge = 'warning';
        if (item.stock <= 3) stockBadge = 'danger';
        
        const delay = index * 50;
        
        let catColor = 'primary';
        if(item.category === 'Lenses') catColor = 'info';
        if(item.category === 'Contact Lens') catColor = 'success';
        if(item.category === 'Accessories') catColor = 'secondary';
        
        html += `
            <tr data-aos="fade-up" data-aos-delay="${delay}">
                <td class="fw-medium text-secondary ps-4">${item.code}</td>
                <td class="fw-bold">${item.name}</td>
                <td><span class="badge category-badge bg-${catColor} bg-opacity-10 text-${catColor} border border-${catColor}">${item.category}</span></td>
                <td class="text-muted">${item.brand}</td>
                <td>
                    <span class="badge bg-${stockBadge} px-2 py-1 rounded-pill">${item.stock} in stock</span>
                    ${item.stock <= 5 ? '<i class="bi bi-exclamation-circle-fill text-danger ms-1" title="Low Stock"></i>' : ''}
                </td>
                <td class="fw-bold text-success">${item.price}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="viewProduct('${item.code}')"><i class="bi bi-eye"></i></button>
                    <button class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></button>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function viewProduct(code) {
    const product = dummyInventory.find(p => p.code === code);
    if(product) {
        const modalBody = document.getElementById('modalBodyContent');
        modalBody.innerHTML = `
            <div class="text-center mb-4">
                <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <i class="bi ${product.category === 'Frames' ? 'bi-eyeglasses' : 'bi-box'} fs-1 text-primary"></i>
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
                    <span class="fw-bold ${product.stock < 10 ? 'text-danger' : 'text-success'}">${product.stock} units</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                    <span class="text-muted">Unit Price</span>
                    <span class="fw-bold">${product.price}</span>
                </li>
            </ul>
        `;
        const modal = new bootstrap.Modal(document.getElementById('productDetailsModal'));
        modal.show();
    }
}

function populateProductsGrid() {
    const grid = document.getElementById('productsGrid');
    let html = '';
    
    dummyInventory.forEach((item, index) => {
        const delay = index * 50;
        
        let icon = 'bi-eyeglasses';
        if(item.category === 'Lenses') icon = 'bi-record-circle';
        if(item.category === 'Contact Lens') icon = 'bi-eye';
        if(item.category === 'Accessories') icon = 'bi-box-seam';
        
        html += `
            <div class="col-12 col-sm-6 col-lg-4 col-xl-3" data-aos="fade-up" data-aos-delay="${delay}">
                <div class="card product-card h-100">
                    <div class="product-img-wrapper position-relative">
                        <i class="bi ${icon} text-primary" style="font-size: 5rem; opacity: 0.2"></i>
                        <span class="badge bg-primary position-absolute top-0 end-0 m-3">${item.category}</span>
                    </div>
                    <div class="card-body">
                        <h6 class="fw-bold text-truncate" title="${item.name}">${item.name}</h6>
                        <small class="text-muted d-block mb-3">${item.brand}</small>
                        
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <h5 class="fw-bold text-success mb-0">${item.price}</h5>
                            <button class="btn btn-sm btn-outline-primary"><i class="bi bi-pencil"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    grid.innerHTML = html;
}
