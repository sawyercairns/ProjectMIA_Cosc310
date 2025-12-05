from typing import List
from app.schemas.productClass import Product
import json
import os
from pathlib import Path

from app.services.Interactor import create_item, remove_item, load_json, write_to_json
from app.schemas.wishlistDiscountNotificationClass import WishlistDiscountNotification
from app.services import notificationInteractor

#Adds new_product to end of json file with id incremented
def create_product(p: Product):
    item = {
        "product_id": str(p.product_id),
        "product_name": p.product_name,
        "product_desc": p.product_desc,
        "price": p._price,                    
        "discount_price": p._discount_price,  
        "discount_percent": p._discount_percent,
        "rating": p._rating,                  
        "rating_count": p._rating_count,
        "units_sold": p._units_sold,
    }
    create_item("products.json", "product_id", item)

def remove_product(id:int):
    remove_item("products.json", "product_id", id)

def get_product(product_id: int):
    """Get a single product by its ID"""
    products = _get_all_products()
    for product in products:
        if int(product["product_id"]) == product_id:
            return {
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "product_desc": product.get("product_desc", ""),
                "actual_price": product.get("price", 0),
                "discount_price": product.get("discount_price", 0),
                "discount_percent": product.get("discount_percent", 0),
                "rating": product.get("rating", 0),
                "rating_count": product.get("rating_count", 0),
                "units_sold": product.get("units_sold", 0)
            }
    return None


def get_products_filtered(category:str = "", keywords:str = "", max_price:float = 100000):
    products = _get_all_products()
    productList = list()
    for product in products:
        if product["price"] <= max_price and keywords.lower() in product["product_name"].lower() and ("category" not in product or product["category"] == category):
            new_product = Product(product["product_id"], product["product_name"], product["product_desc"], product["price"], product["discount_price"], product["discount_percent"], product["rating"], product["rating_count"], product["units_sold"])
            productList.append(new_product)
    return productList


def swap_price_with_discount(product_id: int):
    products = load_json("products.json")
    for product in products:
        if int(product.get("product_id", -1)) == product_id:
            discount_price = product.get("discount_price")
            current_price = product.get("price")
            product_name = product.get("product_name", "Unknown Product")
            
            if discount_price is None or discount_price <= 0:
                raise ValueError("Product does not have a discount price to apply")
            
            # Swap prices
            product["price"], product["discount_price"] = discount_price, current_price
            write_to_json("products.json", products)
            
            # Send notifications to users who have this item in their wishlist
            _notify_wishlist_users_of_discount(
                product_id=product_id,
                product_name=product_name,
                old_price=current_price,
                new_price=discount_price
            )
            return
    raise ValueError("Product not found")


def _notify_wishlist_users_of_discount(product_id: int, product_name: str, old_price: float, new_price: float):
    """
    Find all users who have this product in their wishlist and send them a discount notification.
    """
    wishlist_path = Path(__file__).resolve().parents[1] / "data" / "wishlist.json"
    
    if not os.path.exists(wishlist_path):
        return
    
    try:
        with open(wishlist_path, "r", encoding="UTF-8") as f:
            wishlists = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return
    
    # Find all users who have this product in their wishlist
    for user_id, wishlist_data in wishlists.items():
        entries = wishlist_data.get("entries", [])
        
        # Check if this product is in the user's wishlist
        for entry in entries:
            if entry.get("product_id") == product_id:
                # Create and send notification
                next_id = notificationInteractor._get_next_notification_id(user_id)
                notification = WishlistDiscountNotification(
                    notification_id=next_id,
                    user_id=int(user_id),
                    product_id=product_id,
                    product_name=product_name,
                    old_price=old_price,
                    new_price=new_price
                )
                notificationInteractor.create_notification(user_id, notification)
                break  # Only one notification per user



def _get_all_products():
    path = Path(__file__).resolve().parents[1] / "data" / "products.json"
    with path.open("r", encoding="UTF-8") as f:
        products = json.load(f)
        return products
        
