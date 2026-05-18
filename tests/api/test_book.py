
from tests.test_config import client

def test_create_get_and_delete_book(client):

    dados = {
        "title": "Clean Code",
        "price": 50.0,
        "availability": True,
        "rating": 5
    }

    post_response = client.post("/books/", json=dados)
    assert post_response.status_code == 201

    created_book = post_response.json()
    book_id = created_book["id"]

    get_response = client.get("/books/")
    assert get_response.status_code == 200
    assert isinstance(get_response.json(), list)

    books = get_response.json()
    assert any(book["id"] == book_id for book in books)

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200

    delete_data = delete_response.json()
    assert "message" in delete_data
    assert str(book_id) in delete_data["message"]

    get_after = client.get("/books/")
    assert get_after.status_code == 200

    books_after = get_after.json()
    assert all(book["id"] != book_id for book in books_after)