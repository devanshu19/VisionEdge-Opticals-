// auth.js — Authentication helper functions for VisionEdge

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

function isAuthenticated() {
    const token = getToken();
    const user = getCurrentUser();
    return Boolean(token && user);
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('current_user');
    localStorage.removeItem('user');
    sessionStorage.clear();
    window.location.href = 'index.html';
}

// Expose globally
window.getToken = getToken;
window.getCurrentUser = getCurrentUser;
window.getUser = getCurrentUser;
window.isAuthenticated = isAuthenticated;
window.logout = logout;
