import logging
from weakref import proxy

import anyio
from pyasyncrpc.model.PyScriptConfig import PyScriptConfig
from pyasyncrpc.model.RequestContext import RequestContext
from pyasyncrpc.util.PyScriptActuator import PyScriptActuator
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
    arg = Arg(name=ctx.request.name)
    await anyio.sleep(0.01 if ctx.request_id % 2 else 0.5)
    msg = f"{ctx.request_id}[say: Hello, {arg.name}!]"
    logging.info(msg)
    return Data(message=msg, status=200)


async def execute_py_script(ctx: RequestContext) -> Data:
    """Execute python script."""
    logging.info(ctx.request_id)
    arg = Arg(name=ctx.request.name)
    config = PyScriptConfig.model_validate_json(arg.name)
    actuator = PyScriptActuator(config)
    await anyio.to_thread.run_sync(proxy(actuator))
    msg = f"Execute python script:{actuator.result}"
    logging.info(msg)
    return Data(message=msg, status=200)
