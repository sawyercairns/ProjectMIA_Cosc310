import json
import os
import decimal
from app.schemas.cartClass import Cart
from app.schemas.orderItemClass import OrderItem
from pathlib import Path
from app.services.Interactor import load_json, write_to_json

"""
This file is the functions that the user can interact with.

"""

path = Path(__file__).resolve().parents[1] / "data" / "cart.json"

def load_cart(user_id: str) -> Cart:

    if not os.path.exists(path):
        raise FileNotFoundError("File can not be found")
    
    data = load_json(path.name)

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

    write_to_json(path.name, data)


def add_item(user_id: str, order_item: OrderItem):
    cart = load_cart(user_id)
    
    for existing_item in cart._cart_items:
        if existing_item._product_id == order_item._product_id:
            raise ValueError(f"Product {order_item._product_id} is already in the cart")
    
    cart._cart_items.append(order_item)
    cart._cart_value += order_item._price * order_item._quantity
    _save_cart(cart)
    return cart.to_dict()


def delete_item(user_id: str, product_id: str):
    cart = load_cart(user_id)

    try:
        product_id_int = int(product_id)
    except ValueError:
        raise ValueError(f"Invalid product_id: {product_id}")

    item_to_remove = None
    for item in cart._cart_items:
        if item._product_id == product_id_int:
            item_to_remove = item
            break
    
    if item_to_remove is None:
        raise ValueError(f"Product with id {product_id} not found in cart")
  
    cart._cart_value -= item_to_remove._price * item_to_remove._quantity
    cart._cart_items.remove(item_to_remove)
    
    _save_cart(cart)
    return cart.to_dict()



