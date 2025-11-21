import pytest
from backend.app.schemas.wishlistNotificationClass import WishlistNotification


def test_wishlist_notification_creation():
    notification = WishlistNotification(
        notification_id=1,
        user_id=101,
        product_id=5,
        product_name="USB Cable",
        old_price=20.00,
        new_price=15.00
    )
    
    assert notification.notification_id == 1
    assert notification.user_id == 101
    assert notification.notification_type == "wishlist_discount"
    assert notification.product_id == 5
    assert notification.product_name == "USB Cable"
    assert notification.old_price == 20.00
    assert notification.new_price == 15.00
    assert notification.discount_percent == 25.0


def test_wishlist_notification_message():
    notification = WishlistNotification(
        notification_id=2,
        user_id=102,
        product_id=10,
        product_name="Wireless Mouse",
        old_price=50.00,
        new_price=35.00
    )
    
    message = notification.get_message()
    
    assert "Wireless Mouse" in message
    assert "$35.00" in message
    assert "$50.00" in message
    assert "30.0%" in message


def test_wishlist_notification_to_dict():
    notification = WishlistNotification(
        notification_id=3,
        user_id=103,
        product_id=15,
        product_name="Keyboard",
        old_price=100.00,
        new_price=80.00
    )
    
    data = notification.to_dict()
    
    assert data["notification_id"] == 3
    assert data["user_id"] == 103
    assert data["notification_type"] == "wishlist_discount"
    assert data["product_id"] == 15
    assert data["product_name"] == "Keyboard"
    assert data["old_price"] == 100.00
    assert data["new_price"] == 80.00
    assert data["discount_percent"] == 20.0
    assert "message" in data
