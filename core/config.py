import tomllib
import os

DEFAULT_CONFIG = """
[workspaces]
height = 50
color = 'gray'
focused = 'white'
background = 'black'
position = [0, 0]

[info]
height = 50
color = 'white'
background = 'black'
position = ['right', 0]
"""


def create_default_config(config_filename):
    with open(config_filename, "w") as f:
        f.write(DEFAULT_CONFIG)


def get_config(config_filename):
    if not os.path.exists(config_filename):
        create_default_config(config_filename)
        print(f"Created default configuration file: {config_filename}")

    with open(config_filename, "rb") as f:
        config = tomllib.load(f)

    return config
