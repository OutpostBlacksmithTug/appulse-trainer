import logging
from typing import Optional

log = logging.getLogger("appulse.sigscan")

class SignatureScanner:
    """Pattern scan helper for locating engine offsets at runtime."""

    def __init__(self, memory) -> None:
        self.memory = memory

    @staticmethod
    def compile_pattern(pat: str) -> bytes:
        return bytes(
            int(b, 16) if b != "?" else 0 for b in pat.split()
        )

    def find(self, module_base: int, size: int, pattern: str) -> Optional[int]:
        needle = self.compile_pattern(pattern)
        haystack = self.memory.read(module_base, size)
        idx = haystack.find(needle)
        if idx < 0:
            log.debug("pattern not found: %s", pattern)
            return None
        return module_base + idx