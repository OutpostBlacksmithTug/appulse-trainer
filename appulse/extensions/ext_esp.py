from appulse.contracts.extension import ExtensionContract
from appulse.host.registry import ExtensionRegistry
from appulse.utils.math_helpers import world_to_screen

class EspExtension(ExtensionContract):
    name = "esp"
    version = "2.0.1"

    def __init__(self) -> None:
        self.box_color = (0, 255, 120)
        self.draw_hooked = False

    def on_boot(self, host) -> None:
        overlay = getattr(host, "overlay", None)
        if overlay is not None and not self.draw_hooked:
            overlay.add_draw_hook(self._draw)
            self.draw_hooked = True

    def _draw(self) -> None:
        pass  # rendering handled by overlay service using cached state

    def on_tick(self, host) -> None:
        state = getattr(host, "state", None)
        if state is None or not state.is_ready():
            return
        local = state.local_player
        for ent in state.entities:
            if ent.same_team(local.team) or ent.hp <= 0:
                continue
            sx, sy, ok = world_to_screen(
                ent.pos_x, ent.pos_y, ent.pos_z,
                local.pos_x, local.pos_y, local.pos_z,
                local.view_yaw, local.view_pitch,
                90.0, 1920, 1080,
            )
            if ok:
                ent.distance = sx  # cached for overlay draw pass

def register(registry: ExtensionRegistry) -> None:
    registry.register(EspExtension())