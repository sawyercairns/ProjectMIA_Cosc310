from backend.app.services.productInteractor import get_products_filtered
import pytest
from typing import List

def test_get_products_filtered_one():
    products = get_products_filtered("", "Wayona Nylon Braided USB to Lightning Fast Charging and Data Sync Cable Compatible for iPhone 13, 12,11, X, 8, 7, 6, 5, iPad Air, Pro, Mini (3 FT Pack of 1, Grey)")
    assert len(products) == 1
    assert products[0].product_id == "1"


def test_get_products_filtered_empty():
    products = get_products_filtered("","",0)
    assert len(products) == 0

def test_get_products_filtered_many():
    products = get_products_filtered("","USB", 1000000)
    assert len(products) != 0
    for product in products:
        assert "USB" in product.product_name

    products = get_products_filtered("","", 10)
    for product in products:
        assert product.price <= 10