from abc import ABC, ABCMeta, abstractmethod

from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QWidget


class PanelMeta(ABCMeta, type(QWidget)):
    pass


class PanelABC(ABC):
    @abstractmethod
    def read_config(self, config: dict) -> None:
        pass

    @abstractmethod
    def set_auto_hide_timer(self, delay_seconds: int) -> None:
        pass

    @abstractmethod
    def set_position(self) -> None:
        pass

    @abstractmethod
    def set_content(self) -> None:
        pass

    @abstractmethod
    def process_event(self, event: IpcBaseEvent) -> None:
        pass

    @abstractmethod
    def enterEvent(self, event: QEnterEvent | None) -> None:
        pass

    @abstractmethod
    def leaveEvent(self, a0: QEvent | None) -> None:
        pass
