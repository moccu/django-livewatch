import logging
from contextlib import contextmanager


@contextmanager
def patch_logger(logger_name, log_level):
    """
    Context manager that takes a named logger and the logging level
    and provides a simple mock-like list of messages received
    """
    calls = []

    def replacement(msg):
        calls.append(msg)
    logger = logging.getLogger(logger_name)
    orig = getattr(logger, log_level)
    setattr(logger, log_level, replacement)
    try:
        yield calls
    finally:
        setattr(logger, log_level, orig)
