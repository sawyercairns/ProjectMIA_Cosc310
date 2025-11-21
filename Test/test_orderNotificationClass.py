import pytest
from backend.app.schemas.orderNotificationClass import OrderNotification


def test_order_notification_creation():
    notification = OrderNotification(
        notification_id=1,
        user_id=101,
        order_id=5,
        total_price=125.50,
        item_count=3
    )
    
    assert notification.notification_id == 1
    assert notification.user_id == 101
    assert notification.notification_type == "order_complete"
    assert notification.order_id == 5
    assert notification.total_price == 125.50
    assert notification.item_count == 3


def test_order_notification_message_singular():
    notification = OrderNotification(
        notification_id=2,
        user_id=102,
        order_id=10,
        total_price=29.99,
        item_count=1
    )
    
    message = notification.get_message()
    
    assert "Order #10" in message
    assert "$29.99" in message
    assert "1 item" in message
    assert "items" not in message or "1 item" in message


def test_order_notification_message_plural():
    notification = OrderNotification(
        notification_id=3,
        user_id=103,
        order_id=15,
        total_price=200.00,
        item_count=5
    )
    
    message = notification.get_message()
    
    assert "Order #15" in message
    assert "$200.00" in message
    assert "5 items" in message


def test_order_notification_to_dict():
    notification = OrderNotification(
        notification_id=4,
        user_id=104,
        order_id=20,
        total_price=75.25,
        item_count=2
    )
    
    data = notification.to_dict()
    
    assert data["notification_id"] == 4
    assert data["user_id"] == 104
    assert data["notification_type"] == "order_complete"
    assert data["order_id"] == 20
    assert data["total_price"] == 75.25
    assert data["item_count"] == 2
    assert "message" in data
