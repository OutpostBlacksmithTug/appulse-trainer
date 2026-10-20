import logging
import threading
import time
from typing import Dict, List

from appulse.host.loader import ExtensionLoader
from appulse.host.registry import ExtensionRegistry
from appulse.contracts.extension import ExtensionContract
from appulse.config.settings import Settings
from appulse.services.process_service import ProcessService
from appulse.services.memory_service import MemoryService

log = logging.getLogger("appulse.host")

class TrainerHost:
    """Core host: owns services, extension registry and the tick loop."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.registry = ExtensionRegistry()
        self.loader = ExtensionLoader(self.registry, settings.extensions_dir)
        self.process_service = ProcessService()
        self.memory_service = MemoryService(self.process_service)
        self._stop = threading.Event()
        self._tick_hz = settings.tick_hz

    def boot(self) -> None:
        log.info("attaching to target %s", self.settings.target_process)
        self.process_service.attach(self.settings.target_process)
        self.loader.discover()
        self.loader.load_all()
        for ext in self.registry.all():
            ext.on_boot(self)
            log.info("extension loaded: %s v%s", ext.name, ext.version)

    def run_loop(self) -> None:
        interval = 1.0 / max(1, self._tick_hz)
        while not self._stop.is_set():
            started = time.perf_counter()
            for ext in self.registry.all():
                if ext.enabled:
                    try:
                        ext.on_tick(self)
                    except Exception as exc:  # keep host alive
                        log.exception("extension %s tick failed: %s", ext.name, exc)
            elapsed = time.perf_counter() - started
            sleep_for = max(0.0, interval - elapsed)
            self._stop.wait(sleep_for)

    def shutdown(self) -> None:
        self._stop.set()
        for ext in self.registry.all():
            try:
                ext.on_shutdown(self)
            except Exception:
                log.exception("shutdown failed for %s", ext.name)
        self.memory_service.detach()
        self.process_service.detach()