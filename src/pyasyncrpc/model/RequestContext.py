"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

from pydantic import BaseModel


class RequestContext(BaseModel):
    """request context."""

    request_id: int
    request: Any
    context: Any
