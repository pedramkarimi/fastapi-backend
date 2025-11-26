from fastapi import APIRouter
from .user.router import router as user_router
from .auth.router import router as auth_router
from .user.paths import UserPaths
from .auth.paths import AuthPaths

router = APIRouter()

router.include_router(user_router, prefix=UserPaths.BASE, tags=[UserPaths.TAGS])
router.include_router(auth_router, prefix=AuthPaths.BASE, tags=[AuthPaths.TAGS])