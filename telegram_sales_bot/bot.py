import tracemalloc
tracemalloc.start()
from telegram.ext import Application, CommandHandler
from config import TOKEN, ADMIN_ID
from handlers import start, menu, handle_callbacks

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))

    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(handle_callbacks))

    application.run_polling()

if __name__ == "__main__":
    main()
