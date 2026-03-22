"""CLI argument parsing for nobar."""

from __future__ import annotations

import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse and return CLI arguments."""
    parser = argparse.ArgumentParser(
        description="nobar - a PyQt6 widget system for i3wm",
    )

    parser.add_argument(
        "config",
        help="Path to configuration file (e.g., ~/.config/nobar/config.toml)",
    )

    parser.add_argument(
        "--widgets",
        nargs="*",
        help="Array of active widget names",
    )

    return parser.parse_args()
