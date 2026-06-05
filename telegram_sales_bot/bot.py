import tracemalloc
tracemalloc.start()
from telegram.ext import Application, CommandHandler
from config import TOKEN, ADMIN_ID
from handlers import start, menu, add_handlers

def main():
    application = Application.builder().token(TOKEN).build()
    
    # add_handlers registers everything — start, menu, and all button clicks
    add_handlers(application)
    
    application.run_polling()

if __name__ == "__main__":
    main()
