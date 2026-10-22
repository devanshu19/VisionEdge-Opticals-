// cart.js

// Initialize cart from localStorage robustly
let cart = [];
try {
    const saved = localStorage.getItem('visionEdgeCart') || localStorage.getItem('cart');
    if (saved) {
        cart = JSON.parse(saved);
    }
} catch (e) {
    console.error("Failed to parse cart:", e);
    cart = [];
}
window.cart = cart;

function initCart() {
    const checkNavbar = setInterval(() => {
        const cartBadge = document.getElementById('cartBadge');
        if (cartBadge) {
            clearInterval(checkNavbar);
            updateCartBadge();
            renderCart();
        }
    }, 100);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCart);
} else {
    initCart();
}

// Update the badge in navbar
function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (!badge) return;
    
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    badge.textContent = totalItems;
    
    if (totalItems > 0) {
        badge.style.display = 'block';
    } else {
        badge.style.display = 'none';
    }
}

// Render the cart items in the offcanvas
function renderCart() {
    const container = document.getElementById('cartItemsContainer');
    const totalValue = document.getElementById('cartTotalValue');
    
    if (!container || !totalValue) return;
    
    if (cart.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted py-5 mt-5">
                <i class="bi bi-cart-x fs-1 mb-3 d-block"></i>
                <p>Your cart is empty.</p>
                <button type="button" class="btn btn-outline-primary mt-3" data-bs-dismiss="offcanvas" onclick="window.location.href='products.html'">Continue Shopping</button>
            </div>
        `;
        totalValue.textContent = '₹0';
        return;
    }
    
    let html = '';
    let total = 0;
    
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        html += `
            <div class="card border-0 border-bottom rounded-0 mb-2 pb-2">
                <div class="card-body p-2 d-flex align-items-center">
                    <div style="width: 60px; height: 60px; background: #f8f9fa; border-radius: 8px; overflow: hidden;" class="d-flex align-items-center justify-content-center me-3 flex-shrink-0">
                        ${item.item_image ? `<img src="${item.item_image}" style="width: 100%; height: 100%; object-fit: cover;" alt="${item.name}">` : `<i class="bi bi-eyeglasses fs-3 text-secondary"></i>`}
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="mb-0 fw-bold">${item.name}</h6>
                        <div class="text-muted small">₹${item.price} x ${item.quantity}</div>
                    </div>
                    <div class="text-end">
                        <div class="fw-bold mb-2">₹${itemTotal}</div>
                        <button class="btn btn-sm btn-link text-danger p-0 border-0" onclick="removeFromCart(${index})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    totalValue.textContent = `₹${total}`;
}

// Add item to cart
function addToCart(product) {
    try {
        if (product.stock !== undefined && product.stock !== null && parseInt(product.stock) <= 0) {
            alert("Sorry, this item is out of stock!");
            return;
        }

        const existing = cart.find(item => String(item.id) === String(product.id));
        if (existing) {
            existing.quantity += 1;
        } else {
            cart.push({ ...product, quantity: 1 });
        }
        
        saveCart();
        updateCartBadge();
        renderCart();
        
        // Open offcanvas to show feedback
        let cartOffcanvasEl = document.getElementById('cartOffcanvas');
        
        // Fallback: If navbar hasn't loaded or is missing the cart offcanvas, inject it dynamically.
        if (!cartOffcanvasEl) {
            const offcanvasHtml = `
            <div class="offcanvas offcanvas-end" tabindex="-1" id="cartOffcanvas" aria-labelledby="cartOffcanvasLabel">
                <div class="offcanvas-header border-bottom">
                    <h5 class="offcanvas-title fw-bold" id="cartOffcanvasLabel">Your Cart</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body d-flex flex-column p-0">
                    <div id="cartItemsContainer" class="flex-grow-1 overflow-auto p-3">
                    </div>
                    <div class="p-4 bg-light border-top mt-auto">
                        <div class="d-flex justify-content-between mb-3 fw-bold fs-5">
                            <span>Total:</span>
                            <span id="cartTotalValue">₹0</span>
                        </div>
                        <button class="btn btn-primary w-100 fw-bold py-2 shadow-sm" onclick="proceedToCheckout()">
                            Proceed to Checkout
                        </button>
                    </div>
                </div>
            </div>`;
            document.body.insertAdjacentHTML('beforeend', offcanvasHtml);
            cartOffcanvasEl = document.getElementById('cartOffcanvas');
            // Force a re-render of the cart since the container was just created
            renderCart();
        }

        if (cartOffcanvasEl) {
            if (typeof bootstrap !== 'undefined') {
                let bsOffcanvas = bootstrap.Offcanvas.getInstance(cartOffcanvasEl);
                if (!bsOffcanvas) {
                    bsOffcanvas = new bootstrap.Offcanvas(cartOffcanvasEl);
                }
                bsOffcanvas.show();
            } else {
                alert("Item added to cart! (Bootstrap is still loading)");
            }
        }
    } catch (e) {
        alert("Error in addToCart: " + e.message);
    }
}

// Remove item from cart
window.removeFromCart = function(index) {
    cart.splice(index, 1);
    saveCart();
    updateCartBadge();
    renderCart();
    if (typeof window.renderCheckoutCart === 'function') {
        window.renderCheckoutCart();
    }
}

// Save to localStorage
function saveCart() {
    localStorage.setItem('visionEdgeCart', JSON.stringify(cart));
    localStorage.setItem('cart', JSON.stringify(cart));
    window.cart = cart;
    if (typeof window.renderCheckoutCart === 'function') {
        window.renderCheckoutCart();
    }
}

window.handleAddToCart = function(btn, event) {
    if (event) event.preventDefault();
    try {
        let product = { 
            id: btn.dataset.itemId || Date.now().toString(), 
            item_type: btn.dataset.itemType || 'Frame',
            item_id: btn.dataset.itemId,
            name: btn.dataset.itemName || 'VisionEdge Product', 
            price: parseInt(btn.dataset.itemPrice) || 999,
            selling_price: parseInt(btn.dataset.itemPrice) || 999,
            image: btn.dataset.itemImage || '',
            item_image: btn.dataset.itemImage || '',
            quantity: 1
        };
        
        addToCart(product);
    } catch (e) {
        alert("Error in handleAddToCart: " + e.message);
    }
};

// Immediate One-Click Buy Now
window.handleBuyNow = function(btn, event) {
    if (event) event.preventDefault();
    try {
        let product = { 
            id: btn.dataset.itemId || Date.now().toString(), 
            item_type: btn.dataset.itemType || 'Frame',
            item_id: btn.dataset.itemId,
            name: btn.dataset.itemName || 'VisionEdge Product', 
            price: parseInt(btn.dataset.itemPrice) || 999,
            selling_price: parseInt(btn.dataset.itemPrice) || 999,
            image: btn.dataset.itemImage || '',
            item_image: btn.dataset.itemImage || '',
            quantity: 1
        };
        
        // Find existing or push
        const existing = cart.find(i => String(i.id) === String(product.id));
        if (existing) {
            existing.quantity = (existing.quantity || 0) + 1;
        } else {
            cart.push(product);
        }
        saveCart();
        window.location.href = "checkout.html";
    } catch (e) {
        console.error("Buy now error:", e);
        window.location.href = "checkout.html";
    }
};

// Handle Search Form Submission
window.handleSearch = function(event) {
    event.preventDefault();
    const query = document.getElementById('searchInput').value;
    if (query.trim()) {
        window.location.href = `products.html?search=${encodeURIComponent(query.trim())}`;
    }
}

// Actual Proceed to Checkout
window.proceedToCheckout = function() {
    saveCart();
    if (!cart || cart.length === 0) {
        try {
            const saved = localStorage.getItem('visionEdgeCart') || localStorage.getItem('cart') || '[]';
            cart = JSON.parse(saved);
        } catch (e) { cart = []; }
    }

    if (cart.length === 0) {
        alert("Your cart is empty. Please select an eyewear from products.");
        window.location.href = "products.html";
        return;
    }
    
    const token = localStorage.getItem("access_token") || localStorage.getItem("jwtToken") || sessionStorage.getItem("jwtToken");
    const userStr = localStorage.getItem("current_user") || localStorage.getItem("user") || sessionStorage.getItem("user");
    if (!token || !userStr) {
        window.location.href = "login.html?redirect=checkout.html";
        return;
    }
    
    window.location.href = "checkout.html";
}
