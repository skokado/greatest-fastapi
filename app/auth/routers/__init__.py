from fastapi import APIRouter

router = APIRouter()

from .auth_router import router as auth_router
router.include_router(auth_router, tags=["Auth"])

from .user_router import router as user_router
router.include_router(user_router, prefix="/users", tags=["Auth/Users"])
