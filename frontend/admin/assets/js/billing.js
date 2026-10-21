// billing.js - Live Billing & Invoice Generation for VisionEdge Admin

document.addEventListener("DOMContentLoaded", async () => {
    // Set dynamic date
    const invDateEl = document.getElementById('invDate');
    if (invDateEl) {
        invDateEl.textContent = new Date().toLocaleDateString('en-IN', {
            year: 'numeric', month: 'short', day: 'numeric'
        });
    }

    const invNumEl = document.getElementById('invNumber');
    if (invNumEl) {
        invNumEl.textContent = `VE-INV-${Date.now().toString().slice(-5)}`;
    }

    const addItemBtn = document.getElementById('addItemBtn');
    const itemSelect = document.getElementById('itemSelect');
    const invoiceItems = document.getElementById('invoiceItems');
    const billCustomer = document.getElementById('billCustomer');
    
    // Total fields
    const subtotalEl = document.getElementById('invSubtotal');
    const discAmountEl = document.getElementById('invDiscAmount');
    const gstAmountEl = document.getElementById('invGstAmount');
    const totalEl = document.getElementById('invTotal');
    
    const discInput = document.getElementById('discount');
    const gstInput = document.getElementById('gst');

    let items = [];

    // 1. Load Live Customers
    await loadCustomers(billCustomer);

    // 2. Load Live Products
    await loadProducts(itemSelect);

    // Customer Selection Change Listener
    if (billCustomer) {
        billCustomer.addEventListener('change', (e) => {
            const selectedOpt = e.target.options[e.target.selectedIndex];
            const name = selectedOpt.getAttribute('data-name') || selectedOpt.text;
            const code = selectedOpt.getAttribute('data-code') || `ID #${selectedOpt.value}`;

            const nameEl = document.getElementById('invCustomerName');
            const codeEl = document.getElementById('invCustomerId');
            if (nameEl) nameEl.textContent = name;
            if (codeEl) codeEl.textContent = `Customer Code: ${code}`;
        });
    }

    // Add Item Click
    if (addItemBtn && itemSelect) {
        addItemBtn.addEventListener('click', () => {
            const val = itemSelect.value;
            if (!val || itemSelect.selectedIndex === 0) return;
            
            const opt = itemSelect.options[itemSelect.selectedIndex];
            const name = opt.getAttribute('data-name');
            const price = parseFloat(val);
            
            // Check if already in items
            const existing = items.find(i => i.name === name);
            if (existing) {
                existing.qty += 1;
            } else {
                items.push({ name, price, qty: 1 });
            }
            renderItems();
        });
    }

    if (discInput && gstInput) {
        discInput.addEventListener('input', () => renderItems());
        gstInput.addEventListener('input', () => renderItems());
    }

    function renderItems() {
        if (!invoiceItems) return;

        if (items.length === 0) {
            invoiceItems.innerHTML = '<tr><td colspan="3" class="text-center text-muted py-4">No items added yet.</td></tr>';
            updateTotals(0);
            return;
        }

        let html = '';
        let subtotal = 0;
        
        items.forEach((item, index) => {
            const itemTotal = item.price * item.qty;
            subtotal += itemTotal;
            
            html += `
                <tr>
                    <td class="fw-medium">
                        ${item.name}
                        <button class="btn btn-sm text-danger p-0 ms-2" onclick="removeItem(${index})" title="Remove"><i class="bi bi-x"></i></button>
                    </td>
                    <td class="text-center">
                        <div class="d-inline-flex align-items-center">
                            <button class="btn btn-sm btn-light border py-0 px-2 me-1" onclick="changeQty(${index}, -1)">-</button>
                            <span>${item.qty}</span>
                            <button class="btn btn-sm btn-light border py-0 px-2 ms-1" onclick="changeQty(${index}, 1)">+</button>
                        </div>
                    </td>
                    <td class="text-end">₹${itemTotal.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                </tr>
            `;
        });
        
        invoiceItems.innerHTML = html;
        updateTotals(subtotal);
    }

    window.removeItem = function(index) {
        items.splice(index, 1);
        renderItems();
    };

    window.changeQty = function(index, delta) {
        if (items[index]) {
            items[index].qty += delta;
            if (items[index].qty <= 0) {
                items.splice(index, 1);
            }
            renderItems();
        }
    };
    
    function updateTotals(subtotal) {
        const discPerc = parseFloat(discInput ? discInput.value : 0) || 0;
        const gstPerc = parseFloat(gstInput ? gstInput.value : 0) || 0;
        
        const discAmount = (subtotal * discPerc) / 100;
        const subAfterDisc = subtotal - discAmount;
        const gstAmount = (subAfterDisc * gstPerc) / 100;
        const total = subAfterDisc + gstAmount;
        
        if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        const discPercEl = document.getElementById('invDiscPerc');
        if (discPercEl) discPercEl.textContent = discPerc;
        if (discAmountEl) discAmountEl.textContent = `-₹${discAmount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        const gstPercEl = document.getElementById('invGstPerc');
        if (gstPercEl) gstPercEl.textContent = gstPerc;
        if (gstAmountEl) gstAmountEl.textContent = `+₹${gstAmount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        if (totalEl) totalEl.textContent = `₹${total.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    const genBtn = document.getElementById('generateInvoiceBtn');
    if (genBtn) {
        genBtn.addEventListener('click', () => {
            if (items.length === 0) {
                if (typeof showToast === 'function') showToast('Warning', 'Please add at least one item to invoice', 'warning');
                else alert('Please add at least one item to invoice');
                return;
            }
            if (!billCustomer || !billCustomer.value) {
                if (typeof showToast === 'function') showToast('Warning', 'Please select a customer', 'warning');
                else alert('Please select a customer');
                return;
            }
            
            genBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
            setTimeout(() => {
                if (typeof showToast === 'function') showToast('Success', 'Invoice Generated Successfully!');
                else alert('Invoice Generated Successfully!');
                genBtn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Invoice Ready';
                genBtn.classList.replace('btn-primary', 'btn-success');
            }, 800);
        });
    }
});

async function loadCustomers(selectEl) {
    if (!selectEl) return;
    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');
        const token = localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(`${apiUrl}/customers/`, { headers });
        if (res.ok) {
            const data = await res.json();
            const customers = Array.isArray(data) ? data : (data.customers || []);
            
            selectEl.innerHTML = '<option value="" selected disabled>Select Customer</option>';
            customers.forEach(c => {
                const name = `${c.first_name || ''} ${c.last_name || ''}`.trim() || c.name || `Customer #${c.id}`;
                const code = c.customer_code || `CUST-${String(c.id).padStart(3, '0')}`;
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.setAttribute('data-name', name);
                opt.setAttribute('data-code', code);
                opt.textContent = `${name} (${code})`;
                selectEl.appendChild(opt);
            });
        }
    } catch (err) {
        console.error('Failed to load live customers:', err);
        selectEl.innerHTML = '<option value="" disabled>Failed to load customers</option>';
    }
}

async function loadProducts(selectEl) {
    if (!selectEl) return;
    try {
        const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname) || window.location.hostname.startsWith('192.168.');
        const apiUrl = window.API_BASE_URL || (isLocal ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');
        const [framesRes, lensesRes] = await Promise.all([
            fetch(`${apiUrl}/inventory/frames`),
            fetch(`${apiUrl}/inventory/lenses`)
        ]);

        const frames = framesRes.ok ? await framesRes.json() : [];
        const lenses = lensesRes.ok ? await lensesRes.json() : [];

        selectEl.innerHTML = '<option value="" selected disabled>Select Product / Lens</option>';

        if (frames.length > 0) {
            const frameGroup = document.createElement('optgroup');
            frameGroup.label = 'Frames';
            frames.forEach(f => {
                const opt = document.createElement('option');
                const price = f.price || f.selling_price || 0;
                opt.value = price;
                opt.setAttribute('data-name', f.name || f.model);
                opt.textContent = `${f.name || f.model} (${f.brand}) - ₹${price.toLocaleString('en-IN')}`;
                frameGroup.appendChild(opt);
            });
            selectEl.appendChild(frameGroup);
        }

        if (lenses.length > 0) {
            const lensGroup = document.createElement('optgroup');
            lensGroup.label = 'Lenses';
            lenses.forEach(l => {
                const opt = document.createElement('option');
                const price = l.price || l.selling_price || 0;
                opt.value = price;
                opt.setAttribute('data-name', l.name || `${l.brand} ${l.type}`);
                opt.textContent = `${l.name || `${l.brand} ${l.type}`} - ₹${price.toLocaleString('en-IN')}`;
                lensGroup.appendChild(opt);
            });
            selectEl.appendChild(lensGroup);
        }

        // Add standard service items
        const serviceGroup = document.createElement('optgroup');
        serviceGroup.label = 'Services & Consultations';
        const eyeExamOpt = document.createElement('option');
        eyeExamOpt.value = 300;
        eyeExamOpt.setAttribute('data-name', 'Comprehensive Eye Examination');
        eyeExamOpt.textContent = 'Comprehensive Eye Examination - ₹300';
        serviceGroup.appendChild(eyeExamOpt);
        selectEl.appendChild(serviceGroup);

    } catch (err) {
        console.error('Failed to load live products:', err);
        selectEl.innerHTML = '<option value="" disabled>Failed to load products</option>';
    }
}
