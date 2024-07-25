"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from __future__ import annotations

import importlib.util
import pkgutil
from importlib import import_module
from types import ModuleType
from typing import TypeVar

T = TypeVar("T")


def find_class_by_type(module: ModuleType | None, super_type: T) -> list[T]:
    """获取基类的子类."""
    if not module or not isinstance(super_type, type):
        return []
    ret: list[T] = []
    for cls in module.__dict__.values():
        if not isinstance(cls, type) or cls is super_type or not issubclass(cls, super_type):
            continue
        ret.append(cls)  # type: ignore[arg-type]
    return ret


def get_modules(package_name: str) -> list[ModuleType]:
    """获取指定包下的所有模块."""
    package = importlib.util.find_spec(package_name)
    if package is None or not package.submodule_search_locations:
        info = f"Package {package_name} not found."
        raise ImportError(info)
    package_path = package.submodule_search_locations[0]
    return [
        import_module(name)
        for _, name, is_pkg in pkgutil.walk_packages([package_path], f"{package_name}.")
        if not is_pkg
    ]


def get_special_modules(package_name: str, super_type: T) -> list[T]:
    """获取指定包下指定类型的所有类."""
    ret = []
    for m in get_modules(package_name):
        ret.extend(find_class_by_type(m, super_type))
    return ret
