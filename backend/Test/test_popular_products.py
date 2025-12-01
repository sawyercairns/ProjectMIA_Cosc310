from app.schemas.orderItemClass import OrderItem
from datetime import datetime, timedelta
import pytest
from app.services.popularProducts import get_popular_products


def test_get_popular_products(mocker):
    fake_orders = {"1": {
                        "user_id": 1, 
                        "order_items": [OrderItem(0, "This order should be filtered out by date", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now() - timedelta(weeks = 2),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                        },
                    "2": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 1", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    },
                    "3": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 1", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    },
                    "4": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 1", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    },
                    "5": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 2", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    },
                    "6": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 2", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    },
                    "7": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 3", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    },
                    "8": {
                        "user_id": 2, 
                        "order_items": [OrderItem(0, "Number 4(should not appear)", "desc", 1)],
                        "address": "address",
                        "order_date": datetime.now(),
                        "order_id": "0",
                        "returned": False,
                        "is_gift": False,
                        "gifter_id": None
                    }
                }
    

    mock = mocker.patch("app.services.popularProducts.get_orders_all")
    mock.return_value = fake_orders
    popular_products = get_popular_products()
    assert popular_products[0] == ("Number 1", 3)
    assert popular_products[1] == ("Number 2", 2)
    assert popular_products[2] == ("Number 3", 1)
    assert "Number 4(should not appear)" not in popular_products
    assert "This order should be filtered out by date" not in popular_products
