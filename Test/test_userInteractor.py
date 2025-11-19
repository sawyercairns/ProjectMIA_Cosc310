# Testing validateLogin.py
# Created by: Ethan Wilson
# Reviewed by:


import json
from backend.app.schemas.userClass import User
from backend.app.services.userInteractor import get_user, add_user, remove_user



# Try to login with an invalid user.
def test_fake_user():
    assert get_user("validateLogin@gmail.com", "test") == None


# Check existing user and try to login.
def test_real_user():
    user = get_user("test1@test.com", "test")
    assert user is not None
    assert user.email == "test1@test.com"

def test_add_and_remove():
    user = User(0,"password","email@email.com")
    add_user(user)
    u = get_user("email@email.com", "password")
    assert u is not None
    remove_user(u.user_id)
    u = get_user("email@email.com", "password")
    assert u is None