from typing import Dict, Iterator, Optional
from appulse.contracts.extension import ExtensionContract

class ExtensionRegistry:
    """Central registry of loaded extension contracts."""

    def __init__(self) -> None:
        self._extensions: Dict[str, ExtensionContract] = {}

    def register(self, ext: ExtensionContract) -> None:
        if ext.name in self._extensions:
            raise ValueError(f"duplicate extension: {ext.name}")
        self._extensions[ext.name] = ext

    def get(self, name: str) -> Optional[ExtensionContract]:
        return self._extensions.get(name)

    def all(self) -> Iterator[ExtensionContract]:
        return iter(self._extensions.values())

    def __len__(self) -> int:
        return len(self._extensions)