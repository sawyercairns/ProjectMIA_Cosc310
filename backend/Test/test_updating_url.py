
import pytest
from app.services.userInteractor import update_image_url

def test_update_image_url_success(mocker):
    fake_data = [
        {"user_id": "user1", "image_url": "old_url"},
        {"user_id": "user2", "image_url": "another_url"},
    ]

    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = fake_data
    
    mock_write = mocker.patch("app.services.userInteractor.write_to_json")

    update_image_url("user1", "new_url")

    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert updated_data[0]["image_url"] == "new_url"

def test_update_image_url_user_not_found(mocker):
    fake_data = [
        {"user_id": "user1", "image_url": "old_url"},
    ]

    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.return_value = fake_data

    with pytest.raises(ValueError, match="User not found"):
        update_image_url("nonexistent_user", "new_url")

def test_update_image_url_json_file_not_found(mocker):
    mock_load_json = mocker.patch("app.services.userInteractor.load_json")
    mock_load_json.side_effect = FileNotFoundError("JSON file not found error")

    with pytest.raises(FileNotFoundError, match="JSON file not found error"):
        update_image_url("user1", "new_url")

