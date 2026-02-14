// Authentication Handler

// Check if user is logged in
function checkAuth() {
    const sessionId = localStorage.getItem('sessionId');
    const user = localStorage.getItem('user');

    if (!sessionId || !user) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Load user info on dashboard pages
function loadUserInfo() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const usernameEl = document.getElementById('username');
    const userRoleEl = document.getElementById('userRole');

    if (usernameEl) usernameEl.textContent = user.username || 'User';
    if (userRoleEl) userRoleEl.textContent = user.role || 'User';
}

// Handle login form
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const messageEl = document.getElementById('message');

        try {
            const response = await api.login(email, password);

            if (response.success) {
                localStorage.setItem('sessionId', response.session_id);
                localStorage.setItem('user', JSON.stringify(response.user));

                messageEl.className = 'message success';
                messageEl.textContent = 'Login successful! Redirecting...';

                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            }
        } catch (error) {
            messageEl.className = 'message error';
            messageEl.textContent = error.message || 'Login failed';
        }
    });
}

// Handle register form
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;
        const messageEl = document.getElementById('message');

        try {
            const response = await api.register(username, email, password, role);

            if (response.success) {
                messageEl.className = 'message success';
                messageEl.textContent = 'Registration successful! Redirecting to login...';

                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 1000);
            }
        } catch (error) {
            messageEl.className = 'message error';
            messageEl.textContent = error.message || 'Registration failed';
        }
    });
}

// Handle logout
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('sessionId');
            localStorage.removeItem('user');
            window.location.href = 'login.html';
        });
    }

    // Load user info on dashboard pages
    if (document.querySelector('.layout')) {
        checkAuth();
        loadUserInfo();
    }
});
