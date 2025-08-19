from abc import ABC, ABCMeta, abstractmethod

from PyQt6.QtWidgets import QWidget


class PanelMeta(ABCMeta, type(QWidget)):
    pass


class PanelABC(ABC):
    @abstractmethod
    def read_config(self, config):
        pass

    @abstractmethod
    def set_auto_hide_timer(self, delay_seconds: int):
        pass

    @abstractmethod
    def set_position(self):
        pass

    @abstractmethod
    def process_event(self, event):
        pass
