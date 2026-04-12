# Agent CLI Patterns

Use this reference when designing a reusable CLI for agents.

## Goals

A good agent-facing CLI should:
- run from any working directory
- expose narrow, composable commands
- return stable JSON under `--json`
- separate discovery from mutation
- make auth/config obvious
- provide one honest raw escape hatch

## Recommended command families

### Doctor
Use a health/config command first.

Examples:
- `tool --json doctor`
- `tool doctor --json`

Should report:
- version
- auth presence and source category
- endpoint/base URL
- fixture or offline mode when relevant
- missing setup steps

### Discovery
Top-level listing commands for accounts, teams, projects, workspaces, queues, channels, repos, or dashboards.

Examples:
- `tool projects list`
- `tool teams list`
- `tool queues list --limit 50`

### Resolve
Convert fuzzy user inputs into stable IDs.

Examples:
- `tool resolve project --slug foo`
- `tool resolve build --url https://...`
- `tool resolve customer --email x@example.com`

### Read
Fetch exact objects or bounded lists.

Examples:
- `tool builds get --id bld_123`
- `tool messages search --query fail --limit 20`
- `tool jobs logs --id job_123`

### Write
Each mutation should do one named action.

Examples:
- `tool deploy create --project prj_123 --dry-run`
- `tool tickets comment --id t_123 --file body.md`
- `tool jobs retry --id job_123`

Prefer `--dry-run`, `draft`, or `preview` when the platform supports it.

### Raw escape hatch
Include one low-level command for unsupported calls.

Examples:
- `tool api get /v1/projects`
- `tool request GET /projects/123`

Default raw access to read-only behavior first.

## JSON contract

Under `--json`, output should be machine-readable and stable.

Two valid patterns:

### Pass-through
Return the service payload directly when it is already stable and useful.

### CLI envelope
Wrap responses in a predictable shape such as:

```json
{
  "ok": true,
  "data": {},
  "meta": {
    "nextCursor": null
  }
}
```

Error shape should also be stable, for example:

```json
{
  "ok": false,
  "error": {
    "code": "auth_missing",
    "message": "Set EXAMPLE_TOKEN or run example init"
  }
}
```

Never include credentials or raw secret values in JSON output.

## Auth order

Prefer:
1. standard environment variable
2. config file
3. explicit flag for one-off testing only

## Safety

- Do not bury writes inside vague verbs like `fix`, `sync`, or `auto`
- Do not make destructive raw writes the first path
- Ask before live writes when testing confidence depends on mutation
- Keep pagination bounded and explicit

## Installability

A real CLI should be runnable by command name outside its source repo.

Smoke test from another directory:

```bash
command -v <tool>
<tool> --help
<tool> --json doctor
```

If those fail outside the repo, the CLI is not done yet.
