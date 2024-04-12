import logging
from logging.handlers import TimedRotatingFileHandler
import os


def setup_error_logger(name: str) -> logging.Logger:
    if not os.path.exists("logs"):
        os.makedirs("logs")

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = TimedRotatingFileHandler("logs/game.log", when="midnight", backupCount=7)
    handler.setFormatter(formatter)
    handler.suffix = "%Y%m%d"

    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger
