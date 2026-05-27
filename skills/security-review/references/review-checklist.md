# Review Checklist

## 1. Define the review scope

- Identify whether the target is staged changes, a branch diff, a commit range, or a PR merge-base diff.
- Collect the changed file list, commit subjects, and diffstat.
- Ignore generated files unless the generated artifact itself is executed or published.

## 2. Classify the change surface

Bucket the diff before deep reading:

- Request or API handling
- Auth, session, or permission logic
- Database or query construction
- File system or archive handling
- Shell execution or process spawning
- Outbound HTTP, webhooks, queues, or cloud SDK calls
- Templates, rich text, markdown, HTML rendering
- CI/CD, release automation, package publishing, or infrastructure

Use the bucket to decide which reference files to load next.

## 3. Map trust boundaries

Look for new or changed boundaries such as:

- Anonymous user -> authenticated user
- User -> admin or support operator
- Tenant -> tenant
- Public internet -> internal service
- Forked PR or external contributor -> repository secrets or write token
- Uploaded file or archive -> local filesystem
- Untrusted content -> template, shell, SQL, or interpreter

A finding usually needs a trust-boundary crossing plus a dangerous sink.

## 4. Find the real entry points

Prefer concrete attacker-controlled sources:

- HTTP params, headers, cookies, bodies, uploads, webhooks
- Message queue payloads
- Repository-dispatch, issue, PR, and workflow event fields
- Persisted user-controlled data later rendered or executed
- Cross-service responses from less-trusted systems

Treat environment variables and CLI flags as trusted by default unless the reviewed feature explicitly lets attackers set them.

## 5. Trace to sensitive sinks

Common high-value sinks:

- Query construction and ORM escape hatches
- Shell commands, interpreters, templating engines
- File reads, writes, extraction, path joins
- HTML sinks, raw markdown-to-HTML output, framework bypass APIs
- Token minting, session creation, permission decisions
- Outbound requests to sensitive internal systems
- Workflow `run:` blocks, privileged jobs, deploy steps, release steps

## 6. Compare with established local patterns

Before flagging a vulnerability, inspect nearby helpers and existing code for:

- Validation wrappers
- Centralized authz checks
- Safe query builders
- Path normalization helpers
- Safe HTML rendering utilities
- Workflow templates or reusable actions

Drop findings when a real mitigation is present in the executed path.

## 7. Try to disprove each candidate

For every candidate finding, ask:

- Can the attacker really control the source?
- Is the sink reachable on the changed path?
- Is there an allowlist, encoder, binder, ownership check, or sandbox that blocks exploitation?
- Is the vulnerable behavior only in dead code, tests, docs, or local tooling with no untrusted input path?

If the answer is uncertain, do not report it.

## 8. Prefer changed-code impact

Prioritize findings where the diff:

- Introduces a new sink
- Removes a mitigation
- Broadens privileges or data exposure
- Moves trusted logic earlier than validation or authz
- Changes default behavior toward a less secure state
- Connects an old risky helper to a newly attacker-controlled input

## 9. Keep the final report tight

Only include findings that are concrete, exploitable, and worth a security engineer raising in review.
If there are no such findings, say so directly.
