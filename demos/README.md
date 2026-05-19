# CAN Security Gate — Demo Scenarios

Three scenarios that demonstrate the dual security gate catching different attack types.
Each scenario lives in its own folder. To run a demo, open a PR that adds the payload file
somewhere **outside** the `demos/` folder — the scanners analyze what changed in the PR diff.

---

## How to Run Any Demo

```bash
# 1. Create a demo branch
git checkout main
git pull
git checkout -b demo/scenario-1

# 2. Copy the payload to a location outside demos/
cp demos/scenario-1-both-scanners/payload.py test_payload.py

# 3. Commit and push
git add test_payload.py
git commit -m "test: scenario 1 demo"
git push origin demo/scenario-1

# 4. Open a PR against main — both scanners fire automatically
gh pr create --title "Demo: Scenario 1" --body "Security gate demo"
```

---

## The Three Scenarios

| Scenario | IPI Shield | DeadWire | What triggers it |
|----------|-----------|----------|-----------------|
| [1 — Both Scanners](./scenario-1-both-scanners/) | 🔴 CRITICAL | 🔴 CRITICAL | Injection payload + exposed credential |
| [2 — IPI Shield Only](./scenario-2-ipi-shield-only/) | 🔴 CRITICAL | ✅ Clean | Pure prompt injection, no code issues |
| [3 — DeadWire Only](./scenario-3-deadwire-only/) | ✅ Clean | 🔴 CRITICAL | Secrets + supply chain, no injection |

---

> These files exist for demonstration purposes only. No credentials are real.
