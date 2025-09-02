from abc import ABC, abstractmethod

from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent


class AppABC(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    def event_handler(self, conn: Connection, event: IpcBaseEvent) -> None:
        pass

    @abstractmethod
    def on_tick(self, conn: Connection, event: IpcBaseEvent) -> None:
        pass
