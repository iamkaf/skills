# Workflow and Supply Chain

Use this reference when the diff touches GitHub Actions, CI scripts, release tooling, package publishing, containers, or automation that handles secrets or repository write access.

## High-signal workflow risks

### Untrusted interpolation into `run:`

Report when attacker-controlled workflow context is injected into a shell script or command generation path.

Common untrusted sources:

- PR title or body
- Issue title or body
- Branch names and tag names
- Commit messages
- Label names
- Workflow inputs from lower-trust callers
- Artifact names or outputs derived from untrusted jobs

Strong signals:

- `${{ ... }}` values are inserted directly inside a `run:` script.
- The diff replaces safe action inputs or env indirection with inline shell interpolation.
- Untrusted values reach `bash -c`, PowerShell, Python `-c`, or similar dynamic execution.

Safer patterns:

- Pass the value as an action input.
- Pass the value through `env:` and quote it in the script.

### Dangerous `pull_request_target` usage

Treat `pull_request_target` as privileged.

Report when the workflow combines any of these with untrusted PR content:

- Checking out the PR head or running code from the fork
- Access to repository secrets, environments, or cloud credentials
- Write-capable `GITHUB_TOKEN`
- Artifact or cache data from untrusted jobs flowing into privileged steps

A high-confidence finding usually needs both an untrusted trigger and a privileged side effect.

### Excessive token or credential reachability

Report when an untrusted path can reach meaningful write or deploy capability, such as:

- `contents: write`, `pull-requests: write`, package publish, release creation
- OIDC minting for cloud credentials
- Deployment environments with secrets or reviewers bypassed

Do not report broad permissions by themselves unless the reviewed change makes them reachable from untrusted input or newly introduces the privileged path.

### Third-party action trust

Pinning to a full commit SHA is the safest pattern, but do not report every non-SHA pin as a vulnerability.

Report when the diff newly introduces a privileged third-party action and:

- The workflow has access to secrets, write tokens, releases, or deployments, and
- The action is mutable in a way that would let a compromise immediately affect the repository or environment.

### Artifact, cache, and job-boundary poisoning

Report when data from a lower-trust job can influence a higher-trust job without integrity controls.

Strong signals:

- A privileged job downloads and executes artifacts created from untrusted PR code.
- Shared workspaces or caches allow untrusted code to modify later privileged steps.
- Job outputs from an untrusted context become shell commands, release notes, or deployment inputs.

## Release and build automation

### Scripted downloads and installers

Report when the diff introduces:

- `curl | sh` or equivalent from mutable URLs in privileged contexts
- Remote script execution without integrity pinning in release or deploy flows
- Container or build steps that fetch unverified tooling before privileged actions

### Secret handling

Strong signals:

- Secrets are echoed, transformed without masking, copied into artifacts, or baked into images.
- The change broadens where secrets are available instead of narrowing scope.

### Container and packaging changes

Report when the diff:

- Copies secrets or credential files into final images
- Runs package publish or image push from untrusted triggers
- Uses build arguments or metadata fields that allow attacker-controlled injection into privileged scripts

## Review posture

Prefer concrete exploit chains over best-practice lint.
A finding should explain who controls the input, what privilege is exposed, and how the workflow now crosses that boundary unsafely.
