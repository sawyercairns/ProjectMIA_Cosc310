# Testing productClass.py
# Created by: Ethan Wilson
# Reviewed by: Sawyer
from app.schemas.productClass import Product
import pytest
import os
import sys
from fastapi import FastAPI




# Test if products are created.
def test_product_creation():
    product = Product(1, "Basket Ball", "Bouncing ball for playing", 25.00)
    assert product.product_id == 1
    assert product.product_name == "Basket Ball"


# Test if discounts can be set.
def test_set_discount_price():
    product = Product(2, "Hockey Stick", "Hockey Stick for Adults", 95.00)
    product.set_discount(10)
    assert product._discount_percent == 10
    assert product._discount_price == product._price * (10/100)


# Test if the price can be changed.
def test_change_price():
    product = Product(3, "Mug", "Coffee and Tea Mug", 15.00, 0, 0, 5, 1, 1)
    product.change_price(25.00)
    assert product._price == 25.00


# Test for invalid discount application. Discount greater than 100.
def test_invalid_discount():
    product = Product(4, "Glasses", "Rayband summer glasses", 150.00, 0, 0, 5, 1, 1)
    with pytest.raises(ValueError):
        product.set_discount(300)


# Test for invalid price changes. Negative price.
def test_invalid_pric_change():
    product = Product(6, "Chair", "Lawn chair blue", 45.00, 0, 0, 5, 1, 1)
    with pytest.raises(ValueError):
        product.change_price(-45.00)


#Test the getters and setters for product class
def test_product_class_setters_and_getters():
    product = Product(7, "Bats", "Steel Bat,", 150.00, 0.0, 0, 5, 1, 1)


    product.product_name = "Bat"
    product.product_desc = "Wooden Bat"
    product.price = 100.00
    product.discount_percent = 10
    product.discount_price = 90.00
    product.rating = 4
    product.rating_count = 2
    product.units_sold = 2


    assert product.product_name == "Bat"
    assert product.product_desc == "Wooden Bat"
    assert product.price == 100.00
    assert product.discount_percent == 10
    assert product.discount_price == 90.00
    assert product.rating == 4
    assert product.rating_count == 2
    assert product.units_sold == 2