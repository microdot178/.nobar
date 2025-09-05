from modules.info import Info
from modules.workspaces import Workspaces


class Widgets:
    def __init__(self, arguments, connection, config):
        self.widgets = []

        widget_list = arguments.widgets or ["all"]

        if "workspaces" in widget_list or "all" in widget_list:
            self.widgets.append(Workspaces(connection, config["workspaces"]))

        if "info" in widget_list or "all" in widget_list:
            self.widgets.append(Info(connection, config["info"]))
