from bs4 import BeautifulSoup, Tag
from app.feature.book.dto.book_request import BookRequest


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def parse_price(price_text: str) -> float:
    try:
        return float(price_text.replace("£", "").strip())
    except (ValueError, AttributeError):
        return 0.0


def parse_availability(text: str) -> bool:
    return "in stock" in text.lower()


def parse_rating(book_tag: Tag) -> int:
    rating_tag = book_tag.find("p", class_="star-rating")

    if not rating_tag:
        return 0

    classes = rating_tag.get("class", [])

    for class_name in classes:
        if class_name in RATING_MAP:
            return RATING_MAP[class_name]

    return 0


def parse_book(book_tag: Tag) -> BookRequest:
    h3 = book_tag.find("h3")
    title_tag = h3.find("a") if h3 else None
    title = title_tag.get("title") if title_tag else ""

    price_tag = book_tag.find("p", class_="price_color")
    price_text = price_tag.get_text(strip=True) if price_tag else "0"

    availability_tag = book_tag.find("p", class_="instock availability")
    availability_text = availability_tag.get_text(strip=True) if availability_tag else ""

    return BookRequest(
        title=title,
        price=parse_price(price_text),
        availability=parse_availability(availability_text),
        rating=parse_rating(book_tag),
    )


def parse_books(html: str) -> list[BookRequest]:
    soup = BeautifulSoup(html, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    return [parse_book(book) for book in books]