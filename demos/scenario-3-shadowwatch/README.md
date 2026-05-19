# Scenario 4 — ShadowWatch Only: Behavioral Anomaly

## What This Tests

A contributor with a normal history suddenly accesses **three sensitive path categories simultaneously** in a single PR. The code is clean — no secrets, no injection. DeadWire and IPI Shield both pass. ShadowWatch fires.

## Expected Results

| Scanner | Result | Why |
|---------|--------|-----|
| ☠️ DeadWire | ✅ Clean | No secrets, backdoors, or supply chain issues |
| 🛡️ IPI Shield | ✅ Clean | No injection language anywhere |
| 👁️ ShadowWatch | 🔴 CRITICAL/HIGH | Multi-category sensitive access: auth + config + deploy simultaneously |

## Attack Vector Simulated

**Privilege escalation pattern** — a compromised or malicious insider account making a wide-scope change across authentication, configuration, and deployment infrastructure in a single commit. Each individual path might be explainable; the combination is the signal.

## What ShadowWatch Sees

- `auth/` directory accessed (sensitive category: authentication)
- `config/` directory accessed (sensitive category: configuration)
- `deploy/` directory accessed (sensitive category: deployment)
- 3 sensitive categories in one PR → `MULTI_SENSITIVE_CATEGORY_ACCESS` signal
- If contributor has no prior history in these paths → `NEW_SENSITIVE_PATH_ACCESS` signal

## Files

- `auth/session_handler.py` — clean session management code
- `config/database_config.py` — clean database configuration loader
- `deploy/startup.py` — clean deployment bootstrap script
