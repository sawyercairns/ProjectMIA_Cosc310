from typing import List
import decimal
from backend.app.schemas.orderItemClass import OrderItem
import json, os
from pathlib import Path

class Cart:

    path = Path(__file__).resolve().parents[1] / "data" / "cart.json"

    def __init__(self,
                 user_id: str,
                 cart_items: List[OrderItem] = None,
                 cart_value: decimal=0):
        self._user_id = user_id
        self._cart_items = cart_items
        self._cart_value = cart_value

    def to_dict(self):
        return {
            "cart_value": str(self._cart_value),
            "cart_items": [
                {
                    "product_id": item._product_id,
                    "product_name": item._product_name,
                    "product_desc": item._product_desc,
                    "quantity": item._quantity,
                    "price": str(item._price)
                }
                for item in self._cart_items
            ]
        }
