#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def try_git(*args: str) -> str | None:
    try:
        return git(*args)
    except subprocess.CalledProcessError:
        return None


def choose_base_ref(explicit: str | None) -> str:
    if explicit:
        return explicit
    candidates = ["origin/HEAD", "origin/main", "origin/master", "main", "master"]
    for candidate in candidates:
        if try_git("rev-parse", "--verify", candidate):
            return candidate
    return "HEAD~1"


def bucket_path(path: str) -> str:
    p = path.lower()
    if p.startswith(".github/workflows/") or "/workflows/" in p:
        return "workflow"
    if p.endswith(("dockerfile", ".dockerfile")) or "/docker/" in p:
        return "container"
    if p.startswith(".github/") or p.endswith((".yml", ".yaml")) and ("ci" in p or "release" in p):
        return "automation"
    if any(part in p for part in ("auth", "login", "session", "permission", "policy", "acl")):
        return "auth"
    if any(part in p for part in ("api", "route", "handler", "controller", "middleware", "server")):
        return "request-handling"
    if any(part in p for part in ("query", "sql", "db", "database", "model", "repository")):
        return "data"
    if any(part in p for part in ("template", "view", "html", "jsx", "tsx", "markdown")):
        return "rendering"
    if any(part in p for part in ("test", "spec", "fixture", "__snapshots__")):
        return "tests"
    return "other"


def main() -> int:
    explicit_base = sys.argv[1] if len(sys.argv) > 1 else None
    repo_root = git("rev-parse", "--show-toplevel")
    base_ref = choose_base_ref(explicit_base)
    merge_base = git("merge-base", base_ref, "HEAD")

    changed_files = [line for line in git("diff", "--name-only", f"{merge_base}..HEAD").splitlines() if line]
    commits = [line for line in git("log", "--no-decorate", "--oneline", f"{merge_base}..HEAD").splitlines() if line]
    diff_stat = git("diff", "--stat", "--find-renames", f"{merge_base}..HEAD")
    status = git("status", "--short")

    buckets: dict[str, list[str]] = {}
    for path in changed_files:
        bucket = bucket_path(path)
        buckets.setdefault(bucket, []).append(path)

    payload = {
        "repo_root": repo_root,
        "repo_name": Path(repo_root).name,
        "current_branch": git("branch", "--show-current"),
        "base_ref": base_ref,
        "merge_base": merge_base,
        "changed_files": changed_files,
        "changed_file_count": len(changed_files),
        "buckets": buckets,
        "commits": commits,
        "worktree_status": status.splitlines() if status else [],
        "diff_stat": diff_stat.splitlines(),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
