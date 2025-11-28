from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from .service import UserService
from .schemas import UsersResponse, UserCreate, UserRead
from .paths import UserPaths




router = APIRouter()

user_service = UserService()

# @router.get(UserPaths.LIST, response_model=list[UsersResponse])
# def users():
#     data = user_service.fetch_all_users()
#     return data

@router.get(UserPaths.LIST, response_model=list[UserRead])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return UserService.users(db=db, skip=skip, limit=limit)


@router.post(UserPaths.CREATE, response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db=db, user=user)