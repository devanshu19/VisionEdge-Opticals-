// auth.js — Centralized Authentication Helper for VisionEdge

(function () {
    if (!window.API_BASE_URL) {
        const hostname = window.location.hostname || '';
        const isLocal = hostname === 'localhost' ||
                        hostname === '127.0.0.1' ||
                        hostname.startsWith('192.168.') ||
                        hostname.startsWith('10.') ||
                        hostname.endsWith('.local') ||
                        window.location.protocol === 'file:';

        window.API_BASE_URL = isLocal
            ? 'http://127.0.0.1:5000/api'
            : 'https://visionedge-opticals.onrender.com/api';
    }
})();

function setAuthData(token, user, rememberMe = true) {
    const primaryStorage = rememberMe ? localStorage : sessionStorage;
    const secondaryStorage = rememberMe ? sessionStorage : localStorage;

    // Clear secondary to prevent stale data conflicts
    ['access_token', 'jwtToken', 'current_user', 'user'].forEach(k => secondaryStorage.removeItem(k));

    // Save across all compatibility keys
    primaryStorage.setItem('access_token', token);
    primaryStorage.setItem('jwtToken', token);
    primaryStorage.setItem('current_user', JSON.stringify(user));
    primaryStorage.setItem('user', JSON.stringify(user));
}

function getToken() {
    return localStorage.getItem('access_token') ||
           localStorage.getItem('jwtToken') ||
           sessionStorage.getItem('access_token') ||
           sessionStorage.getItem('jwtToken') ||
           null;
}

function getCurrentUser() {
    try {
        const u = localStorage.getItem('current_user') ||
                  localStorage.getItem('user') ||
                  sessionStorage.getItem('current_user') ||
                  sessionStorage.getItem('user');
        return u ? JSON.parse(u) : null;
    } catch (e) {
        console.error('Error parsing user object:', e);
        return null;
    }
}

function getUser() {
    return getCurrentUser();
}

function getUserRole() {
    const user = getCurrentUser();
    return user && user.role ? user.role.toLowerCase() : null;
}

function isAuthenticated() {
    return Boolean(getToken() && getCurrentUser());
}

async function logout(redirect = true) {
    try {
        await fetch(`${window.API_BASE_URL}/auth/logout`, { method: 'POST' });
    } catch (e) {
        // Proceed with client cleanup regardless
    }

    ['access_token', 'jwtToken', 'current_user', 'user', 'visionEdgeCart', 'cart'].forEach(k => {
        localStorage.removeItem(k);
        sessionStorage.removeItem(k);
    });

    if (redirect) {
        window.location.href = 'login.html';
    }
}

function checkAuth(redirectUrl = 'login.html') {
    if (!isAuthenticated()) {
        window.location.href = redirectUrl;
    }
}

function enforceRoleAccess(allowedRoles, redirectUrl = 'unauthorized.html') {
    const role = getUserRole();
    const roles = allowedRoles.map(r => r.toLowerCase());
    if (!role || !roles.includes(role)) {
        window.location.href = redirectUrl;
    }
}

// Interceptor for API calls
async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const fullUrl = url.startsWith('http')
        ? url
        : (window.API_BASE_URL + (url.startsWith('/') ? '' : '/') + url);

    const response = await fetch(fullUrl, { ...options, headers });

    if (response.status === 401) {
        logout(true);
    }

    return response;
}

// Expose globally
window.setAuthData = setAuthData;
window.getToken = getToken;
window.getCurrentUser = getCurrentUser;
window.getUser = getUser;
window.getUserRole = getUserRole;
window.isAuthenticated = isAuthenticated;
window.logout = logout;
window.checkAuth = checkAuth;
window.enforceRoleAccess = enforceRoleAccess;
window.fetchWithAuth = fetchWithAuth;
