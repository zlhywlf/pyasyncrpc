"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, Callable, List, Sequence, Tuple

import grpc
from pydantic import BaseModel


class GRPCConfig(BaseModel):
    """grpc runtime config."""

    info: "GRPCInfo"
    methods: List["GRPCMethod"]
    handle_func: Callable[[object, grpc.aio.Server], None]
    server_stub: type
    request_func: type
    reply_func: type


class GRPCMethod(BaseModel):
    """method in service."""

    grpc_method_name: str
    method: Callable[[Any], Any]


class GRPCInfo(BaseModel):
    """grpc info."""

    service_name: str
    handle_func_name: str
    server_stub_name: str
    request_func_name: str
    reply_func_name: str
    pd2_pkg: str
    pd2_grpc_pkg: str
    listen_addr: str
    grace: int = 200
    thread_limiter: int = 40
    options: Sequence[Tuple[str, Any]] = ()


class GRPCMethodInfo(BaseModel):
    """method information in service."""

    grpc_method_name: str
    pkg: str
    method_name: str
