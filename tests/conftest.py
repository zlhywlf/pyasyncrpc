"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import socket
from typing import Any, AsyncGenerator

import grpc
import pytest
from grpc import _channel
from pyasyncrpc.model.GRPCConfig import GRPCInfo
from pyasyncrpc.service.GRPCService import GRPCService
from pydantic import BaseModel


class Arg(BaseModel):
    """request arg."""

    name: str


class Data(BaseModel):
    """reply data."""

    message: str
    status: int


async def do_service01(arg: Arg) -> Data:
    """do_service01."""
    return Data(message=f"do_service01: Hello, {arg.name}!", status=200)


async def do_service02(arg: Arg) -> Data:
    """do_service02."""
    return Data(message=f"do_service02: Hello, {arg.name}!", status=200)


@pytest.fixture
async def grpc_addr() -> str:
    """Grpc addr."""
    ip = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, 0))
    return f"{ip}:{sock.getsockname()[1]}"


@pytest.fixture
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
    async with GRPCService(info) as server:
        server.register_method("doSomething01", Arg)(do_service01)
        server.register_method("doSomething02", Arg)(do_service02)
        await server.launch()
        yield server


@pytest.fixture
async def grpc_channel(grpc_addr: str) -> AsyncGenerator[_channel.Channel, Any]:
    """Grpc channel."""
    async with grpc.aio.insecure_channel(grpc_addr) as channel:
        yield channel


@pytest.fixture
async def grpc_stub(grpc_server: GRPCService, grpc_channel: _channel.Channel) -> Any:  # noqa: ANN401
    """Grpc stub."""
    return grpc_server.config.server_stub(grpc_channel)


@pytest.fixture
async def grpc_request(grpc_server: GRPCService) -> type:
    """Grpc request."""
    return grpc_server.config.request_func
