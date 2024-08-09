"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import contextlib

import pytest
from pyasyncrpc.model.PyScriptConfig import PyScriptConfig, PyScriptObject
from pyasyncrpc.util.PyScriptActuator import PyScriptActuator
from script.common import TEST_RESULT_SUCCESS


@pytest.mark.anyio
@pytest.mark.parametrize(
    "info",
    [
        PyScriptObject(name="Simple", methods=[PyScriptObject(name="run")]),
        PyScriptObject(name="run"),
    ],
)
async def test_base(info: PyScriptObject) -> None:
    """Simple test."""
    config = PyScriptConfig(pkg="script.base_case", objects=[info])
    actuator = PyScriptActuator(config)
    await actuator()
    assert actuator.result.result
    assert actuator.result.result.get("run") == TEST_RESULT_SUCCESS
    assert actuator.result.success


@pytest.mark.anyio
async def test_pkg_is_not_found() -> None:
    """Package is not found."""
    cls_info = PyScriptObject(name="Simple", methods=[PyScriptObject(name="run")])
    config = PyScriptConfig(pkg="script.not_found", objects=[cls_info])
    actuator = PyScriptActuator(config)
    with contextlib.suppress(Exception):
        await actuator()
    assert actuator.result.msg == "call_obj:No module named 'script.not_found'"
    assert not actuator.result.success


@pytest.mark.anyio
async def test_class_is_not_found() -> None:
    """Class is not found."""
    cls_info = PyScriptObject(name="not_found", methods=[PyScriptObject(name="run")])
    config = PyScriptConfig(pkg="script.base_case", objects=[cls_info])
    actuator = PyScriptActuator(config)
    with contextlib.suppress(Exception):
        await actuator()
    assert actuator.result.msg == "call_obj:module 'script.base_case' has no attribute 'not_found'"
    assert not actuator.result.success


@pytest.mark.anyio
async def test_method_is_not_found() -> None:
    """Method is not found."""
    cls_info = PyScriptObject(name="Simple", methods=[PyScriptObject(name="not_found")])
    config = PyScriptConfig(pkg="script.base_case", objects=[cls_info])
    actuator = PyScriptActuator(config)
    with contextlib.suppress(Exception):
        await actuator()
    assert actuator.result.msg == "call_obj:'Simple' object has no attribute 'not_found'"
    assert not actuator.result.success
