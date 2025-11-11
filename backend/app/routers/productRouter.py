from typing import List
from fastapi import APIRouter, status
from backend.app.schemas.productClass import Product
import json
from backend.app.services import productInteractor
from backend.app.services.userValidation import user_is_admin

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=None)
def get_products(category: str = "", keyword:str = "", maxPrice: float = 1000000):
    return productInteractor.get_products_filtered(category, keyword, maxPrice)

@router.post("", response_model=None, status_code=201)
def create_product(username:str, password:str, product_name:str, description:str, price:float):
    if user_is_admin(username, password):
        productInteractor.create_product(Product(0, product_name, description, price))
        return "PRODUCT CREATED"
    else: return "CREATION FAILED"

@router.delete("", response_model=None, status_code=204)
def delete_product(username:str, password: str, id:int):
    if user_is_admin(username, password):
        productInteractor.remove_product(id)
        return "PRODUCT REMOVED"
    else: return "REMOVAL FAILED"
    