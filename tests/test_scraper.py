from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.feature.scraper.scraper_controller import get_scraper_service

client = TestClient(app)


def test_scraper_ingest():

    mock_service = MagicMock()

    mock_service.ingest_pages.return_value = [
        {
            "title": "Mock Book",
            "price": 10.0,
            "availability": True,
            "rating": 5
        }
    ]

    # Override da dependência
    app.dependency_overrides[get_scraper_service] = lambda: mock_service

    response = client.post("/scraper/ingest?start=1&end=2")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["title"] == "Mock Book"

    mock_service.ingest_pages.assert_called_once_with(1, 2)

    mock_service.close.assert_called_once()

    # Limpa override
    app.dependency_overrides.clear()