from fastapi import APIRouter
from backend.app.services.userInteractor import get_user, remove_user

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

@router.delete("{user_id}")
def delete_user(user_id: str, email:str, password: str):
    user = get_user(email, password)
    if user is not None and user.is_admin:
        remove_user(user_id)
        return "USER REMOVED"
    else:
        return "REMOVAL FAILED"