"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pyasyncrpc.launcher.LinuxLauncher import LinuxLauncher


class DarwinLauncher(LinuxLauncher):
    """suitable for macOS platform."""
