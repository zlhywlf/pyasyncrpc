"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import time

from script.common import TEST_RESULT_SUCCESS


class Simple:
    """simple tests case."""

    def run(self) -> str:
        """Simple class method."""
        return TEST_RESULT_SUCCESS


def run() -> str:
    """Simple function."""
    return TEST_RESULT_SUCCESS


class ArgClass:
    """the classe with initialization parameters."""

    def __init__(self, name: str) -> None:
        """Init."""
        self._name = name

    def run(self, word: str) -> str:
        """The method with parameters."""
        time.sleep(min(len(word) / 10, 0.5))
        return f"{word}-{self._name}"
