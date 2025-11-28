# src/api/v1/user/repository.py
from typing import Optional, List

from sqlalchemy.orm import Session
from . import models
from .schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def users(self, skip: int = 0, limit: int = 100) -> List[models.User]:
        return (
            self.db.query(models.User)
            .order_by(models.User.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, user: UserCreate, password_hash: str) -> models.User:
        db_user = models.User(
            email=user.email,
            password=password_hash,
            name=user.first_name,
            family=user.last_name,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
