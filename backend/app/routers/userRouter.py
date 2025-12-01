from fastapi import APIRouter, HTTPException, Body
from app.schemas.userClass import User
from app.services.userInteractor import get_user, remove_user, add_user, update_password, update_image_url, update_image_url ,add_follow_reviewer, delete_follow_reviewer, authenticate_admin
from app.services.Interactor import load_json

router = APIRouter(prefix="/login", tags=["login"])


#TODO: Probably at some point we will want to change these responses, 
# just remember to change the tests in test_validationRouter if we do
@router.get("", response_model=None)
def user_validation(email:str, password:str):
    user = get_user(email, password)
    if user is not None:
        return "VALID USER"
    else:
        return "INVALID USERNAME OR PASSWORD"
    
# Used by the profile page. And matches email address to current logged in user. 
@router.get("/users", response_model=None)
def get_all_users():
    try:
        users = load_json("users.json")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("{user_id}")
def delete_user(user_id: str, email:str, password: str):
    authenticate_admin(email, password)
    remove_user(user_id)
    return "USER REMOVED"

@router.post("")
def new_user(email:str, password:str, first_name: str = "", last_name:str = "", age: int = 1):
    add_user(User(0, password, email, first_name, last_name, age))
    return "USER ADDED"

@router.post("/admin")
def new_admin(auth_email:str, auth_password:str, email:str, password:str, first_name: str = "", last_name:str = "", age: int = 1):
    authenticate_admin(auth_email, auth_password)
    u = User(0, password, email, first_name, last_name, age, True)
    add_user(u)
    return "ADMIN ADDED"
    
@router.put("/password")
def update_user_password(user_id: str = Body(...),
                        old_password: str = Body(...),
                        new_password: str = Body(...)):
    try:
        update_password(user_id, old_password, new_password)
        return {"message": "Password updated successfully"}

    except ValueError as e:
        raise HTTPException(status_code = 400, detail=str(e))

    except FileNotFoundError as e:
        raise HTTPException(status_code = 500, detail=str(e))
    
@router.put("/image")
def update_user_profile_image(user_id: str = Body(...),
                              image_url: str = Body(...)):
    try:
        update_image_url(user_id, image_url)
        return {"message": "Profile image updated successfully", "image_url": image_url}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
    
@router.post("/follow")
def add_reviewer_to_follow_list(user_id: str = Body(...),
                                reviewer_id: str = Body(...)):
    try:
        add_follow_reviewer(user_id, reviewer_id)
        return {"message": "Reviewer added to follow list successfully", "reviewer_id": reviewer_id}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/follow")
def remove_reviewer_from_follow_list(user_id: str = Body(...),
                                     reviewer_id: str = Body(...)):
    try:
        delete_follow_reviewer(user_id, reviewer_id)
        return {"message": "Reviewer removed from follow list successfully", "reviewer_id": reviewer_id}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
