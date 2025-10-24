# Product class based off UML schema
# Created by: Ethan Wilson
# Reviewed by: (Insert Name)


class Product:
    def __init__(self, productID, productName, productDesc, price):
        self.productID = productID
        self.productName = productName
        self.productDesc = productDesc
        self.price = price
        self.discount = 0.0 # assuming default discount is 0
        self.discountPercent = 0.0 # assuming defualt discount is 0
        self.rating = 0 # to change upon rating creation
        self.ratingCount = 0 # to change upon rating creation
        self.unitsSold = 0 # to change upon rating creation

    # Set the discount price of the product. Percent should be int and within 0-100.
    def setDiscount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount percent must be within 0 and 100.")
        self.discountPercent = percent
        self.discount = self.price * (percent / 100)
        print("Discount has been set successfully.")

    # Set the price to a new price. Price should be float greater than 0.
    def changePrice(self, price):
        if price < 0:
            raise ValueError("Price cannot be a negative number.")
        self.price = price
        print("New price set successfully.")


