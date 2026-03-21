"""Widget instantiation factory."""

from __future__ import annotations

from typing import Any

import i3ipc

from nobar.modules.info import Info
from nobar.modules.workspaces import Workspaces


class Widgets:
    """Create widget instances based on config and CLI arguments."""

    def __init__(
        self,
        arguments: Any,
        connection: i3ipc.Connection,
        config: dict,
    ) -> None:
        """Initialize and instantiate requested widgets.

        Args:
            arguments: Parsed CLI arguments.
            connection: Synchronous i3 IPC connection.
            config: Full application configuration dict.
        """
        self.widgets: list[Any] = []

        widget_list = arguments.widgets or ["all"]

        if "workspaces" in widget_list or "all" in widget_list:
            self.widgets.append(Workspaces(connection, config["workspaces"]))

        if "info" in widget_list or "all" in widget_list:
            self.widgets.append(Info(connection, config["info"]))
