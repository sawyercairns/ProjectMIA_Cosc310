import json
import os
import decimal
from backend.app.schemas.cartClass import Cart
from backend.app.schemas.orderItemClass import OrderItem
from pathlib import Path

"""
This file is the functions that the user can interact with.

"""

path = Path(__file__).resolve().parents[1] / "data" / "cart.json"

def load_cart(user_id: str) -> Cart:

    if not os.path.exists(path):
        raise FileNotFoundError("File can not be found")
    
    with open(path, "r") as f:
        data = json.load(f)

    user_cart = data.get(user_id)

    if not user_cart:
        empty_cart = Cart(user_id, cart_items=[], cart_value=decimal.Decimal(0))
        _save_cart(empty_cart)
        return empty_cart

    items = [
        OrderItem(
            product_id = item["product_id"],
            product_name = item["product_name"],
            product_desc = item["product_desc"],
            quantity = item["quantity"],
            price = decimal.Decimal(item["price"])
        )
        for item in user_cart.get("cart_items", [])
    ]

    return Cart(
        user_id=user_id,
        cart_items=items,
        cart_value=decimal.Decimal(user_cart["cart_value"])
    )


def _save_cart(cart: Cart):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    user_id = str(cart._user_id)
    existing_cart = data.get(user_id, {})

    new_cart_data = cart.to_dict()
    existing_cart.update(new_cart_data)
    data[user_id] = existing_cart

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def add_item(user_id: str, order_item: OrderItem):
    cart = load_cart(user_id)
    cart._cart_items.append(order_item)
    cart._cart_value += order_item._price * order_item._quantity
    _save_cart(cart)
    return cart.to_dict()


