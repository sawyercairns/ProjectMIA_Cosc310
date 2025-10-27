from backend.app.schemas.reviewClass import Review
import pytest
import os
import sys
from fastapi import FastAPI
from datetime import date

#tests to ensure review is created correctly
def test_review_creation():
    review = Review(12, 1, 1, date(2025, 10, 25), 4.89, 0, "title", "body")
    assert review.review_id == 12
    assert review.user_id == 1
    assert review.product_id == 1
    assert review.created_at == date(2025, 10, 25)
    assert review.likes == 0
    assert review.title == "title"

def test_review_getters_and_setters():
    review = Review(12, 1, 1, date(2025, 10, 25), 4.89, 0, "title", "body")

    review.review_id = 13
    review.user_id = 2
    review.product_id = 2
    review.created_at = date(2026, 10, 25)
    review.rating = 5.00
    review.likes = 5
    review.title = "new"
    assert review.review_id == 13
    assert review.user_id == 2
    assert review.product_id == 2
    assert review.created_at == date(2026, 10, 25)
    assert review.rating == 5.00
    assert review.likes == 5
    assert review.title == "new"

def test_review_update_likes():
    review = Review(12, 1, 1, date(2025, 10, 25), 4.89, 0, "title", "body")
    review.update_likes(10)
    assert review.likes == 10