from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Record
from app.schemas.record import RecordPayload, RecordUpdatePayload


async def create_record(
    record_payload: RecordPayload,
    *,
    db: AsyncSession,
    created_by: int,
):
    record = Record(
        **record_payload.model_dump(),
        created_by=created_by,
        updated_by=created_by,
    )
    db.add(record)
    await db.commit()
    return record


async def get_records(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    title: str = None,
    content: str = None,
):
    query = select(Record)
    if title:
        query = query.where(Record.title.ilike(title))
    if content:
        query = query.where(Record.content.ilike(content))
    query = query.offset(skip).limit(limit)
    result = await db.scalars(query)
    return result.all()


async def get_record(db: AsyncSession, record_id: int):
    query = select(Record).filter(Record.id == record_id)
    return await db.scalar(query)


async def delete_record(db: AsyncSession, record_id: int) -> None:
    query = select(Record).where(Record.id == record_id)
    record = await db.scalar(query)
    await db.delete(record)


async def update_record(
    record_payload: RecordUpdatePayload,
    db: AsyncSession,
    record_id: int,
    updated_by: int,
) -> Optional[Record]:
    query = select(Record).where(Record.id == record_id)
    update_dict = record_payload.model_dump(exclude_unset=True)
    record = await db.scalar(query)
    if update_dict:
        for update_key, update_value in update_dict.items():
            setattr(record, update_key, update_value)
        record.updated_by = updated_by
        await db.commit()
    return record
