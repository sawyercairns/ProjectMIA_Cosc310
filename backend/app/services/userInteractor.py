import json
import os
from pathlib import Path
from backend.app.schemas.userClass import User
from backend.app.services.Interactor import create_item


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
    path = Path(__file__).resolve().parents[1] / "data" / "users.json"
    tmp_path = path.with_suffix(".tmp")
    with path.open("r", encoding="UTF-8") as f:
        users = json.load(f)
        for u in users:
            if u["user_id"] == str(id):
                users.remove(u)
        f.close()
    with tmp_path.open("w", encoding="UTF-8") as t:
        json.dump(users, t, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)

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
        
            