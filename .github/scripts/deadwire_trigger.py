"""
DeadWire trigger script — dispatches PR scan to the DeadWire scanner repo.
Runs inside GitHub Actions on pull_request events.
"""
import json
import os
import sys
import urllib.request
import urllib.error

dispatch_token = os.environ["DISPATCH_TOKEN"]
repo = os.environ.get("REPO", "")
pr_number = os.environ.get("PR_NUMBER", "")
head_sha = os.environ.get("HEAD_SHA", "") or ""

payload = {
    "event_type": "deadwire-scan",
    "client_payload": {
        "target_repo": repo,
        "target_pr_number": pr_number,
        "head_sha": head_sha,
        "event_type": "pull_request",
    }
}

req = urllib.request.Request(
    "https://api.github.com/repos/RainFirestorm/deadwire/dispatches",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": f"Bearer {dispatch_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "DeadWire-Trigger/1.0",
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        source = f"PR #{pr_number}" if pr_number else repo
        print(f"[DeadWire] Scan triggered for {source} — HTTP {resp.status}")
except urllib.error.HTTPError as e:
    print(f"[DeadWire] Trigger failed: {e.code} {e.read().decode()}")
    sys.exit(1)
