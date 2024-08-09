"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import importlib
from types import ModuleType
from typing import Any, Callable, Dict, List, Union

from anyio import Event, from_thread, to_thread

from pyasyncrpc.model.PyScriptConfig import PyScriptConfig, PyScriptObject, PyScriptResult


class PyScriptActuator:
    """execute the python script."""

    def __init__(self, config: PyScriptConfig) -> None:
        """Init."""
        self._config = config
        self._result = PyScriptResult()
        self._event = Event()

    @property
    def result(self) -> PyScriptResult:
        """The result of Python script execution."""
        return self._result

    @property
    def event(self) -> Event:
        """The task event."""
        return self._event

    def handle_exception(self: Callable[[Any, Any], Any]) -> Callable[[Any, Any], object]:  # type: ignore[misc]
        """The decorator used to handle exceptions."""

        def wrapper(obj: "PyScriptActuator", *arg: Any) -> None:
            """Handling exceptions."""
            try:
                self(obj, *arg)
            except Exception as e:
                obj.result.success = False
                obj.result.msg = f"{self.__name__}:{e!s}"
                raise e
            finally:
                from_thread.run_sync(obj.event.set)

        return wrapper

    def _get_keyword_args(self, origin_args: List[Any]) -> Dict[str, Any]:
        """Get keyword args."""
        position_args: Dict[str, Any] = {}
        if not origin_args:
            return position_args
        for _ in origin_args:
            if not isinstance(_, dict):
                self._result.msg = f"{_} not supported"
                continue
            position_args.update(_)
        return position_args

    def _get_obj_result(self, parent: Union[object, ModuleType], info: PyScriptObject) -> object:
        obj = getattr(parent, info.name)
        if not info.args:
            return obj()
        if info.args_is_position:
            return obj(*info.args)
        return obj(**self._get_keyword_args(info.args))

    @handle_exception  # type: ignore[arg-type]
    def call_obj(self) -> None:
        """Load the method from class."""
        module = importlib.import_module(self._config.pkg)
        if not self._config.objects:
            from_thread.run_sync(self._event.set)
            return
        ret = {}
        for obj_info in self._config.objects:
            obj = self._get_obj_result(module, obj_info)
            if not obj_info.methods:
                ret[obj_info.name] = obj
                continue
            for m_info in obj_info.methods:
                m = self._get_obj_result(obj, m_info)
                ret[m_info.name] = m
        self._result.result = ret

    async def __call__(self) -> None:
        """Execute."""
        await to_thread.run_sync(self.call_obj)
        await self._event.wait()

    handle_exception = staticmethod(handle_exception)  # type: ignore[assignment]
