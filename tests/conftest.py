"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import socket
from typing import Any, AsyncGenerator

import grpc
import pytest
from faker import Faker
from grpc import _channel
from pyasyncrpc.log.LoguruLog import LoguruLog
from pyasyncrpc.model.GRPCConfig import GRPCInfo, GRPCMethodInfo
from pyasyncrpc.service.GRPCService import GRPCService


@pytest.fixture(scope="module", autouse=True)
def anyio_backend() -> str:
    """Anyio backend."""
    return "asyncio"


@pytest.fixture(scope="module")
async def faker() -> Faker:
    """Faker."""
    return Faker("zh_CN")


@pytest.fixture(scope="module")
async def grpc_addr() -> AsyncGenerator[str, Any]:
    """Grpc addr."""
    ip = "localhost"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((ip, 0))
        yield f"{ip}:{sock.getsockname()[1]}"


@pytest.fixture(scope="module")
async def grpc_server(grpc_addr: str) -> AsyncGenerator[GRPCService, Any]:
    """Grpc server."""
    info = GRPCInfo(
        service_name="Simple",
        handle_func_name="add_ServiceServicer_to_server",
        server_stub_name="ServiceStub",
        request_func_name="ServiceRequest",
        reply_func_name="ServiceReply",
        pd2_pkg="rpc.simple_pb2",
        pd2_grpc_pkg="rpc.simple_pb2_grpc",
        listen_addr=grpc_addr,
    )
    methods_info = [
        GRPCMethodInfo(
            grpc_method_name="sayHello",
            pkg="rpc",
            method_name="say_hello",
            arg_class_name="Arg",
        ),
        GRPCMethodInfo(
            grpc_method_name="executePyScript",
            pkg="rpc",
            method_name="execute_py_script",
            arg_class_name="Arg",
        ),
    ]
    async with GRPCService(info, methods_info, LoguruLog()) as server:
        await server.start()
        yield server


@pytest.fixture(scope="module")
async def grpc_channel(grpc_addr: str) -> AsyncGenerator[_channel.Channel, Any]:
    """Grpc channel."""
    async with grpc.aio.insecure_channel(grpc_addr) as channel:
        yield channel


@pytest.fixture(scope="module")
async def grpc_stub(grpc_server: GRPCService, grpc_channel: _channel.Channel) -> Any:  # noqa: ANN401
    """Grpc stub."""
    return grpc_server.config.server_stub(grpc_channel)


@pytest.fixture(scope="module")
async def grpc_request(grpc_server: GRPCService) -> type:
    """Grpc request."""
    return grpc_server.config.request_func
