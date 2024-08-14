"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import importlib
from types import ModuleType
from typing import List, Union

from pyasyncrpc.model.PyScriptConfig import PyScriptConfig, PyScriptObject, PyScriptResult


class PyScriptActuator:
    """execute the python script."""

    def __init__(self, config: PyScriptConfig) -> None:
        """Init."""
        self._config = config
        self._result = PyScriptResult()

    @property
    def result(self) -> PyScriptResult:
        """The result of Python script execution."""
        return self._result

    def load_module(self) -> ModuleType:
        """Load module."""
        return importlib.import_module(self._config.pkg)

    def load_methods(self, obj: Union[object, ModuleType], methods: List[PyScriptObject]) -> None:
        """Load methods."""

        def load_method(info: PyScriptObject) -> object:
            """Load method."""
            callable_obj = getattr(obj, info.name)
            if not info.args:
                return callable_obj()
            if not info.transparent:
                if isinstance(info.args, list):
                    return callable_obj(*info.args)
                if isinstance(info.args, dict):
                    return callable_obj(**info.args)
            return callable_obj(info.args)

        for m_info in methods:
            result = load_method(m_info)
            if not m_info.methods:
                self._result.response[m_info.name] = result
                continue
            self.load_methods(result, m_info.methods)

    def call(self) -> None:
        """Call the methods from class."""
        try:
            module = self.load_module()
            if not self._config.objects:
                return
            self.load_methods(module, self._config.objects)
        except Exception as e:
            self._result.success = False
            self._result.msg = f"{e!s}"
            raise e

    def __call__(self) -> None:
        """Execute."""
        self.call()
