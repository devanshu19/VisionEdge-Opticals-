// checkout.js — VisionEdge Seamless Payment Integration

let checkoutCartTotal = 0;

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

    const cardNameEl = document.getElementById('card_name');
    if (cardNameEl && !cardNameEl.value) {
        const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username || 'VisionEdge Customer';
        cardNameEl.value = fullName;
    }

    renderCheckoutCart();
    handlePaymentMethodChange();

    const btn = document.getElementById('btnPlaceOrder');
    if (btn) btn.addEventListener('click', handleUnifiedCheckout);
});

// ─── Fill Demo Test Card ─────────────────────────────────────────────────────
function fillDemoCard() {
    const numEl = document.getElementById('card_number');
    const expEl = document.getElementById('card_expiry');
    const cvvEl = document.getElementById('card_cvv');
    const nameEl = document.getElementById('card_name');

    if (numEl) numEl.value = '4532 8901 2345 6789';
    if (expEl) expEl.value = '12/28';
    if (cvvEl) cvvEl.value = '888';
    if (nameEl && !nameEl.value) {
        const u = typeof getCurrentUser === 'function' ? getCurrentUser() : null;
        nameEl.value = u ? `${u.first_name || ''} ${u.last_name || ''}`.trim() : 'VisionEdge Customer';
    }
}
window.fillDemoCard = fillDemoCard;

// ─── Handle payment method switch ────────────────────────────────────────────
function handlePaymentMethodChange() {
    const selectedPm = document.querySelector('input[name="paymentMethod"]:checked');
    const pm = selectedPm ? selectedPm.value : 'Credit Card';

    const cardDetails = document.getElementById('cardDetailsCard');
    const bankDetails = document.getElementById('bankAccountCard');
    const btn = document.getElementById('btnPlaceOrder');

    if (cardDetails) {
        cardDetails.classList.toggle('d-none', pm !== 'Credit Card');
    }
    if (bankDetails) {
        bankDetails.classList.toggle('d-none', pm !== 'UPI / Bank Transfer');
    }

    if (btn) {
        const totalStr = checkoutCartTotal > 0 ? `₹${checkoutCartTotal.toFixed(2)}` : '';
        if (pm === 'Credit Card') {
            btn.innerHTML = `<i class="bi bi-shield-check me-2"></i>Pay ${totalStr} Securely`;
        } else if (pm === 'UPI / Bank Transfer') {
            btn.innerHTML = `<i class="bi bi-qr-code me-2"></i>Confirm UPI Payment (${totalStr})`;
        } else if (pm === 'Cash on Delivery') {
            btn.innerHTML = `<i class="bi bi-box-seam me-2"></i>Place Order (Cash on Delivery) - ${totalStr}`;
        } else if (pm === 'PayU Sandbox') {
            btn.innerHTML = `<i class="bi bi-box-arrow-up-right me-2"></i>Pay via PayU Gateway (${totalStr})`;
        }
    }
}
window.handlePaymentMethodChange = handlePaymentMethodChange;

// ─── Legacy compatibility toggle ─────────────────────────────────────────────
function toggleBankDetails(show) {
    handlePaymentMethodChange();
}
window.toggleBankDetails = toggleBankDetails;

let checkoutCartSubtotal = 0;
let checkoutDiscountAmount = 0;
let activeCouponCode = null;

// ─── Render cart summary & coupon calculation ─────────────────────────────────
function renderCheckoutCart() {
    if (typeof cart === 'undefined' || !cart || cart.length === 0) {
        alert('Your cart is empty. Redirecting to products page.');
        window.location.href = 'products.html';
        return;
    }

    const container = document.getElementById('checkoutItemsList');
    let html = '';
    let subtotal = 0;

    cart.forEach(item => {
        const price    = item.price || item.unit_price || 0;
        const qty      = item.quantity || 1;
        const itemTotal = price * qty;
        subtotal += itemTotal;
        html += `
            <div class="d-flex align-items-center mb-3 pb-3 border-bottom">
                <div style="width:50px;height:50px;background:#f8f9fa;border-radius:8px;overflow:hidden;"
                     class="d-flex align-items-center justify-content-center me-3 flex-shrink-0">
                    ${item.item_image
                        ? `<img src="${item.item_image}" style="width:100%;height:100%;object-fit:cover;">`
                        : `<i class="bi bi-eyeglasses fs-4 text-secondary"></i>`}
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-0 fw-bold">${item.name || 'Product Item'}</h6>
                    <div class="text-muted small">Qty: ${qty}</div>
                </div>
                <div class="text-end fw-bold">₹${itemTotal.toFixed(2)}</div>
            </div>`;
    });

    checkoutCartSubtotal = subtotal;
    if (container) container.innerHTML = html;

    // Check if an active coupon was copied from offers.html
    const storedCoupon = localStorage.getItem('activeCoupon');
    if (storedCoupon && !activeCouponCode) {
        try {
            const cObj = JSON.parse(storedCoupon);
            if (cObj && cObj.code) {
                applyCouponCode(cObj.code, false);
                return;
            }
        } catch (e) { }
    }
    updateCheckoutTotals();
}

function applyCouponCode(manualCode) {
    const inputEl = document.getElementById('couponCodeInput');
    const feedbackEl = document.getElementById('couponFeedback');
    const code = (manualCode || (inputEl ? inputEl.value : '')).trim().toUpperCase();

    if (!code) {
        if (feedbackEl) feedbackEl.innerHTML = '<span class="text-danger small">Please enter a promo code.</span>';
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
        discount = 0;
        badgeText = 'Free Priority Shipping';
    } else {
        if (feedbackEl) feedbackEl.innerHTML = `<span class="text-danger small">Invalid code "${code}". Try VISION30 or BOGO2026.</span>`;
        return;
    }

    checkoutDiscountAmount = Math.round(discount * 100) / 100;
    activeCouponCode = code;

    localStorage.setItem('activeCoupon', JSON.stringify({
        code: code,
        discountPercent: discount > 0 ? (discount / checkoutCartSubtotal) * 100 : 0
    }));

    if (inputEl) inputEl.value = code;
    if (feedbackEl) {
        feedbackEl.innerHTML = `<span class="text-success small fw-bold"><i class="bi bi-check-circle-fill me-1"></i> Coupon "${code}" applied! <a href="javascript:void(0)" onclick="removeCouponCode()" class="text-danger small ms-1 text-decoration-none">[Remove]</a></span>`;
    }

    updateCheckoutTotals();
}
window.applyCouponCode = applyCouponCode;

function removeCouponCode() {
    activeCouponCode = null;
    checkoutDiscountAmount = 0;
    localStorage.removeItem('activeCoupon');
    const inputEl = document.getElementById('couponCodeInput');
    const feedbackEl = document.getElementById('couponFeedback');
    if (inputEl) inputEl.value = '';
    if (feedbackEl) feedbackEl.innerHTML = '<span class="text-muted small">Coupon removed.</span>';
    updateCheckoutTotals();
}
window.removeCouponCode = removeCouponCode;

function updateCheckoutTotals() {
    const fmt = v => `₹${v.toFixed(2)}`;
    const subEl = document.getElementById('co_subtotal');
    const totEl = document.getElementById('co_total');
    const discRow = document.getElementById('couponDiscountRow');
    const discAmtEl = document.getElementById('co_discount');
    const discBadgeEl = document.getElementById('appliedCouponBadge');

    if (subEl) subEl.textContent = fmt(checkoutCartSubtotal);

    if (checkoutDiscountAmount > 0 && activeCouponCode) {
        if (discRow) discRow.classList.remove('d-none');
        if (discAmtEl) discAmtEl.textContent = `-${fmt(checkoutDiscountAmount)}`;
        if (discBadgeEl) discBadgeEl.textContent = activeCouponCode;
    } else {
        if (discRow) discRow.classList.add('d-none');
    }

    checkoutCartTotal = Math.max(0, checkoutCartSubtotal - checkoutDiscountAmount);
    if (totEl) totEl.textContent = fmt(checkoutCartTotal);

    handlePaymentMethodChange();
}

// ─── Unified Checkout Handler ────────────────────────────────────────────────
async function handleUnifiedCheckout() {
    const form = document.getElementById('checkoutForm');
    if (form && !form.checkValidity()) { 
        form.reportValidity(); 
        return; 
    }

    const selectedPm = document.querySelector('input[name="paymentMethod"]:checked');
    const paymentMethod = selectedPm ? selectedPm.value : 'Credit Card';

    const btn = document.getElementById('btnPlaceOrder');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing Payment...';
    }

    // If PayU Sandbox Gateway was explicitly chosen, use PayU redirect flow
    if (paymentMethod === 'PayU Sandbox') {
        await handlePayUSandboxFlow(btn);
        return;
    }

    // If Credit Card, validate card inputs
    if (paymentMethod === 'Credit Card') {
        const cardNum = document.getElementById('card_number')?.value?.trim();
        const cardExp = document.getElementById('card_expiry')?.value?.trim();
        const cardCvv = document.getElementById('card_cvv')?.value?.trim();

        if (!cardNum || cardNum.replace(/\s/g, '').length < 12) {
            alert('Please enter a valid card number (or click "Fill Demo Card").');
            if (btn) {
                btn.disabled = false;
                handlePaymentMethodChange();
            }
            return;
        }
        if (!cardExp || !cardExp.includes('/')) {
            alert('Please enter a valid expiry date (MM/YY).');
            if (btn) {
                btn.disabled = false;
                handlePaymentMethodChange();
            }
            return;
        }
        if (!cardCvv || cardCvv.length < 3) {
            alert('Please enter a valid 3-digit CVV.');
            if (btn) {
                btn.disabled = false;
                handlePaymentMethodChange();
            }
            return;
        }
    }

    // Direct Instant Payment (Credit Card / UPI / COD)
    await handleDirectPayment(paymentMethod, btn);
}

// ─── Direct Payment Execution ────────────────────────────────────────────────
async function handleDirectPayment(paymentMethod, btn) {
    const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
    const token  = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));

    const isCod = paymentMethod === 'Cash on Delivery';

    // Show stylish payment overlay
    showProcessingOverlay(paymentMethod, checkoutCartTotal);

    const payload = {
        phone:            document.getElementById('co_phone')?.value   || '',
        shipping_address: document.getElementById('co_address')?.value || '',
        payment_method:   paymentMethod,
        discount:         checkoutDiscountAmount,
        coupon_code:      activeCouponCode || '',
        items: cart.map(item => ({
            item_type: item.item_type || 'Frame',
            item_id:   item.item_id  || item.id,
            quantity:  item.quantity || 1
        }))
    };

    try {
        const res  = await fetch(`${apiUrl}/orders/checkout`, {
            method:  'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'Authorization': `Bearer ${token}` 
            },
            body:    JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            // Clear cart from all stores
            if (typeof cart !== 'undefined') {
                cart.length = 0;
            }
            localStorage.setItem('visionEdgeCart', JSON.stringify([]));
            localStorage.setItem('cart', JSON.stringify([]));
            if (typeof updateCartBadge === 'function') updateCartBadge();

            // Brief pause for visual confirmation then redirect
            setTimeout(() => {
                const totalAmt = data.total_amount || checkoutCartTotal || '';
                const txnid = data.transaction_id || `VE-${Date.now().toString(36).toUpperCase()}`;
                const inv = data.invoice_number || '';
                const ord = data.order_id || '';
                const codParam = isCod ? '&cod=1' : '';

                window.location.href = `payment-success.html?order=${ord}&invoice=${inv}&amount=${totalAmt}&txnid=${txnid}&method=${encodeURIComponent(paymentMethod)}${codParam}`;
            }, 900);

        } else {
            removeProcessingOverlay();
            if (res.status === 401) {
                alert('Session expired. Please log in again.');
                window.location.href = 'login.html?redirect=checkout.html';
                return;
            }
            throw new Error(data.message || 'Payment failed. Please try again.');
        }
    } catch (err) {
        removeProcessingOverlay();
        console.error('Payment error:', err);
        alert(`Payment Error: ${err.message}`);
        if (btn) {
            btn.disabled = false;
            handlePaymentMethodChange();
        }
    }
}

// ─── PayU Sandbox Flow ───────────────────────────────────────────────────────
async function handlePayUSandboxFlow(btn) {
    const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
    const token  = typeof getToken === 'function'
        ? getToken()
        : (localStorage.getItem('jwtToken') || localStorage.getItem('access_token') || sessionStorage.getItem('jwtToken'));

    const payload = {
        phone:            document.getElementById('co_phone')?.value   || '',
        shipping_address: document.getElementById('co_address')?.value || '',
        discount:         checkoutDiscountAmount,
        coupon_code:      activeCouponCode || '',
        items: cart.map(item => ({
            item_type: item.item_type || 'Frame',
            item_id:   item.item_id  || item.id,
            quantity:  item.quantity || 1
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

        // Clear cart before redirecting
        if (typeof cart !== 'undefined') cart.length = 0;
        localStorage.setItem('visionEdgeCart', JSON.stringify([]));
        localStorage.setItem('cart', JSON.stringify([]));
        if (typeof updateCartBadge === 'function') updateCartBadge();

        submitPayUForm(data);

    } catch (err) {
        console.error('PayU initiation error:', err);
        alert(`PayU initiation failed: ${err.message}`);
        if (btn) {
            btn.disabled = false;
            handlePaymentMethodChange();
        }
    }
}

function submitPayUForm(params) {
    const existing = document.getElementById('__payuForm');
    if (existing) existing.remove();

    const form = document.createElement('form');
    form.id     = '__payuForm';
    form.method = 'POST';
    form.action = params.payu_url;

    const fields = [
        'key', 'txnid', 'amount', 'productinfo', 'firstname',
        'email', 'phone', 'surl', 'furl', 'hash',
        'udf1', 'udf2', 'service_provider'
    ];

    fields.forEach(name => {
        const input = document.createElement('input');
        input.type  = 'hidden';
        input.name  = name;
        input.value = params[name] || '';
        form.appendChild(input);
    });

    document.body.appendChild(form);
    showProcessingOverlay('PayU Gateway', params.total_amount);
    setTimeout(() => form.submit(), 800);
}

// ─── Processing Overlay ──────────────────────────────────────────────────────
function showProcessingOverlay(method, amount) {
    removeProcessingOverlay();
    const overlay = document.createElement('div');
    overlay.id = '__payOverlay';
    overlay.style.cssText = `
        position:fixed;inset:0;background:rgba(10,14,30,0.94);
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        z-index:99999;color:#fff;font-family:'Poppins',sans-serif;
    `;
    overlay.innerHTML = `
        <div style="text-align:center;padding:2rem;max-width:440px;">
            <div style="width:70px;height:70px;border:4px solid rgba(255,255,255,0.15);
                border-top-color:#6c63ff;border-radius:50%;animation:spin 0.9s linear infinite;margin:0 auto 1.5rem;">
            </div>
            <h3 style="font-size:1.35rem;font-weight:700;margin-bottom:.5rem;">Securing Transaction</h3>
            <p style="opacity:.8;font-size:.9rem;line-height:1.5;">Authorizing ${method} payment & generating your official invoice...</p>
            ${amount ? `<div style="margin-top:1rem;font-size:1.25rem;font-weight:700;color:#a78bfa;">Amount: ₹${parseFloat(amount).toFixed(2)}</div>` : ''}
            <div style="margin-top:1.5rem;display:inline-flex;align-items:center;gap:6px;padding:4px 12px;background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);border-radius:20px;font-size:.78rem;color:#4ade80;">
                <i class="bi bi-shield-check"></i> 256-bit Bank Grade Encryption
            </div>
        </div>
        <style>@keyframes spin{to{transform:rotate(360deg)}}</style>`;
    document.body.appendChild(overlay);
}

function removeProcessingOverlay() {
    const el = document.getElementById('__payOverlay');
    if (el) el.remove();
}
