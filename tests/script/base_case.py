"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from script.common import TEST_RESULT_SUCCESS


class Simple:
    """simple tests case."""

    def run(self) -> str:
        """Simple class method."""
        return TEST_RESULT_SUCCESS


def run() -> str:
    """Simple function."""
    return TEST_RESULT_SUCCESS
