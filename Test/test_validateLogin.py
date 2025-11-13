# Testing validateLogin.py
# Created by: Ethan Wilson
# Reviewed by:


import json
from backend.app.services.validateLogin import get_user

users_path = "backend/app/data/users.json"


# Try to login with an invalid user.
def test_fake_user():
    assert get_user("validateLogin@gmail.com", "test", users_path) == None


# Check existing user and try to login.
def test_real_user():
    user = get_user("test@test.com", "test", users_path)
    assert user is not None
    assert user["email"] == "test@test.com"