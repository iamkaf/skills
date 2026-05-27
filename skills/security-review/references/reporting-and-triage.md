# Reporting and Triage

## Review standard

Return only findings that are concrete, newly introduced, and high confidence.

Use this bar before reporting:

- Confidence must be 8/10 or higher.
- Severity should be High, or clear Medium with an obvious exploit path and meaningful impact.
- The finding should be actionable for a security engineer reviewing the change.

If a candidate does not clear that bar, drop it.

## False-positive filters

Do not report the following unless the user explicitly asks for broader coverage:

- Pure DoS, rate limiting, memory, CPU, or resource exhaustion issues
- Dependency age or outdated library findings by themselves
- Tests, fixtures, notebooks, or docs that do not affect live execution
- Generic missing hardening without a concrete exploit path
- Client-side only missing auth or validation checks with no server impact
- SSRF where only the path is attacker-controlled
- React or Angular XSS without an unsafe sink or escape hatch
- Regex injection or ReDoS
- Log spoofing
- Logging of non-secret, non-PII operational data
- Environment-variable or CLI-flag attacks unless attackers can actually control those inputs in the reviewed feature
- Prompt injection into AI prompts by itself
- “Needs more audit logs” or “needs more defense in depth” comments

## Report format

If there are qualifying findings, return markdown in this shape:

# Finding 1: `<category>` in `path:line`

- Severity: High | Medium
- Confidence: 8/10 to 10/10
- Why it is exploitable: One short paragraph tying source, sink, and missing mitigation together.
- Attack path: One short paragraph describing how an attacker would trigger it in practice.
- Fix: One short paragraph with the safest concrete remediation.

Repeat for each finding.

If there are no qualifying findings, return exactly:

`No newly introduced high-confidence security vulnerabilities found in the reviewed changes.`

## Final pass

Before sending the report:

1. Remove anything speculative.
2. Remove findings that depend on unlikely attacker control.
3. Remove findings that describe only best-practice gaps.
4. Make sure each surviving finding names the changed file and approximate line.
5. Make sure the fix recommendation matches the actual stack or pattern used in the repo.
