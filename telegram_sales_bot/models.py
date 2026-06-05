class Product:
    def __init__(self, id, name, description, price, category, stock, account_type, flash_amount=None, duration=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock = stock
        self.account_type = account_type
        self.flash_amount = flash_amount
        self.duration = duration

class Order:
    def __init__(self, id, user_id, product_id, total_price, status, payment_address, payment_tx_id, created_at):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.total_price = total_price
        self.status = status
        self.payment_address = payment_address
        self.payment_tx_id = payment_tx_id
        self.created_at = created_at

class AccountCredential:
    def __init__(self, id, product_id, username, password, url, additional_info, is_used, order_id):
        self.id = id
        self.product_id = product_id
        self.username = username
        self.password = password
        self.url = url
        self.additional_info = additional_info
        self.is_used = is_used
        self.order_id = order_id