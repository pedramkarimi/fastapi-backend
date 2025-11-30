from fastapi import APIRouter, Depends
from .paths import AuthPaths
from .service import AuthService, get_auth_service
from .schemas import LoginRequest, TokenResponse, AuthenticatedUser
from src.core.response import BaseResponse
from src.api.v1.user.schemas import UserResponse
from .deps import get_current_user_data
from src.api.v1.user import models as user_models
from .guards import AuthGuard

router = APIRouter()

@router.get(AuthPaths.ME, response_model=BaseResponse[AuthenticatedUser])
def read_me(user : AuthenticatedUser = AuthGuard()):
    return BaseResponse[AuthenticatedUser](data=user)


@router.post(AuthPaths.LOGIN, response_model=BaseResponse[TokenResponse])
def login(credentials: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(credentials=credentials)