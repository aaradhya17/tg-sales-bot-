from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import TOKEN
from handlers import start, menu, panels, flash_usdt, orders, help_command

def main():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))

    # Callback handlers
    app.add_handler(CallbackQueryHandler(panels, pattern="^menu_panels$"))
    app.add_handler(CallbackQueryHandler(flash_usdt, pattern="^menu_flash_usdt$"))
    app.add_handler(CallbackQueryHandler(orders, pattern="^menu_orders$"))
    app.add_handler(CallbackQueryHandler(help_command, pattern="^menu_help$"))

    app.run_polling()

if __name__ == "__main__":
    main()