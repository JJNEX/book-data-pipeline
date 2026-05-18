import time

import httpx

from app.core.utils.logger import logger
from app.feature.scraper.base_scraper import BaseScraper


class HttpScraper(BaseScraper):

    BASE_URL = "https://books.toscrape.com/"

    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3
    ):
        self.client = httpx.Client(timeout=timeout)
        self.retries = retries


    def fetch_books_html(self, page: int = 1) -> str:

        url = self._build_url(page)

        logger.info(
            "fetch_books_page",
            extra={
                "page": page,
                "url": url
            }
        )

        return self.fetch_page(url)

    def fetch_page(self, url: str) -> str:

        last_exception = None

        for attempt in range(1, self.retries + 1):

            try:

                logger.info(
                    "request_started",
                    extra={
                        "url": url,
                        "attempt": attempt,
                        "max_retries": self.retries
                    }
                )

                response = self.client.get(url)

                response.raise_for_status()

                logger.info(
                    "request_succeeded",
                    extra={
                        "url": url,
                        "status_code": response.status_code
                    }
                )

                return response.text

            except (
                httpx.RequestError,
                httpx.HTTPStatusError
            ) as error:

                last_exception = error

                logger.warning(
                    "request_failed",
                    extra={
                        "url": url,
                        "attempt": attempt,
                        "max_retries": self.retries,
                        "error": str(error)
                    }
                )

                self._backoff(attempt)

        logger.error(
            "request_exhausted",
            extra={
                "url": url,
                "max_retries": self.retries
            }
        )

        raise last_exception

    def close(self):

        logger.info(
            "http_client_closed"
        )

        self.client.close()


    def _build_url(self, page: int) -> str:

        if page == 1:
            return self.BASE_URL

        return f"{self.BASE_URL}catalogue/page-{page}.html"

    def _backoff(self, attempt: int):

        delay = attempt

        logger.info(
            "retry_backoff",
            extra={
                "attempt": attempt,
                "delay_seconds": delay
            }
        )

        time.sleep(delay)