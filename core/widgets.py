from modules.info import Info
from modules.workspaces import Workspaces


class Widgets:
    def __init__(self, arguments, connection, config):
        self.widgets = []

        if "workspaces" in arguments.widgets:
            self.widgets.append(Workspaces(connection, config["workspaces"]))

        if "info" in arguments.widgets:
            self.widgets.append(Info(connection, config["info"]))
