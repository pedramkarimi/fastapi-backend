# src/core/response.py
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None


class PaginationResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]


class ErrorResponse(BaseModel):
    success: bool = False
    code: str
    message: str
