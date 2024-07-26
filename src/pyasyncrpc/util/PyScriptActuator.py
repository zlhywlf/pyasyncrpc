"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import importlib
from typing import Any, Callable, Dict, List

from anyio import Event, from_thread, to_thread

from pyasyncrpc.model.PyScriptConfig import PyScriptConfig, PyScriptResult


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

        def wrapper(obj: "PyScriptActuator", *arg: Any) -> object:
            """Handling exceptions."""
            try:
                return self(obj, *arg)
            except (AttributeError, ModuleNotFoundError) as e:
                obj.result.msg = f"{self.__name__}:{e!s}"
                from_thread.run_sync(obj.event.set)
                return None

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

    def _load_class(self) -> object:
        """Load the specified class."""
        m = importlib.import_module(self._config.pkg)
        if not self._config.class_name:
            return m
        cls = getattr(m, self._config.class_name)
        if not self._config.class_args:
            return cls()
        if self._config.class_args_is_position:
            return cls(*self._config.class_args)
        return cls(**self._get_keyword_args(self._config.class_args))

    @handle_exception  # type: ignore[arg-type]
    def call_method(self) -> None:
        """Load the method from class."""
        obj = self._load_class()
        if self._config.method_name:
            method = getattr(obj, self._config.method_name)
            if callable(method):
                if not self._config.method_args:
                    self._result.result = method()
                elif self._config.class_args_is_position:
                    self._result.result = method(*self._config.method_args)
                else:
                    self._result.result = method(**self._get_keyword_args(self._config.method_args))
        from_thread.run_sync(self._event.set)

    async def __call__(self) -> PyScriptResult:
        """Execute."""
        await to_thread.run_sync(self.call_method)
        await self._event.wait()
        return self._result

    handle_exception = staticmethod(handle_exception)  # type: ignore[assignment]
