from fastapi import APIRouter
from .service import UserService
from .schemas import UsersResponse, UserCreate
from .paths import UserPaths

router = APIRouter()

user_service = UserService()

@router.get(UserPaths.LIST, response_model=list[UsersResponse])
def users():
    data = user_service.fetch_all_users()
    return data

@router.post(UserPaths.CREATE)
def create_user(user : UserCreate):
    return user