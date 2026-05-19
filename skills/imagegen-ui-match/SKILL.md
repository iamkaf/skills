---
name: imagegen-ui-match
description: Use when implementing a UI from a visual mock and the user wants an imagegen-based compare-and-iterate workflow until the current page closely matches the target screenshot or mock. Covers browser screenshots, explicit side-by-side comparisons, imagegen visual audits, bitmap asset generation, and avoiding stale-reference mistakes.
license: MIT
metadata:
  version: "1.0.0"
---

# Imagegen UI Match

Use this when a user asks to make an implemented UI match a mock, screenshot,
or generated concept, especially when they want `$imagegen` to judge similarity.

## Core Rule

Treat visual matching as an artifact loop, not a vibe loop:

1. Capture the current UI from the browser.
2. Build an explicit side-by-side comparison image from the target and current screenshots.
3. Ask imagegen to judge only that comparison image.
4. Implement only the concrete remaining deltas.
5. Repeat until the imagegen verdict is close enough or the user stops.

Do not ask imagegen to compare against loose conversation context if old
screenshots exist. Always provide a freshly generated comparison image.

## Workflow

### 1. Lock the Target

Identify the target image and save/confirm its path. If there are multiple
mocks, ask or infer the primary one and state it.

Record:

- Target image path
- Current route/URL
- Viewport size used for comparison
- What "close enough" means if the user provided a threshold

Use the target's aspect ratio as the browser viewport when practical.

### 2. Capture the Current UI

Use browser automation for real screenshots. Prefer `agent-browser` when
available:

```bash
agent-browser --session ui-match set viewport 1680 944
agent-browser --session ui-match open http://127.0.0.1:3000/path
agent-browser --session ui-match wait --load networkidle
agent-browser --session ui-match screenshot /tmp/current-ui.png
```

Inspect the screenshot yourself before asking imagegen. Fix obvious breakage
first: blank screens, overflow, clipped panels, missing assets, or wrong route.

### 3. Build an Explicit Comparison Image

Create a single image with the target on the left and the current screenshot on
the right. This prevents stale-image audits.

Using ImageMagick:

```bash
target=/path/to/target.png
current=/tmp/current-ui.png

convert "$target" -resize 840x472\! /tmp/target-840.png
convert "$current" -resize 840x472\! /tmp/current-840.png
convert -size 1680x560 xc:white \
  /tmp/target-840.png -geometry +0+60 -composite \
  /tmp/current-840.png -geometry +840+60 -composite \
  -gravity northwest -pointsize 28 -fill black -annotate +28+36 'TARGET MOCK' \
  -gravity northwest -pointsize 28 -fill black -annotate +868+36 'CURRENT IMPLEMENTATION' \
  /tmp/ui-comparison.png
```

If ImageMagick is unavailable, use any deterministic image composition tool.
Do not handwave the comparison step.

### 4. Ask Imagegen for a Verdict

Use imagegen in infographic/diagram mode with the explicit comparison visible.
Use this prompt shape:

```text
Use case: infographic-diagram
Asset type: visual similarity verdict
Primary request: Evaluate the single provided comparison image. The left half is labeled TARGET MOCK and the right half is labeled CURRENT IMPLEMENTATION.
Composition/framing: Keep the comparison visible. Add a verdict badge at the top: either "VERY SIMILAR - few feel differences" if the implementation reads as the same UI with only minor feel differences, or "NOT THERE YET" if meaningful implementation differences remain. Add at most 4 short callouts for remaining differences.
Criteria to judge: overall layout proportions, header placement and scale, canvas size and position, side panel sizing, asset scale, spacing/density, color palette/visual language, and controls.
Constraints: Use only the provided comparison image. Do not compare against earlier screenshots. Do not invent features. Do not redesign the UI.
```

If imagegen says **NOT THERE YET**, implement the callouts directly. If the
callouts are vague, translate them into measurable CSS/layout changes before
editing.

### 5. Implement the Deltas

Prioritize changes in this order:

1. Overall layout proportions and viewport fit
2. Header height, alignment, and control groups
3. Canvas size, position, and asset scale
4. Side panel widths and density
5. Missing/mismatched controls
6. Palette and visual language
7. Thumbnail/detail fidelity

Use the existing frontend stack and design system. If the mock uses real bitmap
artwork, use or generate bitmap assets. Do not recreate complex illustrations
with CSS or SVG unless the user explicitly asks for code-native art.

### 6. Bitmap Asset Rule

For mock-like UI assets, prefer generated or cropped bitmap assets over CSS art.

If an asset needs transparency:

1. Generate it on a flat chroma-key background (`#00ff00`, `#ff00ff`, or
   `#0000ff`) with no shadow, gradient, checkerboard, or texture.
2. Remove the key locally using the imagegen helper when Pillow is available:

```bash
python3 "$HOME/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input source.png \
  --out asset.png \
  --key-color '#00ff00' \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill \
  --force
```

3. If the helper cannot run, use ImageMagick and inspect over two contrasting
   backgrounds:

```bash
convert source.png -alpha set -fuzz 32% -transparent '#00ff00' asset.png
convert asset.png -background '#ff00ff' -alpha remove -alpha off /tmp/check-magenta.png
convert asset.png -background '#2f80ff' -alpha remove -alpha off /tmp/check-blue.png
```

Do not accept a fake checkerboard background as transparency.

### 7. Completion Audit

Before declaring done, verify with real artifacts:

- Current route screenshot exists and is from the latest code.
- Comparison image uses the latest screenshot, not an earlier one.
- Imagegen verdict was run against that explicit latest comparison.
- Build/typecheck passed if the repo has those commands.
- Remaining imagegen callouts are either fixed or explicitly accepted by the user.

If the imagegen verdict says "VERY SIMILAR - few feel differences", you may
stop after reporting the exact screenshot/comparison paths and verification
commands.

## Failure Modes

- **Stale audit:** imagegen judged an older screenshot. Rebuild the explicit
  comparison and rerun.
- **Proxy confidence:** build passed but the UI does not match. Keep iterating.
- **CSS art drift:** the mock uses bitmap illustration but the implementation
  uses CSS shapes. Generate/crop a bitmap instead.
- **Wrong viewport:** the page only matches at an accidental size. Capture at
  the mock's aspect ratio and at one practical desktop size.
- **Over-redesign:** the audit becomes a new product design. Reject invented
  features and only implement differences visible in the target.
