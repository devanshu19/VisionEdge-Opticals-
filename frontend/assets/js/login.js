const API_BASE_URL = window.API_BASE_URL || (['localhost', '127.0.0.1'].includes(window.location.hostname) ? 'http://127.0.0.1:5000/api' : 'https://visionedge-opticals.onrender.com/api');

document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('loginForm');

    if (!loginForm) {
        console.error('Login form not found.');
        return;
    }

    loginForm.addEventListener('submit', async function (event) {

        event.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('pwdInput').value;

        const loginButton = document.getElementById('loginButton');
        const errorMessage = document.getElementById('loginError');

        errorMessage.classList.add('d-none');
        errorMessage.textContent = '';

        if (!username || !password) {
            errorMessage.textContent = 'Please enter username and password.';
            errorMessage.classList.remove('d-none');
            return;
        }

        loginButton.disabled = true;
        loginButton.innerHTML =
            '<span class="spinner-border spinner-border-sm me-2"></span>Logging in...';

        try {

            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Invalid username or password.');
            }

            // Save JWT token in all compatibility keys
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('jwtToken', data.access_token);

            // Save logged-in user in all compatibility keys
            localStorage.setItem('current_user', JSON.stringify(data.user));
            localStorage.setItem('user', JSON.stringify(data.user));

            console.log('Login successful:', data.user);

            // Redirect to redirect target or dashboard
            const urlParams = new URLSearchParams(window.location.search);
            const redirectUrl = urlParams.get('redirect');
            window.location.href = redirectUrl || 'dashboard.html';

        } catch (error) {

            console.error('Login error:', error);

            errorMessage.textContent = error.message ||
                'Unable to connect to the server.';

            errorMessage.classList.remove('d-none');

            loginButton.disabled = false;
            loginButton.innerHTML = 'Log In';
        }
    });
});