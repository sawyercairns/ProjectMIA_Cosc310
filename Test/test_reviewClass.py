from backend.app.schemas.reviewClass import Review
import pytest
import os
import sys
from fastapi import FastAPI
from datetime import date

#tests to ensure review is created correctly
def test_review_creation():
    review = Review(12, 1, 1, date(2025, 10, 25), 1.99, 4.89, 0, "title", "body")
    assert review.review_id == 12
    assert review.user_id == 1
    assert review.product_id == 1
    assert review.created_at == date(2025, 10, 25)
    assert review.likes == 0
    assert review.title == "title"

def test_review_title_update():
    review = Review(12, 1, 1, date(2025, 10, 25), 1.99, 4.89, 0, "title", "body")
    review.update_title("new")
    assert review.title == "new"

def test_review_body_update():
    review = Review(12, 1, 1, date(2025, 10, 25), 1.99, 4.89, 0, "title", "body")
    review.update_body("new")
    assert review.body == "new"

def test_review_update_rating():
    review = Review(12, 1, 1, date(2025, 10, 25), 1.99, 4.89, 0, "title", "body")
    review.update_rating(5.0)
    assert review.rating == 5.0

def test_review_update_likes():
    review = Review(12, 1, 1, date(2025, 10, 25), 1.99, 4.89, 0, "title", "body")
    review.update_likes(10)
    assert review.likes == 10