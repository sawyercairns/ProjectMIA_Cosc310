
# User class based on UML class diagram
# Created by: Ashton Raber
# Reviewed by: 

class User:
    """
    User class just to store data and check if it is valid.
    The getters and setters are also in here with some utility functions
    """
    def __init__(self, 
                 user_id, 
                 user_password,
                first_name, 
                last_name, 
                age, 
                email):
        if not isinstance(user_id, int):
            raise TypeError("userId must be an integer")
        if not isinstance(age, int):
            raise TypeError("age must be an integer")
        if age <= 0:
            raise ValueError("age must be greater than 0")

        self._user_id = user_id
        self._user_password = user_password
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._email = email

    # -- user_id --
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("user_id must be an integer")
        self._user_id = id

    # -- first_name --
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("first_name must be a string")
        self._first_name = new_name
    
    # -- last_name --
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("last_name must be a string")
        self._last_name = new_name


    # -- age --
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, new_age: int):
        if not isinstance(new_age, int):
            raise TypeError("Age must be an integer")
        if new_age <= 0:
            raise ValueError("age must be greater than 0")
        self._age = new_age
    
    # -- user_password --
    @property
    def user_password(self):
        return self._user_password

    @user_password.setter
    def user_password(self, new_password):
        if not isinstance(new_password, str):
            raise TypeError("Password must be a string")
        self._user_password = new_password

    # -- email --
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email: str):
        if not isinstance(new_email, str):
            raise TypeError("email must be a string")
        if "@" not in new_email:
            raise ValueError("email must contain '@'")
        self._email = new_email

    # -- utility
    """
    def remove_user_account(self):
    Need to create the JSON file to delete the user from plus the interactor for it
    """
   

class InteractUser:
    """
    InteractUser class used for parsing user from the JSON file 
    """
