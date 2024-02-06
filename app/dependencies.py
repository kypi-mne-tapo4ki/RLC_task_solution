from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.core.database import async_session_maker
from typing import Optional

from fastapi import Depends, HTTPException

from app.core.auth import api_key_header
from app.crud import users_crud
from app.models import User
from app.core.token import decode_jwt_token


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_token(authorization: str = Depends(api_key_header)) -> str:
    try:
        return authorization.split()[1]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer Token",
        )


async def get_current_user(
    db: AsyncSession = Depends(get_async_session),
    token: str = Depends(get_token),
) -> Optional[User]:
    jwt_claims = await decode_jwt_token(token)
    if jwt_claims is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    username = jwt_claims["username"]
    return await users_crud.get_user_by_username(username, db=db)
