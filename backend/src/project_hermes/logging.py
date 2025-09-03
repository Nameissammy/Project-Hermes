import logging
import os


def configure_logging() -> None:
    # Minimal json-like formatter without external deps
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='{"level":"%(levelname)s","time":"%(asctime)s","name":"%(name)s","message":"%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(log_level)


