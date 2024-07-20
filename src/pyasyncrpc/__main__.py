"""entrance.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging

from pyasyncrpc._version import version


def main() -> None:
    """The asynchronous rpc application."""
    logging.error(f"hello pyasyncrpc({version})")


if __name__ == "__main__":
    main()
