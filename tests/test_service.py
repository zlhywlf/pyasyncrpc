"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
from typing import Any

import pytest


@pytest.mark.asyncio
async def test_base(grpc_stub: Any, grpc_request: Any) -> Any:  # noqa: ANN401
    """Run service."""
    return await grpc_stub.doSomething01(grpc_request(name="foo"))


@pytest.mark.asyncio
async def test_concurrent_requests(grpc_stub: Any, grpc_request: Any) -> None:  # noqa: ANN401
    """Concurrency test."""
    num = 100
    responses = await asyncio.gather(*[asyncio.create_task(test_base(grpc_stub, grpc_request)) for _ in range(num)])
    for response in responses:
        assert response.status == 200
