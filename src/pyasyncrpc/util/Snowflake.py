"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import time


class Snowflake:
    """snowflake algorithm."""

    def __init__(self, worker_id: int, data_center_id: int) -> None:
        """Init."""
        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = 0
        self.last_timestamp = -1

    def next_id(self) -> int:
        """Get a unique ID."""
        timestamp = int(time.time() * 1000)
        if timestamp < self.last_timestamp:
            raise RuntimeError(
                "Clock moved backwards. Refusing to generate id for %d milliseconds"
                % abs(timestamp - self.last_timestamp)
            )
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095
            if self.sequence == 0:
                timestamp = int(time.time() * 1000)
                while timestamp <= self.last_timestamp:
                    timestamp = int(time.time() * 1000)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        return (
            ((timestamp - 1288834974657) << 22) | (self.data_center_id << 17) | (self.worker_id << 12) | self.sequence
        )
