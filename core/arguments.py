import argparse


class Arguments:
    def __init__(self):
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
            help="Array of active widget",
        )

        self.arguments = self.parser.parse_args()
