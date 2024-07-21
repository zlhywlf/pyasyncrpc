"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import importlib
from typing import Any, Callable

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

    def _load_class(self) -> object:
        """Load the specified class."""
        m = importlib.import_module(self._config.pkg)
        if not self._config.class_name:
            return m
        cls = getattr(m, self._config.class_name)
        return cls(*self._config.class_args) if self._config.class_args else cls()

    @handle_exception  # type: ignore[arg-type]
    def call_method(self) -> None:
        """Load the method from class."""
        obj = self._load_class()
        if self._config.method_name:
            method = getattr(obj, self._config.method_name)
            if callable(method):
                self._result.result = method(*self._config.method_args) if self._config.method_args else method()
        from_thread.run_sync(self._event.set)

    async def __call__(self) -> PyScriptResult:
        """Execute."""
        await to_thread.run_sync(self.call_method)
        await self._event.wait()
        return self._result

    handle_exception = staticmethod(handle_exception)  # type: ignore[assignment]
