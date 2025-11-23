from fastapi import APIRouter
from services import user_service
from schemas import user_schema

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_service = user_service.UserService

@router.get("/list", response_model=list[user_schema.UsersResponse])
def users():
    data = user_service.fetch_all_users()
    return data