from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
import jwt

from config import settings
from common.dependencies import AsyncSessionDep

from .logics.user import get_user
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSessionDep
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise unauthorized

        user_id = int(username)

    except (
        ValueError,
        jwt.exceptions.InvalidTokenError,
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.DecodeError,
    ):
        raise unauthorized

    user = await get_user(user_id, session)
    if user is None:
        raise unauthorized

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]

BearerCredential = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
