# Product class based off UML schema
# Created by: Ethan Wilson
# Reviewed by: Sawyer


class Product:
    def __init__(self, product_id, product_name, product_desc, price):
        self.product_id = product_id
        self.product_name = product_name
        self.product_desc = product_desc
        self._price = price
        self._discount = 0.0 # assuming default discount is 0
        self._discount_percent = 0.0 # assuming defualt discount is 0
        self._rating = 0 # to change upon rating creation
        self._rating_count = 0 # to change upon rating creation
        self._units_sold = 0 # to change upon rating creation

    # Set the discount price of the product. Percent should be int and within 0-100.
    def set_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount percent must be within 0 and 100.")
        self._discount_percent = percent
        self._discount = self._price * (percent / 100)
        print("Discount has been set successfully.")

    # Set the price to a new price. Price should be float greater than 0.
    def change_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be a negative number.")
        self._price = price
        print("New price set successfully.")


