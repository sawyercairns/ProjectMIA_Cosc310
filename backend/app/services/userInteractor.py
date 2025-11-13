import json
import os
from pathlib import Path


# Takes user email, password, and the users.json to check if they exist
# Returns either user it finds or null (None)
def get_user(uEmail, uPassword, fPath='users.json'):
    try:
        with open(fPath, 'r', encoding='utf-8') as file:
            users = json.load(file)
       
        for user in users:
            if user.get("email") == uEmail and user.get("user_password") == uPassword:
                return user


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