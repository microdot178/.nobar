"""Clock label."""

from __future__ import annotations

from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class ClockLabel(QLabel):
    """Displays the current time."""

    def __init__(self, font: QFont, style: str) -> None:
        """Initialize clock label."""
        super().__init__()
        self.setFont(font)
        self.setStyleSheet(style)

    def update_content(self) -> None:
        """Update current time."""
        self.setText(QDateTime.currentDateTime().toString("hh:mm:ss"))
