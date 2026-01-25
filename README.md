# iamkaf/skills

A collection of personal AI agent skills, compatible with the [Agent Skills Standard](https://github.com/vercel-labs/skills).

These skills are designed to be installed via the `npx skills` CLI and work across Claude Code, Codex, and other compatible agents.

## Installation

To install these skills into your local agent environment:

```bash
npx skills add iamkaf/skills

```

You can also install specific skills individually:

```bash
npx skills add iamkaf/skills/ai-writing-audit

```

## Available Skills

| Skill | Description | Version |
| --- | --- | --- |
| **`ai-writing-audit`** | Audits text to remove "AI-isms" (hedging, robotic transitions) and makes writing sound more human. | `1.1.0` |
| **`clean-transient-comments`** | Removes temporary, date-stamped, or author-specific comments while keeping documentation intact. | `1.1.0` |
| **`effective-questioning`** | Forces the agent to pause and ask clarifying questions (The "5 Ws") when requirements are vague. | `0.2.0` |

## Development

### Directory Structure

Each skill lives in its own directory under `skills/` and must contain a `SKILL.md` file with valid YAML frontmatter.

```text
skills/
├── skill-slug/
│   ├── SKILL.md  <-- Required (Must have name, description, version)
│   └── rules.json (Optional assets)

```

### Validation

This repository uses GitHub Actions to validate that all skills follow the correct folder structure and metadata format on every push.
