"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
from typing import Any

import pytest
from faker import Faker
from pyasyncrpc.model.PyScriptConfig import PyScriptConfig, PyScriptObject


@pytest.mark.anyio
async def test_base(grpc_stub: Any, grpc_request: Any, faker: Faker) -> None:  # noqa: ANN401
    """Run service."""
    name = faker.name()
    ret = await grpc_stub.sayHello(grpc_request(name=name))
    assert name in ret.message
    assert ret.status == 200


@pytest.mark.anyio
async def test_execute_py_script(grpc_stub: Any, grpc_request: Any, faker: Faker) -> None:  # noqa: ANN401
    """Execute python script."""
    class_arg = faker.name()
    method_arg = faker.name()
    cls_info = PyScriptObject(
        name="ArgClass", args=[class_arg], methods=[PyScriptObject(name="run", args=[method_arg])]
    )
    config = PyScriptConfig(
        pkg="script.base_case",
        objects=[cls_info],
    )
    ret = await grpc_stub.executePyScript(grpc_request(name=config.model_dump_json()))
    assert class_arg in ret.message
    assert method_arg in ret.message
    assert ret.status == 200


@pytest.mark.parametrize("func", [test_base, test_execute_py_script])
@pytest.mark.anyio
async def test_concurrent_requests(grpc_stub: Any, grpc_request: Any, faker: Faker, func: Any) -> None:  # noqa: ANN401
    """Concurrency test."""
    num = 100
    await asyncio.gather(*[asyncio.create_task(func(grpc_stub, grpc_request, faker)) for _ in range(num)])
