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
