import os

import tomllib

DEFAULT_CONFIG = """
[workspaces]
height = 40
color = 'gray'
focused = 'white'
background = 'black'
position = [0, 0]
fade_out = 5000

[info]
height = 40
color = 'white'
background = 'black'
position = ['right', 0]
fade_out_on_hover = true
"""


class Config:
    def __init__(self, config_filename=None):
        self.config = self.get_config(config_filename)

    def get_config(self, config_filename):
        if not os.path.exists(config_filename):
            self.create_default_config(config_filename)

            print(f"Created default configuration file: {config_filename}")

        with open(config_filename, "rb") as f:
            config = tomllib.load(f)

            print(f"Loaded configuration file: {config_filename}")

        return config

    def create_default_config(self, config_filename):
        with open(config_filename, "w") as f:
            f.write(DEFAULT_CONFIG)
