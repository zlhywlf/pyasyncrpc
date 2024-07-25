"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncrpc.service.Service import Service


class Launcher(ABC):
    """application launcher."""

    @abstractmethod
    def launch(self) -> None:
        """Launch."""

    @abstractmethod
    def add_service(self, service: Service) -> None:
        """Add service."""
