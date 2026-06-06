import tracemalloc
tracemalloc.start()
from telegram import Update
from telegram.ext import CallbackContext
from keyboards import (
    main_menu, panels_menu, flash_usdt_menu,
    payment_menu, panel_payment_menu,
    after_upi_menu, after_crypto_menu
)

# ── EDIT THESE WITH YOUR DETAILS ──────────────────────────
UPI_ID = "aaradhyya@slc"
UPI_NAME = "aaradhya"
CRYPTO_ADDRESS = "0xc2bb8b613c19aDA1605E6c71aF44CC6b4bb9076a"   # ERC20 wallet address
ADMIN_USERNAME = "@@Iamhere0013"
PANEL_PRICE = "₹800"
# ──────────────────────────────────────────────────────────

USDT_PRICES = {
    "100": "₹299",
    "200": "₹599",
    "300": "₹899",
}

PANEL_NAMES = {
    "panel_jeevan":     "Jeevan",
    "panel_trizo":      "Trizo",
    "panel_savingland": "Saving Land",
    "panel_dragonpay":  "Dragon Pay",
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
            "• Pay via UPI or Crypto (ERC20)\n"
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

    # ── PANEL UPI PAYMENT → show only Crypto option after ─
    elif data.startswith("panelpay_upi_"):
        panel_key = data.replace("panelpay_upi_", "")
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        await query.edit_message_text(
            f"💳 *UPI Payment — {panel_name} Panel*\n\n"
            f"Amount: *{PANEL_PRICE}*\n\n"
            f"UPI ID: `{UPI_ID}`\n"
            f"Name: *{UPI_NAME}*\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open GPay / PhonePe / Paytm\n"
            f"2️⃣ Send {PANEL_PRICE} to UPI ID above\n"
            f"3️⃣ Take screenshot of payment\n"
            f"4️⃣ Send screenshot to {ADMIN_USERNAME}\n\n"
            f"✅ Access will be given after confirmation.",
            parse_mode="Markdown",
            reply_markup=after_upi_menu(panel_key, "panel")
        )

    # ── PANEL CRYPTO PAYMENT → show only UPI option after ─
    elif data.startswith("panelpay_crypto_"):
        panel_key = data.replace("panelpay_crypto_", "")
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        await query.edit_message_text(
            f"🪙 *Crypto Payment — {panel_name} Panel*\n\n"
            f"Amount: *{PANEL_PRICE} worth of USDT*\n"
            f"Network: *ERC20*\n\n"
            f"Wallet Address:\n`{CRYPTO_ADDRESS}`\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open your crypto wallet\n"
            f"2️⃣ Send USDT on *ERC20 network*\n"
            f"3️⃣ Copy transaction hash\n"
            f"4️⃣ Send hash to {ADMIN_USERNAME}\n\n"
            f"✅ Access will be given after confirmation.",
            parse_mode="Markdown",
            reply_markup=after_crypto_menu(panel_key, "panel")
        )

    # ── FLASH USDT AMOUNT SELECTED ─────────────────────────
    elif data.startswith("flash_select_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, "")
        await query.edit_message_text(
            f"⚡ *Flash USDT — {amount} USDT*\n\n"
            f"💰 Price: *{inr_price}*\n\n"
            f"Choose payment method:",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── FLASH UPI PAYMENT → show only Crypto option after ─
    elif data.startswith("pay_upi_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, "")
        await query.edit_message_text(
            f"💳 *UPI Payment — {amount} USDT*\n\n"
            f"Amount: *{inr_price}*\n\n"
            f"UPI ID: `{UPI_ID}`\n"
            f"Name: *{UPI_NAME}*\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open GPay / PhonePe / Paytm\n"
            f"2️⃣ Send {inr_price} to UPI ID above\n"
            f"3️⃣ Take screenshot of payment\n"
            f"4️⃣ Send screenshot to {ADMIN_USERNAME}\n\n"
            f"✅ USDT will be sent after confirmation.",
            parse_mode="Markdown",
            reply_markup=after_upi_menu(amount, "flash")
        )

    # ── FLASH CRYPTO PAYMENT → show only UPI option after ─
    elif data.startswith("pay_crypto_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, "")
        await query.edit_message_text(
            f"🪙 *Crypto Payment — {amount} USDT*\n\n"
            f"Amount: *{amount} USDT*\n"
            f"Network: *ERC20*\n\n"
            f"Wallet Address:\n`{CRYPTO_ADDRESS}`\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open your crypto wallet\n"
            f"2️⃣ Send {amount} USDT on *ERC20 network*\n"
            f"3️⃣ Copy transaction hash\n"
            f"4️⃣ Send hash to {ADMIN_USERNAME}\n\n"
            f"✅ Confirmed within 30 minutes.",
            parse_mode="Markdown",
            reply_markup=after_crypto_menu(amount, "flash")
        )
