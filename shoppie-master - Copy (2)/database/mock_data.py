import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Product

def add_sample_products():
    sample_products = [
        {
            'name': 'Classic White T-Shirt',
            'description': 'A comfortable and versatile white t-shirt made from 100% cotton.',
            'price': 29.99,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'category': 'men'
        },
        {
            'name': 'Summer Dress',
            'description': 'A beautiful floral summer dress perfect for warm days.',
            'price': 59.99,
            'image_url': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'category': 'women'
        },
        {
            'name': 'Leather Wallet',
            'description': 'Genuine leather wallet with multiple card slots and coin pocket.',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'category': 'accessories'
        },
        {
            'name': 'Denim Jacket',
            'description': 'Classic denim jacket with a modern fit and comfortable feel.',
            'price': 79.99,
            'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'category': 'men'
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight and comfortable running shoes with excellent support.',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'category': 'accessories'
        },
        {
            'name': 'Floral Blouse',
            'description': 'Elegant floral blouse perfect for both casual and formal occasions.',
            'price': 49.99,
            'image_url': 'https://images.unsplash.com/photo-1564257631407-4deb1f99d992?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'category': 'women'
        }
    ]

    with app.app_context():
        # Clear existing products
        Product.query.delete()
        
        # Add new products
        for product_data in sample_products:
            product = Product(**product_data)
            db.session.add(product)
        
        # Commit changes
        db.session.commit()
        print("Sample products added successfully!")

if __name__ == '__main__':
    add_sample_products() 