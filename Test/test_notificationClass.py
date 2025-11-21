import pytest
from datetime import datetime
from backend.app.schemas.notificationClass import Notification


class MockNotification(Notification):
    """Concrete implementation for testing abstract Notification class."""
    
    def __init__(self, notification_id: int, user_id: int, message: str = "Test message", 
                 product_id: int = None, metadata: dict = None):
        super().__init__(notification_id, user_id, "test")
        self._message = message
        self._product_id = product_id
        self._metadata = metadata or {}
    
    @property
    def product_id(self):
        return self._product_id
    
    def get_message(self) -> str:
        return self._message
    
    def to_dict(self):
        data = super().to_dict()
        if self._product_id is not None:
            data["product_id"] = self._product_id
        if self._metadata:
            data.update(self._metadata)
        return data


def test_notification_creation():
    """Test basic notification creation with all properties."""
    notification = MockNotification(
        notification_id=1,
        user_id=101,
        message="Test notification",
        product_id=123,
        metadata={"key": "value"}
    )
    
    assert notification.notification_id == 1
    assert notification.user_id == 101
    assert notification.notification_type == "test"
    assert notification.get_message() == "Test notification"
    assert notification.product_id == 123
    assert notification.created_at is not None


def test_notification_to_dict():
    """Test notification serialization to dictionary."""
    notification = MockNotification(
        notification_id=5,
        user_id=202,
        message="Serialization test",
        product_id=123,
        metadata={"extra_field": "extra_value"}
    )
    
    result = notification.to_dict()
    
    assert result["notification_id"] == 5
    assert result["user_id"] == 202
    assert result["notification_type"] == "test"
    assert result["message"] == "Serialization test"
    assert result["product_id"] == 123
    assert result["extra_field"] == "extra_value"
    assert "created_at" in result


def test_notification_properties_are_read_only():
    """Test that notification properties cannot be modified after creation."""
    notification = MockNotification(1, 101)
    
    with pytest.raises(AttributeError):
        notification.notification_id = 999
    
    with pytest.raises(AttributeError):
        notification.user_id = 999
    
    with pytest.raises(AttributeError):
        notification.notification_type = "modified"


def test_notification_abstract_methods_required():
    """Test that abstract methods must be implemented by subclasses."""
    with pytest.raises(TypeError):
        class IncompleteNotification(Notification):
            pass
        
        IncompleteNotification(1, 101, "incomplete")