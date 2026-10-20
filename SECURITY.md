# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 2.4.x   | yes       |
| 2.3.x   | security fixes only |
| < 2.3   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub or email
`security@appulse-trainer.invalid`. Do not file public issues for memory
corruption, arbitrary code execution, or loader bypass problems.

We aim to acknowledge reports within 72 hours. Because Appulse Trainer
attaches to other processes, we treat any input that reaches `MemoryService`
or `ExtensionLoader` as security-relevant.

## Scope

In scope:
- `appulse/host/loader.py` (arbitrary import via crafted extension file)
- `appulse/services/memory_service.py` (bounds checks on reads/writes)
- `appulse/config/settings.py` (YAML deserialization)

Out of scope:
- Anti-cheat detection, bans, or account loss on third-party services
- Issues requiring the user to run extensions from untrusted sources

## Safe harbor

Reverse engineering, modding, and offline training use of Appulse Trainer
are considered legitimate. We will not cooperate with requests to disclose
user identities based solely on usage of this project.