from fastapi import FastAPI

from app.feature.book.book_controller import router as book_router
from app.feature.scraper.scraper_controller import router as scraper_router



app = FastAPI()

app.include_router(book_router)
app.include_router(scraper_router)