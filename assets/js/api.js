// API Configuration
const API_CONFIG = {
    BASE_URL: 'https://shoppie-mlw5.onrender.com',
    ENDPOINTS: {
        CHAT: '/chat',
        PRODUCTS: '/api/products',
        LOGIN: '/api/login',
        REGISTER: '/api/register',
        CART: '/api/cart'
    }
};

// Override fetch to use the correct base URL
const originalFetch = window.fetch;
window.fetch = function(url, options) {
    if (url.startsWith('http://localhost:5000')) {
        url = url.replace('http://localhost:5000', API_CONFIG.BASE_URL);
    }
    return originalFetch(url, options);
}; 