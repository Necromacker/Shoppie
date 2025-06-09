import sqlite3

def delete_leather_belt():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('database/shoppie.db')
        cursor = conn.cursor()
        
        # Delete the leather belt product
        cursor.execute("DELETE FROM products WHERE name = 'Leather Belt'")
        
        # Commit the changes
        conn.commit()
        print("Successfully deleted the leather belt product!")
        
    except sqlite3.Error as e:
        print(f"Error deleting product: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    delete_leather_belt() 