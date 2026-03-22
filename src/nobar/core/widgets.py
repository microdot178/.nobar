"""Widget instantiation factory."""

from __future__ import annotations

import i3ipc

from nobar.core.panel import Panel
from nobar.modules.info import Info
from nobar.modules.workspaces import Workspaces

WIDGET_CLASSES: dict[str, type[Panel]] = {
    "workspaces": Workspaces,
    "info": Info,
}


def create_widgets(
    arguments: object,
    connection: i3ipc.Connection,
    config: dict,
) -> list[Panel]:
    """Instantiate widgets based on config and CLI arguments."""
    requested = arguments.widgets or list(WIDGET_CLASSES)

    return [
        WIDGET_CLASSES[name](connection, config[name])
        for name in requested
        if name in WIDGET_CLASSES and name in config
    ]
