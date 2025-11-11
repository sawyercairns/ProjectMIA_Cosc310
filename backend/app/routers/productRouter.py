from typing import List
from fastapi import APIRouter, status
from backend.app.schemas import productClass
import json
from backend.app.services import productInteractor

router = APIRouter(prefix="/products", tags=["products"])

#TODO: Some functions relevant to products included, will need to be filled with proper functions as they are developed

@router.get("", response_model=None)
def get_products(category: str = "", keyword:str = "", maxPrice: float = 1000000):
    return productInteractor.get_products_filtered(category, keyword, maxPrice)