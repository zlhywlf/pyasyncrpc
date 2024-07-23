"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
from typing import Any

import pytest
from faker import Faker


@pytest.mark.anyio
async def test_base(grpc_stub: Any, grpc_request: Any, faker: Faker) -> Any:  # noqa: ANN401
    """Run service."""
    return await grpc_stub.sayHello(grpc_request(name=faker.name()))


@pytest.mark.anyio
async def test_concurrent_requests(grpc_stub: Any, grpc_request: Any, faker: Faker) -> None:  # noqa: ANN401
    """Concurrency test."""
    num = 100
    responses = await asyncio.gather(*[
        asyncio.create_task(test_base(grpc_stub, grpc_request, faker)) for _ in range(num)
    ])
    for response in responses:
        assert response.status == 200
