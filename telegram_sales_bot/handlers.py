from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from keyboards import main_menu, panels_menu, flash_usdt_menu
from database import get_product_by_id, get_available_account, deliver_flash_usdt

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the Account Panel and Flash USDT Bot!", reply_markup=main_menu())

async def menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Main Menu", reply_markup=main_menu())

async def panels(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Available Account Panels", reply_markup=panels_menu())

async def flash_usdt(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Flash USDT Options", reply_markup=flash_usdt_menu())

async def orders(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Your Orders", reply_markup=main_menu())

async def help_command(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Help Menu", reply_markup=main_menu())

async def panel_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    product_id = int(query.data.split('_')[2])
    product = get_product_by_id(product_id)
    if product:
        account = get_available_account(product_id)
        if account:
            await query.edit_message_text(f"Account Details for {product.name}:\n"
                                    f"Username: {account['username']}\n"
                                    f"Password: {account['password']}\n"
                                    f"URL: {account['url']}\n"
                                    f"Additional Info: {account['additional_info']}")
        else:
            await query.edit_message_text("No available accounts for this panel.")
    else:
        await query.edit_message_text("Product not found.")

async def flash_usdt_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    amount = float(query.data.split('_')[2])
    duration_hours = int(query.data.split('_')[3])
    user_wallet_address = "user_wallet_address_here"
    flash_data = deliver_flash_usdt(query.from_user.id, amount, duration_hours, user_wallet_address)
    if flash_data:
        await query.edit_message_text(f"Flash USDT delivered:\n"
                                f"Amount: {flash_data['amount']} USDT\n"
                                f"Duration: {flash_data['duration_hours']} hours\n"
                                f"Expires at: {flash_data['expires_at']}")
    else:
        await query.edit_message_text("Failed to deliver flash USDT.")

async def add_handlers(application):
    application.add_handler(CallbackQueryHandler(panel_handler, pattern="^panel_"))
    application.add_handler(CallbackQueryHandler(flash_usdt_handler, pattern="^flash_usdt_"))
