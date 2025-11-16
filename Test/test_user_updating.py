import json
import pytest
from pathlib import Path
import backend.app.services.userInteractor as interactor

TEST_JSON_PATH = Path(__file__).parent / "test_user.json"

@pytest.fixture(autouse=True)
def setup_test_file(monkeypatch):
    # Initial test data
    initial_data = [
        {"user_id": "101", "user_password": "oldpass", "email": "user1@test.com",
         "first_name": "Alice", "last_name": "", "age": 25},
        {"user_id": "102", "user_password": "mypassword", "email": "user2@test.com",
         "first_name": "Bob", "last_name": "", "age": 30}
    ]

    # Write initial data to test file
    TEST_JSON_PATH.write_text(json.dumps(initial_data))

    # Monkeypatch load_json to read from the test file
    monkeypatch.setattr(
        interactor, 
        "load_json", 
        lambda _: json.loads(TEST_JSON_PATH.read_text())
    )

    # Monkeypatch write_to_json to write to the test file
    def fake_write(_, new_data):
        TEST_JSON_PATH.write_text(json.dumps(new_data))
    monkeypatch.setattr(interactor, "write_to_json", fake_write)

    yield

    # Cleanup after tests
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()


def test_update_password_success():
    interactor.update_password("101", "oldpass", "newpass")
    data = json.loads(TEST_JSON_PATH.read_text())
    user = next(u for u in data if u["user_id"] == "101")
    assert user["user_password"] == "newpass"


def test_update_password_wrong_old():
    with pytest.raises(ValueError, match="Existing password does not match"):
        interactor.update_password("101", "wrongpass", "newpass")


def test_update_password_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        interactor.update_password("999", "oldpass", "newpass")


def test_update_image_url_success():
    interactor.update_image_url("102", "http://example.com/image.png")
    data = json.loads(TEST_JSON_PATH.read_text())
    user = next(u for u in data if u["user_id"] == "102")
    assert user["image_url"] == "http://example.com/image.png"


def test_update_image_url_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        interactor.update_image_url("999", "http://example.com/image.png")
