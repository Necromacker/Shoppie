// Make functions globally accessible
window.showLoginModal = function() {
    console.log('showLoginModal called');
    const loginModal = document.getElementById('loginModal');
    if (!loginModal) {
        console.error('Login modal not found');
        return;
    }
    loginModal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

window.showRegisterModal = function() {
    console.log('showRegisterModal called');
    const registerModal = document.getElementById('registerModal');
    if (!registerModal) {
        console.error('Register modal not found');
        return;
    }
    registerModal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

window.closeModal = function(modalId) {
    console.log('closeModal called for:', modalId);
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.error('Modal not found:', modalId);
        return;
    }
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore background scrolling
}

window.logout = function() {
    console.log('logout called');
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    checkAuth();
}

// Check if user is logged in
function checkAuth() {
    console.log('checkAuth called');
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const authButtons = document.getElementById('authButtons');
    const userInfo = document.getElementById('userInfo');
    const usernameSpan = document.getElementById('username');

    if (!authButtons || !userInfo || !usernameSpan) {
        console.error('Required elements not found');
        return;
    }

    if (token && username) {
        authButtons.style.display = 'none';
        userInfo.style.display = 'flex';
        usernameSpan.textContent = username;
    } else {
        authButtons.style.display = 'flex';
        userInfo.style.display = 'none';
    }
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    console.log('handleLogin called');
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', username);
        
        // Close modal and update UI
        closeModal('loginModal');
        checkAuth();
        
        // Clear form
        document.getElementById('loginForm').reset();
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please check your credentials.');
    }
}

// Handle register
async function handleRegister(event) {
    event.preventDefault();
    console.log('handleRegister called');
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', username);
        
        // Close modal and update UI
        closeModal('registerModal');
        checkAuth();
        
        // Clear form
        document.getElementById('registerForm').reset();
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

// Initialize auth functionality
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing auth');
    checkAuth();
    
    // Add event listeners for forms
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        console.log('Login form found, adding event listener');
        loginForm.addEventListener('submit', handleLogin);
    } else {
        console.error('Login form not found');
    }
    
    if (registerForm) {
        console.log('Register form found, adding event listener');
        registerForm.addEventListener('submit', handleRegister);
    } else {
        console.error('Register form not found');
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
}); 