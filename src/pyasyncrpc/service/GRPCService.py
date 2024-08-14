"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import importlib
import inspect
import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Awaitable, Callable, List, Optional, Tuple, Type

import anyio
import grpc
from pydantic import BaseModel
from typing_extensions import Self, override

from pyasyncrpc.log.Log import Log
from pyasyncrpc.model.GRPCConfig import GRPCConfig, GRPCInfo, GRPCMethod, GRPCMethodInfo
from pyasyncrpc.model.RequestContext import RequestContext
from pyasyncrpc.service.Service import Service
from pyasyncrpc.util.Snowflake import Snowflake


class GRPCServiceMiddleware(ABC):
    """grpc service middleware interface."""

    @abstractmethod
    async def pre(self, ctx: RequestContext) -> None:
        """Execute before service."""

    @abstractmethod
    async def post(self, ctx: RequestContext, ret: BaseModel) -> None:
        """Execute after service."""


class GRPCService(Service):
    """grpc service."""

    def __init__(
        self,
        info: GRPCInfo,
        methods_info: Optional[List[GRPCMethodInfo]] = None,
        log: Optional[Log] = None,
        middlewares: Optional[Tuple[GRPCServiceMiddleware, ...]] = None,
        interceptors: Optional[Tuple[grpc.aio.ServerInterceptor, ...]] = None,
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
            self.register_method(method_info.grpc_method_name)(method_func)
        if log:
            log.init_log()
        self._server: Optional[grpc.Server] = None
        self._snowflake = Snowflake(1, 1)
        self._grace = info.grace
        self._thread_limiter = info.thread_limiter
        self._options = info.options
        self._middlewares = middlewares or ()
        self._interceptors = interceptors or ()

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

    def register_method(self, method_name: str) -> Callable[[Any], Any]:
        """Register rpc method."""

        def wrapper(func: Callable[[RequestContext], Awaitable[BaseModel]]) -> Callable[[Any], Any]:
            if not inspect.iscoroutinefunction(func):
                msg = "a coroutine function was expected"
                raise RuntimeError(msg)

            async def wrap(*args: Any) -> object:
                """Process Parameters."""
                ctx = RequestContext(request_id=self._snowflake.next_id(), request=args[1], context=args[2])
                for middleware in self._middlewares:
                    await middleware.pre(ctx)
                ret = await func(ctx)
                for middleware in self._middlewares:
                    await middleware.post(ctx, ret)
                return self.config.reply_func(**ret.model_dump(by_alias=True))

            logging.info(f"register method:{method_name}")
            self.config.methods.append(GRPCMethod(grpc_method_name=method_name, method=wrap))
            return wrap

        return wrapper

    def create_servicer(self) -> object:
        """Create the servicer."""
        methods = {meta.grpc_method_name: meta.method for meta in self.config.methods}
        return type(self.config.info.service_name, (), methods)()

    @override
    async def start(self) -> None:
        logging.info(f"thread limiter:{self._thread_limiter}")
        anyio.to_thread.current_default_thread_limiter().total_tokens = self._thread_limiter
        logging.info(f"grpc options:{self._options}")
        self._server = grpc.aio.server(options=self._options, interceptors=self._interceptors)
        self.config.handle_func(self.create_servicer(), self._server)
        listen_addr = self.config.info.listen_addr
        self._server.add_insecure_port(listen_addr)
        logging.info("Starting server on %s", listen_addr)
        await self._server.start()

    @override
    async def close(self) -> None:
        logging.info("The asynchronous rpc application will be shut down")
        await self.server.stop(self._grace)
        logging.info("The asynchronous rpc application has been shut down")

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
