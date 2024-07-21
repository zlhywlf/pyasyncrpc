"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pytest
from pyasyncrpc.model.PyScriptConfig import PyScriptConfig
from pyasyncrpc.util.PyScriptActuator import PyScriptActuator
from script.common import TEST_RESULT_SUCCESS


@pytest.mark.anyio
@pytest.mark.parametrize("class_name", ["Simple", None])
async def test_base(class_name: str) -> None:
    """Simple test."""
    config = PyScriptConfig(pkg="script.base_case", class_name=class_name, method_name="run")
    actuator = PyScriptActuator(config)
    ret = await actuator()
    assert ret.result == TEST_RESULT_SUCCESS


@pytest.mark.anyio
async def test_pkg_is_not_found() -> None:
    """Package is not found."""
    config = PyScriptConfig(pkg="script.not_found", class_name="Simple", method_name="run")
    actuator = PyScriptActuator(config)
    ret = await actuator()
    assert ret.msg == "call_method:No module named 'script.not_found'"


@pytest.mark.anyio
async def test_class_is_not_found() -> None:
    """Class is not found."""
    config = PyScriptConfig(pkg="script.base_case", class_name="not_found", method_name="run")
    actuator = PyScriptActuator(config)
    ret = await actuator()
    assert ret.msg == "call_method:module 'script.base_case' has no attribute 'not_found'"


@pytest.mark.anyio
async def test_method_is_not_found() -> None:
    """Method is not found."""
    config = PyScriptConfig(pkg="script.base_case", class_name="Simple", method_name="not_found")
    actuator = PyScriptActuator(config)
    ret = await actuator()
    assert ret.msg == "call_method:'Simple' object has no attribute 'not_found'"
