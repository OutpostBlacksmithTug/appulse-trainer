import logging
from typing import Optional

import pymem
import psutil

log = logging.getLogger("appulse.process")

class ProcessService:
    """Wraps process attach/detach and module enumeration."""

    def __init__(self) -> None:
        self._pm: Optional[pymem.Pymem] = None
        self._pid: Optional[int] = None

    def attach(self, name: str) -> None:
        try:
            self._pm = pymem.Pymem(name)
            self._pid = self._pm.process_id
            log.info("attached to %s (pid=%d)", name, self._pid)
        except pymem.exception.ProcessNotFound:
            log.error("target process not found: %s", name)
            raise

    def module_base(self, module: str) -> int:
        if self._pm is None:
            raise RuntimeError("not attached")
        return pymem.process.module_from_name(self._pm.process_handle, module).lpBaseOfDll

    def detach(self) -> None:
        if self._pm is not None:
            try:
                self._pm.close_process()
            except Exception:
                pass
        self._pm = None
        self._pid = None

    @property
    def pid(self) -> Optional[int]:
        return self._pid