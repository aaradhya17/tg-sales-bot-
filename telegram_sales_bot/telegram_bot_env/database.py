import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Products table for account panels
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT,
        stock INTEGER DEFAULT 0,
        account_type TEXT,  # 'panel' or 'flash_usdt'
        flash_amount REAL,  # For flash USDT products
        duration INTEGER    # Duration in hours for flash USDT
    )
    """)
    
    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        total_price REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        payment_address TEXT,
        payment_tx_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Account credentials table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        username TEXT,
        password TEXT,
        url TEXT,
        additional_info TEXT,
        is_used BOOLEAN DEFAULT FALSE,
        order_id INTEGER
    )
    """)
    
    conn.commit()
    conn.close()jjjnjnjn