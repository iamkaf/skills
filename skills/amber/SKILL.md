---
name: amber
description: Index + progressive-disclosure guide for developing Minecraft mods with Amber (multiloader library for Fabric/Forge/NeoForge).
version: 0.2.0
---

# Amber (Skill Index)

This is an **index skill** for Amber.

Amber is a comprehensive multiloader library for Minecraft mod development (unified APIs across **Fabric**, **Forge**, and **NeoForge**).

## When to use

Use this skill when you need to:
- set up or maintain an Amber-based multiloader project
- implement common modding systems using Amber’s APIs
- debug cross-loader differences in an Amber project
- port between Minecraft versions while staying on Amber conventions

## Quick workflow (progressive disclosure)

**Do not read everything.** Use the smallest page that answers the question.

1) **Pick the correct Amber line for your Minecraft version**
   - Start at: `docs/index.md`
   - Rule of thumb from Amber docs:
     - **Amber 10.x** → Minecraft **26.1**
     - **Amber 9.x** → Minecraft **1.21.11**
     - **Amber 8.x** → Minecraft **1.21.10**
     - **Amber 3.x** → Minecraft **1.21.1**
     - **Amber 1.x** → Minecraft **1.20.1**

2) **Choose the right documentation root**
   - If you’re on MC **1.21.11** → use `docs/v9/…`
   - If you’re on MC **1.21.10** → use `docs/v8/…`
   - If you’re on MC **26.1** → use the Amber 10.x docs (wherever they live in this skill bundle)

3) **Open only the subsystem you need**
   - Prefer subsystem pages over general guides.

4) **If you’re porting**
   - Read: `porting-primer-1.21.11.md` (and any version-specific porting notes packaged with this skill)

## What’s included with this skill

This skill is expected to ship with Amber’s documentation and reference material alongside `SKILL.md` (similar to `mc-porting`).

At minimum, include:
- `docs/index.md`
- `docs/v9/…` (Amber 9.x docs)
- `docs/v8/…` (Amber 8.x docs)
- `porting-primer-1.21.11.md`

## Index: where to look (by task)

### Project setup / dependencies
- Start: `docs/index.md` → **Quick Start** section
- Then: `docs/v9/guide/getting-started` (or the matching version)

### Registry / deferred registration
- `docs/v9/systems/registry`

### Events
- `docs/v9/systems/events`

### Commands
- `docs/v9/systems/commands`

### Networking
- `docs/v9/systems/networking`

### Best practices / architecture
- `docs/v9/advanced/best-practices`

### Porting / version changes
- `porting-primer-1.21.11.md`

## Output expectations (how to answer)

When using this skill to answer a question:
- Give a **minimal working example** first.
- Then link to the **smallest relevant doc page** in this bundle.
- Only expand to deeper pages if the first answer isn’t enough.

