from fastapi import APIRouter, Depends
from sqlalchemy import select

from common.dependencies import AsyncSessionDep

from ..dependencies import get_current_user
from ..models import User
from ..schemas import user_schema as schemas
from ..logics import user as user_logics

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("")
async def list_users(session: AsyncSessionDep) -> list[schemas.UserResponse]:
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSessionDep) -> schemas.UserResponse:
    return await user_logics.get_user(user_id, session)
