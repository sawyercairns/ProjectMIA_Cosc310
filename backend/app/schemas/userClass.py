
# User class based on UML class diagram
# Created by: Ashton Raber
# Reviewed by: 

class User:
    """
    User class just to store data and check if it is valid.
    """
    def __init__(self, 
                 userId, 
                 userPassword,
                firstName, 
                lastName, 
                age, 
                email):
        if not isinstance(userId, int):
            raise TypeError("userId must be an integer")
        if not isinstance(age, int):
            raise TypeError("age must be an integer")
        if age <= 0:
            raise ValueError("age must be greater than 0")

        self.userId = userId
        self.userPassword = userPassword
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.email = email


class InteractUser:
    """
    interactUser class used to get and set variables of a user.
    Also can remove a user account.
    """
    def __init__(self, user: User):
        self.user = user


    def get_user_id(self):
        return self.user.userId

    def get_first_name(self):
        return self.user.firstName
    
    def get_last_name(self):
        return self.user.lastName
    
    def get_age(self):
        return self.user.age
    
    def get_password(self):
        return self.user.userPassword

    def set_password(self, newPassword):
        if not isinstance(newPassword, str):
            raise TypeError("Password must be a string")
        self.user.userPassword = newPassword

    def set_age(self, newAge):
        if not isinstance(newAge, int):
            raise TypeError("Age must be an integer")
        if newAge <= 0:
            raise ValueError("age must be greater than 0")
        self.user.age = newAge

    def remove_user_account(self):
        if self.user is None:
            # Checks if the user is already deleted
            return
        # Would need to remove the user from the json file
        self.user = None

    """ Need to make a user json file 
    def get_user(self, userId) -> User:
        Look through the user json file

        raise ValueError(f"User with ID {userId} not found")
    
    """

    """
    Note: I would assume we would also have a userBrowse function since users can browse products?
    def user_browse():
    """