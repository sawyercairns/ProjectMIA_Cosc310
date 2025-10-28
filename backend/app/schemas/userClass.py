
# User class based on UML class diagram
# Created by: Ashton Raber
# Reviewed by: 

class User:
    """
    User class just to store data and check if it is valid.
    The getters and setters are also in here with some utility functions
    """
    def __init__(self, 
                user_id: int, 
                user_password: str,
                email: str,
                first_name: str = "",
                last_name: str = "",
                age: int = 1):
        
        self._user_id = user_id
        self.user_password = user_password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age 

    # -- user_id --
    @property
    def user_id(self):
        return self._user_id
    
    # -- first_name --
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, new_name: str):
        self._first_name = new_name
    
    # -- last_name --
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, new_name: str):
        self._last_name = new_name

    # -- age --
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, new_age: int):
        if new_age <= 0:
            raise ValueError("age must be greater than 0")
        self._age = new_age
    
    # -- user_password --
    @property
    def user_password(self):
        return self._user_password

    @user_password.setter
    def user_password(self, new_password: str):
        self._user_password = new_password

    # -- email --
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email: str):
        if "@" not in new_email:
            raise ValueError("email must contain '@'")
        self._email = new_email

    # -- utility
    """
    def remove_user_account(self):
    Need to create the JSON file to delete the user from plus the interactor for it
    """
