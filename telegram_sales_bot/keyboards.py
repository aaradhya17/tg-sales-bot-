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
        [InlineKeyboardButton("jeevan", callback_data="panel_jeevan")],
        [InlineKeyboardButton("Trizo", callback_data="panel_Trizo")],
        [InlineKeyboardButton("Saving Land", callback_data="panel_Saving land")],
        [InlineKeyboardButton("Dragon Pay", callback_data="panel_Dragon Pay")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def flash_usdt_menu():
    keyboard = [
        [InlineKeyboardButton("10 USDT for 1 Hour", callback_data="flash_usdt_10_1")],
        [InlineKeyboardButton("50 USDT for 5 Hours", callback_data="flash_usdt_50_5")],
        [InlineKeyboardButton("100 USDT for 10 Hours", callback_data="flash_usdt_100_10")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)
