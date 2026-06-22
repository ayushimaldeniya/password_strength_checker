import sqlite3
import os

#Define the absolute path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'passwords.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    #Allows us to access columns by name instead of index
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Creates the user identity table if it doesn't exist yet."""
    conn = get_db_connection()
    cursor = conn.cursor()

    #Create table schema with strict constraints 
    cursor.execute ("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt_token TEXT NOT NULL,
            stored_hash TEXT NOT NULL,
            risk_tier TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Secure SQLite Database initialized seamlessly.")

#Initialize the database immediately when this module is imported
if __name__ == "__main__":
    initialize_database()