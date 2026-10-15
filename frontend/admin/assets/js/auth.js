// auth.js - Role-Based Authentication Utilities

const API_BASE_URL = 'http://localhost:5000/api';

function setAuthData(token, user, rememberMe = true) {
    const storage = rememberMe ? localStorage : sessionStorage;
    storage.setItem('jwtToken', token);
    storage.setItem('user', JSON.stringify(user));
}

function getToken() {
    return localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken');
}

function getUser() {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function getUserRole() {
    const user = getUser();
    return user ? user.role : null;
}

function logout(expired = false) {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('user');
    sessionStorage.removeItem('jwtToken');
    sessionStorage.removeItem('user');
    window.location.href = expired ? 'login.html?expired=true' : 'login.html';
}

function checkAuth() {
    // If not on login page, check token
    if (!window.location.pathname.endsWith('login.html')) {
        if (!getToken()) {
            window.location.href = 'login.html';
        }
    }
}

function enforceRoleAccess(allowedRoles) {
    const role = getUserRole();
    if (!role || !allowedRoles.includes(role)) {
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
    
    const fullUrl = url.startsWith('http') ? url : (API_BASE_URL + (url.startsWith('/') ? '' : '/') + url);
    const response = await fetch(fullUrl, { ...options, headers });
    
    if (response.status === 401) {
        // Token expired or unauthorized
        logout(true);
    } else if (response.status === 403) {
        window.location.href = 'unauthorized.html';
    }
    
    return response;
}
