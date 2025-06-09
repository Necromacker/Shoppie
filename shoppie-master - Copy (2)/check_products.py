import sqlite3

def check_products():
    try:
        conn = sqlite3.connect('database/shoppie.db')
        cursor = conn.cursor()
        
        # Check if products table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
        if not cursor.fetchone():
            print("Products table does not exist!")
            return
            
        # Count products
        cursor.execute("SELECT COUNT(*) FROM products;")
        count = cursor.fetchone()[0]
        print(f"Number of products in database: {count}")
        
        # Show all products
        cursor.execute("SELECT * FROM products;")
        products = cursor.fetchall()
        print("\nProducts in database:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[3]}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_products() 