# Scenario 4 — All Three Scanners: Full Platform Alert

## What This Tests

The worst-case scenario. A single PR that triggers all three security gates simultaneously. This is the "everything is on fire" demo — an attacker (or compromised insider) who has embedded a prompt injection payload, hardcoded credentials, AND accessed sensitive infrastructure paths.

## Expected Results

| Scanner | Result | Why |
|---------|--------|-----|
| ☠️ DeadWire | 🔴 CRITICAL | Hardcoded AWS credential in auth infrastructure code |
| 🛡️ IPI Shield | 🔴 CRITICAL | Prompt injection payload targeting LLM pipeline embedded in docstring |
| 👁️ ShadowWatch | 🔴 HIGH/CRITICAL | New sensitive path access (auth/) + multi-category sensitive access |

## Attack Vector Simulated

**Full-spectrum compromise** — simulates a sophisticated attack where the threat actor:
1. Embeds a prompt injection payload in a docstring (targeting any LLM that processes the code)
2. Hardcodes exfiltration credentials to establish a persistence mechanism
3. Places the malicious code in authentication infrastructure to maximize blast radius

All three layers of the platform must fire to catch the full threat surface.

## Files

- `auth/compromised_handler.py` — contains all three attack vectors in one file
