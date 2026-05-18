from datetime import datetime
from pydantic import ConfigDict
from app.feature.book.dto.book_request import BookRequest

class BookResponse(BookRequest):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )