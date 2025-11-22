import json
import os
from pathlib import Path
from app.schemas.userClass import User
from app.services.Interactor import create_item, remove_item, load_json, write_to_json


# Takes user email, password, and the users.json to check if they exist
# Returns either user it finds or null (None)
def get_user(uEmail, uPassword):
    data = load_json(file_name)
           
    for user in data:
        if user.get("email") == uEmail and user.get("user_password") == uPassword:
            return User(int(user["user_id"]),
                        user["user_password"], 
                        user["email"], 
                        user["first_name"], 
                        user["last_name"], 
                        int(user["age"]), 
                        bool(user["is_admin"] if "is_admin" in user else False))

    return None


def authenticate_admin(email: str, password: str) -> User:
    """
    Authenticate user and verify admin privileges.
    Returns User object if valid admin, raises HTTPException otherwise.
    """
    from fastapi import HTTPException
    user = get_user(email, password)
    if user is None or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

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

def find_user_by_id(data, user_id: str):
    """Find and return a user by user_id from the data list"""
    user = None
    for u in data:
        if u["user_id"] == user_id:
            user = u
            break
    if user is None:
        raise ValueError("User not found")
    return user

def update_password(user_id: str, old_password: str, new_password: str):

    data = load_json(file_name)

    user = find_user_by_id(data, user_id)

    if user.get("user_password") != old_password:
        raise ValueError("Existing password does not match")
    
    user["user_password"] = new_password

    write_to_json(file_name, data)


def update_image_url(user_id: str,image_url: str):

    data = load_json(file_name)
    
    user = find_user_by_id(data, user_id)

    user["image_url"] = image_url

    write_to_json(file_name, data)


def add_follow_reviewer(user_id: str, reviewer_id: str):
    """Add a reviewer to the user's follow list"""
    data = load_json(file_name)
    
    user = find_user_by_id(data, user_id)

    #Confirms that the reviewer exists
    find_user_by_id(data, reviewer_id)

    if "follow_reviewers_id" not in user:
        user["follow_reviewers_id"] = []
    
    if reviewer_id not in user["follow_reviewers_id"]:
        user["follow_reviewers_id"].append(reviewer_id)
    
    write_to_json(file_name, data)


def delete_follow_reviewer(user_id: str, reviewer_id: str):
    data = load_json(file_name)
    
    user = find_user_by_id(data, user_id)

    if "follow_reviewers_id" not in user:
        raise ValueError("User has no follow list")

    if reviewer_id in user["follow_reviewers_id"]:
        user["follow_reviewers_id"].remove(reviewer_id)
    else:
        raise ValueError(f"Reviewer {reviewer_id} not found in follow list")
    
    write_to_json(file_name, data)
