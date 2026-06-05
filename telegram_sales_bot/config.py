import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # Provide a default value of 0
USDT_WALLET_ADDRESS = os.getenv("USDT_WALLET_ADDRESS")
TON_API_KEY = os.getenv("TON_API_KEY")
DB_PATH = "bot_database.db"