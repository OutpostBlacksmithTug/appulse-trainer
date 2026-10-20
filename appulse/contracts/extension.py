from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from appulse.host.engine import TrainerHost

class ExtensionContract(ABC):
    """Every Appulse extension implements this interface."""

    name: str = "unnamed"
    version: str = "0.0.0"
    enabled: bool = True

    @abstractmethod
    def on_boot(self, host: "TrainerHost") -> None: ...

    @abstractmethod
    def on_tick(self, host: "TrainerHost") -> None: ...

    def on_shutdown(self, host: "TrainerHost") -> None:
        pass

    def on_event(self, event: str, payload: dict[str, Any]) -> None:
        pass