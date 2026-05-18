from app.feature.book.book import Book
from app.feature.book.dto.book_request import BookRequest


def to_model(dto: BookRequest) -> Book:
    return Book(
        title=dto.title,
        price=dto.price,
        availability=dto.availability,
        rating=dto.rating,
    )