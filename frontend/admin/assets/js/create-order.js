let orderItems = [];
let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    // Set min date to today for delivery date
    document.getElementById('deliveryDate').min = new Date().toISOString().split('T')[0];
    
    await loadCustomers();
    
    document.getElementById('customerSelect').addEventListener('change', loadPrescriptions);
    document.getElementById('extraDiscount').addEventListener('input', updateSummary);
    document.getElementById('searchItemInput').addEventListener('input', handleProductSearch);
    document.getElementById('searchItemType').addEventListener('change', handleProductSearch);
    document.getElementById('btnCreateOrder').addEventListener('click', submitOrder);
});

async function loadCustomers() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers`);
        if (response.ok) {
            const customers = await response.json();
            const select = document.getElementById('customerSelect');
            select.innerHTML = '<option value="">Select a Customer</option>';
            customers.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.name} (${c.phone})</option>`;
            });
        }
    } catch (e) {
        console.error("Error loading customers", e);
    }
}

async function loadPrescriptions() {
    const customerId = document.getElementById('customerSelect').value;
    const select = document.getElementById('prescriptionSelect');
    
    if (!customerId) {
        select.innerHTML = '<option value="">Select a customer first...</option>';
        return;
    }
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/customers/${customerId}`);
        if (response.ok) {
            const customer = await response.json();
            select.innerHTML = '<option value="">-- No Prescription Linked --</option>';
            if (customer.prescriptions && customer.prescriptions.length > 0) {
                customer.prescriptions.forEach(p => {
                    select.innerHTML += `<option value="${p.id}">${p.prescription_number} (${new Date(p.date).toLocaleDateString()})</option>`;
                });
            }
        }
    } catch (e) {
        console.error("Error loading prescriptions", e);
    }
}

function handleProductSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        const type = document.getElementById('searchItemType').value; // 'Frame' or 'Lens'
        const query = document.getElementById('searchItemInput').value.trim();
        const resultsContainer = document.getElementById('searchResults');
        
        if (!query) {
            resultsContainer.innerHTML = '<div class="text-center py-4 text-muted">Type to search products...</div>';
            return;
        }
        
        try {
            const endpoint = type === 'Frame' ? 'frames' : 'lenses';
            const response = await fetchWithAuth(`${API_BASE_URL}/inventory/${endpoint}?search=${encodeURIComponent(query)}`);
            if (response.ok) {
                const products = await response.json();
                resultsContainer.innerHTML = '';
                
                if (products.length === 0) {
                    resultsContainer.innerHTML = '<div class="text-center py-4 text-muted">No products found.</div>';
                    return;
                }
                
                products.forEach(p => {
                    const code = type === 'Frame' ? p.frame_code : p.lens_code;
                    const isOutOfStock = p.stock <= 0;
                    const badge = isOutOfStock ? `<span class="badge bg-danger float-end">Out of Stock</span>` : `<span class="badge bg-success float-end">Stock: ${p.stock}</span>`;
                    
                    const div = document.createElement('div');
                    div.className = `list-group-item product-search-result py-3 ${isOutOfStock ? 'opacity-50' : ''}`;
                    if (!isOutOfStock) {
                        div.onclick = () => addProductToOrder(p, type);
                    }
                    
                    div.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1 fw-bold">${code} - ${p.name}</h6>
                                <small class="text-muted">₹${p.selling_price} | GST: ${p.gst_percent}%</small>
                            </div>
                            <div>${badge}</div>
                        </div>
                    `;
                    resultsContainer.appendChild(div);
                });
            }
        } catch (e) {
            resultsContainer.innerHTML = '<div class="text-center py-4 text-danger">Search failed.</div>';
        }
    }, 300);
}

function addProductToOrder(product, type) {
    // Check if already exists in order
    const existing = orderItems.find(i => i.item_id === product.id && i.item_type === type);
    if (existing) {
        if (existing.quantity < product.stock) {
            existing.quantity++;
        } else {
            alert(`Cannot add more. Only ${product.stock} in stock.`);
            return;
        }
    } else {
        const code = type === 'Frame' ? product.frame_code : product.lens_code;
        orderItems.push({
            unique_id: Date.now() + Math.random(),
            item_type: type,
            item_id: product.id,
            name: product.name,
            code: code,
            stock: product.stock,
            quantity: 1,
            unit_price: product.selling_price,
            discount: 0,
            gst_percent: product.gst_percent || 0
        });
    }
    
    bootstrap.Modal.getInstance(document.getElementById('productSearchModal')).hide();
    document.getElementById('searchItemInput').value = '';
    document.getElementById('searchResults').innerHTML = '<div class="text-center py-4 text-muted">Type to search products...</div>';
    
    renderOrderItems();
}

function removeOrderItem(unique_id) {
    orderItems = orderItems.filter(i => i.unique_id !== unique_id);
    renderOrderItems();
}

function updateItemQuantity(unique_id, val) {
    const item = orderItems.find(i => i.unique_id === unique_id);
    if (item) {
        const qty = parseInt(val) || 1;
        if (qty > item.stock) {
            alert(`Cannot exceed available stock (${item.stock}).`);
            renderOrderItems(); // reset UI
            return;
        }
        item.quantity = qty;
        renderOrderItems();
    }
}

function updateItemDiscount(unique_id, val) {
    const item = orderItems.find(i => i.unique_id === unique_id);
    if (item) {
        item.discount = parseFloat(val) || 0;
        renderOrderItems();
    }
}

function renderOrderItems() {
    const tbody = document.getElementById('orderItemsBody');
    tbody.innerHTML = '';
    
    if (orderItems.length === 0) {
        tbody.innerHTML = '<tr id="emptyItemsRow"><td colspan="7" class="text-center py-4 text-muted">No items added yet. Click "Add Product" to begin.</td></tr>';
        updateSummary();
        return;
    }
    
    orderItems.forEach(item => {
        const sub = (item.unit_price * item.quantity) - item.discount;
        const gst = sub * (item.gst_percent / 100);
        const total = sub + gst;
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <div class="fw-bold">${item.code}</div>
                <small class="text-muted">${item.name}</small>
            </td>
            <td><span class="badge bg-secondary">${item.item_type}</span></td>
            <td><input type="number" class="form-control form-control-sm" value="${item.quantity}" min="1" max="${item.stock}" onchange="updateItemQuantity(${item.unique_id}, this.value)"></td>
            <td>₹${item.unit_price.toFixed(2)}</td>
            <td><input type="number" class="form-control form-control-sm" value="${item.discount}" min="0" onchange="updateItemDiscount(${item.unique_id}, this.value)"></td>
            <td class="fw-bold text-primary">₹${total.toFixed(2)}</td>
            <td class="text-end pe-4"><button class="btn btn-sm btn-outline-danger" onclick="removeOrderItem(${item.unique_id})"><i class="bi bi-x-lg"></i></button></td>
        `;
        tbody.appendChild(tr);
    });
    
    updateSummary();
}

function updateSummary() {
    let subtotal = 0;
    let itemDiscount = 0;
    let gst = 0;
    
    orderItems.forEach(item => {
        const rawSub = item.unit_price * item.quantity;
        const sub = rawSub - item.discount;
        const itemGst = sub * (item.gst_percent / 100);
        
        subtotal += rawSub;
        itemDiscount += item.discount;
        gst += itemGst;
    });
    
    const extraDiscount = parseFloat(document.getElementById('extraDiscount').value) || 0;
    const finalTotal = (subtotal - itemDiscount) + gst - extraDiscount;
    
    document.getElementById('summarySubtotal').textContent = `₹${subtotal.toFixed(2)}`;
    document.getElementById('summaryItemDiscount').textContent = `- ₹${itemDiscount.toFixed(2)}`;
    document.getElementById('summaryGst').textContent = `₹${gst.toFixed(2)}`;
    document.getElementById('summaryTotal').textContent = `₹${finalTotal.toFixed(2)}`;
}

async function submitOrder() {
    const customerId = document.getElementById('customerSelect').value;
    if (!customerId) return alert("Please select a customer.");
    if (orderItems.length === 0) return alert("Please add at least one item to the order.");
    
    const btn = document.getElementById('btnCreateOrder');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    
    const payload = {
        customer_id: customerId,
        prescription_id: document.getElementById('prescriptionSelect').value || null,
        expected_delivery_date: document.getElementById('deliveryDate').value || null,
        priority: document.getElementById('priority').value,
        notes: document.getElementById('orderNotes').value.trim(),
        discount: parseFloat(document.getElementById('extraDiscount').value) || 0,
        items: orderItems.map(i => ({
            item_type: i.item_type,
            item_id: i.item_id,
            quantity: i.quantity,
            discount: i.discount
        }))
    };
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            const data = await response.json();
            if(window.showToast) window.showToast('Success', 'Order created successfully');
            window.location.href = `view-order.html?id=${data.order_id}`;
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to create order');
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Confirm & Create Order';
        }
    } catch (e) {
        alert('Network error');
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Confirm & Create Order';
    }
}
