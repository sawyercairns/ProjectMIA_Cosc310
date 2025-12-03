import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.orderClass import Order
from app.schemas.orderItemClass import OrderItem

client = TestClient(app)


def test_get_year_summary_endpoint(mocker):
    item1 = OrderItem(1, "Test Product", "Description", 2, 50.00)
    
    mock_orders = [
        Order(user_id=101, order_items=[item1], order_date="2025-05-15T10:00:00", order_id=1, returned=False),
    ]
    
    mock_reviews = [
        {"review_id": 1, "user_id": 101, "created_at": "2025-06-10", "likes": 5},
    ]
    
    mocker.patch("app.services.yearInReviewInteractor.load_orders", return_value=mock_orders)
    mocker.patch("app.services.yearInReviewInteractor.get_reviews", return_value=mock_reviews)
    
    response = client.get("/summary/101/year/2025")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == 101
    assert data["year"] == 2025
    assert data["total_spent"] == "100.00"
    assert data["total_orders"] == 1


def test_get_year_summary_no_activity(mocker):
    mocker.patch("app.services.yearInReviewInteractor.load_orders", return_value=[])
    mocker.patch("app.services.yearInReviewInteractor.get_reviews", return_value=[])
    
    response = client.get("/summary/999/year/2025")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == 999
    assert data["total_spent"] == "0.00"
    assert data["total_orders"] == 0


def test_get_year_summary_invalid_year(mocker):
    mocker.patch("app.services.yearInReviewInteractor.load_orders", return_value=[])
    mocker.patch("app.services.yearInReviewInteractor.get_reviews", return_value=[])
    
    response = client.get("/summary/101/year/1999")
    
    assert response.status_code == 400
