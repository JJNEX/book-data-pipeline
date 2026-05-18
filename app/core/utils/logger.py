import logging

from pythonjsonlogger import jsonlogger


logger = logging.getLogger("book_pipeline")

logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s"
)

log_handler.setFormatter(formatter)

logger.addHandler(log_handler)