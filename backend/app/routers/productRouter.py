from typing import List
from fastapi import APIRouter, status
from backend.app.schemas import productClass

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=None)
def get_products(categories: str = "", keywords:str = "", maxPrice: float = 1000000):
    return "Test " + categories + " " + keywords + " " + str(maxPrice)