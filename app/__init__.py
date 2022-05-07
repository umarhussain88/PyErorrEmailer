import logging
from .engine import SQLErrors
from .mail import Mailer


def init_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="logs/logs.log",
        filemode="a",
    )

    logger = logging.getLogger(__name__)
    return logger


__all__ = [SQLErrors, Mailer, init_logger]
