---
name: vhs
description: Create, edit, debug, or review Charmbracelet VHS terminal demo recordings and .tape files. Use when the task involves terminal GIFs/videos, VHS scripts, demo cassettes, CLI screencasts, reproducible terminal recordings, or converting terminal interactions into renderable tape files.
license: MIT
metadata:
  version: "0.1.0"
---

Create reproducible terminal recordings with Charmbracelet VHS.

## Start

Check the goal, output format, and execution environment.

- Confirm whether the user wants `.gif`, `.mp4`, `.webm`, screenshots, or a reusable `.tape`.
- Check whether `vhs`, `ttyd`, and `ffmpeg` are available before planning a render.
- If the request is mainly about recording a workflow, prefer writing a clean `.tape` first and rendering second.

```bash
command -v vhs ttyd ffmpeg || true
vhs --help || true
```

If dependencies are missing, still write or fix the `.tape` file and tell the user what is missing to render it.

## Core workflow

1. Write or inspect the `.tape` file.
2. Put `Output`, `Require`, and `Set` directives at the top.
3. Script the interaction with `Type`, key presses, `Sleep`, and `Wait`.
4. Render with `vhs path/to/demo.tape`.
5. Review the result and tighten timings, dimensions, theme, or shell behavior.

Prefer deterministic tapes over ad hoc recording. Use `Wait` when output timing depends on command completion. Use `Sleep` only for deliberate pacing or when no reliable wait condition exists.

## Tape structure

Keep tapes readable and predictable.

- Start with one or more `Output` lines.
- Add `Require` lines for commands the tape depends on.
- Add global `Set` lines before interaction commands.
- Keep comments short and practical.
- Use `Source` only when splitting a large tape improves reuse.

Typical layout:

```text
Output demo.gif
Require glow
Set Shell bash
Set FontSize 32
Set Width 1200
Set Height 700
Set TypingSpeed 80ms

Type "glow README.md"
Enter
Wait /Usage/
Sleep 1s
```

## Command selection

Use the smallest command set that makes the demo stable.

- `Type` for typed text
- `Enter`, `Tab`, `Backspace`, arrow keys, and `Ctrl+<key>` for interaction
- `Wait /regex/` or `WaitLine /regex/` for command completion or prompt state
- `Sleep` for pacing, not synchronization
- `Hide` and `Show` to suppress sensitive or distracting commands
- `Screenshot` for still captures
- `Copy` and `Paste` when clipboard-style interaction is clearer than long typing

If the UI is noisy or slow, prefer `Set TypingSpeed`, `Hide`, and narrower window sizes before adding more sleeps.

## Common fixes

When a tape is flaky, check these first.

- Output appears cut off: increase `Set Width`, `Set Height`, padding, or margins.
- Render is too fast or too slow: adjust `Set TypingSpeed`, `Set PlaybackSpeed`, and targeted `Sleep` values.
- Command output races the tape: replace `Sleep` with `Wait` where possible.
- Demo depends on tools not installed: add `Require` so failures happen early.
- Sensitive values appear on screen: hide the command, inject env via `Env`, or use a sanitized fixture.
- Prompt looks inconsistent across machines: set `Set Shell` explicitly and prefer controlled demo directories.

## Safer demo design

Prefer fixtures and throwaway working directories.

- Run demos against sample files, not personal repos, unless the user asked for a real project demo.
- Sanitize tokens, usernames, hostnames, and paths.
- Prefer commands with deterministic output over network-dependent output.
- If live network access is required, mention that the render may vary and keep the tape easy to rerun.

## Useful patterns

### CLI feature demo

```text
Output cli-demo.gif
Require mytool
Set Shell bash
Set Width 1100
Set Height 700
Set TypingSpeed 70ms

Type "mytool --help"
Enter
Wait /Commands/
Sleep 1200ms
Type "q"
```

### Prompt or TUI walkthrough

```text
Output tui.gif
Set Width 1200
Set Height 800

Type "my-tui"
Enter
Wait /Select an option/
Down
Down
Enter
Wait /Completed/
```

### Static screenshot extraction

```text
Output frames/
Set Framerate 1
```

## Validation

Before finishing, verify the tape and output.

- Re-read the `.tape` from top to bottom for ordering mistakes.
- Render at least once if dependencies exist.
- Confirm the output path matches the requested artifact.
- If a render was requested but could not be run, report the exact missing dependency or failing command.

## References

Read these when needed.

- `vhs manual` for the built-in command reference.
- `examples/` from the upstream repository for idiomatic tapes.
- `THEMES.md` upstream when the task is mainly about terminal themes.
