import sys
import logging
from pathlib import Path
from appulse.host.engine import TrainerHost
from appulse.config.settings import Settings

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    log = logging.getLogger("appulse.bootstrap")

    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config/appulse.yaml")
    settings = Settings.load(cfg_path)
    log.info("Appulse Trainer %s starting, profile=%s", "2.4.1", settings.profile)

    host = TrainerHost(settings)
    try:
        host.boot()
        host.run_loop()
    except KeyboardInterrupt:
        log.info("shutdown requested")
    finally:
        host.shutdown()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())