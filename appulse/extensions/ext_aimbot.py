from appulse.contracts.extension import ExtensionContract
from appulse.host.registry import ExtensionRegistry
from appulse.utils.math_helpers import world_to_screen

class AimbotExtension(ExtensionContract):
    name = "aimbot"
    version = "1.3.0"

    def __init__(self) -> None:
        self.smoothing = 0.35
        self.fov = 90.0
        self.target_index = -1

    def on_boot(self, host) -> None:
        host.process_service.attach(host.settings.target_process)

    def on_tick(self, host) -> None:
        state = getattr(host, "state", None)
        if state is None or not state.is_ready():
            return
        local = state.local_player
        best = None
        best_dist = 1e9
        for idx, ent in enumerate(state.entities):
            if ent.same_team(local.team) or ent.hp <= 0:
                continue
            sx, sy, visible = world_to_screen(
                ent.pos_x, ent.pos_y, ent.pos_z,
                local.pos_x, local.pos_y, local.pos_z,
                local.view_yaw, local.view_pitch,
                self.fov, 1920, 1080,
            )
            if not visible:
                continue
            dist = (ent.pos_x - local.pos_x) ** 2 + (ent.pos_y - local.pos_y) ** 2
            if dist < best_dist:
                best_dist = dist
                best = idx
        self.target_index = best if best is not None else -1

def register(registry: ExtensionRegistry) -> None:
    registry.register(AimbotExtension())