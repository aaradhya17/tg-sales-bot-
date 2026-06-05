from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN, ADMIN_ID
from handlers import start, menu, panels, flash_usdt, orders, help_command, add_handlers
from keyboards import main_menu

def main():
    updater = Updater(TOKEN, use_context=True)  # Set use_context to True
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("help", help_command))

    # Callback handlers
    dp.add_handler(CallbackQueryHandler(panels, pattern="^menu_panels$"))
    dp.add_handler(CallbackQueryHandler(flash_usdt, pattern="^menu_flash_usdt$"))
    dp.add_handler(CallbackQueryHandler(orders, pattern="^menu_orders$"))
    dp.add_handler(CallbackQueryHandler(help_command, pattern="^menu_help$"))

    # Add handlers for panels and flash USDT options
    add_handlers(dp)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
