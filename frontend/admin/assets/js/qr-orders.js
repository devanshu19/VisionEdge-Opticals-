document.addEventListener('DOMContentLoaded', async () => {
    await loadActiveOrders();

    const btnVerify = document.getElementById('btnVerifyQr');
    if (btnVerify) {
        btnVerify.addEventListener('click', verifyQrOrder);
    }

    const selectOrder = document.getElementById('selectQrOrder');
    if (selectOrder) {
        selectOrder.addEventListener('change', generateQrDisplay);
    }
});

async function loadActiveOrders() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/`);
        if (response.ok) {
            const orders = await response.json();
            const select = document.getElementById('selectQrOrder');
            select.innerHTML = '<option value="">Select an active order...</option>';
            orders.forEach(o => {
                const code = o.order_number || o.order_id || `#${o.id}`;
                select.innerHTML += `<option value="${o.id}">${code} - ${o.customer_name || 'Customer'} (₹${(o.total_amount || 0).toFixed(2)})</option>`;
            });
        }
    } catch (e) {
        console.error('Error loading orders for QR:', e);
    }
}

async function verifyQrOrder() {
    const input = document.getElementById('qrOrderInput').value.trim();
    if (!input) return alert('Please enter or scan an Order ID');

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/orders/`);
        if (response.ok) {
            const orders = await response.json();
            const matched = orders.find(o => 
                String(o.id) === input || 
                (o.order_number && o.order_number.toLowerCase() === input.toLowerCase()) ||
                (o.order_id && o.order_id.toLowerCase() === input.toLowerCase())
            );

            const resultCard = document.getElementById('qrResultContainer');
            if (matched) {
                document.getElementById('resOrderNum').textContent = matched.order_number || matched.order_id || `#${matched.id}`;
                document.getElementById('resStatus').textContent = matched.status || 'Pending';
                document.getElementById('resCustomer').textContent = `Customer: ${matched.customer_name || 'Customer'}`;
                document.getElementById('resAmount').textContent = `Total Amount: ₹${(matched.total_amount || 0).toFixed(2)}`;
                document.getElementById('resDate').textContent = `Date: ${matched.order_date || matched.created_at || 'Today'}`;
                document.getElementById('resOrderLink').href = `view-order.html?id=${matched.id}`;
                resultCard.classList.remove('d-none');
            } else {
                alert('Order not found with that QR code / ID');
            }
        }
    } catch (e) {
        alert('Failed to verify QR order');
    }
}

function generateQrDisplay() {
    const id = document.getElementById('selectQrOrder').value;
    const container = document.getElementById('qrGraphicContainer');
    const printBtn = document.getElementById('btnPrintQr');

    if (!id) {
        container.innerHTML = '<i class="bi bi-qr-code fs-1 text-muted"></i><span class="text-muted small mt-2">Select an order above to display QR code</span>';
        printBtn.disabled = true;
        return;
    }

    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=VISIONEDGE-ORDER-${id}`;
    container.innerHTML = `<img src="${qrUrl}" alt="Order QR Code" class="img-fluid rounded shadow-sm">`;
    printBtn.disabled = false;
}
