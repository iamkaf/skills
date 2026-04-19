# iamkaf/skills

A collection of personal AI agent skills, compatible with the [Agent Skills Standard](https://agentskills.io/home).

These skills are designed to be installed via the `npx skills` CLI and work across Claude Code, Codex, and other compatible agents.

## Installation

To install these skills into your local agent environment:

```bash
npx skills add iamkaf/skills
```

## Available Skills

| Skill | Description |
| --- | --- |
| **`ai-writing-audit`** | Audits text to remove "AI-isms" (hedging, robotic transitions) and makes writing sound more human. |
| **`amber`** | Amber docs index for building or porting Minecraft mods that use the Amber multiloader library. |
| **`clean-transient-comments`** | Removes temporary, date-stamped, or author-specific comments while keeping documentation intact. |
| **`cli-creator`** | Builds durable, agent-friendly CLIs from docs, specs, SDKs, examples, browser flows, or existing scripts. |
| **`effective-questioning`** | Forces the agent to pause and ask clarifying questions (The "5 Ws") when requirements are vague. |
| **`vhs`** | Creates, edits, and debugs Charmbracelet VHS `.tape` files for reproducible terminal GIFs, videos, and screenshots. |

## Development

### Directory Structure

Each skill lives in its own directory under `skills/` and must contain a `SKILL.md` file with valid YAML frontmatter.

```text
skills/
├── skill-slug/
│   ├── SKILL.md  <-- Required (Must have valid frontmatter)
│   └── rules.json (Optional assets)

```

### Validation

This repository uses GitHub Actions with `agent-ecosystem/skill-validator` to validate that all skills follow the expected structure and frontmatter format on every push.
