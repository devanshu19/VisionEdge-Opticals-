// checkout.js — VisionEdge Production-Ready Payment & Razorpay Integration

let checkoutCartSubtotal = 0;
let checkoutTaxAmount = 0;
let checkoutDiscountAmount = 0;
let checkoutCartTotal = 0;
let activeCouponCode = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));
    const userStr = localStorage.getItem('user') || localStorage.getItem('current_user') || sessionStorage.getItem('user');

    if (!token || !userStr) {
        alert('Please login to proceed to checkout.');
        window.location.href = 'login.html?redirect=checkout.html';
        return;
    }

    let user = {};
    try { user = JSON.parse(userStr); } catch (e) { user = {}; }

    // Auto-fill user details
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
    setVal('co_firstName', user.first_name || (user.name ? user.name.split(' ')[0] : (user.username || '')));
    setVal('co_lastName',  user.last_name  || (user.name ? user.name.split(' ').slice(1).join(' ') : ''));
    setVal('co_email',     user.email);
    setVal('co_phone',     user.phone);
    setVal('co_address',   user.address);

    renderCheckoutCart();
    handlePaymentMethodChange();

    const btn = document.getElementById('btnPlaceOrder');
    if (btn) btn.addEventListener('click', handleUnifiedCheckout);
});

// ─── Render cart summary & coupon calculation ─────────────────────────────────
function renderCheckoutCart() {
    if (typeof cart === 'undefined' || !cart || cart.length === 0) {
        // Try reload from localStorage
        try {
            const raw = localStorage.getItem('visionEdgeCart') || localStorage.getItem('cart') || '[]';
            window.cart = JSON.parse(raw);
        } catch (e) { window.cart = []; }
    }

    if (!window.cart || window.cart.length === 0) {
        alert('Your cart is empty! Redirecting to products...');
        window.location.href = 'products.html';
        return;
    }

    const itemsContainer = document.getElementById('orderSummaryItems');
    if (!itemsContainer) return;

    itemsContainer.innerHTML = '';
    let subtotal = 0;
    let totalTax = 0;

    window.cart.forEach(item => {
        const price = parseFloat(item.price || item.selling_price || 0);
        const qty = parseInt(item.quantity || 1, 10);
        const itemSubtotal = price * qty;
        const taxRate = parseFloat(item.gst_percent || 18) / 100;
        const itemTax = itemSubtotal * taxRate;

        subtotal += itemSubtotal;
        totalTax += itemTax;

        const name = item.name || item.model_name || 'Eyewear Item';
        const type = item.item_type || item.product_type || 'Frame';
        const img = item.image || item.image_url || 'assets/images/placeholder.jpg';

        itemsContainer.innerHTML += `
            <div class="d-flex align-items-center justify-content-between mb-3 pb-2 border-bottom">
                <div class="d-flex align-items-center">
                    <img src="${img}" alt="${name}" class="rounded me-3 border" style="width: 52px; height: 52px; object-fit: cover;">
                    <div>
                        <h6 class="mb-0 fw-bold small text-truncate" style="max-width: 170px;">${name}</h6>
                        <small class="text-muted d-block">${type} × ${qty}</small>
                    </div>
                </div>
                <div class="text-end">
                    <span class="fw-bold small">₹${itemSubtotal.toLocaleString('en-IN', {minimumFractionDigits:2})}</span>
                </div>
            </div>
        `;
    });

    checkoutCartSubtotal = subtotal;
    checkoutTaxAmount = totalTax;

    // Check pre-applied coupon from cart page
    try {
        const savedCoupon = sessionStorage.getItem('appliedCoupon') || localStorage.getItem('appliedCoupon');
        if (savedCoupon) {
            const cObj = JSON.parse(savedCoupon);
            if (cObj && cObj.code) {
                applyCouponCode(cObj.code, false);
                return;
            }
        }
    } catch (e) { }

    updateCheckoutTotals();
}

function applyCouponCode(manualCode, showSuccessAlert = true) {
    const inputEl = document.getElementById('couponCodeInput');
    const feedbackEl = document.getElementById('couponFeedback');
    const code = (manualCode || (inputEl ? inputEl.value : '')).trim().toUpperCase();

    if (!code) {
        if (feedbackEl) {
            feedbackEl.className = 'text-danger small mt-1';
            feedbackEl.textContent = 'Please enter a valid coupon code.';
        }
        return;
    }

    let discount = 0;
    let badgeText = code;

    if (code === 'VISION30') {
        discount = checkoutCartSubtotal * 0.30;
        badgeText = '30% OFF';
    } else if (code === 'BOGO2026') {
        discount = checkoutCartSubtotal * 0.50;
        badgeText = 'BOGO Free';
    } else if (code === 'STUDENT15') {
        discount = checkoutCartSubtotal * 0.15;
        badgeText = '15% Student Discount';
    } else if (code === 'FREESHIP') {
        discount = Math.min(checkoutCartSubtotal, 100.0);
        badgeText = 'Flat ₹100 Discount';
    } else {
        if (feedbackEl) {
            feedbackEl.className = 'text-danger small mt-1';
            feedbackEl.textContent = 'Invalid promo code. Try VISION30, BOGO2026, or STUDENT15.';
        }
        return;
    }

    checkoutDiscountAmount = Math.round(discount * 100) / 100;
    activeCouponCode = code;

    // Save coupon
    try {
        const payload = JSON.stringify({ code: code, discount: checkoutDiscountAmount });
        sessionStorage.setItem('appliedCoupon', payload);
        localStorage.setItem('appliedCoupon', payload);
    } catch(e) {}

    const appliedContainer = document.getElementById('appliedCouponContainer');
    const tagEl = document.getElementById('appliedCouponTag');
    if (appliedContainer && tagEl) {
        tagEl.innerHTML = `<i class="bi bi-tag-fill me-1"></i>${code} (${badgeText}) - ₹${checkoutDiscountAmount.toFixed(2)}`;
        appliedContainer.classList.remove('d-none');
    }

    if (feedbackEl) {
        feedbackEl.className = 'text-success small mt-1';
        feedbackEl.textContent = `Coupon ${code} applied successfully!`;
    }

    updateCheckoutTotals();
}

function removeCouponCode() {
    checkoutDiscountAmount = 0;
    activeCouponCode = null;
    try {
        sessionStorage.removeItem('appliedCoupon');
        localStorage.removeItem('appliedCoupon');
    } catch (e) {}

    const appliedContainer = document.getElementById('appliedCouponContainer');
    if (appliedContainer) appliedContainer.classList.add('d-none');

    const feedbackEl = document.getElementById('couponFeedback');
    if (feedbackEl) {
        feedbackEl.className = 'text-muted small mt-1';
        feedbackEl.textContent = 'Coupon removed.';
    }

    const inputEl = document.getElementById('couponCodeInput');
    if (inputEl) inputEl.value = '';

    updateCheckoutTotals();
}

function updateCheckoutTotals() {
    const totalBeforeDiscount = checkoutCartSubtotal + checkoutTaxAmount;
    checkoutCartTotal = Math.max(1.0, totalBeforeDiscount - checkoutDiscountAmount);

    const subEl = document.getElementById('co_subtotal');
    if (subEl) subEl.textContent = `₹${checkoutCartSubtotal.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

    const taxEl = document.getElementById('co_tax');
    if (taxEl) taxEl.textContent = `₹${checkoutTaxAmount.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

    const discRow = document.getElementById('co_discountRow');
    const discEl = document.getElementById('co_discount');
    if (checkoutDiscountAmount > 0) {
        if (discRow) discRow.classList.remove('d-none');
        if (discEl) discEl.textContent = `-₹${checkoutDiscountAmount.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    } else {
        if (discRow) discRow.classList.add('d-none');
    }

    const totEl = document.getElementById('co_total');
    if (totEl) totEl.textContent = `₹${checkoutCartTotal.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

    handlePaymentMethodChange();
}

// ─── Payment method toggling & dynamic button ─────────────────────────────────
function handlePaymentMethodChange() {
    const selectedPm = document.querySelector('input[name="paymentMethod"]:checked');
    const pm = selectedPm ? selectedPm.value : 'Razorpay';

    const btn = document.getElementById('btnPlaceOrder');
    if (!btn) return;

    const formattedAmount = `₹${checkoutCartTotal.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

    if (pm === 'Razorpay' || pm === 'Credit Card') {
        btn.innerHTML = `<i class="bi bi-shield-lock-fill me-2"></i>Pay ${formattedAmount} Securely with Razorpay`;
        btn.className = 'btn btn-primary w-100 py-3 fw-bold shadow-sm';
    } else if (pm === 'Cash on Delivery') {
        btn.innerHTML = `<i class="bi bi-cash-stack me-2"></i>Place Cash on Delivery Order (${formattedAmount})`;
        btn.className = 'btn btn-success w-100 py-3 fw-bold shadow-sm';
    } else if (pm === 'PayU Sandbox') {
        btn.innerHTML = `<i class="bi bi-box-arrow-up-right me-2"></i>Pay ${formattedAmount} via PayU Sandbox`;
        btn.className = 'btn btn-info text-white w-100 py-3 fw-bold shadow-sm';
    } else {
        btn.innerHTML = `<i class="bi bi-lock-fill me-2"></i>Proceed to Pay ${formattedAmount}`;
        btn.className = 'btn btn-primary w-100 py-3 fw-bold shadow-sm';
    }
}

// ─── Master Unified Checkout Controller ───────────────────────────────────────
async function handleUnifiedCheckout() {
    const form = document.getElementById('checkoutForm');
    if (form && !form.checkValidity()) { 
        form.reportValidity(); 
        return; 
    }

    const selectedPm = document.querySelector('input[name="paymentMethod"]:checked');
    const paymentMethod = selectedPm ? selectedPm.value : 'Razorpay';

    const btn = document.getElementById('btnPlaceOrder');
    if (btn) {
        btn.disabled = true;
    }

    if (paymentMethod === 'Cash on Delivery') {
        await handleCodCheckout(btn);
    } else if (paymentMethod === 'PayU Sandbox') {
        await handlePayUSandboxFlow(btn);
    } else {
        // Razorpay Standard Checkout
        await handleRazorpayCheckout(btn);
    }
}

// ─── Razorpay Integration Flow ────────────────────────────────────────────────
async function handleRazorpayCheckout(btn) {
    const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
    const token  = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));

    if (btn) {
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Initiating Secure Razorpay Session...';
    }

    const payload = {
        phone:            document.getElementById('co_phone')?.value   || '',
        shipping_address: document.getElementById('co_address')?.value || '',
        coupon_code:      activeCouponCode || '',
        items: (window.cart || []).map(item => ({
            item_type: item.item_type || item.product_type || 'Frame',
            item_id:   item.item_id  || item.product_id || item.id,
            quantity:  parseInt(item.quantity || 1, 10)
        }))
    };

    let orderData = null;
    try {
        const res = await fetch(`${apiUrl}/payment/razorpay/create-order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        orderData = await res.json();

        if (!res.ok) {
            if (res.status === 401) {
                alert('Session expired. Please log in again.');
                window.location.href = 'login.html?redirect=checkout.html';
                return;
            }
            throw new Error(orderData.message || 'Failed to initiate Razorpay order');
        }
    } catch (err) {
        alert(`Payment Initiation Error: ${err.message}`);
        if (btn) {
            btn.disabled = false;
            handlePaymentMethodChange();
        }
        return;
    }

    // Ensure Razorpay SDK is loaded
    if (typeof Razorpay === 'undefined') {
        try {
            await loadScript('https://checkout.razorpay.com/v1/checkout.js');
        } catch (scriptErr) {
            alert('Could not load Razorpay checkout SDK. Please check your internet connection.');
            if (btn) {
                btn.disabled = false;
                handlePaymentMethodChange();
            }
            return;
        }
    }

    // Configure Razorpay Standard Options
    const options = {
        key: orderData.key_id,
        amount: orderData.amount, // in paise
        currency: orderData.currency || 'INR',
        name: 'VisionEdge Opticals',
        description: `Order #${orderData.order_number}`,
        order_id: orderData.razorpay_order_id,
        prefill: {
            name: orderData.customer?.name || '',
            email: orderData.customer?.email || '',
            contact: orderData.customer?.phone || ''
        },
        theme: {
            color: '#6c63ff'
        },
        handler: async function (response) {
            // response.razorpay_payment_id
            // response.razorpay_order_id
            // response.razorpay_signature
            await verifyAndCompleteRazorpayPayment(response, orderData, btn);
        },
        modal: {
            ondismiss: function () {
                // Customer closed Razorpay popup without paying
                // Do NOT clear cart! Allow retry anytime.
                if (btn) {
                    btn.disabled = false;
                    handlePaymentMethodChange();
                }
            }
        }
    };

    const rzp = new Razorpay(options);

    rzp.on('payment.failed', function (resp) {
        const errorDesc = resp.error?.description || 'Payment was declined or failed.';
        const failedPayId = resp.error?.metadata?.payment_id || '';
        window.location.href = `payment-failed.html?order=${orderData.order_id}&txnid=${failedPayId}&reason=${encodeURIComponent(errorDesc)}`;
    });

    rzp.open();
}

// ─── Verify Payment on Server ─────────────────────────────────────────────────
async function verifyAndCompleteRazorpayPayment(rzpResponse, orderData, btn) {
    const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
    const token  = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));

    showProcessingOverlay('Razorpay', orderData.total_amount);

    try {
        const verifyRes = await fetch(`${apiUrl}/payment/razorpay/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                razorpay_order_id:   rzpResponse.razorpay_order_id,
                razorpay_payment_id: rzpResponse.razorpay_payment_id,
                razorpay_signature:  rzpResponse.razorpay_signature,
                order_id:            orderData.order_id
            })
        });

        const verifyData = await verifyRes.json();

        if (verifyRes.ok && verifyData.status === 'success') {
            // Clear cart completely upon confirmed payment
            clearCustomerCart();

            // Redirect to verified payment success page
            setTimeout(() => {
                const ord = verifyData.order_id || orderData.order_id;
                const inv = verifyData.invoice_number || orderData.invoice_number || '';
                const amt = verifyData.amount || orderData.total_amount;
                const txn = verifyData.transaction_id || rzpResponse.razorpay_payment_id;

                window.location.href = `payment-success.html?order=${ord}&invoice=${inv}&amount=${amt}&txnid=${txn}&method=Razorpay`;
            }, 800);
        } else {
            removeProcessingOverlay();
            const reason = verifyData.message || 'Signature verification failed';
            window.location.href = `payment-failed.html?order=${orderData.order_id}&txnid=${rzpResponse.razorpay_payment_id}&reason=${encodeURIComponent(reason)}`;
        }
    } catch (err) {
        removeProcessingOverlay();
        alert(`Verification Network Error: ${err.message}. Please check Payment History.`);
        if (btn) {
            btn.disabled = false;
            handlePaymentMethodChange();
        }
    }
}

// ─── Cash on Delivery Execution ───────────────────────────────────────────────
async function handleCodCheckout(btn) {
    const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
    const token  = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));

    if (btn) {
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Confirming COD Order...';
    }

    showProcessingOverlay('Cash on Delivery', checkoutCartTotal);

    const payload = {
        phone:            document.getElementById('co_phone')?.value   || '',
        shipping_address: document.getElementById('co_address')?.value || '',
        payment_method:   'Cash on Delivery',
        discount:         checkoutDiscountAmount,
        coupon_code:      activeCouponCode || '',
        items: (window.cart || []).map(item => ({
            item_type: item.item_type || item.product_type || 'Frame',
            item_id:   item.item_id  || item.product_id || item.id,
            quantity:  parseInt(item.quantity || 1, 10)
        }))
    };

    try {
        const res = await fetch(`${apiUrl}/orders/checkout`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            clearCustomerCart();

            setTimeout(() => {
                const totalAmt = data.total_amount || checkoutCartTotal || '';
                const txnid = data.transaction_id || `VE-COD-${Date.now().toString(36).toUpperCase()}`;
                const inv = data.invoice_number || '';
                const ord = data.order_id || '';

                window.location.href = `payment-success.html?order=${ord}&invoice=${inv}&amount=${totalAmt}&txnid=${txnid}&method=Cash%20on%20Delivery&cod=1`;
            }, 800);
        } else {
            removeProcessingOverlay();
            if (btn) {
                btn.disabled = false;
                handlePaymentMethodChange();
            }
            alert(data.message || 'Could not place Cash on Delivery order.');
        }
    } catch (err) {
        removeProcessingOverlay();
        if (btn) {
            btn.disabled = false;
            handlePaymentMethodChange();
        }
        alert('Network error while placing order. Please try again.');
    }
}

// ─── PayU Sandbox Flow (Safe Cart Preservation) ──────────────────────────────
async function handlePayUSandboxFlow(btn) {
    const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
    const token  = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));

    if (btn) {
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Connecting to PayU...';
    }

    const payload = {
        phone:            document.getElementById('co_phone')?.value   || '',
        shipping_address: document.getElementById('co_address')?.value || '',
        discount:         checkoutDiscountAmount,
        coupon_code:      activeCouponCode || '',
        items: (window.cart || []).map(item => ({
            item_type: item.item_type || item.product_type || 'Frame',
            item_id:   item.item_id  || item.product_id || item.id,
            quantity:  parseInt(item.quantity || 1, 10)
        }))
    };

    try {
        const res = await fetch(`${apiUrl}/payment/initiate`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body:    JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            if (res.status === 401) {
                alert('Session expired. Please log in again.');
                window.location.href = 'login.html?redirect=checkout.html';
                return;
            }
            throw new Error(data.message || 'Failed to initiate PayU payment');
        }

        // NOTE: We intentionally DO NOT clear cart here so customer doesn't lose items if PayU cancels!
        submitPayUForm(data.payu_url, data.params);

    } catch (err) {
        if (btn) {
            btn.disabled = false;
            handlePaymentMethodChange();
        }
        alert(`PayU Error: ${err.message}`);
    }
}

function submitPayUForm(payuUrl, params) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = payuUrl;
    form.style.display = 'none';

    for (const [key, value] of Object.entries(params)) {
        const input = document.createElement('input');
        input.type  = 'hidden';
        input.name  = key;
        input.value = value;
        form.appendChild(input);
    }

    document.body.appendChild(form);
    form.submit();
}

// ─── Helpers: Script loader, Cart clearing, Overlays ──────────────────────────
function loadScript(src) {
    return new Promise((resolve, reject) => {
        if (document.querySelector(`script[src="${src}"]`)) return resolve();
        const s = document.createElement('script');
        s.src = src;
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
    });
}

function clearCustomerCart() {
    if (typeof cart !== 'undefined' && Array.isArray(cart)) {
        cart.length = 0;
    }
    window.cart = [];
    try {
        localStorage.setItem('visionEdgeCart', JSON.stringify([]));
        localStorage.setItem('cart', JSON.stringify([]));
        sessionStorage.removeItem('appliedCoupon');
        localStorage.removeItem('appliedCoupon');
    } catch (e) {}
    if (typeof updateCartBadge === 'function') updateCartBadge();
}

function showProcessingOverlay(method, total) {
    removeProcessingOverlay();
    const div = document.createElement('div');
    div.id = 'directPaymentOverlay';
    div.style.cssText = `
        position: fixed; inset: 0; z-index: 99999;
        background: rgba(10, 15, 30, 0.88);
        backdrop-filter: blur(8px);
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        color: #fff; font-family: inherit;
    `;
    div.innerHTML = `
        <div class="text-center p-4 rounded-4" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); max-width: 420px; width: 90%;">
            <div class="spinner-border text-primary mb-3" style="width: 3.5rem; height: 3.5rem; border-width: 0.3em;" role="status"></div>
            <h5 class="fw-bold mb-1">Processing Payment</h5>
            <p class="text-white-50 small mb-3">Connecting securely with ${method}...</p>
            <div class="p-3 rounded-3 mb-3 text-start" style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.08);">
                <div class="d-flex justify-content-between small text-white-50 mb-1">
                    <span>Amount</span>
                    <strong class="text-white">₹${parseFloat(total || 0).toLocaleString('en-IN', {minimumFractionDigits:2})}</strong>
                </div>
                <div class="d-flex justify-content-between small text-white-50">
                    <span>Security</span>
                    <span class="text-success"><i class="bi bi-shield-check me-1"></i>256-Bit SSL Encrypted</span>
                </div>
            </div>
            <small class="text-white-50" style="font-size: 0.75rem;">
                <i class="bi bi-info-circle me-1"></i>Please do not refresh or close this window.
            </small>
        </div>
    `;
    document.body.appendChild(div);
}

function removeProcessingOverlay() {
    const el = document.getElementById('directPaymentOverlay');
    if (el) el.remove();
}
