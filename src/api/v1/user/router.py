from fastapi import APIRouter, Depends, status
from .service import UserService, get_user_service
from .schemas import UserResponse, UserCreate, UserUpdate
from .paths import UserPaths
from src.core.response import PaginationResponse, BaseResponse

router = APIRouter()

@router.get(UserPaths.LIST, response_model=PaginationResponse[UserResponse])
def users_list(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
):
    return service.users_list(skip=skip, limit=limit)


@router.post(UserPaths.CREATE, response_model=BaseResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def user_create(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.user_create(user=user)


@router.put(UserPaths.UPDATE, response_model=BaseResponse[UserResponse])
def user_update(user_id: int, user : UserUpdate,  service: UserService = Depends(get_user_service)):
    return service.user_update(user_id= user_id, user = user)


@router.delete(UserPaths.DELETE, response_model=BaseResponse[bool])
def user_delete(user_id : int, service: UserService = Depends(get_user_service)):
    return service.user_delete(user_id = user_id)
    

@router.get(UserPaths.GET_ONE, response_model=BaseResponse[UserResponse])
def get_user_by_id(user_id: int, service: UserService=Depends(get_user_service)):
    return service.get_user_by_id(user_id=user_id)