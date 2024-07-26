"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import importlib
import inspect
import logging
from types import TracebackType
from typing import Any, Awaitable, Callable, List, Optional, Type

import anyio
import grpc
from pydantic import BaseModel
from typing_extensions import Self, override

from pyasyncrpc.log.Log import Log
from pyasyncrpc.model.GRPCConfig import GRPCConfig, GRPCInfo, GRPCMethod, GRPCMethodInfo
from pyasyncrpc.model.RequestContext import RequestContext
from pyasyncrpc.service.Service import Service
from pyasyncrpc.util.Snowflake import Snowflake


class GRPCService(Service):
    """grpc service."""

    def __init__(
        self, info: GRPCInfo, methods_info: Optional[List[GRPCMethodInfo]] = None, log: Optional[Log] = None
    ) -> None:
        """Init."""
        pd2_pkg = importlib.import_module(info.pd2_pkg)
        pd2_grpc_pkg = importlib.import_module(info.pd2_grpc_pkg)
        handle_func = getattr(pd2_grpc_pkg, info.handle_func_name)
        server_stub = getattr(pd2_grpc_pkg, info.server_stub_name)
        request_func = getattr(pd2_pkg, info.request_func_name)
        reply_func = getattr(pd2_pkg, info.reply_func_name)
        self._config = GRPCConfig(
            info=info,
            methods=[],
            handle_func=handle_func,
            server_stub=server_stub,
            request_func=request_func,
            reply_func=reply_func,
        )
        for method_info in methods_info or []:
            method_pkg = importlib.import_module(method_info.pkg)
            method_func = getattr(method_pkg, method_info.method_name)
            arg_class = getattr(method_pkg, method_info.arg_class_name)
            self.register_method(method_info.grpc_method_name, arg_class)(method_func)
        if log:
            log.init_log()
        self._server: Optional[grpc.Server] = None
        self._snowflake = Snowflake(1, 1)
        self._grace = info.grace
        self._thread_limiter = info.thread_limiter
        self._options = info.options

    @property
    def config(self) -> GRPCConfig:
        """Service config."""
        return self._config

    @property
    def server(self) -> grpc.Server:
        """Service config."""
        if not self._server:
            msg = "grpc.Server instance must be added"
            raise RuntimeError(msg)
        return self._server

    def register_method(self, method_name: str, args_type: Type[BaseModel]) -> Callable[[Any], Any]:
        """Register rpc method."""

        def wrapper(func: Callable[[RequestContext], Awaitable[BaseModel]]) -> Callable[[Any], Any]:
            if not inspect.iscoroutinefunction(func):
                msg = "a coroutine function was expected"
                raise RuntimeError(msg)

            async def wrap(*args: Any) -> object:
                """Process Parameters."""
                request = args[1]
                params = args_type.model_validate({k: getattr(request, k) for k in args[1].DESCRIPTOR.fields_by_name})
                ctx = RequestContext(request_id=self._snowflake.next_id(), request_param=params)
                logging.info(f"{ctx.request_id}:[%s]", params)
                ret = await func(ctx)
                return self.config.reply_func(**ret.model_dump(by_alias=True))

            self.config.methods.append(GRPCMethod(grpc_method_name=method_name, method=wrap))
            return wrap

        return wrapper

    def create_servicer(self) -> object:
        """Create the servicer."""
        methods = {meta.grpc_method_name: meta.method for meta in self.config.methods}
        return type(self.config.info.service_name, (), methods)()

    @override
    async def start(self) -> None:
        anyio.to_thread.current_default_thread_limiter().total_tokens = self._thread_limiter
        self._server = grpc.aio.server(options=self._options)
        self.config.handle_func(self.create_servicer(), self._server)
        listen_addr = self.config.info.listen_addr
        self._server.add_insecure_port(listen_addr)
        logging.info("Starting server on %s", listen_addr)
        await self._server.start()

    @override
    async def close(self) -> None:
        logging.info("The asynchronous rpc application will be shut down")
        await self.server.stop(self._grace)

    @override
    async def wait(self) -> None:
        await self.server.wait_for_termination()

    async def __aenter__(self) -> Self:
        """Enter."""
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        """Exit."""
        await self.close()
