from app.schemas.orderItemClass import OrderItem
from datetime import datetime, timedelta
import pytest
from app.services.popularProducts import get_popular_products


def test_get_popular_products(mocker):
    fake_orders = {
        "1": [
            {
                "user_id": 1, 
                "order_items": [{"product_name": "This order should be filtered out by date"}],
                "address": "address",
                "order_date": (datetime.now() - timedelta(weeks=2)).isoformat(),
                "order_id": "0",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            }
        ],
        "2": [
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 1"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "1",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            },
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 1"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "2",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            },
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 1"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "3",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            },
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 2"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "4",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            },
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 2"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "5",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            },
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 3"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "6",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            },
            {
                "user_id": 2, 
                "order_items": [{"product_name": "Number 4(should not appear)"}],
                "address": "address",
                "order_date": datetime.now().isoformat(),
                "order_id": "7",
                "returned": False,
                "is_gift": False,
                "gifter_id": None
            }
        ]
    }
    

    mock = mocker.patch("app.services.popularProducts.get_orders_all")
    mock.return_value = fake_orders
    popular_products = get_popular_products()
    assert popular_products[0] == ("Number 1", 3)
    assert popular_products[1] == ("Number 2", 2)
    assert popular_products[2] == ("Number 3", 1)
    assert "Number 4(should not appear)" not in popular_products
    assert "This order should be filtered out by date" not in popular_products
