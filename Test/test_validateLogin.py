# Testing validateLogin.py
# Created by: Ethan Wilson
# Reviewed by:

import pytest
import json
from backend.app.schemas.userClass import User
from backend.app.schemas.validateLogin import validate_user

users_path = "../backend/app/data/users.json"

# Try to login with an invalid user.
def test_fake_user():
    assert validate_user("validateLogin@gmail.com", "test", users_path) == False

# Check existing user and try to login.
def test_real_user():
    assert validate_user("test@test.com", "test", users_path) == True