from typing import List
from fastapi import APIRouter, status
from backend.app.schemas import productClass

router = APIRouter(prefix="/products", tags=["products"])

#TODO: Some functions relevant to products included, will need to be filled with proper functions as they are developed

@router.get("", response_model=None)
def get_products(categories: str = "", keywords:str = "", maxPrice: float = 1000000):
    return "Test " + categories + " " + keywords + " " + str(maxPrice)