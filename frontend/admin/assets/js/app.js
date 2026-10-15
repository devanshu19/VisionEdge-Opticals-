// Initialize App
document.addEventListener("DOMContentLoaded", () => {
    if (typeof checkAuth === 'function') {
        checkAuth();
        
        // Enforce page-level access
        const path = window.location.pathname.split('/').pop() || 'index.html';
        const pageRoles = {
            'dashboard.html': ['admin'],
            'inventory.html': ['admin'],
            'settings.html': ['admin'],
            'reports.html': ['admin']
        };
        
        if (pageRoles[path]) {
            enforceRoleAccess(pageRoles[path]);
        }
    }

    // Show loader initially and hide it after a short delay
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.style.display = 'none', 500);
        }
    }, 500);

    // Initialize Theme immediately to prevent flicker
    initTheme();
    loadCustomColors();

    // Load Components (Sidebar, Navbar, Footer)
    loadComponents();
});

async function loadComponents() {
    const components = [
        { id: 'sidebar-container', url: 'components/sidebar.html' },
        { id: 'navbar-container', url: 'components/navbar.html' },
        { id: 'footer-container', url: 'components/footer.html' }
    ];

    for (const comp of components) {
        const container = document.getElementById(comp.id);
        if (container) {
            try {
                // Determine base URL path correctly if nested and append cache-buster
                let urlPrefix = window.location.pathname.includes('/pages/') ? '../' : '';
                const response = await fetch(urlPrefix + comp.url + '?v=' + Date.now());
                if (response.ok) {
                    const html = await response.text();
                    container.innerHTML = html;
                } else {
                    console.error(`Failed to load ${comp.url}`);
                }
            } catch (error) {
                console.error(`Error loading ${comp.url}:`, error);
            }
        }
    }

    // Attach event listeners after components are loaded
    attachComponentListeners();

    // Filter sidebar by role
    if (typeof getUserRole === 'function') {
        const role = getUserRole();
        const sidebarItems = document.querySelectorAll('#sidebarMenu .nav-item');
        sidebarItems.forEach(item => {
            const roles = item.getAttribute('data-roles');
            if (roles && !roles.split(',').includes(role)) {
                item.style.display = 'none';
            }
        });
    }
}

// Notification System Polling
document.addEventListener('DOMContentLoaded', () => {
    // Poll every 30 seconds
    if (localStorage.getItem('token')) {
        fetchNotifications();
        setInterval(fetchNotifications, 30000);
    }
});

async function fetchNotifications() {
    try {
        const countRes = await fetchWithAuth(`${API_BASE_URL}/notifications/count`);
        if (countRes.ok) {
            const countData = await countRes.json();
            const badge = document.getElementById('notificationCountBadge');
            if (badge) {
                if (countData.unread > 0) {
                    badge.innerText = countData.unread;
                    badge.classList.remove('d-none');
                } else {
                    badge.classList.add('d-none');
                }
            }
        }
        
        // Fetch latest 5 for dropdown
        const res = await fetchWithAuth(`${API_BASE_URL}/notifications/`);
        if (res.ok) {
            const list = await res.json();
            const container = document.getElementById('notificationDropdownList');
            if (container) {
                container.innerHTML = '';
                if (list.length === 0) {
                    container.innerHTML = '<li><span class="dropdown-item text-muted text-center py-3">No notifications</span></li>';
                    return;
                }
                
                list.slice(0, 5).forEach(notif => {
                    const iconMap = {
                        'LOW_STOCK': { icon: 'bi-box-seam', color: 'bg-danger' },
                        'NEW_ORDER': { icon: 'bi-cart-check', color: 'bg-primary' },
                        'ORDER_READY': { icon: 'bi-check-circle', color: 'bg-success' },
                        'ORDER_COMPLETED': { icon: 'bi-bag-check', color: 'bg-success' },
                        'PAYMENT_PENDING': { icon: 'bi-cash-coin', color: 'bg-warning' },
                        'APPOINTMENT_REMINDER': { icon: 'bi-calendar-event', color: 'bg-info' },
                        'SYSTEM_ALERT': { icon: 'bi-exclamation-triangle', color: 'bg-secondary' }
                    };
                    const styling = iconMap[notif.notification_type] || iconMap['SYSTEM_ALERT'];
                    const opacity = notif.status === 'Unread' ? 'opacity-100' : 'opacity-50';
                    
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <a class="dropdown-item d-flex align-items-center py-2 ${opacity}" href="#" onclick="markNotifRead(${notif.id}, event)">
                            <div class="${styling.color} text-white rounded-circle p-2 me-3 d-flex align-items-center justify-content-center" style="width: 35px; height: 35px;">
                                <i class="bi ${styling.icon}"></i>
                            </div>
                            <div style="max-width: 210px;">
                                <h6 class="mb-0 fs-6 text-truncate">${notif.title}</h6>
                                <small class="text-muted d-block text-wrap" style="line-height:1.2;">${notif.message}</small>
                            </div>
                        </a>
                    `;
                    container.appendChild(li);
                });
            }
        }
    } catch (e) {
        console.error("Failed to poll notifications", e);
    }
}

window.markNotifRead = async function(id, e) {
    if (e) e.preventDefault();
    try {
        await fetchWithAuth(`${API_BASE_URL}/notifications/read/${id}`, { method: 'POST' });
        fetchNotifications();
        if (typeof loadAllNotifications === 'function') loadAllNotifications();
    } catch (err) {
        console.error(err);
    }
}

document.addEventListener('click', async (e) => {
    if (e.target && e.target.id === 'markAllReadBtn') {
        e.preventDefault();
        try {
            await fetchWithAuth(`${API_BASE_URL}/notifications/read-all`, { method: 'POST' });
            fetchNotifications();
            if (typeof loadAllNotifications === 'function') loadAllNotifications();
        } catch (err) {
            console.error(err);
        }
    }
});

function attachComponentListeners() {
    // Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            document.body.classList.toggle('sidebar-collapsed');
            const sidebar = document.getElementById('sidebar');
            if(sidebar) sidebar.classList.toggle('collapsed');
        });
    }

    // Sidebar overlay close for mobile
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', () => {
            document.body.classList.remove('sidebar-mobile-show');
        });
    }
    
    // Mobile toggle
    const mobileToggle = document.getElementById('mobileToggle');
    if(mobileToggle){
        mobileToggle.addEventListener('click', (e) => {
            e.preventDefault();
            document.body.classList.toggle('sidebar-mobile-show');
        });
    }

    // Theme Toggle
    const themeToggleBtn = document.getElementById('themeToggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleTheme();
        });
        
        // Update icon based on current theme
        const currentTheme = localStorage.getItem('theme') || 'light';
        updateThemeIcon(currentTheme);
    }
    
    // Highlight active menu item
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Handle index/dashboard mapping
        if (href === currentPath || (currentPath === '' && href === 'dashboard.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Initialize Bootstrap tooltips and popovers if they exist
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function loadCustomColors() {
    const savedColors = localStorage.getItem('customColors');
    if (savedColors) {
        const colors = JSON.parse(savedColors);
        if (colors.primary) document.documentElement.style.setProperty('--primary-color', colors.primary);
        if (colors.secondary) document.documentElement.style.setProperty('--secondary-color', colors.secondary);
        if (colors.accent) document.documentElement.style.setProperty('--accent-color', colors.accent);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Dispatch custom event if charts need to update
    window.dispatchEvent(new Event('themeChanged'));
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('#themeToggle i');
    if (icon) {
        if (theme === 'dark') {
            icon.className = 'bi bi-sun-fill fs-5';
        } else {
            icon.className = 'bi bi-moon-fill fs-5';
        }
    }
}

// Global Toast Notification function
window.showToast = function(title, message, type = 'success') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        // Professional bottom-center placement
        toastContainer.className = 'toast-container position-fixed bottom-0 start-50 translate-middle-x p-4';
        toastContainer.style.zIndex = '1055';
        toastContainer.style.width = 'max-content';
        toastContainer.style.maxWidth = '90vw';
        document.body.appendChild(toastContainer);
    }

    const toastEl = document.createElement('div');
    const borderColor = type === 'success' ? 'var(--success-color)' : (type === 'danger' ? 'var(--danger-color)' : (type === 'warning' ? 'var(--warning-color)' : 'var(--accent-color)'));
    
    toastEl.className = `toast align-items-center border-0 shadow-lg animate__animated animate__fadeInUp mb-3`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    // Luxury styling injection
    toastEl.style.backgroundColor = 'var(--card-bg)';
    toastEl.style.color = 'var(--text-main)';
    toastEl.style.borderBottom = `4px solid ${borderColor}`;
    toastEl.style.borderRadius = '12px';
    toastEl.style.minWidth = '320px';

    let icon = 'bi-info-circle-fill';
    let iconColor = 'text-primary';
    if(type === 'success') { icon = 'bi-check-circle-fill'; iconColor = 'text-success'; }
    else if(type === 'danger') { icon = 'bi-x-circle-fill'; iconColor = 'text-danger'; }
    else if(type === 'warning') { icon = 'bi-exclamation-triangle-fill'; iconColor = 'text-warning'; }

    toastEl.innerHTML = `
        <div class="d-flex align-items-center p-2">
            <div class="ms-3 fs-3 ${iconColor}">
                <i class="bi ${icon}"></i>
            </div>
            <div class="toast-body flex-grow-1 ms-3 py-2" style="font-size: 0.95rem;">
                <strong class="d-block fw-bold mb-1" style="font-size: 1.05rem;">${title}</strong>
                <span class="text-muted">${message}</span>
            </div>
            <button type="button" class="btn-close me-3 opacity-50" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();

    // Clean up DOM after fade out
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
};
