---
name: security-review
description: Review a git diff, branch, or pull request for newly introduced, high-confidence security vulnerabilities. Use when the user asks for a security review, PR security pass, AppSec triage, exploitability check, or a low-noise audit of changed code, workflows, auth, input handling, secrets, or trust-boundary changes.
license: MIT
metadata:
  version: "1.0.0"
---

# Security Review

Review only newly introduced risk in the requested change set. Favor signal over coverage.

## Start

1. Confirm the review target: current branch diff, staged changes, a commit range, or a PR merge-base diff.
2. Gather git context first. If command execution is available, use `scripts/git_review_context.py` to collect a structured snapshot. Otherwise gather the equivalent context manually: changed files, commit list, base ref, and diffstat.
3. Inspect the changed files, not just the diff summary. Trace data flow from untrusted input to sensitive sinks and across trust boundaries.
4. Consult only the reference files that match the changed surface area.
5. Report only findings that are new in this change set and have a concrete attack path.

## Reference Map

- Read `references/review-checklist.md` for the core workflow.
- Read `references/web-and-api-findings.md` when the diff touches request handling, templates, auth, storage, serializers, file operations, shell execution, or outbound network calls.
- Read `references/workflow-and-supply-chain.md` when the diff touches `.github/workflows/`, CI scripts, release automation, containers, package publishing, or build tooling.
- Read `references/reporting-and-triage.md` before finalizing findings.

## Evidence Bar

Require all of the following before reporting a finding:

- A plausible attacker-controlled source or trust-boundary crossing.
- A reachable vulnerable sink, privilege boundary, or sensitive side effect.
- Missing, bypassed, or broken mitigation in the current code path.
- Evidence that the issue is introduced or materially worsened by the reviewed change.

Prefer changed lines plus the minimum surrounding code needed to prove exploitability.

## Focus Areas

Prioritize these categories:

- Injection with real attacker-controlled input: SQL, NoSQL, command, template, path traversal, XXE, unsafe deserialization.
- Broken authentication or authorization: missing permission checks, BOLA or IDOR, tenant-boundary leaks, privilege escalation, token or session flaws.
- Sensitive data exposure: secrets or PII newly logged, returned, persisted, or sent to third parties.
- Cryptographic trust failures: verification bypasses, weak randomness for secrets or tokens, insecure key handling.
- CI/CD and supply chain issues: untrusted workflow interpolation, dangerous `pull_request_target` flows, excessive token permissions with untrusted triggers, privileged third-party action risk.
- SSRF only when attacker input can influence host, scheme, or a sensitive internal target.
- XSS only when the change introduces an unsafe sink or disables framework protections.

## Noise Filters

Do not report:

- Pre-existing issues unless the change makes them exploitable or materially worse.
- Generic hardening advice without a concrete exploit path.
- Dependency age or upgrade advice by itself.
- Pure client-side missing auth checks with no server impact.
- Tests or docs unless they change live execution behavior.

## Output

Return only high-signal findings. If nothing clears the bar, say so plainly.
Use the report format in `references/reporting-and-triage.md`.
