# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → proven Spatial Forge backend → 3D assets / previews → web viewer → Telegram/Mini App**

MCP is intentionally deferred until the backend and delivery path are independently established. It will later act as a narrow external control adapter, not as an early implementation dependency.

## Current Architecture Decisions

- Repository is intentionally **public** so standard public-repository GitHub-hosted runners can be used under GitHub's public-repo Actions policy.
- Public repo contains engine code, workflow definitions, schemas, skills, viewer code, and non-sensitive generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Blender runs headlessly in Actions.
- P0 proved Blender `4.5.12 LTS` can generate `.blend`, `.glb`, and a preview on `ubuntu-latest` after installing `libegl1`.
- P1 proved MPFB `2.0.17` can be installed non-interactively, generate a generic human from script, apply macro phenotype parameters, attach the built-in `game_engine` rig, export GLB, and render previews headlessly.
- P2 has compact versioned character-build and build-result schemas plus a manifest-driven runtime path for the six proven MPFB macro controls.
- P2.4 proved exact real-world measurement intent can be preserved and explicitly reported unsupported instead of being silently fabricated as an MPFB control.
- The manifest builder reads `mpfb.VERSION` at runtime and fails if it is not `2.0.17`, preventing silent extension drift.
- Exported GLB is validated both structurally and by clean-Blender fresh import when relevant.
- `skills/spatial-forge-3d/SKILL.md` is the project-specific 3D creation intelligence router.
- External Blender-agent skills are research/methodology references only. Do not copy their runtime assumptions blindly and do not upgrade the proven stack merely because another project uses a newer Blender version.
- Phone inspection is now deliberately pulled forward as P2V before P2.5/P2.6 because the Creator currently has no PC access and needs to inspect real 3D outputs from Android.
- The initial viewer must be a small static mobile web app. It should load GLB/preview/metadata URLs directly and must not require a database or VPS just to render a model.
- Preferred future UI hostname: `forge.drthorne.uk`.
- Cloudflare Pages is the preferred static hosting target once connected. The VPS will later provide protected/private build assets and control APIs, not the viewer rendering engine itself.
- Telegram will later send build notifications/previews and open the same web viewer as a Mini App/web view rather than requiring a second viewer implementation.
- Dedicated Flutter client is deferred until web/Mini App usage demonstrates a concrete need.
- MCP is deferred until underlying build/control operations and phone delivery are proven without it. Custom MCP sessions may not expose the built-in connectors needed during implementation/verification.
- Bamboo is temporary bootstrap help only and must not become a permanent system dependency.

## Security Boundary

Never commit credentials, `.env` files, API keys, SSH keys, Telegram tokens, VPS passwords/config secrets, private character manifests, private meshes/textures/renders, or persistent user data.

Current P2/P2V work uses generic non-canonical data only.

## Proven Runtime State

### P0 — PASS

Successful workflow run: `32859113238`
Commit: `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`
Blender: `4.5.12 LTS`

Inspected artifact contents:
- `spatial-forge-smoke.blend` — 441,202 bytes
- `spatial-forge-smoke.glb` — 3,016 bytes
- `preview.png` — 291,816 bytes

The preview was visually inspected and matched the expected cube/ground scene.

### P1 — PASS

Successful rigged workflow run: `32860562804`
Commit: `691939711d29e552d8920a48b6df8b7e091f7c84`
Blender: `4.5.12 LTS`
MPFB: `2.0.17`

Inspected artifact contents:
- `generic-human.blend` — 8,438,771 bytes
- `generic-human.glb` — 8,689,428 bytes
- `front.png` — 355,928 bytes
- `three-quarter.png` — 357,028 bytes

Both previews were visually inspected and showed the expected generic human. Direct GLB inspection found 1 mesh definition, 1 skin, and 53 joints.

### P2.0 — PASS

Current agent-oriented Blender workflows were researched and distilled into the local `spatial-forge-3d` skill rather than installed as core dependencies.

### P2.1–P2.3 — PASS

Schemas:
- `schemas/character-build.schema.json`
- `schemas/build-result.schema.json`

Generic public fixture:
- `fixtures/generic-character-v1.json`

Runtime builder and validator:
- `scripts/build_character.py`
- `scripts/validate_glb.py`
- `.github/workflows/character-manifest.yml`

Successful workflow run: `32864360900`
Commit: `53c5e16bb68a4b588409cb524c0904fbb324225a`
Blender: `4.5.12 LTS`
MPFB: `2.0.17`

The inspected build result contained exactly the six requested normalized MPFB controls. GLB structural inspection found 1 mesh definition, 1 skin, and 53 joints. Clean-Blender fresh import succeeded with 2 mesh objects, 1 armature, and 53 bones. Front and three-quarter previews were visually inspected and showed the expected generic human.

### P2.4 — PASS

Successful workflow run: `32864975879`
Commit: `595bcb5b9768d1f341fac93c803237a0029f3f39`

The downloaded `build-result.json` reported:
- Blender `4.5.12 LTS`
- MPFB `2.0.17`
- only the six proven normalized macros in `applied_controls`
- `chest_circumference = 110 cm` preserved in `unsupported_fields`
- a clear reason that MPFB `2.0.17` has no proven direct control guaranteeing that exact real-world measurement
- 1 GLB mesh definition, 1 skin, 53 joints

Clean fresh import succeeded with 2 mesh objects, 1 armature, and 53 joints. This proves unsupported exact precision is reported rather than fabricated.

## Current Slice

### P2V — Phone Viewer Foundation

This slice is intentionally pulled forward before P2.5/P2.6 so the Creator can inspect real Spatial Forge outputs from Android without PC access.

Target sequence:
1. add a framework-free static viewer under `viewer/`
2. load GLB from an explicit URL
3. support touch rotate/zoom plus camera reset
4. show optional front and three-quarter preview URLs
5. load `build-result.json` and display runtime/applied/unsupported/structural metadata
6. define the smallest URL contract for model/preview/metadata assets
7. establish a static deployment path suitable for `forge.drthorne.uk`
8. verify with a real generic Spatial Forge GLB on Android

Do not add a database, account system, large SPA framework, VPS render dependency, Telegram bot, private canon, or MCP in the initial viewer foundation.

After P2V is usable, return to P2.5 version/lock semantics and P2.6 two-revision runtime proof, then build the VPS protected asset/control path.

## Verification Method

IANEO can inspect GitHub Actions directly. An issue is not required for workflow checking. Use run → jobs/steps → failed logs → artifact list → artifact download → content/structural inspection → fresh import when relevant → visual inspection as applicable. A green run alone is not enough when output correctness matters.

For the web viewer, verify the smallest real behavior: page loads, supplied GLB renders, touch interaction works, metadata is truthful, and no private asset is accidentally committed or permanently exposed.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for any 3D/Blender/MPFB work.
- Use `IMPLEMENTATION_PLAN.md` as the canonical checkbox state.
- Keep changes small and directly tied to the current slice.
- Avoid over-engineering and unnecessary tests/guards.
- Preserve the proven Blender `4.5.12 LTS` + MPFB `2.0.17` baseline unless a dedicated upgrade slice proves a replacement.
- Do not claim runtime success without inspecting the actual workflow result/artifacts.
- After each completed slice, synchronize `IMPLEMENTATION_PLAN.md`, `ROADMAP.md` when needed, and this file.
