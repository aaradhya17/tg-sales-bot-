import tracemalloc
tracemalloc.start()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN, ADMIN_ID
from handlers import start, menu, panels, flash_usdt, orders, help_command, add_handlers
from keyboards import main_menu

def main():
    # Create the Application object
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("help", help_command))

    # Callback handlers
    application.add_handler(CallbackQueryHandler(panels, pattern="^menu_panels$"))
    application.add_handler(CallbackQueryHandler(flash_usdt, pattern="^menu_flash_usdt$"))
    application.add_handler(CallbackQueryHandler(orders, pattern="^menu_orders$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^menu_help$"))

    # Add handlers for panels and flash USDT options
    add_handlers(application)

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
