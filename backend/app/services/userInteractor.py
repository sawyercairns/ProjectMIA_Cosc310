import json
import os
from pathlib import Path
from backend.app.schemas.userClass import User


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
        path = Path(__file__).resolve().parents[1] / "data" / "users.json"
        tmp_path = path.with_suffix(".tmp")
        with path.open("r", encoding="UTF-8") as f:
            users = json.load(f)
            f.close()
        users.append({
            "user_id": str(int(users[-1]["user_id"]) + 1),
            "user_password": u.user_password,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "age": u.age,
        })
        with tmp_path.open("w", encoding="UTF-8") as t:
            json.dump(users, t, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)


path = Path(__file__).resolve().parents[1] / "data" / "users.json"

def update_password(user_id: str, old_password: str, new_password: str):

    if not os.path.exists(path):
        raise FileNotFoundError("users.json file not found")

    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)

    user = next((u for u in data if u["user_id"] == user_id), None)
    if user is None:
        raise ValueError("User not found")

    if user.get("user_password") != old_password:
        raise ValueError("Existing password does not match")
    
    user["user_password"] = new_password

    temp_path = Path(str(path) + ".tmp")
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)

def update_image_url(user_id: str,image_url: str):

    if not os.path.exists(path):
        raise FileNotFoundError("users.json file not found")

    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)

    user = next((u for u in data if u["user_id"] == user_id), None)
    if user is None:
        raise ValueError("User not found")

    user["image_url"] = image_url

    temp_path = Path(str(path) + ".tmp")
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)