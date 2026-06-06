import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # Provide a default value of 0
USDT_WALLET_ADDRESS = os.getenv("USDT_WALLET_ADDRESS")
TON_API_KEY = os.getenv("TON_API_KEY")
DB_PATH = "bot_database.db"

import os

TOKEN = os.environ.get("TOKEN", "").strip()
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

if not TOKEN:
    raise ValueError("TOKEN environment variable is not set!")

ADMIN_ID = 123456789  
