import json


# Takes user email, password, and the users.json to check if they exist
# Returns either true or false
def validate_user(uEmail, uPassword, fPath='users.json'):
    try:
        with open(fPath, 'r', encoding='utf-8') as file:
            users = json.load(file)
       
        for user in users:
            if user.get("email") == uEmail and user.get("user_password") == uPassword:
                return True

        return False
   
    except FileNotFoundError:
        print("JSON file not found error")
        return False