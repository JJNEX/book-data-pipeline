from typing import List

from app.feature.book.book_repository import BookRepository
from app.feature.book.book import Book
from app.feature.book.dto.book_request import BookRequest
from app.feature.book.book_mapper import to_model


class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository


    # CREATE SINGULAR

    def create(self, book_dto: BookRequest) -> Book:

        existing = self.repository.get_by_title(book_dto.title)

        if existing:
            return existing

        book = to_model(book_dto)
        return self.repository.add(book)


    # CREATE MÚLTIPLO

    def create_many(self, books: List[BookRequest]) -> List[Book]:

        to_save: List[Book] = []

        for book_dto in books:

            exists = self.repository.get_by_title(book_dto.title)

            if exists:
                continue

            book = to_model(book_dto)

            to_save.append(book)

        if not to_save:
            return []

        return self.repository.add_many(to_save)


    # READS

    def get_all(self) -> List[Book]:
        return self.repository.get_all()

    def get_by_id(self, book_id: int) -> Book | None:
        return self.repository.get_by_id(book_id)

    def get_by_title(self, title: str) -> Book | None:
        return self.repository.get_by_title(title)

    # DELETES
    
    def delete_all(self) -> int:
        return self.repository.delete_all()
    
    def delete_by_id(self, book_id: int) -> bool:
        book = self.repository.get_by_id(book_id)

        if not book:
             return False

        self.repository.delete(book)

        return True

    def ingest_books(self, books: List[BookRequest]) -> List[Book]:
        """
        Caso de uso típico de pipeline/scraper:
        transforma BookRequest -> Book e persiste.
        """
        return self.create_many(books)