from modules.info import Info
from modules.workspaces import Workspaces


class Widgets:
    def __init__(self, arguments, connection, config):
        self.widgets = []

        widgets_list = arguments.widgets or ["all"]

        if "workspaces" in widgets_list or "all" in widgets_list:
            self.widgets.append(Workspaces(connection, config["workspaces"]))

        if "info" in widgets_list or "all" in widgets_list:
            self.widgets.append(Info(connection, config["info"]))
