from fastapi import APIRouter, Depends, status
from .service import UserService, get_user_service
from .schemas import UserResponse, UserCreate
from .paths import UserPaths

router = APIRouter()

@router.get(UserPaths.LIST, response_model=list[UserResponse])
def users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
):
    return service.users(skip=skip, limit=limit)


@router.post(UserPaths.CREATE, response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user=user)