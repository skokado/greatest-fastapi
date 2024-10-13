from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from auth.utils.jwt import create_access_token
from common.dependencies import AsyncSessionDep
from ..models import User
from ..utils.password import check_password
from ..schemas import auth_schema as schemas

router = APIRouter()


@router.post("/login")
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSessionDep
) -> schemas.LoginResponse:
    login_failed = HTTPException(status_code=401, detail="Incorrect email or password")

    stmt = select(User).where(User.email == data.username)
    user = (await session.execute(stmt)).scalar()
    if not user:
        raise login_failed

    if not check_password(data.password, user.hashed_password):
        raise login_failed

    payload = {
        "sub": user.id,
        "email": user.email,
    }
    token = create_access_token(payload)
    return schemas.LoginResponse(access_token=token, token_type="bearer")
