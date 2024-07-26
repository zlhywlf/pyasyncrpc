"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import platform
from typing import ClassVar

import pyasyncrpc.launcher
from pyasyncrpc.launcher.Launcher import Launcher
from pyasyncrpc.service.Service import Service
from pyasyncrpc.util.utils import get_special_modules


class LauncherFactory:
    """application launcher factory."""

    PLATFORM: ClassVar[str] = platform.system()

    @staticmethod
    def create_launcher(service: Service, cpu: int) -> Launcher:
        """Create launcher."""
        launchers = get_special_modules(pyasyncrpc.launcher.__name__, Launcher)
        for launcher in launchers:
            if LauncherFactory.PLATFORM in launcher.__name__:
                ret = launcher()  # type: ignore[abstract]
                ret.add_service(service)
                ret.set_cpu(cpu)
                return ret
        msg = "No Implementation"
        raise RuntimeError(msg)
