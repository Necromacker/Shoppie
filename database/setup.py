import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt
import json

# Load environment variables
load_dotenv()

# Database configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

def setup_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Read and execute schema.sql
        with open('database/schema.sql', 'r') as file:
            schema = file.read()
            for statement in schema.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()

        # Switch to the database
        cursor.execute('USE buymax_db')

        # Insert sample categories
        categories = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Fashion and apparel'),
            ('Books', 'Books and publications'),
            ('Home & Kitchen', 'Home appliances and kitchenware')
        ]
        cursor.executemany(
            'INSERT INTO categories (name, description) VALUES (%s, %s)',
            categories
        )

        # Insert sample products
        products = [
            ('Smartphone X', 'Latest smartphone with advanced features', 699.99, 1, 
             'https://example.com/phone.jpg',
             json.dumps(['S', 'M', 'L']),
             json.dumps(['Black', 'White', 'Gold']),
             100),
            ('Designer T-Shirt', 'Comfortable cotton t-shirt', 29.99, 2,
             'https://example.com/tshirt.jpg',
             json.dumps(['S', 'M', 'L', 'XL']),
             json.dumps(['Red', 'Blue', 'Green']),
             50),
            ('Python Programming', 'Learn Python programming', 39.99, 3,
             'https://example.com/book.jpg',
             json.dumps(['Standard']),
             json.dumps(['Paperback']),
             30),
            ('Smart Coffee Maker', 'Programmable coffee maker', 89.99, 4,
             'https://example.com/coffee.jpg',
             json.dumps(['Standard']),
             json.dumps(['Black', 'Silver']),
             20)
        ]
        cursor.executemany(
            '''INSERT INTO products 
               (name, description, price, category_id, image_url, sizes, colors, stock) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
            products
        )

        # Insert a test user
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
            ('testuser', 'test@example.com', hashed_password)
        )

        conn.commit()
        print("Database setup completed successfully!")

    except Exception as e:
        print(f"Error setting up database: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    setup_database() 