from fastapi import FastAPI

from app.core.routers import init_routers


def create_app() -> FastAPI:
    fast_api = FastAPI(docs_url="/")
    init_routers(fast_api)
    return fast_api


app = create_app()
