"""CLI argument parsing for nobar."""

from __future__ import annotations

import argparse


class Arguments:
    """Parse and store command-line arguments."""

    def __init__(self) -> None:
        """Set up argument parser and parse CLI args."""
        self.parser = argparse.ArgumentParser(
            description="nobar - a sleek PyQt6 widget system for i3wm",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        self.parser.add_argument(
            "config",
            help="Path to configuration file (e.g., ~/.config/nobar/config.toml)",
        )

        self.parser.add_argument(
            "--widgets",
            nargs="*",
            help="Array of active widget names",
        )

        self.arguments = self.parser.parse_args()
