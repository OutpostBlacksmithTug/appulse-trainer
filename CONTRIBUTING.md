# Contributing to Appulse Trainer

Thanks for wanting to hack on Appulse Trainer. This project is a modular
Python trainer host: the core (`appulse/host/`) stays small, and everything
game-specific lives in `appulse/extensions/ext_*.py`.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m appulse.bootstrap
```

## Adding an extension

1. Drop a file into `appulse/extensions/` named `ext_<feature>.py`.
2. Subclass `appulse.contracts.extension.ExtensionContract`.
3. Implement `on_boot` and `on_tick`, optionally `on_shutdown` / `on_event`.
4. Export `register(registry)` that calls `registry.register(YourExt())`.
5. Enable it in `config/appulse.yaml` under `enabled_extensions`.

Extensions must be idempotent on `on_tick` and must never raise — the host
logs and continues, but noisy exceptions will get your PR rejected.

## Style

- Python 3.11+, type hints on public functions.
- Keep extension files under ~200 lines. If it grows, split into a package.
- No hardcoded offsets in extensions — put them in `config/appulse.yaml`.

## Tests

```bash
pytest tests/
```

## Responsible use

Appulse Trainer is for offline / private-server tinkering and reverse
engineering education. Do not use it on live matchmaking services. Use at
your own risk; the maintainers take no responsibility for bans.
</analysis>