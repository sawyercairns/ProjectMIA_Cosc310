# Product class based off UML schema
# Created by: Ethan Wilson
# Reviewed by: Sawyer


import decimal
from pydantic import BaseModel

class Product:


    def __init__(self,
                product_id: int,
                product_name: str,
                product_desc: str,
                price: decimal,
                discount_price: decimal = 0,
                discount_percent:decimal = 0.0,
                rating: decimal = 0.0,
                rating_count: int = 0,
                units_sold: int = 0):
        self._product_id = product_id
        self.product_name = product_name
        self.product_desc = product_desc
        self.price = price
        self.discount_price = discount_price
        self.discount_percent = discount_percent
        self.rating = rating
        self.rating_count = rating_count
        self.units_sold = units_sold


    # Set the discount price of the product. Percent should be int and within 0-100.
    def set_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount percent must be within 0 and 100.")
        self._discount_percent = percent
        self._discount_price = self._price * (percent / 100)
        print("Discount has been set successfully.")


    # Set the price to a new price. Price should be float greater than 0.
    def change_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be a negative number.")
        self._price = price
        print("New price set successfully.")


    #Setters/Getters for all attributes of the class.
    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name
   
    @product_name.setter
    def product_name(self, id:str):
        self._product_name = id


    @property
    def product_desc(self):
        return self._product_desc


    @product_desc.setter
    def product_desc(self, id:str):
        self._product_desc = id


    @property
    def price(self):
        return self._price


    @price.setter
    def price(self, id:decimal):
        self._price = id            


    @property
    def discount_price(self):
        return self._discount_price


    @discount_price.setter
    def discount_price(self, id:decimal):
        self._discount_price = id


    @property
    def discount_percent(self):
        return self._discount_percent
   
    @discount_percent.setter
    def discount_percent(self, id:int):
        self._discount_percent = id


    @property
    def rating(self):
        return self._rating
   
    @rating.setter
    def rating(self, id:decimal):
        self._rating = id


    @property
    def rating_count(self):
        return self._rating_count
   
    @rating_count.setter
    def rating_count(self, id:int):
        self._rating_count = id


    @property
    def units_sold(self):
        return self._units_sold
   
    @units_sold.setter
    def units_sold(self, id:int):
        self._units_sold = id