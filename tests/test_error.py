from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest

from app.main import app
from app.feature.scraper.scraper_controller import get_scraper_service

client = TestClient(app)


def test_scraper_ingest_http_error(monkeypatch):
    # Cria um mock para o ScraperService
    mock_service = MagicMock()

    # Simula erro no ingest_pages
    mock_service.ingest_pages.side_effect = Exception("Scraping failed")

    # Monkeypatch na dependência para retornar nosso mock
    app.dependency_overrides[get_scraper_service] = lambda: mock_service

    # Faz a requisição para o endpoint
    response = client.post("/scraper/ingest?start=1&end=2")

    # Verifica se o status code é 500
    assert response.status_code == 500

    # Verifica se o detalhe da exceção foi passado
    assert response.json()["detail"] == "Scraping failed"

    # Verifica se close() foi chamado mesmo com erro
    mock_service.close.assert_called_once()

    # Limpa o override de dependência
    app.dependency_overrides.clear()