import os

TOKEN = os.environ.get("TOKEN", "").strip()
ADMIN_ID = 6130754844

if not TOKEN:
    raise ValueError("TOKEN environment variable is not set!")
