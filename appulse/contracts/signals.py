import logging
from collections import defaultdict
from typing import Any, Callable, DefaultDict, List

log = logging.getLogger("appulse.signals")

Handler = Callable[[dict[str, Any]], None]

class SignalBus:
    """Tiny pub/sub used by extensions to communicate without imports."""

    def __init__(self) -> None:
        self._subs: DefaultDict[str, List[Handler]] = defaultdict(list)

    def subscribe(self, topic: str, fn: Handler) -> None:
        self._subs[topic].append(fn)

    def emit(self, topic: str, payload: dict[str, Any]) -> None:
        for fn in list(self._subs.get(topic, ())):
            try:
                fn(payload)
            except Exception:
                log.exception("signal handler failed for %s", topic)