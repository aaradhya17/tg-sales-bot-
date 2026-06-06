import tracemalloc
tracemalloc.start()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, filters
from keyboards import (
    main_menu, panels_menu, flash_usdt_menu,
    payment_menu, panel_payment_menu,
    after_upi_menu, after_crypto_menu
)

# ── EDIT THESE WITH YOUR DETAILS ──────────────────────────
UPI_ID = "aaradhyya@slc"
UPI_NAME = "aaradhya"
CRYPTO_ADDRESS = "0xc2bb8b613c19aDA1605E6c71aF44CC6b4bb9076a"
ADMIN_USERNAME = "@Iamhere0013"
ADMIN_ID = 123456789    # ← replace with your real Telegram ID from @userinfobot
PANEL_PRICE = "₹800"
# ──────────────────────────────────────────────────────────

USDT_PRICES = {
    "100": {"inr": "₹299", "usdt": "3.10"},
    "200": {"inr": "₹599", "usdt": "6.50"},
    "300": {"inr": "₹899", "usdt": "9.55"},
}

PANEL_NAMES = {
    "panel_jeevan":     "Jeevan",
    "panel_trizo":      "Trizo",
    "panel_savingland": "Saving Land",
    "panel_dragonpay":  "Dragon Pay",
    "panel_kuvera":     "Kuvera",
    "panel_bigwinner":  "Big Winner",
    "panel_qqpay":      "QQ Pay",
    "panel_indepay":    "Inde Pay",
}

# Panel details sent to buyer after admin confirms payment
PANEL_DETAILS = {
    "jeevan":      "🌐 URL: https://jeevan.example.com\n👤 User: jeevan_user\n🔑 Pass: jeevan123",
    "trizo":       "🌐 URL: https://trizo.example.com\n👤 User: trizo_user\n🔑 Pass: trizo123",
    "savingland":  "🌐 URL: https://savingland.example.com\n👤 User: saving_user\n🔑 Pass: saving123",
    "dragonpay":   "🌐 URL: https://dragonpay.example.com\n👤 User: dragon_user\n🔑 Pass: dragon123",
    "kuvera":      "🌐 URL: https://kuvera.example.com\n👤 User: kuvera_user\n🔑 Pass: kuvera123",
    "bigwinner":   "🌐 URL: https://bigwinner.example.com\n👤 User: big_user\n🔑 Pass: big123",
    "qqpay":       "🌐 URL: https://qqpay.example.com\n👤 User: qq_user\n🔑 Pass: qq123",
    "indepay":     "🌐 URL: https://indepay.example.com\n👤 User: inde_user\n🔑 Pass: inde123",
}

# stores pending orders: {admin_msg_id: {user_id, panel_key, type}}
pending_orders = {}


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

# ── SCREENSHOT HANDLER ─────────────────────────────────────
async def handle_screenshot(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_data = context.user_data

    # Check if user has a pending order stored
    panel_key = user_data.get("pending_panel")
    order_type = user_data.get("pending_type", "panel")
    amount = user_data.get("pending_amount", "")

    if not panel_key:
        await update.message.reply_text(
            "⚠️ Please select a panel or USDT amount first before sending screenshot."
        )
        return

    # Build order description
    if order_type == "panel":
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        order_desc = f"💳 Panel: *{panel_name}*\n💰 Amount: *{PANEL_PRICE}*"
    else:
        prices = USDT_PRICES.get(amount, {})
        order_desc = f"⚡ Flash USDT: *{amount} USDT*\n💰 Amount: *{prices.get('inr','')}* ({prices.get('usdt','')} USDT)"

    # Admin confirm/reject buttons
    confirm_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm Payment", callback_data=f"confirm_{user.id}_{panel_key}_{order_type}_{amount}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ])

    # Forward screenshot to admin with order info
    caption = (
        f"📸 *New Payment Screenshot*\n\n"
        f"👤 User: [{user.first_name}](tg://user?id={user.id})\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📋 Order:\n{order_desc}"
    )

    admin_msg = await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=confirm_kb
    )

    # Save pending order
    pending_orders[admin_msg.message_id] = {
        "user_id": user.id,
        "panel_key": panel_key,
        "order_type": order_type,
        "amount": amount
    }

    await update.message.reply_text(
        "📸 *Screenshot received!*\n\n"
        "✅ Your payment is being verified by admin.\n"
        "You will receive your order details shortly.",
        parse_mode="Markdown"
    )


async def handle_callbacks(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── ADMIN CONFIRM PAYMENT ──────────────────────────────
    if data.startswith("confirm_"):
        parts = data.split("_")
        user_id = int(parts[1])
        panel_key = parts[2]
        order_type = parts[3]
        amount = parts[4] if len(parts) > 4 else ""

        if order_type == "panel":
            panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
            details = PANEL_DETAILS.get(panel_key, "Contact admin for details.")
            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"✅ *Payment Confirmed!*\n\n"
                    f"🎉 Thank you! Here are your *{panel_name}* panel details:\n\n"
                    f"{details}\n\n"
                    f"⚠️ Keep these credentials safe.\n"
                    f"For support: {ADMIN_USERNAME}"
                ),
                parse_mode="Markdown"
            )
        else:
            prices = USDT_PRICES.get(amount, {})
            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"✅ *Payment Confirmed!*\n\n"
                    f"⚡ Your *{prices.get('usdt','')} USDT* has been processed.\n"
                    f"It will be sent to your wallet shortly.\n\n"
                    f"For support: {ADMIN_USERNAME}"
                ),
                parse_mode="Markdown"
            )

        # Update admin message to show confirmed
        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ *CONFIRMED by admin*",
            parse_mode="Markdown"
        )

    # ── ADMIN REJECT PAYMENT ───────────────────────────────
    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ *Payment Rejected*\n\n"
                "Your payment could not be verified.\n"
                "Please check and try again or contact admin.\n\n"
                f"Admin: {ADMIN_USERNAME}"
            ),
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        await query.edit_message_caption(
            caption=query.message.caption + "\n\n❌ *REJECTED by admin*",
            parse_mode="Markdown"
        )

    # ── MAIN NAVIGATION ───────────────────────────────────
    elif data == "menu_main":
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

    # ── PANEL SELECTED ─────────────────────────────────────
    elif data in PANEL_NAMES:
        panel_name = PANEL_NAMES[data]
        panel_key = data.replace("panel_", "")
        context.user_data["pending_panel"] = panel_key
        context.user_data["pending_type"] = "panel"
        await query.edit_message_text(
            f"💳 *{panel_name} Panel*\n\n"
            f"💰 Price: *{PANEL_PRICE}*\n\n"
            f"Choose your payment method:",
            parse_mode="Markdown",
            reply_markup=panel_payment_menu(panel_key)
        )

    # ── PANEL UPI PAYMENT ─────────────────────────────────
    elif data.startswith("panelpay_upi_"):
        panel_key = data.replace("panelpay_upi_", "")
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        context.user_data["pending_panel"] = panel_key
        context.user_data["pending_type"] = "panel"
        await query.edit_message_text(
            f"💳 *UPI Payment — {panel_name} Panel*\n\n"
            f"Amount: *{PANEL_PRICE}*\n\n"
            f"UPI ID: `{UPI_ID}`\n"
            f"Name: *{UPI_NAME}*\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open GPay / PhonePe / Paytm\n"
            f"2️⃣ Send {PANEL_PRICE} to UPI ID above\n"
            f"3️⃣ Take screenshot of payment\n"
            f"4️⃣ *Send screenshot here in this chat*\n\n"
            f"✅ Access will be given after confirmation.",
            parse_mode="Markdown",
            reply_markup=after_upi_menu(panel_key, "panel")
        )

    # ── PANEL CRYPTO PAYMENT ───────────────────────────────
    elif data.startswith("panelpay_crypto_"):
        panel_key = data.replace("panelpay_crypto_", "")
        panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
        context.user_data["pending_panel"] = panel_key
        context.user_data["pending_type"] = "panel"
        await query.edit_message_text(
            f"🪙 *Crypto Payment — {panel_name} Panel*\n\n"
            f"Amount: *{PANEL_PRICE} worth of USDT*\n"
            f"Network: *ERC20*\n\n"
            f"Wallet Address:\n`{CRYPTO_ADDRESS}`\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open your crypto wallet\n"
            f"2️⃣ Send USDT on *ERC20 network*\n"
            f"3️⃣ Take screenshot of transaction\n"
            f"4️⃣ *Send screenshot here in this chat*\n\n"
            f"✅ Access will be given after confirmation.",
            parse_mode="Markdown",
            reply_markup=after_crypto_menu(panel_key, "panel")
        )

    # ── FLASH USDT AMOUNT SELECTED ─────────────────────────
    elif data.startswith("flash_select_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, {}).get("inr", "")
        usdt_amount = USDT_PRICES.get(amount, {}).get("usdt", "")
        context.user_data["pending_type"] = "flash"
        context.user_data["pending_amount"] = amount
        await query.edit_message_text(
            f"⚡ *Flash USDT*\n\n"
            f"💰 Price: *{inr_price}* ({usdt_amount} USDT)\n\n"
            f"Choose payment method:",
            parse_mode="Markdown",
            reply_markup=payment_menu(amount)
        )

    # ── FLASH UPI PAYMENT ──────────────────────────────────
    elif data.startswith("pay_upi_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, {}).get("inr", "")
        usdt_amount = USDT_PRICES.get(amount, {}).get("usdt", "")
        context.user_data["pending_type"] = "flash"
        context.user_data["pending_amount"] = amount
        await query.edit_message_text(
            f"💳 *UPI Payment*\n\n"
            f"Amount: *{inr_price}* ({usdt_amount} USDT)\n\n"
            f"UPI ID: `{UPI_ID}`\n"
            f"Name: *{UPI_NAME}*\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open GPay / PhonePe / Paytm\n"
            f"2️⃣ Send {inr_price} to UPI ID above\n"
            f"3️⃣ Take screenshot of payment\n"
            f"4️⃣ *Send screenshot here in this chat*\n\n"
            f"✅ USDT will be sent after confirmation.",
            parse_mode="Markdown",
            reply_markup=after_upi_menu(amount, "flash")
        )

    # ── FLASH CRYPTO PAYMENT ───────────────────────────────
    elif data.startswith("pay_crypto_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, {}).get("inr", "")
        usdt_amount = USDT_PRICES.get(amount, {}).get("usdt", "")
        context.user_data["pending_type"] = "flash"
        context.user_data["pending_amount"] = amount
        await query.edit_message_text(
            f"🪙 *Crypto Payment*\n\n"
            f"Amount: *{usdt_amount} USDT* ({inr_price})\n"
            f"Network: *ERC20*\n\n"
            f"Wallet Address:\n`{CRYPTO_ADDRESS}`\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open your crypto wallet\n"
            f"2️⃣ Send {usdt_amount} USDT on *ERC20 network*\n"
            f"3️⃣ Take screenshot of transaction\n"
            f"4️⃣ *Send screenshot here in this chat*\n\n"
            f"✅ Confirmed within 30 minutes.",
            parse_mode="Markdown",
            reply_markup=after_crypto_menu(amount, "flash")
        )
