from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.token import create_jwt_token


async def get_user_by_username(
    username: str,
    db: AsyncSession,
) -> Optional[User]:
    query = select(User).where(User.username == username)
    return await db.scalar(query)


async def create_user(
    username: str,
    db: AsyncSession,
) -> str:
    user = await get_user_by_username(username=username, db=db)
    if user:
        user.updated_at = datetime.utcnow()
    else:
        user = User(username=username)
        db.add(user)
    await db.commit()
    return await create_jwt_token(username=username)
