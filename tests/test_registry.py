from appulse.host.registry import ExtensionRegistry
from appulse.contracts.extension import ExtensionContract

class _Dummy(ExtensionContract):
    name = "dummy"
    version = "0.0.1"
    def on_boot(self, host): pass
    def on_tick(self, host): pass

def test_register_and_get():
    reg = ExtensionRegistry()
    reg.register(_Dummy())
    assert len(reg) == 1
    assert reg.get("dummy") is not None

def test_duplicate_rejected():
    reg = ExtensionRegistry()
    reg.register(_Dummy())
    try:
        reg.register(_Dummy())
    except ValueError:
        return
    raise AssertionError("duplicate registration should raise")