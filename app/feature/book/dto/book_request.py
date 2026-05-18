from pydantic import BaseModel


class BookRequest(BaseModel):
    title: str
    price: float
    availability: bool
    rating: int