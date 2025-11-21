from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_update_profile_image_success(mocker):
    """Test successful profile image URL update"""
    user_id = "123"
    image_url = "https://example.com/profile.jpg"
    
    mock_users = [
        {
            "user_id": user_id,
            "user_password": "password123",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/image",
        json={
            "user_id": user_id,
            "image_url": image_url
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "Profile image updated successfully",
        "image_url": image_url
    }
    
    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert updated_data[0]["image_url"] == image_url


def test_update_profile_image_user_not_found(mocker):
    """Test profile image update fails when user doesn't exist"""
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
    
    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    response = client.put(
        "/login/image",
        json={
            "user_id": "999999", 
            "image_url": "https://example.com/profile.jpg"
        }
    )
    
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_update_profile_image_file_not_found(mocker):
    """Test profile image update handles file not found error"""
    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = None
    
    response = client.put(
        "/login/image",
        json={
            "user_id": "123",
            "image_url": "https://example.com/profile.jpg"
        }
    )
    
    assert response.status_code == 500
    assert "JSON file not found error" in response.json()["detail"]


def test_update_profile_image_empty_url(mocker):
    """Test profile image update with empty URL string"""
    user_id = "123"
    image_url = ""
    
    mock_users = [
        {
            "user_id": user_id,
            "user_password": "password123",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/image",
        json={
            "user_id": user_id,
            "image_url": image_url
        }
    )
    
    assert response.status_code == 200
    
    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert updated_data[0]["image_url"] == ""



def test_update_profile_image_special_characters(mocker):
    """Test profile image update with special characters in URL"""
    user_id = "123"
    image_url = "https://example.com/profile?user=test&size=large#avatar"
    
    mock_users = [
        {
            "user_id": user_id,
            "user_password": "password123",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "age": 25
        }
    ]
    
    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = mock_users
    
    mock_write = mocker.patch("app.services.userInteractor.write_to_json")
    
    response = client.put(
        "/login/image",
        json={
            "user_id": user_id,
            "image_url": image_url
        }
    )
    
    assert response.status_code == 200
    
    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert updated_data[0]["image_url"] == image_url


def test_update_profile_image_different_protocols(mocker):
    """Test profile image update with different URL protocols"""
    user_id = "123"
    test_urls = [
        "http://example.com/profile.jpg",
        "https://example.com/profile.jpg",
    ]
    
    for image_url in test_urls:
        mock_users = [
            {
                "user_id": user_id,
                "user_password": "password123",
                "email": "test@test.com",
                "first_name": "Test",
                "last_name": "User",
                "age": 25
            }
        ]
        
        mock_load_json = mocker.patch("app.services.userInteractor.load_json")
        mock_load_json.return_value = mock_users
        
        mock_write = mocker.patch("app.services.userInteractor.write_to_json")
        
        response = client.put(
            "/login/image",
            json={
                "user_id": user_id,
                "image_url": image_url
            }
        )
        
        mock_write.assert_called_once()
        assert response.status_code == 200
        assert response.json()["image_url"] == image_url
