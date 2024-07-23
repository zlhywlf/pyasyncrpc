import logging

import anyio
from pyasyncrpc.model.RequestContext import RequestContext
from pydantic import BaseModel


class Arg(BaseModel):
    """request arg."""

    name: str


class Data(BaseModel):
    """reply data."""

    message: str
    status: int


async def say_hello(ctx: RequestContext) -> Data:
    """Say hello."""
    await anyio.sleep(0.01 if ctx.request_id % 2 else 0.5)
    msg = f"{ctx.request_id}[say: Hello, {ctx.request_param.name}!]"
    logging.info(msg)
    return Data(message=msg, status=200)


async def do_service02(ctx: RequestContext) -> Data:
    """do_service02."""
    logging.info(ctx.request_id)
    return Data(message=f"do_service02: Hello, {ctx.request_param.name}!", status=200)
