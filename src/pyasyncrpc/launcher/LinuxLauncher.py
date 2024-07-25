"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import signal

import anyio
from typing_extensions import override

from pyasyncrpc.launcher.Launcher import Launcher
from pyasyncrpc.service.Service import Service


class LinuxLauncher(Launcher, Service):
    """suitable for linux platform."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()

    @override
    def launch(self) -> None:
        anyio.run(self.start)
        logging.info("The asynchronous rpc application has been shut down")

    @override
    async def start(self) -> None:
        async with anyio.create_task_group() as tg:
            tg.start_soon(self.close)
            await self.service.start()
            await self.wait()

    @override
    async def close(self) -> None:
        with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
            async for _ in signals:
                await self.service.close()
                return

    @override
    async def wait(self) -> None:
        await self.service.wait()
