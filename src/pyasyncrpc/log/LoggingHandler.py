"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from typing import ClassVar, Dict

import loguru
from typing_extensions import override


class LoggingHandler(logging.Handler):
    """logging redirects to loguru."""

    LEVEL_MAPPING: ClassVar[Dict[int, str]] = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL",
    }

    @override
    def emit(self, record: logging.LogRecord) -> None:
        loguru.logger.opt(depth=7).log(LoggingHandler.LEVEL_MAPPING.get(record.levelno, "INFO"), record.getMessage())
