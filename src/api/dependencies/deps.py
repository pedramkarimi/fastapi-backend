# src/api/v1/auth/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.core.security import Security
from src.api.v1.user.repository import UserRepository
from src.api.v1.user import models as user_models
from jose import JWTError
from src.core.errors import ErrorMessages
from src.core.exceptions import InvalidCredentialsException, NotFoundException, PermissionDeniedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  

def get_current_user_data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> user_models.User:
    try:
        token_data = Security.decode_access_token(token)
        sub = token_data.get("sub")
    except JWTError:
        raise InvalidCredentialsException(ErrorMessages.INVALID_CREDENTIALS)

    repo = UserRepository(db)
    user = repo.get_user_by_id(int(sub))

    if user is None:
        raise NotFoundException(ErrorMessages.USER_NOT_FOUND)
    
    if not user.is_active:
        raise PermissionDeniedException(ErrorMessages.USER_IS_INACTIVE)

    return user