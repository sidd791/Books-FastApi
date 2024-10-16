from sqlalchemy.ext.asyncio import AsyncSession
from src.Books.schema import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from src.Books.models import Book


class BookService:
    async def get_all_books(self, session : AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        books = result.scalars().all()
        return books

    async def get_one_book(self, book_id:str, session : AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.execute(statement)
        book = result.scalar_one_or_none()
        return book

    async def create_book(self, book_data : BookCreateModel, session : AsyncSession):
        book_dict = book_data.model_dump()
        new_book = Book(**book_dict)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_id:str, update_data : BookUpdateModel, session : AsyncSession):
        book_to_update = await self.get_one_book(book_id, session)
        if book_to_update is not None:
            update_data = update_data.model_dump()
            for k, v in update_data.items():
                setattr(book_to_update, k, v)
            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, book_id:str, session : AsyncSession):
        book_to_delete = await self.get_one_book(book_id, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None