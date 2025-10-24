# Testing productClass.py
# Created by: Ethan Wilson
# Reviewed by: (Insert Name)
from backend.app.schemas.productClass import Product
import pytest
import os
import sys
from fastapi import FastAPI


# Test if products are created.
def test_ProductCreation():
    product = Product(1, "Basket Ball", "Bouncing ball for playing", 25.00)
    assert product.productID == 1
    assert product.productName == "Basket Ball"

# Test if discounts can be set.
def test_SetDiscount():
    product = Product(2, "Hockey Stick", "Hockey Stick for Adults", 95.00)
    product.setDiscount(10)
    assert product.discountPercent == 10
    assert product.discount == 95 * (10/100)

# Test if the price can be changed.
def test_ChangePrice():
    product = Product(3, "Mug", "Coffee and Tea Mug", 15.00)
    product.changePrice(25.00)
    assert product.price == 25.00

# Test for invalid discount application. Discount greater than 100.
def test_InvalidDiscount():
    product = Product(4, "Glasses", "Rayband summer glasses", 150.00)
    with pytest.raises(ValueError):
        product.setDiscount(300) 

# Test for invalid price changes. Negative price.
def test_InvalidPriceChange():
    product = Product(6, "Chair", "Lawn chair blue", 45.00)
    with pytest.raises(ValueError):
        product.changePrice(-45.00)