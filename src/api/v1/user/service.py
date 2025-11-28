from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from .schemas import UserCreate, UserResponse, to_user_response 
from .repository import UserRepository
from src.core.security import Security
from src.core.errors import ErrorMessages


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)


    def create_user(self, user: UserCreate) -> UserResponse:

        email_existing = self.user_repo.get_user_by_email(user.email)
        if email_existing:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.USER_EMAIL_EXISTS,
            )

        password_hash = Security.hash_password(user.password)

        user = self.user_repo.create(user=user, password_hash=password_hash)

        return to_user_response(user)

    def users(self, skip: int, limit: int) -> list[UserResponse]:
        users = self.user_repo.users(skip=skip, limit=limit)

        return [to_user_response(u) for u in users]
    

def get_user_service(db: Session = Depends(get_db)) -> UserService:
        return UserService(db)