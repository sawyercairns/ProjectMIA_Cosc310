import decimal
from app.schemas.productClass import Product

class OrderItem:

    def __init__(self,
                 product_id: int,
                 product_name: str,
                 product_desc: str,
                 quantity: int,
                 price: decimal=0):
        self._product_id = product_id
        self._product_name = product_name
        self._product_desc = product_desc
        self._quantity = quantity
        self._price = decimal.Decimal(str(price))
        
    @classmethod
    def order_item(cls, product: Product, quantity: int):
        return cls(
            product_id = product.product_id,
            product_name = product.product_name,
            product_desc = product.product_desc,
            quantity = quantity,
            price = product.price
        )

    # -- Properties --
    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name

    @property
    def product_desc(self):
        return self._product_desc

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    def to_dict(self):
        """
        Convert OrderItem to dictionary for JSON serialization.
        """
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_desc": self.product_desc,
            "quantity": self.quantity,
            "price": str(self.price)
        }
