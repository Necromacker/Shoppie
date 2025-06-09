from flask import Flask, request, jsonify, session, send_from_directory
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
CORS(app)

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
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change this to a secure secret key

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
    
    # Create products table with all necessary columns
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

        # Build query
        query = 'SELECT * FROM products WHERE 1=1'
        params = []

        if category and category != 'all':
            query += ' AND category = ?'
            params.append(category)

        if search:
            query += ' AND (name LIKE ? OR description LIKE ?)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param])

        if min_price:
            query += ' AND price >= ?'
            params.append(float(min_price))

        if max_price:
            query += ' AND price <= ?'
            params.append(float(max_price))

        # Execute query
        cursor.execute(query, params)
        products = cursor.fetchall()

        # Convert to list of dictionaries
        product_list = []
        for product in products:
            product_list.append({
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': product[3],
                'image_url': product[4],
                'category': product[5],
                'created_at': product[6]
            })

        return jsonify(product_list)

    except Exception as e:
        print(f"Error fetching products: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/chat', methods=['POST'])
@token_required
def chat_endpoint(current_user):
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Get response from Buymax AI
        response = model.generate_content(message)
        
        # Store chat in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create or get session
        cursor.execute(
            'SELECT id FROM chat_sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
            (current_user,)
        )
        session_result = cursor.fetchone()
        
        if not session_result:
            cursor.execute(
                'INSERT INTO chat_sessions (user_id, session_id) VALUES (?, ?)',
                (current_user, str(datetime.now().timestamp()))
            )
            session_id = cursor.lastrowid
        else:
            session_id = session_result[0]

        # Store messages
        cursor.execute(
            'INSERT INTO chat_messages (session_id, message, is_user) VALUES (?, ?, ?)',
            (session_id, message, True)
        )
        cursor.execute(
            'INSERT INTO chat_messages (session_id, message, is_user) VALUES (?, ?, ?)',
            (session_id, response.text, False)
        )
        
        conn.commit()
        
        return jsonify({
            'response': response.text,
            'session_id': session_id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/chat/history', methods=['GET'])
@token_required
def chat_history(current_user):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT m.*, s.session_id 
            FROM chat_messages m
            JOIN chat_sessions s ON m.session_id = s.id
            WHERE s.user_id = ?
            ORDER BY m.created_at ASC
        ''', (current_user,))
        
        messages = cursor.fetchall()
        return jsonify(messages)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/chat', methods=['POST'])
def chat():
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Buymax AI server on http://localhost:5000")
    app.run(debug=True) 