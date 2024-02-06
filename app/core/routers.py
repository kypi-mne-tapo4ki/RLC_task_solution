from fastapi import FastAPI

from app.routers import records, users


def init_routers(app: FastAPI) -> None:
    app.include_router(users.router, tags=["users"])
    app.include_router(records.router, tags=["records"])
