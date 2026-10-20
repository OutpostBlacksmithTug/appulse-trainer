from dataclasses import dataclass, field
from typing import Dict, List

from appulse.models.player import PlayerSnapshot
from appulse.models.entity import Entity

@dataclass
class GameState:
    local_player: PlayerSnapshot | None = None
    entities: List[Entity] = field(default_factory=list)
    module_base: int = 0
    tick: int = 0
    extras: Dict[str, float] = field(default_factory=dict)

    def is_ready(self) -> bool:
        return self.local_player is not None and self.module_base != 0