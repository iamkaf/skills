# Web and API Findings

Use this reference when the diff touches application code, APIs, handlers, serializers, templates, files, or outbound network calls.

## Injection and execution

Report only when untrusted input reaches a dangerous sink without an effective mitigation.

### SQL or NoSQL injection

Strong signals:

- User input is concatenated into raw query text.
- User input controls query operators, field names, sort clauses, or filter objects without allowlisting.
- The change bypasses parameter binding or replaces a safe query helper with raw execution.

Usually do not report when:

- The code uses parameterized queries correctly.
- Field names or operators are chosen from a fixed allowlist.

### Command injection

Strong signals:

- Untrusted input is embedded into `sh -c`, `bash -c`, `exec`, `system`, `Runtime.exec`, or similar shell strings.
- The change flips from argv-style execution to shell parsing.
- Archive names, branch names, filenames, or request fields reach a shell.

Usually do not report when:

- The code passes fixed commands as argv arrays without shell parsing.
- The input is selected from a narrow allowlist.

### Template injection or eval

Strong signals:

- User input is compiled or executed as template code.
- The change introduces `eval`, `Function`, unsafe expression evaluation, or server-side template rendering from attacker content.

### Unsafe deserialization

Strong signals:

- The change introduces `pickle.loads`, unsafe `yaml.load`, native object deserialization, or similar logic on untrusted data.
- A trusted-only serialization path becomes reachable from a request, webhook, or queue.

### Path traversal and archive extraction

Strong signals:

- User-controlled paths are joined directly and used for file reads or writes.
- Canonicalization or root-prefix checks were removed.
- Archive extraction writes attacker-controlled filenames without traversal protection.

## Authentication and authorization

### Broken object or tenant authorization

Strong signals:

- The change looks up resources by user-supplied ID, slug, or account key without ownership or tenant checks.
- A privileged action moved behind authentication but not authorization.
- The diff switches from scoped queries to global queries.

### Privilege escalation

Strong signals:

- Request fields can set role, plan, tenant, or policy values without server-side validation.
- Support or admin routes now share handlers with lower-trust callers.
- A previously required permission, feature flag, or policy check was removed.

### Session and token flaws

Strong signals:

- Secrets, session IDs, refresh tokens, or signing keys are logged or returned.
- Token verification is weakened or bypassed.
- Sensitive actions stop requiring re-auth or freshness checks where they previously did.

## Web output and content rendering

### XSS

Report only when the diff introduces a real unsafe sink or disables existing escaping.

Strong signals:

- `innerHTML`, `outerHTML`, `dangerouslySetInnerHTML`, `bypassSecurityTrustHtml`, raw markdown-to-HTML output, or equivalent unsafe rendering.
- User content is inserted into script, style, or attribute contexts without context-aware encoding.

Usually do not report when:

- React, Angular, Vue, or server templates are using their normal escaping path.
- The concern is generic “input not sanitized” with no unsafe sink.

## Outbound network and SSRF

Report SSRF only when attacker input can influence the host, scheme, or a sensitive internal destination.

Strong signals:

- Full URL, host, protocol, or redirect target comes from user input.
- The request can hit metadata endpoints, localhost, cluster services, admin panels, or private ranges.
- A safe allowlist or URL parser was removed.

Usually do not report when:

- The attacker controls only a path or query string on a fixed safe host.

## Secrets, logging, and data exposure

Strong signals:

- The change logs API keys, bearer tokens, passwords, private keys, session cookies, reset tokens, or raw PII.
- Sensitive fields are newly returned from an endpoint or included in webhook payloads.
- Debug or error output now exposes internals that materially help exploitation.

Usually do not report when:

- The log contains non-secret operational data only.
- The concern is a general lack of audit logging.

## Crypto and verification

Strong signals:

- TLS or certificate verification is disabled.
- Token or password material uses predictable randomness.
- Encryption or signature verification is replaced with decode-only logic.
- Secrets move from a secure store to code, config, logs, or client-visible output.

Usually do not report when:

- The issue is only that a third-party crypto library could be newer.
