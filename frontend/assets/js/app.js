const currentHost = window.location.hostname || 'localhost';
window.API_BASE_URL = `http://${currentHost}:5000/api`;

window.fetchWithAuth = async function(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(window.API_BASE_URL + url, {
        ...options,
        headers
    });
    return response;
};

window.logout = function() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('current_user');
    window.location.href = 'index.html';
};

// We are now loading cart.js explicitly via script tags in HTML files.

document.addEventListener("DOMContentLoaded", () => {
    // 1. Hide Loader
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => loader.style.display = 'none', 500);
        }, 800);
    }

    // 2. Load Components (Navbar, Footer)
    loadComponents();

    // 3. Initialize Animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100,
            easing: 'ease-out-cubic'
        });
    }
});

async function loadComponents() {
    const components = [
        { id: 'navbar-container', url: 'components/navbar.html' },
        { id: 'footer-container', url: 'components/footer.html' }
    ];

    for (const comp of components) {
        const container = document.getElementById(comp.id);
        if (container) {
            try {
                // Determine base URL if we are ever in subdirectories, though flat structure used here
                const response = await fetch(comp.url + '?t=' + new Date().getTime());
                if (response.ok) {
                    const html = await response.text();
                    container.innerHTML = html;
                    
                    // Attach logic specific to components
                    if(comp.id === 'navbar-container') {
                        initNavbarLogic();
                    }
                }
            } catch (error) {
                console.error(`Error loading ${comp.url}:`, error);
            }
        }
    }
}

function initNavbarLogic() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    // Check if this page has a transparent hero navbar (e.g. index.html)
    const isHeroPage = document.querySelector('.hero-section') !== null;
    
    if (isHeroPage) {
        navbar.classList.add('transparent');
    } else {
        navbar.classList.add('scrolled');
        navbar.classList.remove('transparent');
    }

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            navbar.classList.remove('transparent');
        } else if (isHeroPage) {
            navbar.classList.add('transparent');
            navbar.classList.remove('scrolled');
        }
    });
    
    // Highlight active link
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Update Auth Buttons based on login state
    const authContainer = navbar.querySelector('.ms-3.d-none.d-lg-flex.gap-2');
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('current_user');
    
    if (authContainer && token && userStr) {
        const user = JSON.parse(userStr);
        authContainer.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-primary btn-sm fw-bold dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <i class="bi bi-person-circle me-1"></i> ${user.first_name || user.username}
                </button>
                <ul class="dropdown-menu dropdown-menu-end border-0 shadow-sm glass-panel mt-2">
                    <li><a class="dropdown-item py-2" href="dashboard.html">Dashboard</a></li>
                    <li><a class="dropdown-item py-2" href="profile.html">Profile</a></li>
                    <li><a class="dropdown-item py-2" href="orders.html">My Orders</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item py-2 text-danger" href="#" onclick="window.logout(event)">Logout</a></li>
                </ul>
            </div>
        `;
    }
    
    // Set correct icon on load
    if (window.updateThemeIcon) {
        window.updateThemeIcon(document.documentElement.getAttribute('data-bs-theme'));
    }
}

// Theme initialization & Toggle Logic
window.toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('visionEdgeTheme', newTheme);
    window.updateThemeIcon(newTheme);
};

window.updateThemeIcon = (theme) => {
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        if (theme === 'dark') {
            themeIcon.classList.remove('bi-moon-stars');
            themeIcon.classList.add('bi-sun');
        } else {
            themeIcon.classList.remove('bi-sun');
            themeIcon.classList.add('bi-moon-stars');
        }
    }
};
