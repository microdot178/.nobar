"""Battery status label."""

from __future__ import annotations

import psutil
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class BatteryLabel(QLabel):
    """Displays battery percentage with color based on state."""

    def __init__(self, font: QFont, config: dict) -> None:
        """Initialize battery label with color config."""
        super().__init__()
        self.setFont(font)
        self._charging_color = config.get("battery_charging_color", "green")
        self._normal_color = config.get("battery_color", config["color"])
        self._low_color = config.get("battery_low_color", "red")
        self._threshold = config.get("battery_threshold", 20)

    def update_content(self) -> None:
        """Update battery percentage and color."""
        battery = psutil.sensors_battery()
        if not battery:
            self.setText("?")
            return

        self.setText(str(round(battery.percent)))

        if battery.power_plugged:
            color = self._charging_color
        elif battery.percent < self._threshold:
            color = self._low_color
        else:
            color = self._normal_color

        self.setStyleSheet(f"color: {color}")
