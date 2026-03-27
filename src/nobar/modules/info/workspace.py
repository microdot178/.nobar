"""Workspace name label."""

from __future__ import annotations

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class WorkspaceLabel(QLabel):
    """Displays the focused workspace name."""

    def __init__(self, font: QFont, style: str) -> None:
        """Initialize workspace label."""
        super().__init__()
        self.setFont(font)
        self.setStyleSheet(style)

    def update_content(self, name: str, state: str) -> None:
        """Update workspace name."""
        self.setText(state if state == "resize" else name)
