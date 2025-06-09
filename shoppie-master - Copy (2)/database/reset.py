import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

def reset_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Drop database if exists
        cursor.execute('DROP DATABASE IF EXISTS buymax_db')
        print("Database dropped successfully!")

    except Exception as e:
        print(f"Error resetting database: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    reset_database() 