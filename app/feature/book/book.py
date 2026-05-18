from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, CheckConstraint,  func

from app.database.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False, unique=True, index=True)

    price = Column(Numeric(10, 2), nullable=False)

    availability = Column(Boolean, default=True, nullable=False)

    rating = Column(Integer, nullable=True)
    __table_args__ = (
    CheckConstraint("rating >= 0 AND rating <= 5"),
)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)