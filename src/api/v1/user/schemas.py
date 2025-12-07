from pydantic import BaseModel, Field, EmailStr
from src.api.v1.user import models
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool


class UserCreate(BaseModel):
    email : EmailStr = Field(..., min_length = 3, max_length = 50)
    password : str = Field(..., min_length = 3)
    first_name : str 
    last_name : str


def to_user_response(user: models.User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.name,
        last_name=user.family,
        is_active=user.is_active,
    )

class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=3)
    first_name: Optional[str] = None
    last_name: Optional[str] = None