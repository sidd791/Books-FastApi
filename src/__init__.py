from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.Books.routes import book_router
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server started")
    await init_db()
    yield
    print("Server stopped")


version = "v1"

app = FastAPI(
    title="API", description="A Book Api", version=version, lifespan=life_span
)

app.include_router(book_router, prefix = f"/{version}/books" , tags=['books'])