from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_update_password_success(mocker):
    """Test successful password update"""
    user_id = "123"
    old_password = "oldpassword123"
    new_password = "newpassword456"

    mock_users = [
        {
            "user_id": user_id,
            "user_password": old_password,
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/password",
        json={
            "user_id": user_id,
            "old_password": old_password,
            "new_password": new_password
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully"}
    
    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert updated_data[0]["user_password"] == new_password


def test_update_password_user_not_found(mocker):
    """Test password update fails when user doesn't exist"""
    mock_users = [
        {
            "user_id": "123",
            "user_password": "somepass",
            "email": "other@test.com",
            "first_name": "Other",
            "last_name": "User",
            "age": 30
        }
    ]
    
    mock_load_json = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    response = client.put(
        "/login/password",
        json={
            "user_id": "999999",
            "old_password": "somepassword",
            "new_password": "newpassword"
        }
    )
    
    assert response.status_code == 400
    assert "User not found" in response.json()["detail"]


def test_update_password_incorrect_old_password(mocker):
    """Test password update fails when old password is incorrect"""
    user_id = "123"
    correct_password = "correctpass123"
    
    mock_users = [
        {
            "user_id": user_id,
            "user_password": correct_password,
            "email": "wrongpass@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/password",
        json={
            "user_id": user_id,
            "old_password": "wrongoldpassword",
            "new_password": "newpassword456"
        }
    )
    
    assert response.status_code == 400
    assert "Existing password does not match" in response.json()["detail"]
    
    mock_write.assert_not_called()


def test_update_password_file_not_found(mocker):
    """Test password update handles file not found error"""
    mock_load_json = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load_json.return_value = None
    
    response = client.put(
        "/login/password",
        json={
            "user_id": "123",
            "old_password": "oldpass",
            "new_password": "newpass"
        }
    )
    
    assert response.status_code == 500
    assert "JSON file not found error" in response.json()["detail"]


def test_update_password_same_password(mocker):
    """Test updating password to the same value"""
    user_id = "123"
    password = "samepassword123"
    
    mock_users = [
        {
            "user_id": user_id,
            "user_password": password,
            "email": "samepass@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/password",
        json={
            "user_id": user_id,
            "old_password": password,
            "new_password": password
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully"}
    
    mock_write.assert_called_once()


def test_update_password_special_characters(mocker):
    """Test password update with special characters in password"""
    user_id = "123"
    old_password = "old!@#$%^&*()"
    new_password = "new!@#$%^&*()_+{}:|<>?"
    
    mock_users = [
        {
            "user_id": user_id,
            "user_password": old_password,
            "email": "specialchars@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/password",
        json={
            "user_id": user_id,
            "old_password": old_password,
            "new_password": new_password
        }
    )
    
    assert response.status_code == 200
    
    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert updated_data[0]["user_password"] == new_password



