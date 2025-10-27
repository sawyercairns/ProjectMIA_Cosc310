
# Testing userClass.py
# Created by: Ashton Raber
# Reviewed by: 

from backend.app.schemas.userClass import User
import pytest

# Test if a user can be created
def test_User():
    result = User(10, 
                  "test", 
                  "Ashton", 
                  "Raber", 
                  23, 
                  "email@gmail.com")
    assert result.user_id == 10
    assert result.user_password == "test"
    assert result.first_name == "Ashton"
    assert result.last_name == "Raber"
    assert result.age == 23
    assert result.email == "email@gmail.com"


# Test to make sure the age is a int
def test_age_int():
    with pytest.raises(TypeError):
        User(10, 
             "test", 
             "Ashton", 
             "Raber", 
             "23", 
             "email@gmail.com")

# Test to make sure the userId is a int
def test_user_id_int():
    with pytest.raises(TypeError):
        User("10", 
             "test", 
             "Ashton", 
             "Raber", 
             23, 
             "email@gmail.com")

# Test to make sure User can not have a age less than 1
def test_age_invalid_1():
    with pytest.raises(ValueError):
        User(10, 
             "test", 
             "Ashton", 
             "Raber", 
             -1, 
             "email@gmail.com")


# Testing user_id
def test_user_id():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    assert user.user_id == 10
    # Setter 
    user.user_id = 12
    assert user.user_id == 12



# Testing first_name
def test_first_name():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    assert user.first_name == "Ashton"
    # Setter
    user.first_name = "Dan"
    assert user.first_name == "Dan"


# Test last_name
def test_last_name():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    assert user.last_name == "Raber"
    # Setter
    user.last_name = "Bassi"
    assert user.last_name == "Bassi"

# Test user_password
def test_user_password():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    assert user.user_password == "test"
    # Setter
    user.user_password = "test2"
    assert user.user_password == "test2"

# Test age
def test_age():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    assert user.age == 23
    # Setter
    user.age = 24
    assert user.age== 24

# Test email
def test_email():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    assert user.email == "email@gmail.com"
    # Setter
    user.email = "emailTwo@gmail.com"
    assert user.email == "emailTwo@gmail.com"
    # Invalid Email
    with pytest.raises(ValueError):
        user.email = "emailgmail.com"

# Test age for a invalid age
def test_age_invalid_2():
    user = User(10, 
                "test", 
                "Ashton", 
                "Raber", 
                23, 
                "email@gmail.com")
    with pytest.raises(ValueError):
        user.age = -2
