from flask import Flask, request, jsonify, session, send_from_directory, redirect
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
import bcrypt
from functools import wraps
import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Configure CORS to allow all origins and methods
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Configure JWT
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_EXPIRATION = timedelta(days=1)

# Configure Buymax AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("No API key found. Please set GOOGLE_API_KEY in your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# JWT configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# Database initialization
def init_db():
    conn = sqlite3.connect('database/shoppie.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create categories table
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL)''')
    
    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  image_url TEXT,
                  category_id INTEGER,
                  stock_quantity INTEGER DEFAULT 0,
                  sizes TEXT,
                  colors TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (category_id) REFERENCES categories (id))''')
    
    # Create cart table
    c.execute('''CREATE TABLE IF NOT EXISTS cart
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  product_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL DEFAULT 1,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (product_id) REFERENCES products (id))''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

def get_db_connection():
    return sqlite3.connect('database/shoppie.db')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Endpoints
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            return jsonify({'error': 'Username or email already exists'}), 400

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )
        conn.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get user
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user[3], password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Generate token
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.utcnow() + JWT_EXPIRATION
        }, JWT_SECRET)

        return jsonify({
            'token': token,
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2]
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get query parameters
        category = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')

        # Base query
        query = 'SELECT * FROM products'
        params = []

        # Add filters
        if category:
            query += ' WHERE category_id = ?'
            params.append(category)
        if search:
            query += ' WHERE name LIKE ?' if not category else ' AND name LIKE ?'
            params.append(f'%{search}%')
        if min_price:
            query += ' WHERE price >= ?' if not (category or search) else ' AND price >= ?'
            params.append(min_price)
        if max_price:
            query += ' WHERE price <= ?' if not (category or search or min_price) else ' AND price <= ?'
            params.append(max_price)

        # Execute query
        cursor.execute(query, params)
        products = cursor.fetchall()

        # Format response
        product_list = []
        for product in products:
            product_list.append({
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': product[3],
                'image_url': product[4],
                'category_id': product[5],
                'stock_quantity': product[6],
                'sizes': product[7],
                'colors': product[8]
            })

        return jsonify(product_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
            
        # Generate response using Gemini
        response = model.generate_content(user_message)
        
        return jsonify({
            'response': response.text
        })
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

# Add a catch-all route for chat requests
@app.route('/<path:path>', methods=['POST', 'OPTIONS'])
def catch_all(path):
    if path == 'chat':
        return chat()
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run() 