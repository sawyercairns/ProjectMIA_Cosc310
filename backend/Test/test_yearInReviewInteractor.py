import pytest
import decimal
from app.schemas.orderClass import Order
from app.schemas.orderItemClass import OrderItem
from app.services.yearInReviewInteractor import (
    get_year_in_review,
    _filter_orders_by_year,
    _calculate_total_spent,
    _calculate_items_purchased,
    _find_biggest_order
)


def test_filter_orders_by_year():
    item = OrderItem(1, "Product", "Desc", 1, 10.00)
    
    orders = [
        Order(user_id=101, order_items=[item], order_date="2025-01-15T10:00:00", order_id=1),
        Order(user_id=101, order_items=[item], order_date="2025-06-20T14:30:00", order_id=2),
        Order(user_id=101, order_items=[item], order_date="2024-12-25T09:00:00", order_id=3),
    ]
    
    result_2025 = _filter_orders_by_year(orders, 2025)
    assert len(result_2025) == 2
    
    result_2024 = _filter_orders_by_year(orders, 2024)
    assert len(result_2024) == 1


def test_calculate_total_spent():
    item1 = OrderItem(1, "Product 1", "Desc", 2, 10.00)
    item2 = OrderItem(2, "Product 2", "Desc", 1, 25.50)
    
    orders = [
        Order(user_id=101, order_items=[item1], order_id=1),
        Order(user_id=101, order_items=[item2], order_id=2),
    ]
    
    result = _calculate_total_spent(orders)
    assert result == decimal.Decimal("45.50")


def test_calculate_items_purchased():
    item1 = OrderItem(1, "Product 1", "Desc", 3, 10.00)
    item2 = OrderItem(2, "Product 2", "Desc", 2, 15.00)
    
    orders = [
        Order(user_id=101, order_items=[item1, item2], order_id=1),
    ]
    
    result = _calculate_items_purchased(orders)
    assert result == 5


def test_find_biggest_order():
    item1 = OrderItem(1, "Product 1", "Desc", 1, 50.00)
    item2 = OrderItem(2, "Product 2", "Desc", 2, 100.00)
    
    orders = [
        Order(user_id=101, order_items=[item1], order_id=1),
        Order(user_id=101, order_items=[item2], order_id=2),
    ]
    
    result = _find_biggest_order(orders)
    assert result == decimal.Decimal("200.00")


def test_get_year_in_review_integration(mocker):
    item1 = OrderItem(1, "Product 1", "Desc", 2, 25.00)
    
    mock_orders = [
        Order(user_id=101, order_items=[item1], order_date="2025-03-15T10:00:00", order_id=1, returned=False),
    ]
    
    mock_reviews = [
        {"review_id": 1, "user_id": 101, "created_at": "2025-04-10", "likes": 7},
    ]
    
    mocker.patch("app.services.yearInReviewInteractor.load_orders", return_value=mock_orders)
    mocker.patch("app.services.yearInReviewInteractor.get_reviews", return_value=mock_reviews)
    
    result = get_year_in_review("101", 2025)
    
    assert result.user_id == 101
    assert result.year == 2025
    assert result.total_spent == decimal.Decimal("50.00")
    assert result.total_orders == 1
    assert result.reviews_written == 1
    assert result.likes_received == 7
