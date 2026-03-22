"""TOML configuration loader."""

from __future__ import annotations

from pathlib import Path

import tomllib

DEFAULT_CONFIG = """\
[workspaces]
height = 40
color = 'gray'
focused = 'white'
background = 'black'
position = [0, 0]
screen = 0
fade_out = 5000

[info]
height = 40
color = 'white'
background = 'black'
position = ['right', 0]
screen = 0
fade_out_on_hover = true
"""


def load_config(path: str) -> dict:
    """Load TOML config, creating default if missing."""
    config_path = Path(path)

    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG)
        print(f"Created default configuration file: {path}")

    with config_path.open("rb") as f:
        config = tomllib.load(f)

    print(f"Loaded configuration file: {path}")
    return config
