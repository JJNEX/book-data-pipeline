import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from app.core.utils.logger import logger
from app.feature.scraper.parser import parse_books


class ScraperService:

    def __init__(self, scraper, book_service):
        self.scraper = scraper
        self.book_service = book_service


    def ingest_pages(
        self,
        start: int = 1,
        end: int = 1,
        max_workers: int = 5
    ):

        logger.info(
            "ingestion_started",
            extra={
                "start_page": start,
                "end_page": end,
                "max_workers": max_workers
            }
        )

        pipeline_start = time.perf_counter()

        pages = list(range(start, end + 1))

        total_found = 0
        total_ingested = 0
        total_failed = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            futures = {
                executor.submit(self._process_page, page): page
                for page in pages
            }

            for future in as_completed(futures):

                page = futures[future]

                try:

                    result = future.result()

                    total_found += result["found"]
                    total_ingested += result["ingested"]

                except Exception as error:

                    total_failed += 1

                    logger.error(
                        "page_processing_failed",
                        extra={
                            "page": page,
                            "error": str(error)
                        }
                    )

        elapsed = time.perf_counter() - pipeline_start

        logger.info(
            "ingestion_completed",
            extra={
                "pages": len(pages),
                "found": total_found,
                "ingested": total_ingested,
                "failed": total_failed,
                "elapsed_seconds": round(elapsed, 2)
            }
        )

        return {
            "start": start,
            "end": end,
            "found": total_found,
            "ingested": total_ingested,
            "failed": total_failed,
            "workers": max_workers,
            "elapsed_seconds": round(elapsed, 2)
        }

    def close(self):

        logger.info(
            "scraper_service_closed"
        )

        self.scraper.close()


    def _process_page(self, page: int):

        logger.info(
            "page_processing_started",
            extra={
                "page": page
            }
        )

        page_start = time.perf_counter()

        html = self.scraper.fetch_books_html(page)

        books = parse_books(html)

        saved = self.book_service.ingest_books(books)

        elapsed = time.perf_counter() - page_start

        logger.info(
            "page_processed",
            extra={
                "page": page,
                "found": len(books),
                "ingested": len(saved),
                "elapsed_seconds": round(elapsed, 2)
            }
        )

        return {
            "found": len(books),
            "ingested": len(saved)
        }