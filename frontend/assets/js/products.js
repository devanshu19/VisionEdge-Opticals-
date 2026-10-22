let allProducts = [];
window.activeCategory = 'All';

window.getFallbackSVG = function(name, id) {
    const colors = ['#2563eb', '#06b6d4', '#8b5cf6', '#10b981', '#f59e0b', '#dc2626', '#0f172a'];
    const color = colors[(id || 1) % colors.length];
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
        <rect width="600" height="400" fill="#f8fafc"/>
        <ellipse cx="300" cy="305" rx="180" ry="18" fill="#0f172a" opacity="0.06"/>
        <g transform="translate(300, 185)">
            <rect x="-145" y="-30" width="92" height="65" rx="14" fill="${color}" fill-opacity="0.15" stroke="${color}" stroke-width="6"/>
            <rect x="53" y="-30" width="92" height="65" rx="14" fill="${color}" fill-opacity="0.15" stroke="${color}" stroke-width="6"/>
            <path d="M -55,-10 C -25,-25 25,-25 55,-10" stroke="${color}" stroke-width="8" stroke-linecap="round" fill="none"/>
            <path d="M -145,-15 C -170,-20 -200,-5 -220,10" stroke="${color}" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M 145,-15 C 170,-20 200,-5 220,10" stroke="${color}" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M -135,-15 L -100,25" stroke="#ffffff" stroke-width="4" opacity="0.6" stroke-linecap="round"/>
            <path d="M 65,-15 L 100,25" stroke="#ffffff" stroke-width="4" opacity="0.6" stroke-linecap="round"/>
        </g>
        <text x="300" y="340" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">${name || 'VisionEdge Optical Specs'}</text>
    </svg>`;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
};

window.getDistinctProductImage = function(p) {
    if (p.image && p.image.trim() && !p.image.includes('placeholder') && !p.image.includes('via.placeholder')) {
        return p.image;
    }
    return window.getFallbackSVG(p.name, p.id);
};

window.matchesCategory = function(p, catName) {
    if (!catName || catName.toLowerCase() === 'all') return true;
    const target = catName.toLowerCase().trim();
    const pCat = (p.category || '').toLowerCase().trim();
    const pType = (p.item_type || '').toLowerCase().trim();
    const pName = (p.name || '').toLowerCase().trim();
    const pBrand = (p.brand || '').toLowerCase().trim();

    const isKids = pCat === 'kids glasses' || pCat.includes('kid') || 
                   pName.includes('kids') || pName.includes('junior') || pName.includes('flexikids') ||
                   pBrand.includes('junior') || pBrand.includes('kids');

    if (target === 'kids glasses') {
        return isKids;
    }

    // Kids products MUST NOT be included under Eyeglasses, Sunglasses, or Computer Glasses
    if (isKids) {
        return false;
    }

    if (target === 'eyeglasses') {
        if (pCat) return pCat === 'eyeglasses';
        return pName.includes('eyeglasses') || pName.includes('specs') || pName.includes('frame');
    }
    if (target === 'sunglasses') {
        if (pCat) return pCat === 'sunglasses';
        return pName.includes('sunglasses') || pName.includes('shades');
    }
    if (target === 'computer glasses') {
        if (pCat) return pCat === 'computer glasses';
        return pName.includes('computer') || pName.includes('blue') || pName.includes('screen') || pName.includes('gamer');
    }
    if (target.includes('lenses') || target.includes('contact')) {
        if (pCat) return pCat.includes('lenses') || pCat.includes('contact') || pType === 'lens';
        return pType === 'lens' || ((pName.includes('contact') || pName.includes('acuvue') || pName.includes('freshlook')) && !pName.includes('sunglasses'));
    }
    return false;
};

window.filterByCategory = function(categoryName, btnEl) {
    window.activeCategory = categoryName || 'All';

    // Highlight active category tab
    const catTabBtns = document.querySelectorAll('.cat-tab-btn');
    catTabBtns.forEach(btn => {
        btn.classList.remove('btn-primary', 'active');
        btn.classList.add('btn-outline-secondary');
    });

    if (btnEl) {
        btnEl.classList.remove('btn-outline-secondary');
        btnEl.classList.add('btn-primary', 'active');
    } else {
        catTabBtns.forEach(btn => {
            const cat = btn.getAttribute('data-cat') || '';
            if (cat.toLowerCase() === window.activeCategory.toLowerCase()) {
                btn.classList.remove('btn-outline-secondary');
                btn.classList.add('btn-primary', 'active');
            }
        });
    }

    // Sync sidebar checkboxes
    const catCheckboxes = document.querySelectorAll('.cat-checkbox');
    catCheckboxes.forEach(cb => {
        if (window.activeCategory === 'All') {
            cb.checked = true;
        } else {
            cb.checked = window.matchesCategory({ category: cb.value, name: cb.value, item_type: '' }, window.activeCategory);
        }
    });

    window.filterAndRenderProducts();
};

window.filterAndRenderProducts = function() {
    const productsContainer = document.getElementById('productsContainer');
    const countText = document.getElementById('productCount');
    const priceRange = document.getElementById('priceRange');
    const sortSelect = document.getElementById('sortSelect');
    const shapeButtons = document.querySelectorAll('.shape-btn');
    const catCheckboxes = document.querySelectorAll('.cat-checkbox');

    if (!productsContainer) return;
    let currentFiltered = [...allProducts];

    // 1. Price Filter
    if (priceRange) {
        const maxPrice = parseInt(priceRange.value);
        if (maxPrice < 5000) {
            currentFiltered = currentFiltered.filter(p => {
                const price = p.selling_price || p.price || 0;
                return price <= maxPrice;
            });
        }
    }

    // 2. Category Filter
    const selectedCatValues = Array.from(catCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

    if (window.activeCategory !== 'All') {
        currentFiltered = currentFiltered.filter(p => window.matchesCategory(p, window.activeCategory));
    } else if (selectedCatValues.length > 0 && selectedCatValues.length < catCheckboxes.length) {
        currentFiltered = currentFiltered.filter(p => {
            return selectedCatValues.some(catVal => window.matchesCategory(p, catVal));
        });
    }

    // 3. Frame Shape Tags
    const activeShapes = Array.from(shapeButtons)
        .filter(btn => btn.classList.contains('btn-primary'))
        .map(btn => btn.textContent.trim().toLowerCase());

    if (activeShapes.length > 0) {
        currentFiltered = currentFiltered.filter(p => {
            const name = (p.name || '').toLowerCase();
            const shape = (p.shape || '').toLowerCase();
            return activeShapes.some(s => name.includes(s) || shape.includes(s));
        });
    }

    // 4. URL Search Query Filter
    const urlParams = new URLSearchParams(window.location.search);
    const search = urlParams.get('search');
    if (search) {
        const q = search.toLowerCase();
        currentFiltered = currentFiltered.filter(p => 
            (p.name || '').toLowerCase().includes(q) || 
            (p.frame_code && p.frame_code.toLowerCase().includes(q)) ||
            (p.lens_code && p.lens_code.toLowerCase().includes(q)) ||
            (p.category && p.category.toLowerCase().includes(q))
        );
    }

    // 5. Sorting
    const sortVal = sortSelect ? sortSelect.value : 'recommended';
    if (sortVal === 'low-high') {
        currentFiltered.sort((a, b) => (a.selling_price || a.price || 0) - (b.selling_price || b.price || 0));
    } else if (sortVal === 'high-low') {
        currentFiltered.sort((a, b) => (b.selling_price || b.price || 0) - (a.selling_price || a.price || 0));
    } else if (sortVal === 'newest') {
        currentFiltered.sort((a, b) => (b.id || 0) - (a.id || 0));
    }

    const limit = productsContainer.dataset.limit;
    if (limit && parseInt(limit) > 0) {
        currentFiltered = currentFiltered.slice(0, parseInt(limit));
    }

    if (countText) {
        countText.textContent = `Showing ${currentFiltered.length} products${search ? ` for "${search}"` : ''}`;
    }

    window.renderProducts(currentFiltered, productsContainer);
};

window.renderProducts = function(products, container) {
    if (products.length === 0) {
        container.innerHTML = '<div class="col-12 text-center py-5"><i class="bi bi-search display-3 text-muted mb-3 d-block"></i><p class="text-muted fs-5">No products found matching your filters.</p></div>';
        return;
    }
    
    let html = '';
    products.forEach((p, index) => {
        const delay = (index % 3) * 100;
        const type = p.item_type || 'Frame';
        const category = p.category || (type === 'Lens' ? 'Contact & Optical Lenses' : 'Eyeglasses');
        const code = p.frame_code || p.lens_code || '';
        const price = p.selling_price || p.price || 0;
        const name = p.name || `${type} #${p.id}`;
        const imgUrl = window.getDistinctProductImage(p);
        const fallbackSvg = window.getFallbackSVG(name, p.id);
        
        const isOutOfStock = (p.stock !== undefined && p.stock !== null && parseInt(p.stock) <= 0 && p.status !== 'Available') ||
                             (p.status && (p.status.toLowerCase() === 'out of stock' || p.status.toLowerCase() === 'inactive'));

        html += `
            <div class="col-md-6 col-xl-4" data-aos="fade-up" data-aos-delay="${delay}">
                <div class="card product-card h-100 border-0 shadow-sm position-relative overflow-hidden">
                    <span class="position-absolute top-0 start-0 bg-primary text-white px-2 py-1 m-2 rounded-pill small fw-semibold shadow-sm" style="z-index: 5; font-size: 0.75rem;">
                        ${category}
                    </span>
                    ${isOutOfStock ? `<span class="position-absolute top-0 end-0 bg-danger text-white px-2 py-1 m-2 rounded small fw-bold shadow-sm" style="z-index: 5;"><i class="bi bi-x-circle me-1"></i>Out of Stock</span>` : ''}
                    <button class="wishlist-btn" onclick="this.querySelector('i').classList.toggle('bi-heart-fill'); this.querySelector('i').classList.toggle('text-danger');" style="z-index: 4;"><i class="bi bi-heart"></i></button>
                    
                    <div class="overflow-hidden rounded-top position-relative" style="background: var(--bg-light, #f8fafc);">
                        <img src="${imgUrl}" class="card-img-top ${isOutOfStock ? 'opacity-50' : ''}" alt="${name}" style="height: 220px; object-fit: cover; width: 100%; transition: transform 0.4s ease;" onerror="this.onerror=null; this.src='${fallbackSvg}';">
                    </div>
                    
                    <div class="card-body d-flex flex-column p-3">
                        <div class="d-flex align-items-center justify-content-between mb-1">
                            <div class="text-warning small">
                                <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-half"></i>
                            </div>
                            <span class="text-muted extra-small">${p.brand || 'VisionEdge'}</span>
                        </div>
                        
                        <h5 class="card-title fw-bold fs-6 mb-1 text-truncate" title="${name}">${name}</h5>
                        <p class="text-muted small mb-3">${code ? code + ' • ' : ''}${p.shape || p.material || p.type || 'Authentic'}</p>
                        
                        <div class="mt-auto d-flex justify-content-between align-items-center pt-2 border-top">
                            <div>
                                <span class="fs-5 fw-bold text-primary">₹${price}</span>
                                ${p.price && p.price > price ? `<span class="text-muted text-decoration-line-through small ms-1">₹${p.price}</span>` : ''}
                            </div>
                                <div class="d-flex gap-2">
                                    ${(() => {
                                        let vtoCutout = p.vto_image;
                                        if (!vtoCutout) {
                                            const s = (p.shape || '').toLowerCase();
                                            if (s.includes('aviator')) vtoCutout = 'assets/images/frames/aviator_vto.png';
                                            else if (s.includes('round') || s.includes('oval')) vtoCutout = 'assets/images/frames/round_vto.png';
                                            else if (s.includes('rectangle') || s.includes('square')) vtoCutout = 'assets/images/frames/rectangle_vto.png';
                                            else if (s.includes('cat')) vtoCutout = 'assets/images/frames/cateye_vto.png';
                                            else if (s.includes('rimless')) vtoCutout = 'assets/images/frames/rimless_vto.png';
                                            else vtoCutout = 'assets/images/frames/wayfarer_vto.png';
                                        }
                                        return isOutOfStock ? `
                                            <span class="badge bg-secondary bg-opacity-75 text-white px-3 py-2 rounded-pill"><i class="bi bi-slash-circle me-1"></i>Out of Stock</span>
                                        ` : `
                                            ${type === 'Frame' ? `
                                            <button class="btn btn-sm btn-outline-info rounded-pill px-3 fw-bold btn-vto shadow-sm" 
                                                data-item-id="${p.id}"
                                                data-item-name="${name}"
                                                data-item-image="${vtoCutout}">
                                                <i class="bi bi-magic me-1"></i>Try On
                                            </button>
                                            ` : ''}
                                        `;
                                    })()}
                                        <button class="btn btn-sm btn-primary rounded-pill px-3 fw-bold shadow-sm"
                                            onclick="window.handleBuyNow(this, event)"
                                            data-item-id="${p.id}"
                                            data-item-type="${type}"
                                            data-item-name="${name}"
                                            data-item-price="${price}"
                                            data-item-image="${imgUrl}">
                                            Buy Now
                                        </button>
                                        <button class="btn btn-outline-primary btn-sm rounded-circle p-2 lh-1 shadow-sm add-to-cart-btn" 
                                            title="Add to Cart"
                                            onclick="window.handleAddToCart(this, event)"
                                            data-item-id="${p.id}"
                                            data-item-type="${type}"
                                            data-item-name="${name}"
                                            data-item-price="${price}"
                                            data-item-image="${imgUrl}">
                                            <i class="bi bi-cart-plus" style="pointer-events: none;"></i>
                                        </button>
                                    `}
                                </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
};

document.addEventListener("DOMContentLoaded", async () => {
    const productsContainer = document.getElementById('productsContainer');
    const priceRange = document.getElementById('priceRange');
    const priceDisplay = document.getElementById('priceDisplay');
    const applyFiltersBtn = document.getElementById('applyFiltersBtn');
    const sortSelect = document.getElementById('sortSelect');
    const shapeButtons = document.querySelectorAll('.shape-btn');
    const catCheckboxes = document.querySelectorAll('.cat-checkbox');

    if (priceRange && priceDisplay) {
        priceRange.addEventListener('input', (e) => {
            const val = parseInt(e.target.value);
            priceDisplay.textContent = val >= 5000 ? '₹5,000+' : `₹${val}`;
        });
    }

    // Checkbox Events
    catCheckboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            const checkedBoxes = Array.from(catCheckboxes).filter(c => c.checked);
            const catTabBtns = document.querySelectorAll('.cat-tab-btn');
            catTabBtns.forEach(b => {
                b.classList.remove('btn-primary', 'active');
                b.classList.add('btn-outline-secondary');
            });

            if (checkedBoxes.length === catCheckboxes.length || checkedBoxes.length === 0) {
                window.activeCategory = 'All';
                const allBtn = document.querySelector('.cat-tab-btn[data-cat="All"]');
                if (allBtn) {
                    allBtn.classList.remove('btn-outline-secondary');
                    allBtn.classList.add('btn-primary', 'active');
                }
            } else if (checkedBoxes.length === 1) {
                window.activeCategory = checkedBoxes[0].value;
                const matchBtn = document.querySelector(`.cat-tab-btn[data-cat="${window.activeCategory}"]`);
                if (matchBtn) {
                    matchBtn.classList.remove('btn-outline-secondary');
                    matchBtn.classList.add('btn-primary', 'active');
                }
            } else {
                window.activeCategory = 'All';
            }

            window.filterAndRenderProducts();
        });
    });

    // Frame Shape Buttons
    shapeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('btn-primary');
            btn.classList.toggle('btn-outline-secondary');
            window.filterAndRenderProducts();
        });
    });

    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', window.filterAndRenderProducts);
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', window.filterAndRenderProducts);
    }

    if (!productsContainer) return;
    productsContainer.innerHTML = '<div class="col-12 text-center py-5"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Loading products...</p></div>';

    try {
        const apiUrl = window.API_BASE_URL || 'http://127.0.0.1:5000/api';
        const [framesRes, lensesRes] = await Promise.all([
            fetch(apiUrl + '/inventory/frames'),
            fetch(apiUrl + '/inventory/lenses')
        ]);
        
        let frames = [];
        let lenses = [];
        
        if (framesRes.ok) frames = await framesRes.json();
        if (lensesRes.ok) lenses = await lensesRes.json();
        
        frames = frames.map(f => ({ ...f, item_type: 'Frame' }));
        lenses = lenses.map(l => ({ ...l, item_type: 'Lens', category: 'Contact & Optical Lenses' }));
        
        allProducts = [...frames, ...lenses];

        // Update Dynamic Category Counts
        const countFor = (cat) => allProducts.filter(p => window.matchesCategory(p, cat)).length;
        const cEye = countFor('Eyeglasses');
        const cSun = countFor('Sunglasses');
        const cCmp = countFor('Computer Glasses');
        const cKid = countFor('Kids Glasses');
        const cLns = countFor('Contact & Optical Lenses');
        const cAll = allProducts.length;

        const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setTxt('tabCountAll', cAll);
        setTxt('tabCountEye', cEye);
        setTxt('tabCountSun', cSun);
        setTxt('tabCountCmp', cCmp);
        setTxt('tabCountKid', cKid);
        setTxt('tabCountLns', cLns);

        setTxt('sideCountEye', cEye);
        setTxt('sideCountSun', cSun);
        setTxt('sideCountCmp', cCmp);
        setTxt('sideCountKid', cKid);
        setTxt('sideCountLns', cLns);

        const urlParams = new URLSearchParams(window.location.search);
        const search = urlParams.get('search');
        if (search) {
            const header = document.querySelector('.page-header h2');
            if (header) header.textContent = `Products matching "${search}"`;
            
            const searchLower = search.toLowerCase();
            if (searchLower.includes('sun')) window.activeCategory = 'Sunglasses';
            else if (searchLower.includes('eye')) window.activeCategory = 'Eyeglasses';
            else if (searchLower.includes('computer')) window.activeCategory = 'Computer Glasses';
            else if (searchLower.includes('kids')) window.activeCategory = 'Kids Glasses';
            else if (searchLower.includes('lens') || searchLower.includes('contact')) window.activeCategory = 'Contact & Optical Lenses';
        }

        window.filterByCategory(window.activeCategory);
        
    } catch (error) {
        console.error("Error fetching products:", error);
        productsContainer.innerHTML = '<div class="col-12 text-center py-5 text-danger"><i class="bi bi-exclamation-triangle fs-1"></i><p>Failed to load products. Please try again later.</p></div>';
    }
});
