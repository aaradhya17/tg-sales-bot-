import tracemalloc
tracemalloc.start()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from keyboards import (
    main_menu, panels_menu, flash_usdt_menu,
    payment_menu, panel_payment_menu,
    after_upi_menu, after_crypto_menu
)

# ── EDIT THESE WITH YOUR DETAILS ──────────────────────────
UPI_ID = "aaradhyya@slc"
UPI_NAME = "aaradhya"
CRYPTO_ADDRESS = "0xc2bb8b613c19aDA1605E6c71aF44CC6b4bb9076a"
ADMIN_USERNAME = "@mrjinhere"
ADMIN_ID = 8612577961
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

    panel_key = user_data.get("pending_panel", "unknown")
    order_type = user_data.get("pending_type", "panel")
    amount = user_data.get("pending_amount", "")
    wallet = user_data.get("wallet_address", "")

    # If flash order and no wallet yet — save screenshot and ask for wallet
    if order_type == "flash" and not wallet:
        user_data["pending_screenshot"] = update.message.photo[-1].file_id
        await update.message.reply_text(
            "👛 *Please enter your ERC20 wallet address:*\n\n"
            "Type and send your wallet address below — "
            "then your order will be submitted automatically.",
            parse_mode="Markdown"
        )
        return

    await _submit_order(update, context, user, user_data,
                        panel_key, order_type, amount, wallet)


# ── SUBMIT ORDER TO ADMIN ──────────────────────────────────
async def _submit_order(update, context, user, user_data,
                        panel_key, order_type, amount, wallet):

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

    photo_id = user_data.pop("pending_screenshot", None)
    if not photo_id and update.message:
        photo_id = update.message.photo[-1].file_id

    try:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=admin_kb
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⚠️ Could not forward screenshot.\n\n{caption}\n\nError: {e}",
            parse_mode="Markdown",
            reply_markup=admin_kb
        )

    user_data.pop("wallet_address", None)


# ── TEXT HANDLER (wallet address input) ───────────────────
async def handle_text(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data

    if user_data.get("waiting_wallet"):
        wallet = update.message.text.strip()
        user_data["wallet_address"] = wallet
        user_data["waiting_wallet"] = False

        pending_screenshot = user_data.get("pending_screenshot")
        if pending_screenshot:
            await update.message.reply_text(
                f"✅ Wallet saved: `{wallet}`\n\n"
                f"📤 Submitting your order now...",
                parse_mode="Markdown"
            )
            user = update.message.from_user
            panel_key = user_data.get("pending_panel", "unknown")
            order_type = user_data.get("pending_type", "flash")
            amount = user_data.get("pending_amount", "")
            await _submit_order(update, context, user, user_data,
                                panel_key, order_type, amount, wallet)
        else:
            await update.message.reply_text(
                f"✅ Wallet address saved:\n`{wallet}`\n\n"
                f"📸 Now send your payment screenshot.",
                parse_mode="Markdown"
            )
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

    # ── BUYER CONFIRMS PAYMENT SENT ────────────────────────
    elif data.startswith("buyerconfirm_"):
        await query.edit_message_text(
            "✅ *Payment confirmation received!*\n\n"
            "🔍 Our admin is reviewing your screenshot now.\n\n"
            "⏳ Your order will be delivered to you shortly.\n\n"
            f"For any help: {ADMIN_USERNAME}",
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
        panel_key = data.replace("panel_", ""
