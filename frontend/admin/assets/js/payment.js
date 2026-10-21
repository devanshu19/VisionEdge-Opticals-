document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([
        loadPaymentStats(),
        loadPayments(),
        loadInvoiceOptions()
    ]);

    const filterStatus = document.getElementById('filterStatus');
    if (filterStatus) {
        filterStatus.addEventListener('change', () => loadPayments());
    }

    const form = document.getElementById('recordPaymentForm');
    if (form) {
        form.addEventListener('submit', handleRecordPaymentSubmit);
    }
});

async function loadPaymentStats() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/stats`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('kpiTodayReceived').textContent = `₹${(data.todays_sales || 0).toFixed(2)}`;
            document.getElementById('kpiPendingPayments').textContent = data.pending_payments || 0;
            document.getElementById('kpiMonthlyRevenue').textContent = `₹${(data.monthly_revenue || 0).toFixed(2)}`;
        }
    } catch (e) {
        console.error('Error loading payment stats:', e);
    }
}

async function loadInvoiceOptions() {
    try {
        const select = document.getElementById('payInvoiceSelect');
        if (!select) return;
        
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/`);
        if (response.ok) {
            const bills = await response.json();
            select.innerHTML = '<option value="">Select Invoice...</option>';
            
            // Show bills that are not fully paid first
            bills.forEach(b => {
                const total = (b.total_amount || 0).toFixed(2);
                const statusBadge = b.payment_status || 'Pending';
                select.innerHTML += `<option value="${b.id}">${b.invoice_number} - ${b.customer_name || 'Customer'} (Total: ₹${total} • ${statusBadge})</option>`;
            });
        }
    } catch (e) {
        console.error('Error loading invoice options:', e);
    }
}

async function loadPayments() {
    try {
        const status = document.getElementById('filterStatus')?.value || 'all';
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/payments`);
        if (!response.ok) throw new Error('Failed to fetch payments');

        let payments = await response.json();
        if (status && status !== 'all') {
            payments = payments.filter(p => p.status === status);
        }

        const tbody = document.getElementById('paymentTableBody');
        tbody.innerHTML = '';

        if (payments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted"><i class="bi bi-wallet2 fs-2 d-block mb-2"></i>No payment transactions recorded.</td></tr>';
            return;
        }

        payments.forEach(p => {
            const dateStr = p.payment_date ? p.payment_date.replace('T', ' ').split('.')[0] : '-';
            const methodIcon = getMethodIcon(p.payment_method);
            const statusClass = (p.status === 'Paid' || p.gateway_status === 'captured') ? 'success' : (p.status === 'Refunded' ? 'danger' : (p.status === 'Partial' ? 'info' : 'warning'));
            const pdfUrl = `${API_BASE_URL}/billing/${p.billing_id}/pdf`;

            const isRzp = (p.gateway === 'Razorpay' || (p.gateway_payment_id && p.gateway_payment_id.startsWith('pay_')));
            const canRefund = isRzp && (p.gateway_status === 'captured' || p.status === 'Paid') && p.refund_status !== 'full';

            const refundBadge = p.refund_status
                ? `<span class="badge bg-danger-subtle text-danger border border-danger-subtle ms-1" style="font-size:0.7rem;">Refunded ₹${(p.refunded_amount || 0).toFixed(2)}</span>`
                : '';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4">
                    <div class="fw-bold text-primary">${p.invoice_number}</div>
                    <small class="text-muted font-monospace">${p.gateway_payment_id || p.transaction_id || '-'}</small>
                </td>
                <td class="text-muted">${dateStr}</td>
                <td class="fw-medium">${p.customer_name || 'Customer'}</td>
                <td class="fw-bold text-success">
                    ₹${(p.amount || 0).toFixed(2)}
                    ${refundBadge}
                </td>
                <td>
                    <span class="badge bg-light text-dark border">${methodIcon} ${p.payment_method || 'Cash'}</span>
                    ${isRzp ? '<span class="badge bg-primary-subtle text-primary border border-primary-subtle ms-1" style="font-size:0.68rem;">Razorpay</span>' : ''}
                </td>
                <td>
                    <span class="badge bg-${statusClass} bg-opacity-10 text-${statusClass} px-3 py-1 rounded-pill border border-${statusClass}">${p.gateway_status || p.status || 'Paid'}</span>
                </td>
                <td class="text-end pe-4">
                    <a href="${pdfUrl}" target="_blank" class="btn btn-sm btn-outline-primary" title="Receipt PDF">
                        <i class="bi bi-file-earmark-text me-1"></i>PDF
                    </a>
                    ${canRefund ? `
                        <button type="button" class="btn btn-sm btn-outline-danger ms-1" onclick="openRefundModal(${p.id}, '${p.gateway_payment_id || p.transaction_id}', ${p.amount}, ${p.refunded_amount || 0})" title="Process Razorpay Refund">
                            <i class="bi bi-arrow-counterclockwise me-1"></i>Refund
                        </button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error('Error loading payments:', e);
        document.getElementById('paymentTableBody').innerHTML = '<tr><td colspan="7" class="text-center py-4 text-danger">Failed to load payments data.</td></tr>';
    }
}

// ─── Razorpay Admin Refund Handlers ──────────────────────────────────────────
let activeRefundPayment = null;

function openRefundModal(paymentId, gatewayPaymentId, amount, alreadyRefunded) {
    activeRefundPayment = {
        paymentId: paymentId,
        gatewayPaymentId: gatewayPaymentId,
        amount: parseFloat(amount || 0),
        alreadyRefunded: parseFloat(alreadyRefunded || 0)
    };

    const maxRefundable = Math.max(0, activeRefundPayment.amount - activeRefundPayment.alreadyRefunded);

    document.getElementById('refundPaymentId').value = paymentId;
    document.getElementById('refundGatewayPayId').textContent = gatewayPaymentId;
    document.getElementById('refundOriginalAmount').textContent = `₹${activeRefundPayment.amount.toFixed(2)}`;
    document.getElementById('refundMaxAmount').textContent = `₹${maxRefundable.toFixed(2)}`;

    document.getElementById('refundFull').checked = true;
    toggleRefundAmountInput();
    document.getElementById('refundReason').value = '';

    const modal = new bootstrap.Modal(document.getElementById('refundModal'));
    modal.show();
}

function toggleRefundAmountInput() {
    const isPartial = document.getElementById('refundPartial').checked;
    const group = document.getElementById('partialAmountGroup');
    const input = document.getElementById('refundCustomAmount');
    if (isPartial) {
        group.classList.remove('d-none');
        input.required = true;
        const maxRefundable = activeRefundPayment ? (activeRefundPayment.amount - activeRefundPayment.alreadyRefunded) : 0;
        input.max = maxRefundable;
        input.value = maxRefundable.toFixed(2);
    } else {
        group.classList.add('d-none');
        input.required = false;
        input.value = '';
    }
}

async function handleRefundSubmit(event) {
    event.preventDefault();
    if (!activeRefundPayment) return;

    const btn = document.getElementById('btnConfirmRefund');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Processing Refund...';

    const isPartial = document.getElementById('refundPartial').checked;
    let refundAmount = null;
    if (isPartial) {
        refundAmount = parseFloat(document.getElementById('refundCustomAmount').value);
    }
    const reason = document.getElementById('refundReason').value.trim();

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/payment/razorpay/refund`, {
            method: 'POST',
            body: JSON.stringify({
                payment_id: activeRefundPayment.gatewayPaymentId || activeRefundPayment.paymentId,
                amount: refundAmount,
                reason: reason
            })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            const modalEl = document.getElementById('refundModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            alert(`Refund Successful! Refund ID: ${data.refund_id}. Total Refunded: ₹${data.total_refunded}`);
            await loadPayments();
            await loadPaymentStats();
        } else {
            alert(data.message || 'Refund request failed. Check server logs.');
        }
    } catch (err) {
        alert(`Error executing refund: ${err.message}`);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-arrow-counterclockwise me-1"></i>Execute Razorpay Refund';
    }
}

function getMethodIcon(method) {
    if (!method) return '<i class="bi bi-cash me-1"></i>';
    const m = method.toLowerCase();
    if (m.includes('card')) return '<i class="bi bi-credit-card me-1"></i>';
    if (m.includes('upi')) return '<i class="bi bi-phone me-1"></i>';
    if (m.includes('bank')) return '<i class="bi bi-bank me-1"></i>';
    return '<i class="bi bi-cash me-1"></i>';
}

async function handleRecordPaymentSubmit(e) {
    e.preventDefault();

    const billingId = document.getElementById('payInvoiceSelect').value;
    const data = {
        amount: parseFloat(document.getElementById('payAmount').value),
        payment_method: document.getElementById('payMethod').value,
        transaction_id: document.getElementById('payTxnId').value.trim()
    };

    if (!billingId) return alert('Please select an invoice');
    if (!data.amount || data.amount <= 0) return alert('Enter a valid amount');

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/billing/${billingId}/payments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const modalEl = document.getElementById('recordPaymentModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            document.getElementById('recordPaymentForm').reset();
            if (window.showToast) window.showToast('Success', 'Payment recorded successfully');

            await Promise.all([loadPaymentStats(), loadPayments()]);
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to record payment');
        }
    } catch (err) {
        alert('Network Error');
    }
}
