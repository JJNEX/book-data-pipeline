from fastapi import APIRouter, Depends, HTTPException

from app.database.session import get_db

from sqlalchemy.orm import Session

from app.feature.book.book_repository import BookRepository
from app.feature.book.book_service import BookService

from app.feature.scraper.http_scraper import HttpScraper
from app.feature.scraper.scraper_service import ScraperService


router = APIRouter(
    prefix="/scraper",
    tags=["Scraper"]
)

# DEPENDENCY

def get_scraper_service(
    db: Session = Depends(get_db)
) -> ScraperService:

    repository = BookRepository(db)

    book_service = BookService(repository)

    scraper = HttpScraper()

    return ScraperService(
        scraper=scraper,
        book_service=book_service
    )


# INGEST

@router.post("/ingest")
def ingest_books(
    start: int = 1,
    end: int = 1,
    service: ScraperService = Depends(get_scraper_service)
):

    try:
        return service.ingest_pages(start, end)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close()