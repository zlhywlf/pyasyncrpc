import logging

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
    await anyio.sleep(0.01 if ctx.request_id % 2 else 0.5)
    msg = f"{ctx.request_id}[say: Hello, {ctx.request_param.name}!]"
    logging.info(msg)
    return Data(message=msg, status=200)


async def execute_py_script(ctx: RequestContext) -> Data:
    """Execute python script."""
    logging.info(ctx.request_id)
    config = PyScriptConfig.model_validate_json(ctx.request_param.name)
    actuator = PyScriptActuator(config)
    ret = await actuator()
    return Data(message=f"Execute python script:{ret}", status=200)
