document.addEventListener('DOMContentLoaded', async () => {
    await loadUnbilledOrders();
    
    document.getElementById('orderSelect').addEventListener('change', async (e) => {
        const orderId = e.target.value;
        if (orderId) {
            await previewOrder(orderId);
            document.getElementById('billPreviewContainer').style.display = 'block';
        } else {
            document.getElementById('billPreviewContainer').style.display = 'none';
        }
    });
    
    document.getElementById('btnGenerateBill').addEventListener('click', generateBill);
});

async function loadUnbilledOrders() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/`);
        if (response.ok) {
            const orders = await response.json();
            const select = document.getElementById('orderSelect');
            select.innerHTML = '<option value="">Select an order...</option>';
            
            // Only show orders that are NOT cancelled and NOT completed
            const validOrders = orders.filter(o => o.status !== 'Cancelled' && o.status !== 'Completed');
            
            if (validOrders.length === 0) {
                select.innerHTML = '<option value="">No unbilled orders found</option>';
            }
            
            validOrders.forEach(o => {
                const total = (o.total_amount || 0).toFixed(2);
                const code = o.order_number || o.order_id || `ORD-#${o.id}`;
                select.innerHTML += `<option value="${o.id}">${code} - ${o.customer_name || 'Customer'} (Total: ₹${total})</option>`;
            });
        }
    } catch (e) {
        console.error("Error loading orders", e);
    }
}

async function previewOrder(id) {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/${id}`);
        if (!response.ok) throw new Error('Failed to load order details');
        
        const order = await response.json();
        
        document.getElementById('previewOrderNumber').textContent = order.order_number || order.order_id || `#${order.id}`;
        document.getElementById('custName').textContent = order.customer_name || 'Customer';
        
        const custPhone = (order.customer_details && order.customer_details.phone) || order.customer_phone || 'N/A';
        const custAddr = (order.customer_details && order.customer_details.address) || order.customer_address || 'N/A';
        
        document.getElementById('custPhone').textContent = custPhone;
        document.getElementById('custAddress').textContent = custAddr;
        
        const tbody = document.getElementById('billItemsBody');
        tbody.innerHTML = '';
        
        const items = order.items || [];
        items.forEach(item => {
            const pCode = item.product_code || item.item_code || `ITEM-#${item.id}`;
            const pName = item.product_name || item.item_name || 'Optical Item';
            const iType = item.item_type || item.product_type || 'Frame';
            const qty = item.quantity || 1;
            const uPrice = (item.unit_price || item.price || 0).toFixed(2);
            const disc = (item.discount || 0).toFixed(2);
            const tPrice = (item.total_price || (qty * uPrice)).toFixed(2);

            tbody.innerHTML += `
                <tr>
                    <td>
                        <div class="fw-bold">${pCode}</div>
                        <small class="text-muted">${pName}</small>
                    </td>
                    <td><span class="badge bg-secondary">${iType}</span></td>
                    <td class="text-center">${qty}</td>
                    <td class="text-end">₹${uPrice}</td>
                    <td class="text-end">₹${disc}</td>
                    <td class="text-end pe-4 fw-bold">₹${tPrice}</td>
                </tr>
            `;
        });
        
        const subtotal = order.subtotal || order.total_amount || 0;
        const discount = order.discount || 0;
        const gst = order.gst || 0;
        const total = order.total_amount || 0;

        document.getElementById('billSubtotal').textContent = `₹${subtotal.toFixed(2)}`;
        document.getElementById('billDiscount').textContent = `- ₹${discount.toFixed(2)}`;
        document.getElementById('billGst').textContent = `₹${gst.toFixed(2)}`;
        document.getElementById('billTotal').textContent = `₹${total.toFixed(2)}`;
        
    } catch (e) {
        alert("Could not preview order.");
        console.error(e);
    }
}

async function generateBill() {
    const orderId = document.getElementById('orderSelect').value;
    const paymentMethod = document.getElementById('paymentMethod').value;
    const paymentStatus = document.getElementById('paymentStatus').value;
    
    if (!orderId) return alert("Please select an order first.");
    
    const btn = document.getElementById('btnGenerateBill');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
    
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                order_id: orderId,
                payment_method: paymentMethod,
                payment_status: paymentStatus
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (window.showToast) window.showToast('Success', 'Invoice generated successfully!');
            window.location.href = `billing-history.html?highlight=${data.billing.id}`;
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to generate invoice');
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-file-earmark-pdf me-2"></i>Generate Invoice PDF';
        }
    } catch (e) {
        alert("Network Error");
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-file-earmark-pdf me-2"></i>Generate Invoice PDF';
    }
}
