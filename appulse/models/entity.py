from dataclasses import dataclass

@dataclass
class Entity:
    address: int
    name: str = ""
    hp: int = 0
    team: int = 0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    distance: float = 0.0

    def same_team(self, other_team: int) -> bool:
        return self.team == other_team