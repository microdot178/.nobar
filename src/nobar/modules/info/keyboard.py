"""Keyboard layout label."""

from __future__ import annotations

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from xkbgroup import XKeyboard


class KeyboardLabel(QLabel):
    """Displays the current keyboard layout."""

    def __init__(self, font: QFont, style: str) -> None:
        """Initialize keyboard layout label."""
        super().__init__()
        self.setFont(font)
        self.setStyleSheet(style)
        self._xkb = XKeyboard()

    def update_content(self) -> None:
        """Update keyboard layout."""
        self.setText(self._xkb.group_symbol.upper())
