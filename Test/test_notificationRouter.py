import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import notificationInteractor
from backend.app.schemas.notificationClass import Notification
from pathlib import Path
import json


class MockNotification(Notification):
    
    def __init__(self, notification_id: int, user_id: int, message: str = "Test"):
        super().__init__(notification_id, user_id, "test")
        self._message = message
    
    def get_message(self) -> str:
        return self._message


TEST_JSON_PATH = Path(__file__).parent / "test_notifications_router.json"
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    original_path = notificationInteractor.path
    notificationInteractor.path = TEST_JSON_PATH
    
    with open(TEST_JSON_PATH, "w") as f:
        json.dump({}, f)
    
    yield
    
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()
    
    notificationInteractor.path = original_path


def test_get_notifications_empty():
    response = client.get("/notifications/999")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_notifications_with_data():
    notif1 = MockNotification(1, 101, "First notification")
    notif2 = MockNotification(2, 101, "Second notification")
    
    notificationInteractor.create_notification("101", notif1)
    notificationInteractor.create_notification("101", notif2)
    
    response = client.get("/notifications/101")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["message"] == "First notification"
    assert data[1]["message"] == "Second notification"


def test_dismiss_notification():
    notification = MockNotification(1, 101, "To be dismissed")
    notificationInteractor.create_notification("101", notification)
    
    response = client.delete("/notifications/101/1")
    
    assert response.status_code == 200
    assert "dismissed successfully" in response.json()["message"]
    
    remaining = notificationInteractor.get_user_notifications("101")
    assert len(remaining) == 0


def test_get_notification_by_id_found():
    notification = MockNotification(5, 101, "Find me")
    notificationInteractor.create_notification("101", notification)
    
    response = client.get("/notifications/101/5")
    
    assert response.status_code == 200
    data = response.json()
    assert data["notification_id"] == 5
    assert data["message"] == "Find me"


def test_get_notification_by_id_not_found():
    response = client.get("/notifications/101/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
