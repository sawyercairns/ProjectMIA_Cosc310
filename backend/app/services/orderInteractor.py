import json
import os
from backend.app.schemas.orderClass import Order
from backend.app.schemas.orderItemClass import OrderItem
from backend.app.schemas.addressClass import Address
from pathlib import Path
from typing import List

"""
This file contains the functions for order operations.
Handles loading, saving, and managing user orders.
"""

path = Path(__file__).resolve().parents[1] / "data" / "orders.json"

def load_orders(user_id: str) -> List[Order]:
    """
    Load all orders for a specific user.
    Returns empty list if user has no orders.
    """
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f, indent=4)
        return []
    
    with open(path, "r") as f:
        data = json.load(f)

    user_orders_dict = data.get(str(user_id), {})

    orders = []
    for order_id_str, order_data in user_orders_dict.items():
        items = [
            OrderItem(
                product_id=item["product_id"],
                product_name=item["product_name"],
                product_desc=item["product_desc"],
                quantity=item["quantity"],
                price=item["price"]
            )
            for item in order_data.get("order_items", [])
        ]

        address = None
        if order_data.get("address"):
            addr_data = order_data["address"]
            address = Address(
                line1=addr_data["line1"],
                line2=addr_data.get("line2", ""),
                city=addr_data["city"],
                province=addr_data["province"],
                country=addr_data["country"]
            )

        order = Order(
            order_id=order_data["order_id"],
            user_id=order_data["user_id"],
            order_items=items,
            address=address,
            order_date=order_data["order_date"]
        )

        orders.append(order)

    return orders


def add_order(user_id: str, order: Order):
    """
    Add a new order to user's order history.
    """
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    user_id_str = str(user_id)
    order_id_str = str(order.order_id)
    
    if user_id_str not in data:
        data[user_id_str] = {}
    
    data[user_id_str][order_id_str] = order.to_dict()

    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.replace(tmp_path, path)
    
    return order.to_dict()


def get_order_by_id(order_id: int, user_id: str = None) -> Order:
    """
    Get a specific order by order_id, with optional user_id for fast lookup.
    """
    if not os.path.exists(path):
        return None
    
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None

    order_id_str = str(order_id)
    
    if user_id is not None:
        user_orders = data.get(str(user_id), {})
        if order_id_str not in user_orders:
            return None
        order_data = user_orders[order_id_str]
    else:
        order_data = None
        for user_orders in data.values():
            if order_id_str in user_orders:
                order_data = user_orders[order_id_str]
                break
        
        if order_data is None:
            return None
    
    items = [
        OrderItem(
            product_id=item["product_id"],
            product_name=item["product_name"],
            product_desc=item["product_desc"],
            quantity=item["quantity"],
            price=item["price"]
        )
        for item in order_data.get("order_items", [])
    ]

    address = None
    if order_data.get("address"):
        addr_data = order_data["address"]
        address = Address(
            line1=addr_data["line1"],
            line2=addr_data.get("line2", ""),
            city=addr_data["city"],
            province=addr_data["province"],
            country=addr_data["country"]
        )

    return Order(
        order_id=order_data["order_id"],
        user_id=order_data["user_id"],
        order_items=items,
        address=address,
        order_date=order_data["order_date"]
    )


def get_next_order_id() -> int:
    """
    Get the next available order_id across all users.
    """
    if not os.path.exists(path):
        return 1
    
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return 1

    max_id = 0

    for user_orders in data.values():
        for order_id_str, order_data in user_orders.items():
            order_id = order_data["order_id"]
            if order_id > max_id:
                max_id = order_id
    
    return max_id + 1
