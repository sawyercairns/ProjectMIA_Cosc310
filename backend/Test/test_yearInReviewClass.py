import pytest
import decimal
from app.schemas.yearInReviewClass import YearInReview


def test_year_in_review_creation():
    summary = YearInReview(
        user_id=101,
        year=2025,
        total_spent=decimal.Decimal("523.47"),
        total_orders=8,
        avg_order_amount=decimal.Decimal("65.43"),
        items_purchased=15,
        reviews_written=3,
        likes_received=12,
        biggest_order=decimal.Decimal("156.99"),
        orders_returned=1
    )
    
    assert summary.user_id == 101
    assert summary.year == 2025
    assert summary.total_spent == decimal.Decimal("523.47")
    assert summary.total_orders == 8
    assert summary.items_purchased == 15
    assert summary.reviews_written == 3


def test_year_in_review_defaults():
    summary = YearInReview(user_id=102, year=2025)
    
    assert summary.total_spent == decimal.Decimal("0.00")
    assert summary.total_orders == 0
    assert summary.items_purchased == 0
    assert summary.reviews_written == 0


def test_year_in_review_to_dict():
    summary = YearInReview(
        user_id=103,
        year=2025,
        total_spent=decimal.Decimal("100.50"),
        total_orders=2
    )
    
    result = summary.to_dict()
    
    assert result["user_id"] == 103
    assert result["year"] == 2025
    assert result["total_spent"] == "100.50"
    assert result["total_orders"] == 2


def test_invalid_user_id():
    with pytest.raises(ValueError):
        YearInReview(user_id=-1, year=2025)


def test_invalid_year():
    with pytest.raises(ValueError):
        YearInReview(user_id=101, year=1999)
