"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, List, Optional

from pydantic import BaseModel


class PyScriptConfig(BaseModel):
    """the configuration of the executed python script."""

    pkg: str
    class_name: Optional[str] = None
    method_name: Optional[str] = None
    class_args: Optional[List[Any]] = None
    method_args: Optional[List[Any]] = None
    method_args_is_position: bool = True
    class_args_is_position: bool = True


class PyScriptResult(BaseModel):
    """the result of python script execution."""

    result: Optional[Any] = None
    msg: Optional[str] = None
