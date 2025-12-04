from typing import List
from fastapi import APIRouter, status
from app.schemas.productClass import Product
import json
from app.services import productInteractor
from app.services.userInteractor import authenticate_admin
from app.schemas.userClass import User
from app.services.popularProducts import get_popular_products

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=None)
def get_products(category: str = "", keyword:str = "", maxPrice: float = 1000000):
    return productInteractor.get_products_filtered(category, keyword, maxPrice)

@router.get("/popularProducts", response_model = None)
def get_popular():
    return get_popular_products()

@router.get("/{product_id}", response_model=None)
def get_product_by_id(product_id: int):
    return productInteractor.get_product(product_id)

@router.post("", response_model=None, status_code=201)
def create_product(email:str, password:str, product_name:str, description:str, price:float, discount_price: float = 0.0):
    authenticate_admin(email, password)
    productInteractor.create_product(Product(0, product_name, description, price, discount_price))
    return "PRODUCT CREATED"

@router.delete("", response_model=None, status_code=204)
def delete_product(email:str, password: str, id:int):
    authenticate_admin(email, password)
    productInteractor.remove_product(id)
    return "PRODUCT REMOVED"
    