from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from keyboards import main_menu, panels_menu, flash_usdt_menu

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