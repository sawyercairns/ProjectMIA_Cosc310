from typing import List
from backend.app.schemas.productClass import Product
import json
import os
from pathlib import Path


#Takes all filters, returns a List of Product which match those filters
def get_products_filtered(category:str = "", keywords:str = "", max_price:float = 100000):
    products = _get_all_products()
    productList = list()
    for product in products:
        if product["price"] <= max_price and keywords.lower() in product["product_name"].lower() and ("category" not in product or product["category"] == category):
            new_product = Product(product["product_id"], product["product_name"], product["product_desc"], product["price"], product["discount_price"], product["discount_percent"], product["rating"], product["rating_count"], product["units_sold"])
            productList.append(new_product)
    return productList



def _get_all_products():
    path = Path(__file__).resolve().parents[1] / "data" / "products.json"
    with path.open("r", encoding="UTF-8") as f:
        products = json.load(f)
        return products
        
