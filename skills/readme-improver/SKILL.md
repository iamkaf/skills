---
name: readme-improver
description: Transform boring, flat README files into polished, visually compelling project pages. Use when the user asks to improve, redesign, or make a README more interesting. Covers structure, copy, badges, banner images, and overall presentation. Produces GitHub-flavored Markdown that renders well on GitHub, npm, and similar platforms.
license: MIT
metadata:
  version: "1.1.0"
---

# README Improver

Transform a project README from a flat wall of text into a polished, memorable
project page that makes people want to try the software.

## When to use this skill

- The user says their README is "boring", "plain", or "needs work"
- The user asks you to "make the README better" or "more interesting"
- You are creating a new project and need to write a README from scratch

## Process

### 1. Understand the project first

Before touching the README, read enough of the codebase to understand:

- **What it does** — one sentence, no jargon
- **Who it's for** — developers, end users, other agents, etc.
- **How it's used** — CLI, library, HTTP API, GUI, MCP, etc.
- **What makes it different** — the hook, the reason someone would pick this over alternatives
- **Package metadata** — `package.json`, `Cargo.toml`, `pyproject.toml`, etc. for repo URL, license, version, engine requirements

Read the existing README fully. Identify what content exists and what's missing.
Do not discard existing technical content — reorganize and elevate it.

### 2. Generate a banner image

Use the `generate_image` tool to create a banner that captures the project's
essence. Guidelines:

- **Dark backgrounds work best** on GitHub (renders on both light and dark themes)
- **No text in the image** — text gets blurry at small sizes and can't be localized
- **Abstract and evocative** — represent the concept, not a screenshot
- **Match the project's mood** — a playful tool gets a playful image, a serious
  infrastructure project gets something more austere
- **Keep it simple** — the banner should complement the README, not overwhelm it

Place the image in `assets/banner.png` (create the directory if needed).

Display it centered with a constrained width so it doesn't dominate the page:

```html
<p align="center">
  <img src="assets/banner.png" alt="Project name banner" width="480" />
</p>
```

Width guidelines:
- `480` — good default for most projects
- `360` — for smaller, more subtle banners
- `600` — for projects where the visual is the main draw

Never go above `720`. The banner should invite, not shout.

### 3. Structure the header

The header block follows a strict order. Use centered HTML for alignment:

```html
<!-- 1. Banner image -->
<p align="center">
  <img src="assets/banner.png" alt="Project name banner" width="480" />
</p>

<!-- 2. Badges -->
<p align="center">
  <!-- see badge section below -->
</p>

<!-- 3. Project name -->
<h1 align="center">Project Name</h1>

<!-- 4. One-line description -->
<p align="center">
  <strong>What it does in one sentence.</strong>
</p>

<!-- 5. Navigation links (optional, for longer READMEs) -->
<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#section">Section</a> ·
  <a href="#another">Another</a>
</p>
```

After the header block, add a horizontal rule (`---`) and then the body.

### 4. Write the opening paragraph

Immediately after the `---`, write 1-2 sentences that explain what the project
does. This is the most important copy in the entire README. Rules:

- **No filler.** Every word earns its place.
- **Be concrete.** "Downloads a source snapshot and answers your question with
  file-level citations" beats "AI-powered codebase exploration utility."
- **Active voice.** The project does things; it doesn't "allow" or "enable."
- **Skip the word "powerful."** And "elegant." And "blazing fast." If it's fast,
  show a benchmark. If it's elegant, the code will speak for itself.

Optionally follow with an etymology or meaning block if the project name has one:

```markdown
> **im·ma·nence** */ˈimənəns/*
> The quality of being contained within. Here, answers come from the codebase itself.
```

### 5. Add badges

Use [shields.io](https://shields.io) badges. Always use the `for-the-badge`
style with custom colors for a premium look. Pick colors that feel cohesive with
each other and with the banner.

**Color palette approach:** Choose 3 colors from a harmonious palette. Use a
dark `labelColor` (e.g., `1a1a2e`, `0d1117`, `16161d`) so badges feel unified.

**Common badges to include (pick what's relevant):**

```html
<!-- License -->
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-a78bfa?style=for-the-badge&labelColor=1a1a2e" alt="MIT License" /></a>

<!-- Language/runtime version -->
<img src="https://img.shields.io/badge/node-%E2%89%A520-5eead4?style=for-the-badge&logo=node.js&logoColor=5eead4&labelColor=1a1a2e" alt="Node 20+" />

<!-- npm version (if published) -->
<a href="https://www.npmjs.com/package/PACKAGE"><img src="https://img.shields.io/npm/v/PACKAGE?style=for-the-badge&color=fbbf24&logo=npm&logoColor=fbbf24&labelColor=1a1a2e" alt="npm" /></a>

<!-- crates.io (Rust) -->
<a href="https://crates.io/crates/CRATE"><img src="https://img.shields.io/crates/v/CRATE?style=for-the-badge&color=fbbf24&logo=rust&logoColor=fbbf24&labelColor=1a1a2e" alt="crates.io" /></a>

<!-- PyPI (Python) -->
<a href="https://pypi.org/project/PACKAGE"><img src="https://img.shields.io/pypi/v/PACKAGE?style=for-the-badge&color=fbbf24&logo=python&logoColor=fbbf24&labelColor=1a1a2e" alt="PyPI" /></a>

<!-- CI status -->
<a href="https://github.com/OWNER/REPO/actions"><img src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?style=for-the-badge&labelColor=1a1a2e" alt="CI" /></a>
```

**Color suggestions by role:**
| Role | Good hex colors |
|------|----------------|
| License | `a78bfa` (violet), `818cf8` (indigo), `c084fc` (purple) |
| Runtime/version | `5eead4` (teal), `6ee7b7` (emerald), `86efac` (green) |
| Package registry | `fbbf24` (amber), `fb923c` (orange), `f472b6` (pink) |
| CI/status | `38bdf8` (sky), `22d3ee` (cyan), `60a5fa` (blue) |

**Rules:**
- 2-4 badges. More than 4 looks cluttered.
- Always link badges to something useful (the license file, the npm page, CI runs).
- Static badges (like runtime version) don't need a link.

### 6. Organize the body

Use this general structure, adapting to what the project actually needs:

```
## How It Works        ← brief conceptual overview (diagram, flowchart, or short list)
## Quick Start         ← install + first meaningful command
## [Interface docs]    ← CLI reference, API docs, etc. (use tables)
## Platform Notes      ← OS-specific quirks, if any
## Configuration       ← env vars, config files (use tables)
## Limits              ← honest about what it can't do
## Contributing        ← how to run from source, test, build
## License             ← one-liner with link
```

**Never mix user-facing and developer-facing sections.** Keep adoption and usage content together near the top, then move contributor and maintainer material later under clearly labeled sections like `Contributing`, `Development`, or `Architecture`.

Bad pattern:
- Install for users
- Internal build notes
- CLI usage
- Release process

Good pattern:
- What it is
- Quick Start
- Usage / API / Configuration
- Limits
- Contributing / Development
- License

**Formatting rules:**

- **Use tables** for commands, options, endpoints, env vars — anything with a
  name-description pattern. Tables are more scannable than bullet lists.
- **Use code blocks** for anything the user will copy-paste.
- **Use ASCII diagrams** or simple flowcharts for "how it works" sections.
  Keep them short (6-8 lines max).
- **Avoid deeply nested lists.** If you're past two indent levels, restructure.
- **One blank line** between sections. No double blanks.

### 7. Copy style

Follow these principles for all prose in the README:

- **Short sentences.** If a sentence has a comma, consider splitting it.
- **Active voice.** "Immanence pins the commit" not "The commit is pinned by Immanence."
- **Second person for instructions.** "Run `npm install`" not "The user should run..."
- **No marketing speak.** No "powerful", "seamless", "elegant", "blazing fast",
  "cutting-edge", "next-generation". Describe what it does, not how great it is.
- **Be specific.** "Caches snapshots by commit SHA" beats "intelligent caching."
- **Contractions are fine.** "It's", "don't", "you'll" — READMEs aren't legal docs.
- **No emoji in headings.** They look unprofessional on GitHub.
- **No trailing punctuation on list items** unless they're full sentences.

### 8. Review checklist

Before finishing, verify:

- [ ] Banner image exists at `assets/banner.png` and renders at a reasonable size
- [ ] Badges use `for-the-badge` style with cohesive custom colors
- [ ] First sentence answers "what does this project do?"
- [ ] Quick Start section gets someone from zero to working in under a minute
- [ ] All CLI commands, API endpoints, and config options use tables
- [ ] License is mentioned with a link
- [ ] No orphaned content from the original README was lost
- [ ] No marketing fluff or AI-sounding superlatives slipped in
- [ ] The README renders correctly in standard GitHub Markdown

## Example transformation

### Before (typical flat README)

```markdown
# myproject

A tool for doing things.

## Install

npm install

## Usage

Run myproject --help

## Options

- --verbose: verbose output
- --port: port number
- --config: config file path

## License

MIT
```

### After (improved)

```html
<p align="center">
  <img src="assets/banner.png" alt="myproject banner" width="480" />
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-a78bfa?style=for-the-badge&labelColor=1a1a2e" alt="MIT" /></a>
  <img src="https://img.shields.io/badge/node-%E2%89%A520-5eead4?style=for-the-badge&logo=node.js&logoColor=5eead4&labelColor=1a1a2e" alt="Node 20+" />
</p>

<h1 align="center">myproject</h1>

<p align="center">
  <strong>One sentence about what it actually does.</strong>
</p>
```

```markdown
---

Myproject does X by doing Y, producing Z.

## Quick start

### Install

​```bash
npm install -g myproject
​```

### Run

​```bash
myproject --help
​```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--verbose` | Verbose output | `false` |
| `--port <n>` | Port number | `3000` |
| `--config <path>` | Config file path | `./config.json` |

## License

[MIT](LICENSE)
```

## Reference: shields.io URL format

```
https://img.shields.io/badge/<LABEL>-<MESSAGE>-<COLOR>?style=for-the-badge&labelColor=<HEX>&logo=<LOGO>&logoColor=<HEX>
```

- Spaces in LABEL/MESSAGE: use `%20` or `_` (underscores render as spaces)
- Special characters: URL-encode them (`≥` → `%E2%89%A5`)
- Logo names: see [Simple Icons](https://simpleicons.org) for the full list
- Dynamic badges (npm version, CI status, etc.) use a different URL pattern —
  see [shields.io docs](https://shields.io)
