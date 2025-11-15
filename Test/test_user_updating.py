import json
import pytest
from pathlib import Path

import backend.app.services.userInteractor as interactor

TEST_JSON_PATH = Path(__file__).parent / "test_user.json"
interactor.path = TEST_JSON_PATH  

@pytest.fixture(autouse=True)
def cleanup():
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()
    TEST_JSON_PATH.write_text(json.dumps([
        {
            "user_id": "101",
            "user_password": "oldpass",
            "email": "user1@test.com",
            "first_name": "Alice",
            "last_name": "",
            "age": 25
        },
        {
            "user_id": "102",
            "user_password": "mypassword",
            "email": "user2@test.com",
            "first_name": "Bob",
            "last_name": "",
            "age": 30
        }
    ]))
    yield
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()


def test_update_password_success():
    interactor.update_password("101", "oldpass", "newpass")

    with open(TEST_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

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

    with open(TEST_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    user = next(u for u in data if u["user_id"] == "102")
    assert user["image_url"] == "http://example.com/image.png"


def test_update_image_url_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        interactor.update_image_url("999", "http://example.com/image.png")