import sqlite3
from config import DB_PATH

class AccountDelivery:
    def __init__(self):
        pass
    
    def get_available_account(self, product_id):
        """Get an unused account for the specified product"""
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
            # Mark account as used
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
                "additional_info