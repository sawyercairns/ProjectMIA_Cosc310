import pytest
import json
from pathlib import Path
from backend.app.schemas.notificationClass import Notification
from backend.app.services import notificationInteractor


class MockNotification(Notification):
    """Mock implementation of abstract Notification class for testing."""
    
    def __init__(self, notification_id: int, user_id: int, message: str = "Test", 
                 product_id: int = None):
        super().__init__(notification_id, user_id, "test")
        self._message = message
        self._product_id = product_id
    
    @property
    def product_id(self):
        return self._product_id
    
    def get_message(self) -> str:
        return self._message
    
    def to_dict(self):
        data = super().to_dict()
        if self._product_id is not None:
            data["product_id"] = self._product_id
        return data


TEST_JSON_PATH = Path(__file__).parent / "test_notifications.json"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test - use test file instead of real one."""
    original_path = notificationInteractor.path
    notificationInteractor.path = TEST_JSON_PATH
    
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()
    
    yield

    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()
    
    notificationInteractor.path = original_path


def test_create_and_retrieve_notifications():
    """Test creating and retrieving notifications for a user."""
    notif1 = MockNotification(1, 101, "First notification")
    notif2 = MockNotification(2, 101, "Second notification")
    
    notificationInteractor.create_notification("101", notif1)
    notificationInteractor.create_notification("101", notif2)
    
    notifications = notificationInteractor.get_user_notifications("101")
    
    assert len(notifications) == 2
    assert notifications[0]["message"] == "First notification"
    assert notifications[1]["message"] == "Second notification"


def test_dismiss_notification():
    """Test dismissing a notification removes it from system."""
    notif1 = MockNotification(1, 101, "Keep this")
    notif2 = MockNotification(2, 101, "Delete this")
    
    notificationInteractor.create_notification("101", notif1)
    notificationInteractor.create_notification("101", notif2)
    
    notificationInteractor.dismiss_notification("101", 2)
    
    notifications = notificationInteractor.get_user_notifications("101")
    assert len(notifications) == 1
    assert notifications[0]["notification_id"] == 1


def test_multiple_users_isolated():
    """Test that notifications are isolated per user."""
    notif_user1 = MockNotification(1, 101, "User 101 notification")
    notif_user2 = MockNotification(1, 102, "User 102 notification")
    
    notificationInteractor.create_notification("101", notif_user1)
    notificationInteractor.create_notification("102", notif_user2)
    
    user1_notifications = notificationInteractor.get_user_notifications("101")
    user2_notifications = notificationInteractor.get_user_notifications("102")
    
    assert len(user1_notifications) == 1
    assert len(user2_notifications) == 1
    assert user1_notifications[0]["message"] == "User 101 notification"
    assert user2_notifications[0]["message"] == "User 102 notification"


def test_notification_id_generation():
    """Test that notification IDs are generated correctly per user."""
    notif1 = MockNotification(1, 101, "First")
    notif2 = MockNotification(2, 101, "Second")
    
    notificationInteractor.create_notification("101", notif1)
    notificationInteractor.create_notification("101", notif2)
    
    notifications = notificationInteractor.get_user_notifications("101")
    assert notifications[0]["notification_id"] == 1
    assert notifications[1]["notification_id"] == 2


def test_json_persistence():
    """Test that notifications persist across operations."""
    notification = MockNotification(1, 101, "Persisted message")
    notificationInteractor.create_notification("101", notification)
    
    with open(TEST_JSON_PATH, "r") as f:
        data = json.load(f)
    
    assert "101" in data
    assert len(data["101"]) == 1
    assert data["101"][0]["message"] == "Persisted message"