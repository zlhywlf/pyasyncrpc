"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Optional

from pyasyncrpc.service.Service import Service


class Launcher(ABC):
    """application launcher."""

    def __init__(self) -> None:
        """Init."""
        self._service: Optional[Service] = None

    @abstractmethod
    def launch(self) -> None:
        """Launch."""

    def add_service(self, service: Service) -> None:
        """Add service."""
        self._service = service

    @property
    def service(self) -> Service:
        """Service."""
        if not self._service:
            msg = "Service instance must be added"
            raise RuntimeError(msg)
        return self._service
