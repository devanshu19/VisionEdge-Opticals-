document.addEventListener("DOMContentLoaded", () => {
    
    // Billing logic
    const addItemBtn = document.getElementById('addItemBtn');
    const itemSelect = document.getElementById('itemSelect');
    const invoiceItems = document.getElementById('invoiceItems');
    
    // Total fields
    const subtotalEl = document.getElementById('invSubtotal');
    const discAmountEl = document.getElementById('invDiscAmount');
    const gstAmountEl = document.getElementById('invGstAmount');
    const totalEl = document.getElementById('invTotal');
    
    const discInput = document.getElementById('discount');
    const gstInput = document.getElementById('gst');
    
    // Customer Change
    const billCustomer = document.getElementById('billCustomer');
    if (billCustomer) {
        billCustomer.addEventListener('change', (e) => {
            const name = e.target.options[e.target.selectedIndex].text;
            document.getElementById('invCustomerName').textContent = name.split(' (')[0];
        });
    }

    let items = [];

    if (addItemBtn && itemSelect) {
        addItemBtn.addEventListener('click', () => {
            const val = itemSelect.value;
            if (!val || val === 'Select Product/Lens') return;
            
            const name = itemSelect.options[itemSelect.selectedIndex].getAttribute('data-name');
            const price = parseFloat(val);
            
            items.push({ name, price, qty: 1 });
            renderItems();
        });
    }

    if (discInput && gstInput) {
        discInput.addEventListener('input', renderItems);
        gstInput.addEventListener('input', renderItems);
    }

    function renderItems() {
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
                    <td class="fw-medium">${item.name}</td>
                    <td class="text-center">${item.qty}</td>
                    <td class="text-end">$${itemTotal.toFixed(2)}</td>
                </tr>
            `;
        });
        
        invoiceItems.innerHTML = html;
        updateTotals(subtotal);
    }
    
    function updateTotals(subtotal) {
        const discPerc = parseFloat(discInput.value) || 0;
        const gstPerc = parseFloat(gstInput.value) || 0;
        
        const discAmount = (subtotal * discPerc) / 100;
        const subAfterDisc = subtotal - discAmount;
        const gstAmount = (subAfterDisc * gstPerc) / 100;
        const total = subAfterDisc + gstAmount;
        
        subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        
        document.getElementById('invDiscPerc').textContent = discPerc;
        discAmountEl.textContent = `-$${discAmount.toFixed(2)}`;
        
        document.getElementById('invGstPerc').textContent = gstPerc;
        gstAmountEl.textContent = `+$${gstAmount.toFixed(2)}`;
        
        totalEl.textContent = `$${total.toFixed(2)}`;
    }

    const genBtn = document.getElementById('generateInvoiceBtn');
    if (genBtn) {
        genBtn.addEventListener('click', () => {
            if(items.length === 0) {
                if(typeof showToast === 'function') showToast('Error', 'Please add items to invoice', 'warning');
                return;
            }
            if(!billCustomer.value) {
                if(typeof showToast === 'function') showToast('Error', 'Please select a customer', 'warning');
                return;
            }
            
            genBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
            setTimeout(() => {
                if(typeof showToast === 'function') showToast('Success', 'Invoice Generated Successfully!');
                genBtn.innerHTML = '<i class="bi bi-receipt me-2"></i>Invoice Created';
                genBtn.classList.replace('btn-primary', 'btn-success');
            }, 1000);
        });
    }
});
