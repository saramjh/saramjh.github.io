#!/usr/bin/env python3
"""Read the prior successful Pages deployment before a new blog release.

This only reads the owner's GitHub release history. No search-provider calls.
If exact predecessor evidence is missing, the notifier remains disabled.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

REPOSITORY = "saramjh/saramjh.github.io"
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
API_ROOT = "https://api.github.com"


def github_json(path: str, token: str) -> object:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dev-pages-predecessor-guard",
        },
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.load(response)


def resolve_previous_successful_deployment(
    target_sha: str,
    fetch,
    is_ancestor,
) -> tuple[str, int] | None:
    """Choose the most recent successful deployment, never an arbitrary parent.

    The existing Pages workflow serializes main releases. Identical predecessor
    and target SHAs yield a safe empty changed-URL list rather than a replay.
    """
    if not SHA_RE.fullmatch(target_sha or ""):
        return None
    deployments = fetch(
        f"/repos/{REPOSITORY}/deployments?environment=github-pages&per_page=30"
    )
    if not isinstance(deployments, list):
        return None
    for deployment in deployments:
        if not isinstance(deployment, dict):
            return None
        if deployment.get("environment") != "github-pages" or deployment.get("ref") != "main":
            continue
        sha = deployment.get("sha", "")
        deployment_id = deployment.get("id")
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            return None
        if not isinstance(deployment_id, int) or deployment_id <= 0:
            return None
        statuses = fetch(
            f"/repos/{REPOSITORY}/deployments/{deployment_id}/statuses?per_page=1"
        )
        if not isinstance(statuses, list) or not statuses:
            return None
        if not isinstance(statuses[0], dict):
            return None
        if statuses[0].get("state") != "success":
            continue
        if sha == target_sha or is_ancestor(sha, target_sha):
            return sha, deployment_id
        return None
    return None


def _git_ancestor(before: str, after: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", before, after],
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def main() -> int:
    target = os.environ.get("GITHUB_SHA", "").strip().lower()
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    output = os.environ.get("GITHUB_OUTPUT", "")
    before = ""
    native_id = ""
    if repo != REPOSITORY or not token or not output:
        print("[Pages] Exact owner, token or output missing; release diff unverified.")
    else:
        try:
            result = resolve_previous_successful_deployment(
                target, lambda path: github_json(path, token), _git_ancestor
            )
            if result:
                before, native_id = result
                print(f"[Pages] Verified prior deployment id={native_id} sha={before}.")
            else:
                print("[Pages] No safe predecessor; notification remains skipped.")
        except (OSError, ValueError, TypeError, urllib.error.URLError, subprocess.SubprocessError) as exc:
            print(f"[Pages] Prior deployment unavailable ({type(exc).__name__}); fail closed.")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"before_sha={before}\n")
            handle.write(f"before_deployment_id={native_id}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
