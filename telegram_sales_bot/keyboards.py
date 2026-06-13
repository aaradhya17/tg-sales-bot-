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
        [InlineKeyboardButton("Trizo", callback_data="panel_trizo")],
        [InlineKeyboardButton("Saving Land", callback_data="panel_savingland")],
        [InlineKeyboardButton("Dragon Pay", callback_data="panel_dragonpay")],
        [InlineKeyboardButton("Kuvera", callback_data="panel_kuvera")],
        [InlineKeyboardButton("Big Winner", callback_data="panel_bigwinner")],
        [InlineKeyboardButton("QQ Pay", callback_data="panel_qqpay")],
        [InlineKeyboardButton("Inde Pay", callback_data="panel_indepay")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def flash_usdt_menu():
    keyboard = [
        [InlineKeyboardButton("10 USDT — ₹50", callback_data="flash_select_100")],
        [InlineKeyboardButton("100 USDT — ₹199", callback_data="flash_select_200")],
        [InlineKeyboardButton("300 USDT — ₹299", callback_data="flash_select_300")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def payment_menu(amount):
    keyboard = [
        [InlineKeyboardButton("💳 Pay via UPI", callback_data=f"pay_upi_{amount}")],
        [InlineKeyboardButton("🪙 Pay via Crypto (ERC20)", callback_data=f"pay_crypto_{amount}")],
        [InlineKeyboardButton("🟡 Pay via Binance UID", callback_data=f"pay_binance_{amount}")],
        [InlineKeyboardButton("⬅️ Back to USDT Menu", callback_data="menu_flash_usdt")]
    ]
    return InlineKeyboardMarkup(keyboard)

def after_upi_menu(amount, type):
    if type == "flash":
        keyboard = [
            [InlineKeyboardButton("🪙 Pay via Crypto instead (ERC20)", callback_data=f"pay_crypto_{amount}")],
            [InlineKeyboardButton("🟡 Pay via Binance UID instead", callback_data=f"pay_binance_{amount}")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"flash_select_{amount}")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("🪙 Pay via Crypto instead (ERC20)", callback_data=f"panelpay_crypto_{amount}")],
            [InlineKeyboardButton("🟡 Pay via Binance UID instead", callback_data=f"panelpay_binance_{amount}")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"panel_{amount}")]
        ]
    return InlineKeyboardMarkup(keyboard)

def after_crypto_menu(amount, type):
    if type == "flash":
        keyboard = [
            [InlineKeyboardButton("💳 Pay via UPI instead", callback_data=f"pay_upi_{amount}")],
            [InlineKeyboardButton("🟡 Pay via Binance UID instead", callback_data=f"pay_binance_{amount}")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"flash_select_{amount}")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("💳 Pay via UPI instead", callback_data=f"panelpay_upi_{amount}")],
            [InlineKeyboardButton("🟡 Pay via Binance UID instead", callback_data=f"panelpay_binance_{amount}")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"panel_{amount}")]
        ]
    return InlineKeyboardMarkup(keyboard)

def after_binance_menu(amount, type):
    if type == "flash":
        keyboard = [
            [InlineKeyboardButton("💳 Pay via UPI instead", callback_data=f"pay_upi_{amount}")],
            [InlineKeyboardButton("🪙 Pay via Crypto instead (ERC20)", callback_data=f"pay_crypto_{amount}")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"flash_select_{amount}")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("💳 Pay via UPI instead", callback_data=f"panelpay_upi_{amount}")],
            [InlineKeyboardButton("🪙 Pay via Crypto instead (ERC20)", callback_data=f"panelpay_crypto_{amount}")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"panel_{amount}")]
        ]
    return InlineKeyboardMarkup(keyboard)

def panel_payment_menu(panel):
    keyboard = [
        [InlineKeyboardButton("💳 Pay via UPI", callback_data=f"panelpay_upi_{panel}")],
        [InlineKeyboardButton("🪙 Pay via Crypto (ERC20)", callback_data=f"panelpay_crypto_{panel}")],
        [InlineKeyboardButton("🟡 Pay via Binance UID", callback_data=f"panelpay_binance_{panel}")],
        [InlineKeyboardButton("⬅️ Back to Panels", callback_data="menu_panels")]
    ]
    return InlineKeyboardMarkup(keyboard)
