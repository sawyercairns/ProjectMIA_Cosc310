
# Testing userClass.py
# Created by: Ashton Raber
# Reviewed by: 

from backend.app.schemas.userClass import User, InteractUser
import pytest

# Test if a user can be created
def test_User():
    result = User(10, 
                  "test", 
                  "Ashton", 
                  "Raber", 
                  23, 
                  "email@gmail.com")
    assert result.userId == 10
    assert result.userPassword == "test"
    assert result.firstName == "Ashton"
    assert result.lastName == "Raber"
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
def test_age_invalid():
    with pytest.raises(ValueError):
        User(10, 
             "test", 
             "Ashton", 
             "Raber", 
             -1, 
             "email@gmail.com")


# Test getUserId
def test_get_user_id():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    assert interactU.get_user_id() == 10

# Test getFirstName
def test_get_first_name():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    assert interactU.get_first_name() == "Ashton"

# Test getLastName
def test_get_last_name():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    assert interactU.get_last_name() == "Raber"

# Test setting a new password
def test_set_password():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    assert interactU.get_password() == "test"
    interactU.set_password("test2")
    assert interactU.get_password() == "test2"

# Test setAge
def test_set_age():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    assert interactU.get_age() == 23
    interactU.set_age(24)
    assert interactU.get_age() == 24

# Test setAge for a invalid age
def test_set_age_invalid():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    with pytest.raises(ValueError):
        interactU.set_age(-2)

# Test removing an account
def test_remove_account():
    interactU = InteractUser(User(10, 
                                  "test", 
                                  "Ashton", 
                                  "Raber", 
                                  23, 
                                  "email@gmail.com"))
    interactU.remove_user_account()
    assert interactU.user is None