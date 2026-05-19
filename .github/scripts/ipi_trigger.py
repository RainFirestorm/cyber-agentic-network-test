"""
IPI Shield trigger script — fetches PR/issue content and dispatches to IPI Shield.
Runs inside GitHub Actions on pull_request and issues events.
"""
import json
import os
import sys
import urllib.request
import urllib.error

token = os.environ["GH_TOKEN"]          # built-in GITHUB_TOKEN — reads own repo
dispatch_token = os.environ["DISPATCH_TOKEN"]  # DEADWIRE_PAT — cross-repo dispatch
event = os.environ.get("EVENT_NAME", "")
repo = os.environ.get("REPO", "")
is_pr = event == "pull_request"


def gh_get(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "IPI-Shield-Trigger/1.0",
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


if is_pr:
    pr_number = os.environ.get("PR_NUMBER", "")
    title = os.environ.get("PR_TITLE", "") or ""
    body = os.environ.get("PR_BODY", "") or ""
    head_sha = os.environ.get("HEAD_SHA", "") or ""

    # Fetch changed files and their diffs
    try:
        files = gh_get(f"/repos/{repo}/pulls/{pr_number}/files")
        diff_sections = []
        for f in files[:20]:
            filename = f.get("filename", "")
            patch = f.get("patch", "")
            if patch:
                diff_sections.append(f"--- {filename} ---\n{patch}")
        diff_content = "\n\n".join(diff_sections)
    except Exception as e:
        print(f"[IPI Shield] Warning: could not fetch diff: {e}")
        diff_content = ""

    content = f"PR Title: {title}\n\nPR Description:\n{body}\n\n--- CHANGED FILES (DIFF) ---\n{diff_content}"
    source = f"PR #{pr_number}: {title}"
    output_mode = "pr_comment"

else:
    title = os.environ.get("ISSUE_TITLE", "") or ""
    body = os.environ.get("ISSUE_BODY", "") or ""
    pr_number = ""
    content = f"Issue Title: {title}\n\nIssue Body:\n{body}"
    source = f"Issue: {title}"
    output_mode = "github_issue"

payload = {
    "event_type": "ipi-scan",
    "client_payload": {
        "scan_content": content[:8000],
        "scan_source": source[:200],
        "target_repo": "RainFirestorm/cyber-agentic-network-test",
        "output_mode": output_mode,
        "pr_number": pr_number,
        "head_sha": head_sha,
    }
}

req = urllib.request.Request(
    "https://api.github.com/repos/RainFirestorm/ipi-shield/dispatches",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": f"Bearer {dispatch_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "IPI-Shield-Trigger/1.0",
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print(f"[IPI Shield] Scan triggered for {source} — HTTP {resp.status}")
except urllib.error.HTTPError as e:
    print(f"[IPI Shield] Trigger failed: {e.code} {e.read().decode()}")
    sys.exit(1)
