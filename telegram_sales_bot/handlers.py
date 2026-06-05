from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from keyboards import main_menu, panels_menu, flash_usdt_menu, payment_menu
from database import get_product_by_id, get_available_account, deliver_flash_usdt

# ── YOUR UPI AND CRYPTO DETAILS — edit these ──
UPI_ID = "yourname@upi"          # e.g. yourname@paytm
CRYPTO_ADDRESS = "TYourWalletAddressHere"  # your USDT TRC20 wallet address
# ─────────────────────────────────────────────

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 Welcome to the Bot!\nChoose an option below:",
        reply_markup=main_menu()
    )

async def menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Main Menu", reply_markup=main_menu())

async def handle_callbacks(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── MAIN MENU NAVIGATION ──
    if data == "menu_main":
        await query.edit_message_text(
            "🏠 Main Menu — choose an option:",
            reply_markup=main_menu()
        )

    elif data == "menu_panels":
        await query.edit_message_text(
            "💳 Available Account Panels:",
            reply_markup=panels_menu()
        )

    elif data == "menu_flash_usdt":
        await query.edit_message_text(
            "⚡ Flash USDT — select amount:",
            reply_markup=flash_usdt_menu()
        )

    elif data == "menu_orders":
        await query.edit_message_text(
            "📦 Your Orders\n\nNo orders yet.",
            reply_markup=main_menu()
        )

    elif data == "menu_help":
        await query.edit_message_text(
            "ℹ️ Help\n\n"
            "• Use Account Panels to buy panel access\n"
            "• Use Flash USDT to purchase USDT\n"
            "• Contact admin if you face any issues",
            reply_markup=main_menu()
        )

    # ── FLASH USDT AMOUNT SELECTED → SHOW PAYMENT OPTIONS ──
    elif data.startswith("flash_select_"):
        amount = data.split("_")[2]   # gets 100, 200, or 300
        await query.edit_message_text(
            f"💰 You selected *{amount} USDT*\n\nChoose payment method:",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── UPI PAYMENT ──
    elif data.startswith("pay_upi_"):
        amount = data.split("_")[2]
        await query.edit_message_text(
            f"💳 *UPI Payment*\n\n"
            f"Amount: ₹{amount} (or equivalent)\n"
            f"UPI ID: `{UPI_ID}`\n\n"
            f"1. Open any UPI app (GPay, PhonePe, Paytm)\n"
            f"2. Send payment to the UPI ID above\n"
            f"3. Send screenshot to admin for confirmation\n\n"
            f"After payment, contact @YourAdminUsername",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── CRYPTO PAYMENT ──
    elif data.startswith("pay_crypto_"):
        amount = data.split("_")[2]
        await query.edit_message_text(
            f"🪙 *Crypto Payment*\n\n"
            f"Amount: *{amount} USDT* (TRC20)\n"
            f"Wallet Address:\n`{CRYPTO_ADDRESS}`\n\n"
            f"1. Send exactly {amount} USDT on TRC20 network\n"
            f"2. Send transaction hash to admin\n\n"
            f"After payment, contact @YourAdminUsername",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── PANEL SELECTED ──
    elif data.startswith("panel_"):
        panel_name = data.replace("panel_", "")
        product = get_product_by_id(panel_name)
        if product:
            account = get_available_account(panel_name)
            if account:
                await query.edit_message_text(
                    f"✅ *Account Details for {panel_name}:*\n"
                    f"Username: `{account['username']}`\n"
                    f"Password: `{account['password']}`\n"
                    f"URL: {account['url']}\n"
                    f"Info: {account['additional_info']}",
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    f"❌ No available accounts for *{panel_name}* right now.",
                    parse_mode="Markdown",
                    reply_markup=panels_menu()
                )
        else:
            await query.edit_message_text(
                f"ℹ️ *{panel_name}* panel selected.\n\nContact admin to purchase.",
                parse_mode="Markdown",
                reply_markup=panels_menu()
            )

async def add_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    # ONE handler catches ALL button clicks
    application.add_handler(CallbackQueryHandler(handle_callbacks))
