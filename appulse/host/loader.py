import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import List

from appulse.host.registry import ExtensionRegistry
from appulse.contracts.extension import ExtensionContract

log = logging.getLogger("appulse.loader")

class ExtensionLoader:
    """Discovers and imports extension modules from a directory."""

    def __init__(self, registry: ExtensionRegistry, extensions_dir: Path) -> None:
        self.registry = registry
        self.extensions_dir = Path(extensions_dir)
        self._modules: List[ModuleType] = []

    def discover(self) -> List[Path]:
        if not self.extensions_dir.exists():
            log.warning("extensions dir missing: %s", self.extensions_dir)
            return []
        return sorted(
            p for p in self.extensions_dir.glob("ext_*.py") if p.is_file()
        )

    def load_all(self) -> None:
        for path in self.discover():
            self._load_one(path)

    def _load_one(self, path: Path) -> None:
        mod_name = f"appulse.ext.{path.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, path)
        if spec is None or spec.loader is None:
            log.error("cannot build spec for %s", path)
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            log.exception("import failed: %s", path)
            return
        self._modules.append(module)
        register = getattr(module, "register", None)
        if callable(register):
            register(self.registry)
        else:
            log.warning("no register() in %s", path.name)