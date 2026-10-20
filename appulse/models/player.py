from dataclasses import dataclass

@dataclass
class PlayerSnapshot:
    hp: int = 0
    max_hp: int = 0
    armor: int = 0
    team: int = 0
    ammo: int = 0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    view_yaw: float = 0.0
    view_pitch: float = 0.0

    @property
    def alive(self) -> bool:
        return self.hp > 0