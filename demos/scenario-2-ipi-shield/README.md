# Scenario 2 — IPI Shield Only

**Use case:** Simulates malicious content injected into a document store, knowledge base,
or RAG pipeline. The code itself is clean — no secrets, no backdoors. The danger is
entirely in the text content that an LLM would consume.

## Expected Results

### 🛡️ IPI Shield — CRITICAL
- **Agent:** Pre-flight Scanner
- **Patterns:** `ignore_previous`, `jailbreak` (DAN), `print_system_prompt`, `exfiltration`
- **Finding:** Multiple injection categories detected in retrieved content

### ☠️ DeadWire — ✅ CLEAN
- No secrets, no suspicious code, no supply chain issues
- Scan completes, no findings posted, commit status: success

## Only IPI Shield blocks this PR. DeadWire gives it the green light.
