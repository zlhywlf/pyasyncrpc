"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class Log(ABC):
    """log config."""

    @abstractmethod
    def init_log(self) -> None:
        """Initialize log configuration."""
