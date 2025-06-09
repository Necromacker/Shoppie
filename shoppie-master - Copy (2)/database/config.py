import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'buymax_db'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 86400))  # 24 hours in seconds

# Server Configuration
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true' 