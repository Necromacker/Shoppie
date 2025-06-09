import sqlite3
from datetime import datetime
import json

def insert_product_data():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('database/shoppie.db')
        cursor = conn.cursor()

        # Insert categories if they don't exist
        categories = [
            ('Men\'s Clothing',),
            ('Women\'s Clothing',),
            ('Kids\' Clothing',),
            ('Accessories',),
            ('Footwear',)
        ]
        cursor.executemany(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            categories
        )

        # Get category IDs
        cursor.execute("SELECT id, name FROM categories")
        category_map = {name: id for id, name in cursor.fetchall()}

        # Real product data
        products = [
            # Men's Clothing
            {
                'name': 'Classic Fit Dress Shirt',
                'description': 'Premium cotton dress shirt with a classic fit. Perfect for formal occasions.',
                'price': 49.99,
                'category_id': category_map['Men\'s Clothing'],
                'image_url': 'https://images.unsplash.com/photo-1598033129183-c4f50c736f10',
                'stock_quantity': 50,
                'sizes': ['S', 'M', 'L', 'XL'],
                'colors': ['White', 'Blue', 'Black']
            },
            {
                'name': 'Slim Fit Chino Pants',
                'description': 'Modern slim fit chinos made from stretch cotton for comfort and style.',
                'price': 59.99,
                'category_id': category_map['Men\'s Clothing'],
                'image_url': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80',
                'stock_quantity': 45,
                'sizes': ['30', '32', '34', '36'],
                'colors': ['Khaki', 'Navy', 'Black']
            },
            # Women's Clothing
            {
                'name': 'Floral Print Dress',
                'description': 'Elegant floral print dress perfect for summer occasions.',
                'price': 79.99,
                'category_id': category_map['Women\'s Clothing'],
                'image_url': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1',
                'stock_quantity': 35,
                'sizes': ['XS', 'S', 'M', 'L'],
                'colors': ['Pink', 'Blue', 'Yellow']
            },
            {
                'name': 'High-Waisted Jeans',
                'description': 'Stylish high-waisted jeans with a comfortable stretch fit.',
                'price': 69.99,
                'category_id': category_map['Women\'s Clothing'],
                'image_url': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246',
                'stock_quantity': 40,
                'sizes': ['26', '28', '30', '32'],
                'colors': ['Blue', 'Black', 'Gray']
            },
            # Kids' Clothing
            {
                'name': 'Cartoon Print T-Shirt',
                'description': 'Fun and colorful cartoon print t-shirt for kids.',
                'price': 24.99,
                'category_id': category_map['Kids\' Clothing'],
                'image_url': 'https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8',
                'stock_quantity': 60,
                'sizes': ['3-4Y', '5-6Y', '7-8Y'],
                'colors': ['Red', 'Blue', 'Green']
            },
            # Accessories
            {
                'name': 'Leather Belt',
                'description': 'Genuine leather belt with classic buckle design.',
                'price': 39.99,
                'category_id': category_map['Accessories'],
                'image_url': 'https://images.unsplash.com/photo-1624222247344-550fb60583f1',
                'stock_quantity': 30,
                'sizes': ['S', 'M', 'L'],
                'colors': ['Brown', 'Black']
            },
            {
                'name': 'Designer Handbag',
                'description': 'Elegant designer handbag with multiple compartments.',
                'price': 129.99,
                'category_id': category_map['Accessories'],
                'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3',
                'stock_quantity': 25,
                'sizes': ['One Size'],
                'colors': ['Black', 'Brown', 'Red']
            },
            # Footwear
            {
                'name': 'Leather Oxford Shoes',
                'description': 'Classic leather oxford shoes for formal occasions.',
                'price': 89.99,
                'category_id': category_map['Footwear'],
                'image_url': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4',
                'stock_quantity': 35,
                'sizes': ['7', '8', '9', '10', '11'],
                'colors': ['Black', 'Brown']
            },
            {
                'name': 'Running Sneakers',
                'description': 'Comfortable running sneakers with cushioned soles.',
                'price': 79.99,
                'category_id': category_map['Footwear'],
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
                'stock_quantity': 40,
                'sizes': ['7', '8', '9', '10', '11'],
                'colors': ['White', 'Black', 'Red']
            }
        ]

        # Insert products
        for product in products:
            # Convert lists to JSON strings
            sizes_json = json.dumps(product['sizes'])
            colors_json = json.dumps(product['colors'])
            cursor.execute("""
                INSERT INTO products (
                    name, description, price, category_id, image_url,
                    stock_quantity, sizes, colors, created_at, updated_at
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                product['name'],
                product['description'],
                product['price'],
                product['category_id'],
                product['image_url'],
                product['stock_quantity'],
                sizes_json,
                colors_json,
                datetime.now(),
                datetime.now()
            ))

        # Commit the changes
        conn.commit()
        print("Successfully inserted product data into SQLite database!")

    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
            print("SQLite connection closed.")

if __name__ == "__main__":
    insert_product_data() 