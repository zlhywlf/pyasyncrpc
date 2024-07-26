"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PyScriptConfig(BaseModel):
    """the configuration of the executed python script."""

    pkg: str
    objects: Optional[List["PyScriptObject"]] = None


class PyScriptResult(BaseModel):
    """the result of python script execution."""

    result: Optional[Dict[str, Any]] = None
    msg: Optional[str] = None
    success: bool = True


class PyScriptObject(BaseModel):
    """The methods or classes of the executed python script."""

    name: str
    args: Optional[List[Any]] = None
    args_is_position: bool = True
    methods: Optional[List["PyScriptObject"]] = None
