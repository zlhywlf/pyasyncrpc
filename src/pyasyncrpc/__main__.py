"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

import click

from pyasyncrpc._version import version
from pyasyncrpc.launcher.LauncherFactory import LauncherFactory
from pyasyncrpc.log.LoguruLog import LoguruLog
from pyasyncrpc.model.GRPCConfig import GRPCInfo, GRPCMethodInfo
from pyasyncrpc.service.GRPCService import GRPCService


@click.command()
@click.option("-v", "--version", is_flag=True, help="print version")
@click.option("--service_name", help="any string")
@click.option("--handle_func_name", help="eg. add_XXServicer_to_server")
@click.option("--server_stub_name", help="eg. XXStub")
@click.option("--request_func_name", help="grpc request message name")
@click.option("--reply_func_name", help="grpc response message name")
@click.option("--pd2_pkg", help="")
@click.option("--pd2_grpc_pkg", help="")
@click.option("--listen_addr", default="[::]:50051", help="service address")
@click.option("--method", multiple=True, default=(), help="JSON format configuration")
def main(**kwargs: Any) -> None:
    """The asynchronous rpc application."""
    if kwargs.get("version"):
        print(version)  # noqa: T201
        return
    info = GRPCInfo.model_validate(kwargs)
    methods_info = [GRPCMethodInfo.model_validate_json(_) for _ in kwargs.get("method", [])]
    service = GRPCService(info, methods_info, LoguruLog())
    launcher = LauncherFactory.create_launcher(service)
    launcher.launch()


if __name__ == "__main__":
    main()
