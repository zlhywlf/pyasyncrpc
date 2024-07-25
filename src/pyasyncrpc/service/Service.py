"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class Service(ABC):
    """abstract service interface."""

    @abstractmethod
    async def start(self) -> None:
        """Launch service."""

    @abstractmethod
    async def close(self) -> None:
        """Close the service."""
