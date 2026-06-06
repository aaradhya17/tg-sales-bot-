import os

TOKEN = os.environ.get("TOKEN", "").strip()
ADMIN_ID = 8612577961

if not TOKEN:
    raise ValueError("TOKEN environment variable is not set!")
