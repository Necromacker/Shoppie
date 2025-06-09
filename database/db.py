import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from .config import MYSQL_CONFIG

@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        yield connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

def execute_query(query, params=None, fetch=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()

def get_products(category=None, search=None, min_price=None, max_price=None):
    query = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        WHERE 1=1
    """
    params = []
    
    if category:
        query += " AND c.name = %s"
        params.append(category)
    
    if search:
        query += " AND (p.name LIKE %s OR p.description LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param])
    
    if min_price is not None:
        query += " AND p.price >= %s"
        params.append(min_price)
    
    if max_price is not None:
        query += " AND p.price <= %s"
        params.append(max_price)
    
    query += " ORDER BY p.created_at DESC"
    
    return execute_query(query, params, fetch=True)

def get_categories():
    query = "SELECT * FROM categories ORDER BY name"
    return execute_query(query, fetch=True)

def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    return execute_query(query, (email,), fetch=True)

def create_user(username, email, password_hash):
    query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
    """
    return execute_query(query, (username, email, password_hash))

def create_chat_session(user_id):
    query = """
        INSERT INTO chat_sessions (user_id, session_id)
        VALUES (%s, UUID())
    """
    return execute_query(query, (user_id,))

def save_chat_message(session_id, message, is_user=True):
    query = """
        INSERT INTO chat_messages (session_id, message, is_user)
        VALUES (%s, %s, %s)
    """
    return execute_query(query, (session_id, message, is_user))

def get_chat_history(session_id):
    query = """
        SELECT * FROM chat_messages 
        WHERE session_id = %s 
        ORDER BY created_at ASC
    """
    return execute_query(query, (session_id,), fetch=True)

def create_user_session(user_id, token, expires_at):
    query = """
        INSERT INTO user_sessions (user_id, token, expires_at)
        VALUES (%s, %s, %s)
    """
    return execute_query(query, (user_id, token, expires_at))

def get_user_session(token):
    query = """
        SELECT us.*, u.username, u.email 
        FROM user_sessions us
        JOIN users u ON us.user_id = u.id
        WHERE us.token = %s AND us.expires_at > NOW()
    """
    return execute_query(query, (token,), fetch=True) 