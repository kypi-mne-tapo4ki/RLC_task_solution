from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from app.crud import users_crud
from app.schemas.user import RegistrationResponse, UserCheckResponse
from app.core.token import decode_jwt_token

router = APIRouter(prefix="/users")


@router.post("/registration", response_model=RegistrationResponse)
async def registration(
    username: str,
    db: AsyncSession = Depends(get_async_session),
) -> RegistrationResponse:
    token = await users_crud.create_user(username=username, db=db)
    return RegistrationResponse(token=token)


@router.get("/user_check", response_model=UserCheckResponse)
async def user_check(
    token: str,
    db: AsyncSession = Depends(get_async_session),
) -> UserCheckResponse:
    payload = await decode_jwt_token(token)
    if payload:
        username = payload["username"]
        user = await users_crud.get_user_by_username(username=username, db=db)
        return UserCheckResponse(
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
            token_expiry=datetime.fromtimestamp(payload["exp"]),
        )
