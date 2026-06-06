import tracemalloc
tracemalloc.start()
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN, ADMIN_ID
from handlers import start, menu, handle_callbacks, handle_screenshot

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(handle_callbacks))

    # Listens for screenshots sent by users
    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    application.run_polling()

if __name__ == "__main__":
    main()
