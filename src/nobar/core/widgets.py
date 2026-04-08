"""Widget instantiation factory."""

from __future__ import annotations

import argparse

from i3ipc.aio import Connection

from nobar.core.panel import Panel
from nobar.modules.info import Info
from nobar.modules.workspaces import Workspaces

WIDGET_CLASSES: dict[str, type[Panel]] = {
    "workspaces": Workspaces,
    "info": Info,
}


async def create_widgets(
    arguments: argparse.Namespace,
    connection: Connection,
    config: dict,
) -> list[Panel]:
    """Instantiate widgets based on config and CLI arguments."""
    requested = arguments.widgets or list(WIDGET_CLASSES)

    widgets = []
    for name in requested:
        if name in WIDGET_CLASSES and name in config:
            widget = WIDGET_CLASSES[name](connection, config[name])
            await widget.init()
            widgets.append(widget)

    return widgets
