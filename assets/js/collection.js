import config from './config.js';

document.addEventListener('DOMContentLoaded', () => {
    const productsContainer = document.querySelector('.products-grid');
    const categoryFilters = document.querySelectorAll('.category-filter');
    const searchInput = document.querySelector('.search-input');
    const priceRange = document.querySelector('.price-range');
    const sortSelect = document.querySelector('.sort-select');

    let currentCategory = 'all';
    let currentSearch = '';
    let currentPriceRange = [0, 1000];
    let currentSort = 'newest';

    // Load products from the database
    async function loadProducts() {
        try {
            const response = await fetch(`${config.API_BASE_URL}/api/products`);
            if (!response.ok) {
                throw new Error('Failed to load products');
            }
            const products = await response.json();
            displayProducts(products);
        } catch (error) {
            console.error('Error loading products:', error);
            showError('Failed to load products. Please try again later.');
        }
    }

    // Display products in the collection grid
    function displayProducts(products) {
        const collectionGrid = document.querySelector('.collection-grid');
        if (!collectionGrid) {
            console.error('Collection grid not found');
            return;
        }
        
        collectionGrid.innerHTML = ''; // Clear existing content

        products.forEach(product => {
            const productCard = `
                <div class="collection-card">
                    <figure class="card-banner">
                        <img src="${product.image_url}" width="448" height="470" loading="lazy" alt="${product.name}" class="img-cover">
                    </figure>
                    <div class="card-content">
                        <h3 class="h3 title">${product.name}</h3>
                        <p class="card-text">${product.description}</p>
                        <div class="price">$${product.price.toFixed(2)}</div>
                        <button class="btn btn-primary" onclick="addToCart(${product.id})">
                            <span class="span">Add to Cart</span>
                            <ion-icon name="arrow-forward" aria-hidden="true"></ion-icon>
                        </button>
                    </div>
                </div>
            `;
            collectionGrid.innerHTML += productCard;
        });
    }

    // Add to cart functionality
    async function addToCart(productId) {
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please login to add items to cart');
            return;
        }

        try {
            const response = await fetch(`${config.API_BASE_URL}/api/cart`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: 1
                })
            });

            if (!response.ok) {
                throw new Error('Failed to add item to cart');
            }

            const data = await response.json();
            alert('Item added to cart successfully!');
            updateCartCount();
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert('Failed to add item to cart. Please try again.');
        }
    }

    // Update cart count
    async function updateCartCount() {
        const token = localStorage.getItem('token');
        if (!token) return;

        try {
            const response = await fetch(`${config.API_BASE_URL}/api/cart`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get cart items');
            }

            const cartItems = await response.json();
            const cartCount = cartItems.reduce((total, item) => total + item.quantity, 0);
            const cartBtn = document.querySelector('.cart-btn .span');
            if (cartBtn) {
                cartBtn.textContent = `Cart (${cartCount})`;
            }
        } catch (error) {
            console.error('Error updating cart count:', error);
        }
    }

    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        const collection = document.querySelector('.collection');
        if (collection) {
            collection.prepend(errorDiv);
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }

    // Event listeners for filters - only add if elements exist
    if (categoryFilters.length > 0) {
        categoryFilters.forEach(filter => {
            filter.addEventListener('click', (e) => {
                e.preventDefault();
                currentCategory = e.target.dataset.category;
                loadProducts();
            });
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            currentSearch = e.target.value;
            loadProducts();
        }, 300));
    }

    if (priceRange) {
        priceRange.addEventListener('change', (e) => {
            currentPriceRange = e.target.value.split(',').map(Number);
            loadProducts();
        });
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            currentSort = e.target.value;
            loadProducts();
        });
    }

    // Debounce function for search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Initialize
    loadProducts();
    updateCartCount();
}); 