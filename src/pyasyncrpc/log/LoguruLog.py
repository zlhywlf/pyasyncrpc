"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging

from typing_extensions import override

from pyasyncrpc.log.Log import Log
from pyasyncrpc.log.LoggingHandler import LoggingHandler


class LoguruLog(Log):
    """loguru config."""

    @override
    def init_log(self) -> None:
        logging.root.handlers = [LoggingHandler()]
        logging.root.setLevel(logging.NOTSET)
