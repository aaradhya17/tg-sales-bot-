import tracemalloc
tracemalloc.start()
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from keyboards import main_menu, panels_menu, flash_usdt_menu, payment_menu, panel_payment_menu

# ── EDIT THESE WITH YOUR DETAILS ──────────────────────────
UPI_ID = "aaradhyya@slc"               # your UPI ID
UPI_NAME = "AARADHYA"                # name shown on UPI
CRYPTO_ADDRESS = "0xc2bb8b613c19aDA1605E6c71aF44CC6b4bb9076a"    # USDT ERC20 wallet address
ADMIN_USERNAME = "@@Iamhere0013" # your Telegram username
PANEL_PRICE = "₹800"
# ──────────────────────────────────────────────────────────

PANEL_NAMES = {
    "panel_jeevan":      "Jeevan",
    "panel_trizo":       "Trizo",
    "panel_savingland":  "Saving Land",
    "panel_dragonpay":   "Dragon Pay",
}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 Welcome to the Bot!\nChoose an option below:",
        reply_markup=main_menu()
    )

async def menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🏠 Main Menu:",
        reply_markup=main_menu()
    )

async def handle_callbacks(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── MAIN NAVIGATION ───────────────────────────────────
    if data == "menu_main":
        await query.edit_message_text(
            "🏠 Main Menu — choose an option:",
            reply_markup=main_menu()
        )

    elif data == "menu_panels":
        await query.edit_message_text(
            "💳 *Account Panels*\nPrice: *₹800 each*\n\nSelect a panel:",
            parse_mode="Markdown",
            reply_markup=panels_menu()
        )

    elif data == "menu_flash_usdt":
        await query.edit_message_text(
            "⚡ *Flash USDT* — select amount:",
            parse_mode="Markdown",
            reply_markup=flash_usdt_menu()
        )

    elif data == "menu_orders":
        await query.edit_message_text(
            "📦 *Your Orders*\n\nNo orders yet.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif data == "menu_help":
        await query.edit_message_text(
            "ℹ️ *Help*\n\n"
            "• Select a panel to buy access\n"
            "• Pay via UPI or Crypto\n"
            "• Send payment screenshot to admin\n"
            f"• Admin: {ADMIN_USERNAME}",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    # ── PANEL SELECTED → SHOW PRICE + PAYMENT OPTIONS ─────
    elif data in PANEL_NAMES:
        panel_name = PANEL_NAMES[data]
        panel_key = data.replace("panel_", "")
        await query.edit_message_text(
            f"💳 *{panel_name} Panel*\n\n"
            f"💰 Price: *{PANEL_PRICE}*\n\n"
            f"Choose your payment method:",
            parse_mode="Markdown",
            reply_markup=panel_payment_menu(panel_key)
        )

    # ── PANEL UPI PAYMENT ──────────────────────────────────
    elif data.startswith("panelpay_upi_"):
        panel_key = data.replace("panelpay_upi_", "")
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        await query.edit_message_text(
            f"💳 *UPI Payment — {panel_name} Panel*\n\n"
            f"Amount: *{PANEL_PRICE}*\n\n"
            f"UPI ID: `{UPI_ID}`\n"
            f"Name: {UPI_NAME}\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open GPay / PhonePe / Paytm\n"
            f"2️⃣ Send {PANEL_PRICE} to UPI ID above\n"
            f"3️⃣ Take screenshot of payment\n"
            f"4️⃣ Send screenshot to {ADMIN_USERNAME}\n\n"
            f"✅ Access will be given after confirmation.",
            parse_mode="Markdown",
            reply_markup=panel_payment_menu(panel_key)
        )

    # ── PANEL CRYPTO PAYMENT ───────────────────────────────
    elif data.startswith("panelpay_crypto_"):
        panel_key = data.replace("panelpay_crypto_", "")
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        await query.edit_message_text(
            f"🪙 *Crypto Payment — {panel_name} Panel*\n\n"
            f"Amount: *{PANEL_PRICE} worth of USDT* (TRC20)\n\n"
            f"Wallet Address:\n`{CRYPTO_ADDRESS}`\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open your crypto wallet\n"
            f"2️⃣ Send USDT on TRC20 network\n"
            f"3️⃣ Copy transaction hash\n"
            f"4️⃣ Send hash to {ADMIN_USERNAME}\n\n"
            f"✅ Access will be given after confirmation.",
            parse_mode="Markdown",
            reply_markup=panel_payment_menu(panel_key)
        )

    # ── FLASH USDT AMOUNT SELECTED ─────────────────────────
    elif data.startswith("flash_select_"):
        amount = data.split("_")[2]
        await query.edit_message_text(
            f"⚡ *Flash USDT — {amount} USDT*\n\nChoose payment method:",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── FLASH UPI PAYMENT ──────────────────────────────────
    elif data.startswith("pay_upi_"):
        amount = data.split("_")[2]
        await query.edit_message_text(
            f"💳 *UPI Payment — {amount} USDT*\n\n"
            f"UPI ID: `{UPI_ID}`\n"
            f"Name: {UPI_NAME}\n\n"
            f"1️⃣ Send payment to UPI ID above\n"
            f"2️⃣ Screenshot → {ADMIN_USERNAME}",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── FLASH CRYPTO PAYMENT ───────────────────────────────
    elif data.startswith("pay_crypto_"):
        amount = data.split("_")[2]
        await query.edit_message_text(
            f"🪙 *Crypto Payment — {amount} USDT*\n\n"
            f"Network: TRC20\n"
            f"Wallet:\n`{CRYPTO_ADDRESS}`\n\n"
            f"1️⃣ Send {amount} USDT on TRC20\n"
            f"2️⃣ Transaction hash → {ADMIN_USERNAME}",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )
