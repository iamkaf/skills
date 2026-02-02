---
name: amber
description: Development guide for using the Amber multiloader library in Minecraft mods (Fabric/Forge/NeoForge), with a progressive-disclosure workflow.
version: 0.1.0
---

# Amber Development

Use this skill when you’re developing a Minecraft mod that uses **Amber** (a multiloader library that provides unified APIs across Fabric, Forge, and NeoForge).

## When to use

- You’re building a **multiloader** mod (common + fabric/forge/neoforge) and want **one set of APIs** for registries/events/networking/etc.
- You need to **port** a mod between loaders/versions and want to know the Amber way to do it.
- You’re wiring your project to use Kaf’s **platform version-catalog** approach (i.e. dependencies and plugin versions are centralized).

## Quick workflow (progressive disclosure)

Do **not** read everything.

1) **Start here**: `docs/index.md`
   - Pick the correct Amber major line for your MC version (e.g. Amber **9.x → MC 1.21.11**, Amber **8.x → MC 1.21.10**, Amber **10.x → MC 26.1**).

2) **Then read only what you need** (choose one):
   - Getting started: `docs/v9/guide/getting-started` (or `docs/v8/...` for MC 1.21.10)
   - One subsystem:
     - Registry system
     - Events system
     - Commands
     - Networking

3) **Implement in your mod** using the minimal pattern:
   - call `AmberInitializer.initialize(MOD_ID)` in common init
   - register content with Amber-friendly patterns (e.g. deferred registers)

4) **If something behaves differently per loader**:
   - check platform/service wiring in your project
   - confirm you’re using the correct platform-specific Amber artifact

## Key concepts

- **Write once, run everywhere**: Amber provides consistent APIs across Fabric/Forge/NeoForge.
- **Common-first architecture**: most of your code lives in `common/` and calls into Amber.
- **Platform-specific artifacts**: you typically depend on `amber-common` in common, and a loader-specific artifact (`amber-fabric` / `amber-forge` / `amber-neoforge`) in each loader module.
- **Service-based abstraction**: platform differences are handled behind interfaces; avoid direct loader APIs unless absolutely necessary.

## Common tasks

### 1) Add Amber dependencies (version-catalog style)

If your project consumes a **platform version catalog** (recommended for Kaf’s workflow), the exact coordinates depend on how your catalog names them, but conceptually you want:

- `com.iamkaf:amber-common:<amberVersion>`
- `com.iamkaf:amber-fabric:<amberVersion>`
- `com.iamkaf:amber-forge:<amberVersion>`
- `com.iamkaf:amber-neoforge:<amberVersion>`

After adding them to your catalog, wire them like:

**common/build.gradle(.kts)**
```kotlin
dependencies {
  implementation(libs.amber.common)
}
```

**fabric/build.gradle(.kts)**
```kotlin
dependencies {
  modImplementation(libs.amber.fabric)
}
```

(Forge/NeoForge analogous.)

If you’re *not* using a catalog, Amber docs show a Gradle snippet in `docs/index.md`.

### 2) Initialize Amber

In your **common** entry point:

```java
import com.iamkaf.amber.api.core.v2.AmberInitializer;

public final class TemplateMod {
  public static final String MOD_ID = "template";

  public static void init() {
    AmberInitializer.initialize(MOD_ID);
    // register your content / hooks here
  }
}
```

### 3) Register content (items/blocks/etc.)

Use Amber’s recommended registration approach (often `DeferredRegister` + `RegistrySupplier` patterns in Amber-based projects).

When implementing:
- keep registrations in `common/`
- call the “register” hook from your common init

### 4) Events

Prefer Amber’s unified event system when available. Implement handlers in common, and avoid loader-specific buses unless required.

### 5) Debug “works on Fabric but not on Forge”

Checklist:
- Are you depending on the correct loader-specific Amber artifact?
- Did you call `AmberInitializer.initialize(MOD_ID)` early enough?
- Are you accidentally calling loader APIs in `common/`?
- Does your service wiring / META-INF services file match the loader module?

## Where to look in the Amber repo

- `README.md` — high-level overview
- `docs/index.md` — **entry point** + version mapping (Amber 8/9/10 → MC versions)
- `docs/v9/…` — Amber 9 docs (MC 1.21.11)
- `docs/v8/…` — Amber 8 docs (MC 1.21.10)
- `porting-primer-1.21.11.md` — porting notes for the 1.21.11 era
- Source layout (for implementation reference):
  - `common/` + `fabric/` + `forge/` + `neoforge/`

## Output expectations

When answering, prefer:
- **the smallest working snippet** (common init + one registry/event example)
- **the specific doc path** to consult next (progressive disclosure)
- loader/version-specific gotchas only if relevant
