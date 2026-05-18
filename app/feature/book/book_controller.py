from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.feature.book.book_service import BookService
from app.feature.book.book_repository import BookRepository

from app.feature.book.dto.book_request import BookRequest
from app.feature.book.dto.book_response import BookResponse



router = APIRouter(
    prefix="/books",
    tags=["Books"]
)



# DEPENDENCY


def get_service(db: Session = Depends(get_db)) -> BookService:
    repository = BookRepository(db)

    return BookService(repository)



# CREATE

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(
    book: BookRequest,
    service: BookService = Depends(get_service)
):
    return service.create(book)



# CREATE MÚLTIPLO


@router.post("/bulk", response_model=list[BookResponse], status_code=201)
def create_many_books(
    books: list[BookRequest],
    service: BookService = Depends(get_service)
):
    return service.create_many(books)



# GET ALL

@router.get("/", response_model=list[BookResponse])
def get_all_books(
    service: BookService = Depends(get_service)
):
    return service.get_all()


# DELETE ALL 

@router.delete("/")
def delete_all_books(
    service: BookService = Depends(get_service)
):
    deleted = service.delete_all()

    return {
        "deleted": deleted
    }



# GET BY ID

@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(
    book_id: int,
    service: BookService = Depends(get_service)
):
    book = service.get_by_id(book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# DELETE BY ID

@router.delete("/{book_id}")
def delete_book_by_id(
    book_id: int,
    service: BookService = Depends(get_service)
):
    deleted = service.delete_by_id(book_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": f"Book {book_id} deleted successfully"
    }