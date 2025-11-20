import json
import os
from pathlib import Path
from backend.app.schemas.userClass import User
from backend.app.services.Interactor import create_item, remove_item, load_json, write_to_json


# Takes user email, password, and the users.json to check if they exist
# Returns either user it finds or null (None)
def get_user(uEmail, uPassword):
    path = Path(__file__).resolve().parents[1] / "data" / "users.json"
    try:
        with open(path, 'r', encoding='utf-8') as file:
            users = json.load(file)
       
        for user in users:
            if user.get("email") == uEmail and user.get("user_password") == uPassword:
                return User(int(user["user_id"]),
                            user["user_password"], 
                            user["email"], 
                            user["first_name"], 
                            user["last_name"], 
                            int(user["age"]), 
                            bool(user["is_admin"] if "is_admin" in user else False))


        return None
   
    except FileNotFoundError:
        print("JSON file not found error")
        return None

def remove_user(id):
    remove_item("users.json", "user_id", id)

def add_user(u:User):
    if get_user(u.email, u.user_password) is None:
        item = {
            "user_id": str(u.user_id),
            "user_password": u.user_password,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "age": u.age,
        }
        create_item("users.json", "user_id", item)

file_name = "users.json"

def update_password(user_id: str, old_password: str, new_password: str):

    data = load_json(file_name)

    if data == None:
        raise FileNotFoundError("JSON file not found error")

    user = next((u for u in data if u["user_id"] == user_id), None)
    if user is None:
        raise ValueError("User not found")

    if user.get("user_password") != old_password:
        raise ValueError("Existing password does not match")
    
    user["user_password"] = new_password

    write_to_json(file_name, data)


def update_image_url(user_id: str,image_url: str):

    data = load_json(file_name)
    
    if data == None:
        raise FileNotFoundError("JSON file not found error")

    user = next((u for u in data if u["user_id"] == user_id), None)
    if user is None:
        raise ValueError("User not found")

    user["image_url"] = image_url

    write_to_json(file_name, data)