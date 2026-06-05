from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💳 Account Panels", callback_data="menu_panels")],
        [InlineKeyboardButton("⚡ Flash USDT", callback_data="menu_flash_usdt")],
        [InlineKeyboardButton("📦 My Orders", callback_data="menu_orders")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def panels_menu():
    keyboard = [
        [InlineKeyboardButton("Jeevan", callback_data="panel_jeevan")],
        [InlineKeyboardButton("Trizo", callback_data="panel_Trizo")],
        [InlineKeyboardButton("Saving Land", callback_data="panel_Saving land")],
        [InlineKeyboardButton("Dragon Pay", callback_data="panel_Dragon Pay")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def flash_usdt_menu():
    keyboard = [
        [InlineKeyboardButton("100 USDT", callback_data="flash_select_100")],
        [InlineKeyboardButton("200 USDT", callback_data="flash_select_200")],
        [InlineKeyboardButton("300 USDT", callback_data="flash_select_300")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def payment_menu(amount):
    keyboard = [
        [InlineKeyboardButton("💳 Pay via UPI", callback_data=f"pay_upi_{amount}")],
        [InlineKeyboardButton("🪙 Pay via Crypto", callback_data=f"pay_crypto_{amount}")],
        [InlineKeyboardButton("⬅️ Back to USDT Menu", callback_data="menu_flash_usdt")]
    ]
    return InlineKeyboardMarkup(keyboard)
