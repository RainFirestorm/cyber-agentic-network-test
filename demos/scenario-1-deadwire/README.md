# Scenario 3 — DeadWire Only

**Use case:** Simulates a backdoored dependency update and compromised config file —
the kind of change that passes a normal code review but hides malicious intent.
Zero injection language anywhere in the content.

## Expected Results

### ☠️ DeadWire — CRITICAL
- **Agent:** Secret Scanner — exposed API token in config
- **Agent:** Commit Analyst — base64-encoded payload decoded and executed, subprocess
  spawning curl with credentials to external URL
- **Agent:** Supply Chain Checker — typosquatted packages in requirements.txt

### 🛡️ IPI Shield — ✅ CLEAN
- No prompt injection patterns, no role hijacking, no exfiltration triggers in content
- Scan completes, no findings posted, commit status: success

## Only DeadWire blocks this PR. IPI Shield gives it the green light.
