
import pytest
from unittest.mock import patch
from backend.app.services.userInteractor import update_password

@pytest.fixture
def mock_user_data():
    with patch("backend.app.services.userInteractor.load_json") as mock_load, \
         patch("backend.app.services.userInteractor.write_to_json") as mock_write:
        yield mock_load, mock_write

def test_update_password_success(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Fake JSON data returned by load_json
    fake_data = [
        {"user_id": "user1", "user_password": "oldpass"},
        {"user_id": "user2", "user_password": "abc123"},
    ]

    mock_load.return_value = fake_data

    assert fake_data[0]["user_password"] == "oldpass"

    update_password("user1", "oldpass", "newpass")

    mock_load.assert_called_once()

    updated = mock_write.call_args[0][1]
    assert updated[0]["user_password"] == "newpass"

def test_update_wrong_old_password(mock_user_data):
    mock_load, mock_write = mock_user_data
    fake_data = [
        {"user_id": "user1", "user_password": "oldpass"},
    ]
    mock_load.return_value = fake_data

    try:
        update_password("user1", "wrongoldpass", "newpass")
    except ValueError as e:
        assert str(e) == "Existing password does not match"
    else:
        assert False, "Expected ValueError for wrong old password"

def test_update_password_user_not_found(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test when user_id doesn't exist
    fake_data = [
        {"user_id": "user1", "user_password": "oldpass"},
        {"user_id": "user2", "user_password": "abc123"},
    ]
    mock_load.return_value = fake_data

    try:
        update_password("nonexistent_user", "oldpass", "newpass")
        assert False, "Expected ValueError for user not found"
    except ValueError as e:
        assert str(e) == "User not found"
    
    # Ensure write was not called
    mock_write.assert_not_called()

def test_update_password_json_file_not_found(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test when JSON file is not found
    mock_load.return_value = None

    try:
        update_password("user1", "oldpass", "newpass")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as e:
        assert str(e) == "JSON file not found error"
    
    # Ensure write was not called
    mock_write.assert_not_called()

def test_update_password_empty_user_list(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test with empty user list
    mock_load.return_value = []

    try:
        update_password("user1", "oldpass", "newpass")
        assert False, "Expected ValueError for user not found"
    except ValueError as e:
        assert str(e) == "User not found"
    
    mock_write.assert_not_called()

def test_update_password_multiple_users(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test that only the correct user's password is updated
    fake_data = [
        {"user_id": "user1", "user_password": "pass1"},
        {"user_id": "user2", "user_password": "pass2"},
        {"user_id": "user3", "user_password": "pass3"},
    ]
    mock_load.return_value = fake_data

    update_password("user2", "pass2", "newpass2")

    updated = mock_write.call_args[0][1]
    # Check user2's password is updated
    assert updated[1]["user_password"] == "newpass2"
    # Check other users' passwords remain unchanged
    assert updated[0]["user_password"] == "pass1"
    assert updated[2]["user_password"] == "pass3"

def test_update_password_empty_strings(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test with empty password strings
    fake_data = [
        {"user_id": "user1", "user_password": ""},
    ]
    mock_load.return_value = fake_data

    # Should allow updating from empty to new password
    update_password("user1", "", "newpass")

    updated = mock_write.call_args[0][1]
    assert updated[0]["user_password"] == "newpass"

def test_update_password_special_characters(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test with special characters in passwords
    fake_data = [
        {"user_id": "user1", "user_password": "P@ssw0rd!#$%"},
    ]
    mock_load.return_value = fake_data

    new_password = "N3w!P@$$w0rd&*()_+"
    update_password("user1", "P@ssw0rd!#$%", new_password)

    updated = mock_write.call_args[0][1]
    assert updated[0]["user_password"] == new_password

def test_update_password_same_as_old(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test updating password to the same value
    fake_data = [
        {"user_id": "user1", "user_password": "samepass"},
    ]
    mock_load.return_value = fake_data

    update_password("user1", "samepass", "samepass")

    updated = mock_write.call_args[0][1]
    assert updated[0]["user_password"] == "samepass"
    mock_write.assert_called_once()

def test_update_password_case_sensitive(mock_user_data):
    mock_load, mock_write = mock_user_data
    # Test that password comparison is case-sensitive
    fake_data = [
        {"user_id": "user1", "user_password": "Password123"},
    ]
    mock_load.return_value = fake_data

    try:
        update_password("user1", "password123", "newpass")
        assert False, "Expected ValueError for case mismatch"
    except ValueError as e:
        assert str(e) == "Existing password does not match"
    
    mock_write.assert_not_called()