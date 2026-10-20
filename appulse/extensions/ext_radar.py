from appulse.contracts.extension import ExtensionContract
from appulse.host.registry import ExtensionRegistry

class RadarExtension(ExtensionContract):
    name = "radar"
    version = "0.9.4"
    enabled = True

    def on_boot(self, host) -> None:
        self._range = 5000.0
        self._blips = []

    def on_tick(self, host) -> None:
        state = getattr(host, "state", None)
        if state is None or not state.is_ready():
            return
        local = state.local_player
        self._blips = [
            (e.pos_x - local.pos_x, e.pos_y - local.pos_y)
            for e in state.entities
            if not e.same_team(local.team) and e.hp > 0
        ]

    def blips(self):
        return list(self._blips)

def register(registry: ExtensionRegistry) -> None:
    registry.register(RadarExtension())