from http.client import HTTPException

from fastapi import Depends, status, APIRouter
from typing import List
from src.Books.models import Book
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.Books.schema import BookCreateModel, BookUpdateModel
from src.db.main import get_session
from src.Books.service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model = List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session) ):
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model = Book)
async def create_book(book_data : BookCreateModel, session:AsyncSession = Depends(get_session)):
    book = await book_service.create_book(book_data, session)
    return book

@book_router.get("/{book_id}", response_model = Book)
async def get_one_book(book_id, session:AsyncSession = Depends(get_session)):
    book = await book_service.get_one_book(book_id, session)
    return book

@book_router.patch("/{book_id}", response_model = Book)
async def update_book(book_id : str, book_data:BookUpdateModel, session:AsyncSession = Depends(get_session)):
    book = await book_service.update_book(book_id, book_data, session)
    return book

@book_router.delete("/{book_id}")
async def delete_book(book_id:str, session : AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_id, session)
    print(book_to_delete)
    if book_to_delete is not None:
        return {}
    else:
        raise HTTPException()