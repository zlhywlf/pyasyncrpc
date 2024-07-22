import logging

import anyio
from pydantic import BaseModel


class Arg(BaseModel):
    """request arg."""

    name: str


class Data(BaseModel):
    """reply data."""

    message: str
    status: int


async def do_service01(arg: Arg, request_id: int) -> Data:
    """do_service01."""
    await anyio.sleep(0.5 if request_id % 2 else 0.8)
    msg = f"{request_id}[do_service01: Hello, {arg.name}!]"
    logging.info(msg)
    return Data(message=msg, status=200)


async def do_service02(arg: Arg, request_id: int) -> Data:
    """do_service02."""
    logging.info(request_id)
    return Data(message=f"do_service02: Hello, {arg.name}!", status=200)
