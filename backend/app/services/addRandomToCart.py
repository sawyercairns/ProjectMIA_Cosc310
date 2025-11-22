# Add a random product to users cart.
import json
import os
import decimal 
import random

from pathlib import Path
from app.schemas.orderItemClass import OrderItem
from app.services.cartInteractor import add_item

def add_random_product(user_id: str):
    product_path = Path(__file__).resolve().parents[1] / "data" / "products.json"

    with product_path.open("r", encoding="UTF-8") as f:
        products = json.load(f)

    if not products:
        raise ValueError("No products found.")
    
    random_product = random.choice(products)

    order_item = OrderItem(  
        product_id=int(random_product["product_id"]),  
        product_name=random_product["product_name"],   
        product_desc=random_product["product_desc"],   
        quantity=1,                                    
        price=decimal.Decimal(str(random_product["price"]))  
    )

    add_item(user_id, order_item)