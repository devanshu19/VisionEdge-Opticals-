// Initialize App
document.addEventListener("DOMContentLoaded", () => {
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
                // Determine base URL path correctly if nested
                let urlPrefix = window.location.pathname.includes('/pages/') ? '../' : '';
                const response = await fetch(urlPrefix + comp.url);
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
}

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
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${type} border-0 animate__animated animate__fadeInRight`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <strong>${title}</strong><br>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
};
