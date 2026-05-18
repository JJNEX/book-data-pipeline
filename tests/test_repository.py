# tests/repository/test_book_repository.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.feature.book.book import Book
from app.feature.book.book_repository import BookRepository
from app.database.base import Base  # seu declarative_base


@pytest.fixture
def db_session():

    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def repository(db_session: Session):
    return BookRepository(db_session)


def test_add_and_get_book(repository: BookRepository):

    book = Book(title="Clean Code", price=50.0, availability=True, rating=5)
    repository.add(book)

    retrieved = repository.get_by_id(book.id)
    assert retrieved is not None
    assert retrieved.title == "Clean Code"

    books = repository.get_all()
    assert len(books) == 1
    assert books[0].title == "Clean Code"


def test_add_many_and_delete(repository: BookRepository):
    books = [
        Book(title="Book 1", price=10.0, availability=True, rating=3),
        Book(title="Book 2", price=20.0, availability=False, rating=4)
    ]

    added_books = repository.add_many(books)
    assert len(added_books) == 2
   
    repository.delete(added_books[0])
    remaining_books = repository.get_all()
    assert len(remaining_books) == 1
    assert remaining_books[0].title == "Book 2"

    deleted_count = repository.delete_all()
    assert deleted_count == 1
    assert repository.get_all() == []