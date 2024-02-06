from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import records_crud
from app.dependencies import get_current_user, get_async_session
from app.models import User
from app.schemas.record import (
    RecordResponse,
    RecordPayload,
    RecordUpdatePayload,
)

router = APIRouter(prefix="/records")


@router.post("", response_model=RecordResponse)
async def create_record(
    record: RecordPayload,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
) -> RecordResponse:
    """The method for creating a new record."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    return await records_crud.create_record(
        record,
        db=db,
        created_by=current_user.id,
    )


@router.get("")
async def read_records(
    skip: int = 0,
    limit: int = 10,
    title: str = None,
    content: str = None,
    db: AsyncSession = Depends(get_async_session),
):
    """Route for getting records."""
    return await records_crud.get_records(
        db,
        skip=skip,
        limit=limit,
        title=title,
        content=content,
    )


@router.get("/{record_id}")
async def read_record(
    record_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Route for getting a specific record."""
    record = await records_crud.get_record(db, record_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )
    return record


@router.patch("/{record_id}")
async def update_record_route(
    record_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    record: RecordUpdatePayload,
    db: AsyncSession = Depends(get_async_session),
):
    """Route for updating a record."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    return await records_crud.update_record(
        record,
        record_id=record_id,
        db=db,
        updated_by=current_user.id,
    )


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_record_route(
    record_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
):
    """Route for deleting a record."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    record = await records_crud.get_record(db, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )
    await records_crud.delete_record(db, record_id)
