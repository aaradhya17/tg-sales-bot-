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
    conn.close()

def get_product_by_id(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if product:
        return {
            "id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "category": product[4],
            "stock": product[5],
            "account_type": product[6],
            "flash_amount": product[7],
            "duration": product[8]
        }
    return None

def get_available_account(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, username, password, url, additional_info
    FROM account_credentials
    WHERE product_id = ? AND is_used = FALSE
    LIMIT 1
    """, (product_id,))
    account = cursor.fetchone()
    if account:
        cursor.execute("""
        UPDATE account_credentials
        SET is_used = TRUE
        WHERE id = ?
        """, (account[0],))
        conn.commit()
        conn.close()
        return {
            "username": account[1],
            "password": account[2],
            "url": account[3],
            "additional_info": account[4]
        }
    conn.close()
    return None

def deliver_flash_usdt(user_id, amount, duration_hours, user_wallet_address):
    from crypto_payment import USDTProcessor
    processor = USDTProcessor()
    flash_data = processor.generate_flash_usdt(amount, duration_hours)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO orders (user_id, product
