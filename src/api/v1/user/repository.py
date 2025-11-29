from typing import Optional, List
from sqlalchemy.orm import Session
from . import models
from .schemas import UserCreate, UserUpdate
from sqlalchemy import select, func


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def users_list(self, skip: int, limit: int) -> List[models.User]:
        return  (
            self.db.query(models.User)
            .order_by(models.User.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def users_count(self) -> int:
        # return self.db.query(func.count(models.User.id)).scalar()
        stmt = select(func.count(models.User.id))
        return self.db.execute(stmt).scalar_one()

    def user_create(self, user: UserCreate, password_hash: str) -> models.User:
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

    def user_update(self, db_user: models.User, fields: dict) -> models.User:        
        if "password" in fields:
            db_user.password = fields["password"]

        if "first_name" in fields:
            db_user.name = fields["first_name"]

        if "last_name" in fields:
            db_user.family = fields["last_name"]

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
        