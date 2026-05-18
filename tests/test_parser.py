from bs4 import BeautifulSoup
import pytest

from app.feature.scraper.parser import (
    parse_price,
    parse_availability,
    parse_rating,
    parse_book,
    parse_books,
)
from app.feature.book.dto.book_request import BookRequest


def test_parse_price():
    assert parse_price("£51.77") == 51.77
    assert parse_price("£0") == 0.0
    assert parse_price("") == 0.0
    assert parse_price(None) == 0.0


def test_parse_availability():
    assert parse_availability("In stock") is True
    assert parse_availability("In Stock ") is True
    assert parse_availability("out of stock") is False
    assert parse_availability("") is False


def test_parse_rating():
    # Precisa passar o <article> que contém o <p class="star-rating">
    html = '<article class="product_pod"><p class="star-rating Three"></p></article>'
    tag = BeautifulSoup(html, "html.parser").article
    assert parse_rating(tag) == 3

    html_no_rating = '<article class="product_pod"><p class="star-rating"></p></article>'
    tag_no = BeautifulSoup(html_no_rating, "html.parser").article
    assert parse_rating(tag_no) == 0

    html_empty = '<article class="product_pod"></article>'
    tag_empty = BeautifulSoup(html_empty, "html.parser").article
    assert parse_rating(tag_empty) == 0


def test_parse_book():
    html = """
    <article class="product_pod">
        <h3><a title="Clean Code"></a></h3>
        <p class="price_color">£50.0</p>
        <p class="instock availability">In stock</p>
        <p class="star-rating Five"></p>
    </article>
    """
    tag = BeautifulSoup(html, "html.parser").article
    book = parse_book(tag)

    assert isinstance(book, BookRequest)
    assert book.title == "Clean Code"
    assert book.price == 50.0
    assert book.availability is True
    assert book.rating == 5


def test_parse_books_multiple():
    html = """
    <article class="product_pod">
        <h3><a title="Book One"></a></h3>
        <p class="price_color">£10.0</p>
        <p class="instock availability">In stock</p>
        <p class="star-rating Two"></p>
    </article>
    <article class="product_pod">
        <h3><a title="Book Two"></a></h3>
        <p class="price_color">£20.0</p>
        <p class="instock availability">Out of stock</p>
        <p class="star-rating Four"></p>
    </article>
    """
    books = parse_books(html)
    assert len(books) == 2
    assert books[0].title == "Book One"
    assert books[0].price == 10.0
    assert books[0].availability is True
    assert books[0].rating == 2

    assert books[1].title == "Book Two"
    assert books[1].price == 20.0
    assert books[1].availability is False
    assert books[1].rating == 4