import decimal
from backend.app.schemas.productClass import Product

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


