import logging
import threading
from typing import Callable, List, Optional

log = logging.getLogger("appulse.overlay")

class OverlayService:
    """External overlay renderer (uses a transparent Tk window)."""

    def __init__(self) -> None:
        self._thread: Optional[threading.Thread] = None
        self._draw_hooks: List[Callable] = []
        self._running = False

    def add_draw_hook(self, fn: Callable) -> None:
        self._draw_hooks.append(fn)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._render_loop, daemon=True)
        self._thread.start()
        log.info("overlay thread started")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _render_loop(self) -> None:
        # Placeholder: real overlay uses customtkinter over a layered window.
        import time
        while self._running:
            for hook in self._draw_hooks:
                try:
                    hook()
                except Exception:
                    log.exception("draw hook failed")
            time.sleep(1.0 / 60.0)