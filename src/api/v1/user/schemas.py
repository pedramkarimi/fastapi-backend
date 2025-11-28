from pydantic import BaseModel, Field, EmailStr
from src.api.v1.user import models
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()


class UsersResponse(BaseModel):
    id : int
    email : str
    # fullname : Fullname


    model_config = {
        "populate_by_name": True,
        "alias_generator": None,
        # "from_attributes" = True  # برای تبدیل خودکار از ORM (SQLAlchemy) به Pydantic
    }


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool


class UserCreate(BaseModel):
    email : EmailStr = Field(..., min_length = 3, max_length = 20)
    password : str = Field(..., min_length = 3)
    first_name : str 
    last_name : str


def to_user_read(user: models.User) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        first_name=user.name,
        last_name=user.family,
        is_active=user.is_active,
    )