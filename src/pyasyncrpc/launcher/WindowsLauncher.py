"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import ctypes
import logging
import sys
from typing import Optional

import anyio
from anyio.abc import CancelScope, TaskGroup, TaskStatus
from typing_extensions import override

from pyasyncrpc.launcher.Launcher import Launcher
from pyasyncrpc.service.Service import Service


class WindowsLauncher(Launcher, Service):
    """suitable for windows platform."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self._event_loop: Optional[TaskGroup] = None
        self._cancel_scope: Optional[CancelScope] = None

    @override
    def launch(self) -> None:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handler_func = ctypes.WINFUNCTYPE(ctypes.c_void_p)(self.run_callback)
        if not kernel32.SetConsoleCtrlHandler(handler_func, True):  # noqa: FBT003
            err = ctypes.get_last_error()
            logging.info(f"Error setting control handler: {err}")
            sys.exit(1)
        try:
            anyio.run(self.start)
        except KeyboardInterrupt:
            if handler_func:
                kernel32.SetConsoleCtrlHandler(handler_func, False)  # noqa: FBT003
            logging.info("The asynchronous rpc application has been shut down")

    @override
    async def start(self) -> None:
        await self.service.start()
        async with anyio.create_task_group() as tg:
            tg.start_soon(self.wait)
            self._event_loop = tg
            self._cancel_scope = tg.cancel_scope
        await self.close()

    @override
    async def close(self) -> None:
        await self.service.close()

    @override
    async def wait(self) -> None:
        while True:  # noqa: ASYNC110 RUF100
            await anyio.sleep(3)

    async def cancel(self, task_status: TaskStatus[None]) -> None:
        """Cancel waiting."""
        task_status.started()
        if self._cancel_scope:
            await self._cancel_scope.cancel()

    def run_callback(self) -> None:
        """ctrl+c callback."""
        if self._event_loop:
            anyio.run(self._event_loop.start, self.cancel)
