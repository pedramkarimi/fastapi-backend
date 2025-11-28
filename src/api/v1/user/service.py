from sqlalchemy.orm import Session
from fastapi import Depends
from src.db.session import get_db
from . import models
from .schemas import UserCreate, UsersResponse, UserRead, to_user_read 



from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .repository import UserRepository
from src.core.security import hash_password


class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserRead:
        repo = UserRepository(db)

        # 1) ایمیل تکراری نباشه
        existing = repo.get_user_by_email(user.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists.",
            )

        # 2) hash کردن پسورد
        password_hash = hash_password(user.password)

        # 3) ساخت user در دیتابیس
        user = repo.create(user=user, password_hash=password_hash)

        # 4) تبدیل به schema خروجی
        # return UserRead.model_validate(user)
        return to_user_read(user)

    @staticmethod
    def users(db: Session, skip: int = 0, limit: int = 100) -> list[UserRead]:
        repo = UserRepository(db)
        users = repo.users(skip=skip, limit=limit)
        # return [UserRead.model_validate(u) for u in users]
        return [to_user_read(u) for u in users]