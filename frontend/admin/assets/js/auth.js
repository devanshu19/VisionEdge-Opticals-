// auth.js - Role-Based Authentication Utilities for VisionEdge Admin

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

const API_BASE_URL = window.API_BASE_URL;

function setAuthData(token, user, rememberMe = true) {
    const primaryStorage = rememberMe ? localStorage : sessionStorage;
    const secondaryStorage = rememberMe ? sessionStorage : localStorage;

    ['jwtToken', 'access_token', 'user', 'current_user'].forEach(k => secondaryStorage.removeItem(k));

    primaryStorage.setItem('jwtToken', token);
    primaryStorage.setItem('access_token', token);
    primaryStorage.setItem('user', JSON.stringify(user));
    primaryStorage.setItem('current_user', JSON.stringify(user));
}

function getToken() {
    return localStorage.getItem('jwtToken') || 
           localStorage.getItem('access_token') || 
           sessionStorage.getItem('jwtToken') || 
           sessionStorage.getItem('access_token');
}

function getUser() {
    const userStr = localStorage.getItem('user') || 
                    localStorage.getItem('current_user') || 
                    sessionStorage.getItem('user') || 
                    sessionStorage.getItem('current_user');
    return userStr ? JSON.parse(userStr) : null;
}

function getUserRole() {
    const user = getUser();
    return user && user.role ? user.role.toLowerCase() : null;
}

async function logout(expired = false) {
    try {
        await fetch(`${window.API_BASE_URL}/auth/logout`, { method: 'POST' });
    } catch (e) {}

    ['jwtToken', 'access_token', 'user', 'current_user'].forEach(k => {
        localStorage.removeItem(k);
        sessionStorage.removeItem(k);
    });

    window.location.href = expired ? 'login.html?expired=true' : 'login.html';
}

function checkAuth() {
    const p = window.location.pathname.toLowerCase();
    const isLoginPage = p.endsWith('login.html') || p.endsWith('index.html') || p.endsWith('/admin') || p.endsWith('/admin/');
    if (!isLoginPage) {
        const token = getToken();
        const role = getUserRole();
        if (!token || !role || !['admin', 'staff'].includes(role)) {
            window.location.href = 'login.html';
        }
    }
}

function enforceRoleAccess(allowedRoles) {
    const role = getUserRole();
    const allowed = allowedRoles.map(r => r.toLowerCase());
    if (!role || !allowed.includes(role)) {
        window.location.href = 'unauthorized.html';
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
    } else if (response.status === 403) {
        window.location.href = 'unauthorized.html';
    }
    
    return response;
}

window.API_BASE_URL = API_BASE_URL;
window.setAuthData = setAuthData;
window.getToken = getToken;
window.getUser = getUser;
window.getUserRole = getUserRole;
window.logout = logout;
window.checkAuth = checkAuth;
window.enforceRoleAccess = enforceRoleAccess;
window.fetchWithAuth = fetchWithAuth;
