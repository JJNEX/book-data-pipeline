from typing import List, Optional

from sqlalchemy.orm import Session

from app.feature.book.book import Book


class BookRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def add(self, book: Book) -> Book:
        try:
            self.db.add(book)
            self.db.commit()
            self.db.refresh(book)

            return book

        except Exception:
            self.db.rollback()
            raise

    def add_many(self, books: List[Book]) -> List[Book]:
        try:
            self.db.add_all(books)
            self.db.commit()

            for book in books:
                self.db.refresh(book)

            return books

        except Exception:
            self.db.rollback()
            raise

 
    # READ
 
    def get_all(self) -> List[Book]:
        return self.db.query(Book).all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return (
            self.db
            .query(Book)
            .filter(Book.id == book_id)
            .first()
        )

    def get_by_title(self, title: str) -> Optional[Book]:
        return (
            self.db
            .query(Book)
            .filter(Book.title == title)
            .first()
        )


    # DELETE

    def delete(self, book: Book) -> None:
        try:
            self.db.delete(book)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def delete_all(self) -> int:
        try:
            deleted_count = (
                self.db
                .query(Book)
                .delete(synchronize_session=False)
            )

            self.db.commit()

            return deleted_count

        except Exception:
            self.db.rollback()
            raise
    