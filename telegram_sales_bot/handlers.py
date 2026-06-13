import tracemalloc
tracemalloc.start()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from keyboards import (
    main_menu, panels_menu, flash_usdt_menu,
    payment_menu, panel_payment_menu,
    after_upi_menu, after_crypto_menu, after_binance_menu
)

# ── EDIT THESE WITH YOUR DETAILS ──────────────────────────
UPI_ID = "aaradhyya@slc"
UPI_NAME = "aaradhya"
CRYPTO_ADDRESS = "0xc2bb8b613c19aDA1605E6c71aF44CC6b4bb9076a"
BINANCE_UID = ""    
ADMIN_USERNAME = "@mrjinhere"
ADMIN_ID = 8612577961
PANEL_PRICE = "₹800"
# ──────────────────────────────────────────────────────────

USDT_PRICES = {
    "10": {"inr": "₹50", "usdt": "0,7"},
    "100": {"inr": "₹199", "usdt": "2.50"},
    "300": {"inr": "₹299", "usdt": "3.560"},
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

PANEL_DETAILS = {
    "jeevan":     "🌐 URL: https://www.okbinances.com/cmw/#/login/Qlf5N1SU",
    "trizo":      "🌐 URL: https://trizo.xyraflo.com/register.html?inviteCode=yUodx3",
    "savingland": "🌐 URL: https://savings-land.com/reg?code=6nmjOs",
    "dragonpay":  "🌐 URL: https://dragonpay.example.com",
    "kuvera":     "🌐 URL: https://mobile.kvrpay.in/#/pages/user/register?invite_code=jjD2d5",
    "bigwinner":  "🌐 URL: https://bigwinner.example.com",
    "qqpay":      "🌐 URL: https://qqpay.example.com",
    "indepay":    "🌐 URL: https://indepay.example.com",
}

# ── GLOBAL STORAGE — persists across messages ──────────────
# { user_id: { "photo_id": ..., "panel_key": ..., "order_type": ..., "amount": ... } }
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


# ── SCREENSHOT HANDLER ─────────────────────────────────────#
async def handle_screenshot(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_data = context.user_data

    panel_key = user_data.get("pending_panel", "unknown")
    order_type = user_data.get("pending_type", "panel")
    amount = user_data.get("pending_amount", "")

    pending_orders[user.id] = {
        "photo_id":       update.message.photo[-1].file_id,
        "panel_key":      panel_key,
        "order_type":     order_type,
        "amount":         amount,
        "waiting_wallet": order_type == "flash",
    }

    print(f"DEBUG screenshot saved for user {user.id}: {pending_orders[user.id]}")

    if order_type == "flash":
        await update.message.reply_text(
            "👛 *Please enter your ERC20 wallet address:*\n\n"
            "Type and send it here — your order will be submitted automatically after.",
            parse_mode="Markdown"
        )
        return

    await _submit_order(context, user, panel_key, order_type, amount, "")


# ── SUBMIT ORDER TO ADMIN ──────────────────────────────────
async def _submit_order(context, user, panel_key, order_type, amount, wallet):
    try:
        # Get stored data from global dict
        order_data = pending_orders.get(user.id, {})
        photo_id = order_data.get("photo_id")

        print(f"DEBUG _submit_order: user={user.id} order_type={order_type} panel_key={panel_key} amount={amount} wallet={wallet} photo_id={photo_id}")

        if order_type == "panel":
            panel_name = PANEL_NAMES.get(f"panel_{panel_key}", panel_key)
            order_desc = f"💳 Panel: *{panel_name}*\n💰 Amount: *{PANEL_PRICE}*"
        else:
            prices = USDT_PRICES.get(amount, {})
            order_desc = (
                f"⚡ Flash USDT: *{amount} USDT*\n"
                f"💰 Amount: *{prices.get('inr', '')}* "
                f"({prices.get('usdt', '')} USDT)\n"
                f"👛 Buyer Wallet: `{wallet}`"
            )

        # Thank you + confirm button to buyer
        confirm_buyer_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "✅ Confirm Payment Sent",
                callback_data=f"buyerconfirm_{panel_key}_{order_type}_{amount}"
            )]
        ])

        await context.bot.send_message(
            chat_id=user.id,
            text=(
                "🙏 *Thank you for your purchase!*\n\n"
                "⏳ Please wait while we confirm your payment.\n\n"
                "📦 Your order will be sent to you after confirmation.\n\n"
                "👇 Click below to confirm you have sent the payment:"
            ),
            parse_mode="Markdown",
            reply_markup=confirm_buyer_kb
        )

        # Admin buttons
        admin_kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Confirm & Send Order",
                    callback_data=f"confirm_{user.id}_{panel_key}_{order_type}_{amount}"
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject_{user.id}"
                )
            ]
        ])

        caption = (
            f"📸 *New Payment Screenshot*\n\n"
            f"👤 User: [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 User ID: `{user.id}`\n\n"
            f"📋 *Order Details:*\n{order_desc}"
        )

        if photo_id:
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=photo_id,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=admin_kb
            )
        else:
            # No photo — send text only
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"⚠️ No screenshot.\n\n{caption}",
                parse_mode="Markdown",
                reply_markup=admin_kb
            )

        # Clear from global dict after sending
        pending_orders.pop(user.id, None)

    except Exception as e:
        print(f"ERROR in _submit_order: {e}")
        await context.bot.send_message(
            chat_id=user.id,
            text=f"⚠️ Something went wrong. Please contact {ADMIN_USERNAME}\n\nError: {e}"
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⚠️ Order submission error\nUser: {user.id}\nError: {e}"
        )


# ── TEXT HANDLER (wallet address) ─────────────────────────
async def handle_text(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user

    # Check global dict instead of context.user_data
    order_data = pending_orders.get(user.id, {})

    if order_data.get("waiting_wallet"):
        wallet = update.message.text.strip()

        print(f"DEBUG wallet received from {user.id}: {wallet}")
        print(f"DEBUG order_data: {order_data}")

        # Update global dict
        pending_orders[user.id]["waiting_wallet"] = False

        await update.message.reply_text(
            f"✅ Wallet saved:\n`{wallet}`\n\n"
            f"📤 Submitting your order now...",
            parse_mode="Markdown"
        )

        panel_key  = order_data.get("panel_key", "unknown")
        order_type = order_data.get("order_type", "flash")
        amount     = order_data.get("amount", "")

        await _submit_order(context, user, panel_key, order_type, amount, wallet)

    else:
        await update.message.reply_text(
            "Please use the menu to navigate.",
            reply_markup=main_menu()
        )


# ── CALLBACK HANDLER ───────────────────────────────────────
async def handle_callbacks(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── ADMIN CONFIRM ──────────────────────────────────────
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
                    f"🎉 Here are your *{panel_name}* panel details:\n\n"
                    f"{details}\n\n"
                    f"⚠️ Keep these details safe.\n"
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
                    f"⚡ Your *{prices.get('usdt', '')} USDT* has been processed.\n"
                    f"It will be sent to your wallet shortly.\n\n"
                    f"For support: {ADMIN_USERNAME}"
                ),
                parse_mode="Markdown"
            )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ *CONFIRMED — Order sent to user*",
            parse_mode="Markdown"
        )

    # ── BUYER CONFIRMS ─────────────────────────────────────
    elif data.startswith("buyerconfirm_"):
        await query.edit_message_text(
            "✅ *Payment confirmation received!*\n\n"
            "🔍 Our admin is reviewing your screenshot now.\n\n"
            "⏳ Your order will be delivered to you shortly.\n\n"
            f"For any help: {ADMIN_USERNAME}",
            parse_mode="Markdown"
        )

    # ── ADMIN REJECT ───────────────────────────────────────
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
    # ── FLASH BINANCE PAYMENT ──────────────────────────────
    elif data.startswith("pay_binance_"):
        amount = data.split("_")[2]
        inr_price = USDT_PRICES.get(amount, {}).get("inr", "")
        usdt_amount = USDT_PRICES.get(amount, {}).get("usdt", "")
        context.user_data["pending_type"] = "flash"
        context.user_data["pending_amount"] = amount
        await query.edit_message_text(
            f"🟡 *Binance UID Payment*\n\n"
            f"Amount: *{usdt_amount} USDT* ({inr_price})\n\n"
            f"Binance UID: `{BINANCE_UID}`\n\n"
            f"*Steps:*\n"
            f"1️⃣ Open Binance app\n"
            f"2️⃣ Go to Pay → Send\n"
            f"3️⃣ Enter UID: `{BINANCE_UID}`\n"
            f"4️⃣ Send {usdt_amount} USDT\n"
            f"5️⃣ Take screenshot of payment\n"
            f"6️⃣ *Send screenshot here in this chat*\n\n"
            f"✅ Confirmed within 30 minutes.",
            parse_mode="Markdown",
            reply_markup=after_binance_menu(amount, "flash")
        )
