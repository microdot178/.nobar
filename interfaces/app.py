from abc import ABC, abstractmethod
from typing import Any, List, Optional

import i3ipc
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent


class AppABC(ABC):
    @property
    @abstractmethod
    def i3(self) -> Optional[Connection]:
        pass

    @property
    @abstractmethod
    def connection(self) -> i3ipc.Connection:
        pass

    @property
    @abstractmethod
    def widgets(self) -> List[Any]:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    def event_handler(self, conn: Connection, event: IpcBaseEvent) -> None:
        pass

    @abstractmethod
    def on_tick(self, conn: Connection, event: IpcBaseEvent) -> None:
        pass
