import pytest
from backend.app.services.userInteractor import add_follow_reviewer, delete_follow_reviewer


def test_add_follow_reviewer_success(mocker):
    """Test successfully adding a reviewer to follow list"""
    user_id = "101"
    reviewer_id = "102"
    
    mock_data = [
        {
            "user_id": "101",
            "user_password": "password",
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "One",
            "age": 25
        },
        {
            "user_id": "102",
            "user_password": "password",
            "email": "reviewer@test.com",
            "first_name": "Reviewer",
            "last_name": "Two",
            "age": 30
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")

    add_follow_reviewer(user_id, reviewer_id)
    
    mock_write.assert_called_once()
    
    updated_data = mock_write.call_args[0][1]
    assert "follow_reviewers_id" in updated_data[0]
    assert reviewer_id in updated_data[0]["follow_reviewers_id"]


def test_add_follow_reviewer_user_not_found(mocker):
    """Test adding reviewer fails when user doesn't exist"""
    user_id = "999"
    reviewer_id = "102"
    
    mock_data = [
        {
            "user_id": "102",
            "user_password": "password",
            "email": "reviewer@test.com",
            "first_name": "Reviewer",
            "last_name": "Two",
            "age": 30
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data
   
    with pytest.raises(ValueError, match = "User not found"):
        add_follow_reviewer(user_id, reviewer_id)


def test_add_follow_reviewer_reviewer_not_found(mocker):
    """Test adding reviewer fails when reviewer doesn't exist"""
    user_id = "101"
    reviewer_id = "999"
  
    mock_data = [
        {
            "user_id": "101",
            "user_password": "password",
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "One",
            "age": 25
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data

    with pytest.raises(ValueError, match = "Reviewer with id 999 does not exist"):
        add_follow_reviewer(user_id, reviewer_id)


def test_add_follow_reviewer_no_duplicates(mocker):
    """Test that duplicate reviewers are not added"""
    user_id = "101"
    reviewer_id = "102"
    
    mock_data = [
        {
            "user_id": "101",
            "user_password": "password",
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "One",
            "age": 25,
            "follow_reviewers_id": ["102"]
        },
        {
            "user_id": "102",
            "user_password": "password",
            "email": "reviewer@test.com",
            "first_name": "Reviewer",
            "last_name": "Two",
            "age": 30
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    add_follow_reviewer(user_id, reviewer_id)

    updated_data = mock_write.call_args[0][1]
    assert len(updated_data[0]["follow_reviewers_id"]) == 1


def test_delete_follow_reviewer_success(mocker):
    """Test successfully deleting a reviewer from follow list"""
    user_id = "101"
    reviewer_id = "102"
    
    mock_data = [
        {
            "user_id": "101",
            "user_password": "password",
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "One",
            "age": 25,
            "follow_reviewers_id": ["102", "103"]
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data
    
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    delete_follow_reviewer(user_id, reviewer_id)
    
    mock_write.assert_called_once()
    
    updated_data = mock_write.call_args[0][1]
    assert reviewer_id not in updated_data[0]["follow_reviewers_id"]
    assert "103" in updated_data[0]["follow_reviewers_id"]


def test_delete_follow_reviewer_user_not_found(mocker):
    """Test deleting reviewer fails when user doesn't exist"""
    user_id = "999"
    reviewer_id = "102"
    
    mock_data = []
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data
    
    with pytest.raises(ValueError, match = "User not found"):
        delete_follow_reviewer(user_id, reviewer_id)

def test_delete_follow_reviewer_not_in_list(mocker):
    """Test deleting reviewer fails when reviewer not in follow list"""
    user_id = "101"
    reviewer_id = "999"
    
    mock_data = [
        {
            "user_id": "101",
            "user_password": "password",
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "One",
            "age": 25,
            "follow_reviewers_id": ["102"]
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_load.return_value = mock_data
    
    with pytest.raises(ValueError, match = "Reviewer 999 not found in follow list"):
        delete_follow_reviewer(user_id, reviewer_id)

def test_add_multiple_reviewers(mocker):
    """Test adding multiple reviewers to follow list"""
    user_id = "101"
    
    mock_data = [
        {
            "user_id": "101",
            "user_password": "password",
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "One",
            "age": 25
        },
        {
            "user_id": "102",
            "user_password": "password",
            "email": "reviewer1@test.com",
            "first_name": "Reviewer",
            "last_name": "One",
            "age": 30
        },
        {
            "user_id": "103",
            "user_password": "password",
            "email": "reviewer2@test.com",
            "first_name": "Reviewer",
            "last_name": "Two",
            "age": 35
        }
    ]
    
    mock_load = mocker.patch("backend.app.services.userInteractor.load_json")
    mock_write = mocker.patch("backend.app.services.userInteractor.write_to_json")
    
    mock_load.return_value = mock_data
    add_follow_reviewer(user_id, "102")
    
    mock_data[0]["follow_reviewers_id"] = ["102"]
    
    mock_load.return_value = mock_data
    add_follow_reviewer(user_id, "103")
    
    updated_data = mock_write.call_args[0][1]
    assert "102" in updated_data[0]["follow_reviewers_id"]
    assert "103" in updated_data[0]["follow_reviewers_id"]
