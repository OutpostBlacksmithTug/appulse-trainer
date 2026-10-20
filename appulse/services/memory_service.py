import ctypes
import logging
from typing import Iterable

from appulse.services.process_service import ProcessService

log = logging.getLogger("appulse.memory")

class MemoryService:
    """Read/write helpers exposed to extensions."""

    def __init__(self, process: ProcessService) -> None:
        self.process = process

    def read(self, address: int, size: int) -> bytes:
        pm = self.process._pm  # noqa: SLF001 - internal access by design
        if pm is None:
            raise RuntimeError("not attached")
        return pm.read_bytes(address, size)

    def read_int(self, address: int) -> int:
        return int.from_bytes(self.read(address, 4), "little", signed=True)

    def read_float(self, address: int) -> float:
        return ctypes.c_float.from_buffer_copy(self.read(address, 4)).value

    def write_int(self, address: int, value: int) -> None:
        pm = self.process._pm  # noqa: SLF001
        if pm is None:
            raise RuntimeError("not attached")
        pm.write_int(address, value)

    def write_float(self, address: int, value: float) -> None:
        pm = self.process._pm  # noqa: SLF001
        if pm is None:
            raise RuntimeError("not attached")
        pm.write_float(address, value)

    def read_chain(self, base: int, offsets: Iterable[int]) -> int:
        addr = base
        offs = list(offsets)
        for off in offs[:-1]:
            addr = self.read_int(addr + off)
        return addr + offs[-1]

    def detach(self) -> None:
        pass