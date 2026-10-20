from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml

@dataclass
class Settings:
    profile: str = "default"
    target_process: str = "game.exe"
    extensions_dir: Path = Path("appulse/extensions")
    tick_hz: int = 120
    overlay_enabled: bool = True
    enabled_extensions: List[str] = field(default_factory=list)
    offsets: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "Settings":
        if not path.exists():
            return cls()
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        settings = cls()
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        if isinstance(settings.extensions_dir, str):
            settings.extensions_dir = Path(settings.extensions_dir)
        return settings