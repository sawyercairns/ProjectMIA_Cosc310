
# Testing userClass.py
# Created by: Ashton Raber
# Reviewed by: 

from app.schemas.userClass import User
import pytest

# Test if a user can be created
def test_user():
    result = User(user_id=10, 
                  user_password="test",
                  email="email@gmail.com", 
                  first_name="Ashton", 
                  last_name="Raber", 
                  age=23)
                  
    assert result.user_id == 10
    assert result.user_password == "test"
    assert result.email == "email@gmail.com"
    assert result.first_name == "Ashton"
    assert result.last_name == "Raber"
    assert result.age == 23
   

# Test for a minimal user
def test_minimal_user():
    result = User(user_id=10, 
                  user_password="test",
                  email="email@gmail.com", 
                  )
                  
    assert result.user_id == 10
    assert result.user_password == "test"
    assert result.email == "email@gmail.com"
    assert result.first_name == ""
    assert result.last_name == ""
    assert result.age == 1

# Test to make sure User can not have an age less than 1
def test_age_invalid_1():
    with pytest.raises(ValueError):
        User(10, 
            "test", 
            "email@gmail.com",
            "Ashton", 
            "Raber", 
            -1)
        
def test_age_invalid_2():
    user = User(10, 
            "test", 
            "email@gmail.com",
            "Ashton", 
            "Raber", 
            23)
    assert user.age == 23
    with pytest.raises(ValueError):
        user.age = -1

# Test email
def test_invalid_email():
    with pytest.raises(ValueError):
        user = User(10, 
                    "test", 
                    "emailgmail.com")

def test_email_2():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.email == "email@gmail.com"
    user.email = "emailTwo@gmail.com"
    assert user.email == "emailTwo@gmail.com"
    with pytest.raises(ValueError):
        user.email = "emailgmail.com"

# Testing first_name
def test_first_name():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.first_name == "Ashton"
    user.first_name = "Robert"
    assert user.first_name == "Robert"


# Test last_name
def test_last_name():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.last_name == "Raber"
    user.last_name = "Bassi"
    assert user.last_name == "Bassi"

# Test user_password
def test_user_password():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.user_password == "test"
    user.user_password = "test2"
    assert user.user_password == "test2"

# Test age
def test_age():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.age == 23
    user.age = 24
    assert user.age== 24

def test_admin():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.is_admin == False
    with pytest.raises(AttributeError):
        user.is_admin = True

    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23,
                True)
    assert user.is_admin == True
    with pytest.raises(AttributeError):
        user.is_admin = False

# image url unit testing

def test_image_url_empty():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23)
    assert user.image_url == ""

def test_image_url():
    user = User(10, 
                "test", 
                "email@gmail.com",
                "Ashton", 
                "Raber", 
                23,
                False,
                "http:thisimage.com")
    assert user.image_url == "http:thisimage.com"
    user.image_url = "http:thisimage2.com"
    assert user.image_url == "http:thisimage2.com"

