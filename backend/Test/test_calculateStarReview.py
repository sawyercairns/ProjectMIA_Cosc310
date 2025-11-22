# Uses Mocking to test calculateStarReview.py

import pytest
from app.services.calculateStarReview import calculate_star_review 

def test_calculate_star_review(mocker):
    product_id = 123

    mock_get_reviews = mocker.patch(
        "app.services.calculateStarReview.get_reviews"
    )

    mock_get_reviews.return_value = [
        {"rating": 5},
        {"rating": 4},
        {"rating": 3},
        {"rating": 5},
        {"rating": 4},
    ]

    star_review = calculate_star_review(product_id)

    assert star_review == 4



def test_calculate_star_no_reviews(mocker):
    product_id = 456

    mock_get_reviews = mocker.patch(
        "app.services.calculateStarReview.get_reviews"
    )

    mock_get_reviews.return_value = []

    star_review = calculate_star_review(product_id)

    assert star_review == 0