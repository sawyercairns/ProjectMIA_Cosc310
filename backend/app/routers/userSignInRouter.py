from fastapi import APIRouter
from backend.app.services.userValidation import user_is_valid

router = APIRouter(prefix="/login", tags=["login"])

#TODO: Probably at some point we will want to change these responses, 
# just remember to change the tests in test_validationRouter if we do
@router.get("{user_name}", response_model=None)
def user_validation(user_name:str, password:str):
    if user_is_valid(user_name, password):
        return "VALID USER"
    else:
        return "INVALID USERNAME OR PASSWORD"