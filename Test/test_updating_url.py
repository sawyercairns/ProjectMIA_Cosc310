
from backend.app.services.userInteractor import update_image_url

def test_update_image_url_success(monkeypatch):
    fake_data = [
        {"user_id": "user1", "image_url": "old_url"},
        {"user_id": "user2", "image_url": "another_url"},
    ]

    def mock_load_json(file_name):
        return fake_data

    written_data = {}
    def mock_write_to_json(file_name, data):
        nonlocal written_data
        written_data = data

    monkeypatch.setattr("backend.app.services.userInteractor.load_json", mock_load_json)
    monkeypatch.setattr("backend.app.services.userInteractor.write_to_json", mock_write_to_json)

    assert fake_data[0]["image_url"] == "old_url"

    update_image_url("user1", "new_url")

    updated = written_data
    assert updated[0]["image_url"] == "new_url"

def test_update_image_url_user_not_found(monkeypatch):
    fake_data = [
        {"user_id": "user1", "image_url": "old_url"},
    ]

    def mock_load_json(file_name):
        return fake_data

    monkeypatch.setattr("backend.app.services.userInteractor.load_json", mock_load_json)

    try:
        update_image_url("nonexistent_user", "new_url")
    except ValueError as e:
        assert str(e) == "User not found"
    else:
        assert False, "Expected ValueError for user not found"

def test_update_image_url_json_file_not_found(monkeypatch):
    def mock_load_json(file_name):
        return None

    monkeypatch.setattr("backend.app.services.userInteractor.load_json", mock_load_json)

    try:
        update_image_url("user1", "new_url")
    except FileNotFoundError as e:
        assert str(e) == "JSON file not found error"
    else:
        assert False, "Expected FileNotFoundError for missing JSON file"

