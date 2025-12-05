import pytest
from app.schemas.wishlistDiscountNotificationClass import WishlistDiscountNotification


def test_wishlist_discount_notification_creation():
    """Test creating a wishlist discount notification."""
    notification = WishlistDiscountNotification(
        notification_id=1,
        user_id=101,
        product_id=5,
        product_name="Test Product",
        old_price=100.00,
        new_price=75.00
    )
    
    assert notification.notification_id == 1
    assert notification.user_id == 101
    assert notification.product_id == 5
    assert notification.product_name == "Test Product"
    assert notification.old_price == 100.00
    assert notification.new_price == 75.00
    assert notification.notification_type == "wishlist_discount"


def test_wishlist_discount_notification_message():
    """Test the notification message is formatted correctly."""
    notification = WishlistDiscountNotification(
        notification_id=1,
        user_id=101,
        product_id=5,
        product_name="Cool Gadget",
        old_price=100.00,
        new_price=75.00
    )
    
    message = notification.get_message()
    assert "Cool Gadget" in message
    assert "$100.00" in message
    assert "$75.00" in message
    assert "25%" in message


def test_wishlist_discount_notification_discount_percent():
    """Test discount percentage calculation."""
    notification = WishlistDiscountNotification(
        notification_id=1,
        user_id=101,
        product_id=5,
        product_name="Test",
        old_price=200.00,
        new_price=150.00
    )
    
    assert notification.discount_percent == 25


def test_wishlist_discount_notification_to_dict():
    """Test serialization to dict."""
    notification = WishlistDiscountNotification(
        notification_id=1,
        user_id=101,
        product_id=5,
        product_name="Test Product",
        old_price=100.00,
        new_price=80.00
    )
    
    data = notification.to_dict()
    
    assert data["notification_id"] == 1
    assert data["user_id"] == 101
    assert data["notification_type"] == "wishlist_discount"
    assert data["product_id"] == 5
    assert data["product_name"] == "Test Product"
    assert data["old_price"] == 100.00
    assert data["new_price"] == 80.00
    assert data["discount_percent"] == 20
    assert "message" in data
