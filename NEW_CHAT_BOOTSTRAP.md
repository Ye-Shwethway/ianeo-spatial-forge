# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → proven Spatial Forge backend → 3D assets / previews → Telegram + Mini App**

MCP is intentionally deferred until the backend and delivery path are independently established. It will later act as a narrow external control adapter, not as an early implementation dependency.

## Current Architecture Decisions

- Repository is intentionally **public** so standard public-repository GitHub-hosted runners can be used under GitHub's public-repo Actions policy.
- Public repo contains engine code, workflow definitions, schemas, skills, and non-sensitive generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Blender runs headlessly in Actions.
- P0 proved Blender `4.5.12 LTS` can generate `.blend`, `.glb`, and a preview on `ubuntu-latest` after installing `libegl1`.
- P1 proved MPFB `2.0.17` can be installed non-interactively, generate a generic human from script, apply macro phenotype parameters, attach the built-in `game_engine` rig, export GLB, and render previews headlessly.
- `skills/spatial-forge-3d/SKILL.md` is the project-specific 3D creation intelligence router. It encodes reproducible generation, truthful precision, scoped revisions, structural-vs-visual validation, export/fresh-import checks, and version-aware Blender/MPFB reference policy.
- External Blender-agent skills are research/methodology references only. Do not copy their runtime assumptions blindly and do not upgrade the proven stack merely because another project uses a newer Blender version.
- VPS will later be a lightweight control plane and temporary private asset store, not the heavy rendering machine.
- Telegram bot will be the notification/delivery layer.
- Telegram Mini App is the first planned interactive 3D viewer.
- Dedicated Flutter client is deferred until Mini App usage demonstrates a concrete need.
- MCP is deferred until underlying build/control operations and phone delivery are proven without it. Custom MCP sessions may not expose the built-in connectors needed during implementation/verification.
- Bamboo is temporary bootstrap help only and must not become a permanent system dependency. After foundation/deployment automation is stable, GitHub Actions is the normal path.

## Security Boundary

Never commit credentials, `.env` files, API keys, SSH keys, Telegram tokens, VPS passwords/config secrets, private character manifests, private meshes/textures/renders, or persistent user data.

P2 still uses generic non-canonical manifests only.

## Proven Runtime State

### P0 — PASS

Successful workflow run: `32859113238`
Commit: `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`
Blender: `4.5.12 LTS`

Inspected artifact contents:
- `spatial-forge-smoke.blend` — 441,202 bytes
- `spatial-forge-smoke.glb` — 3,016 bytes
- `preview.png` — 291,816 bytes

The preview was visually inspected and matched the expected cube/ground scene. The first attempt exposed one missing runtime library (`libEGL.so.1`); installing Ubuntu package `libegl1` resolved it.

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

Both previews were visually inspected and showed the expected generic human. Direct inspection of the GLB JSON chunk found 1 mesh, 1 skin, and 53 joints, confirming that the built-in `game_engine` rig survived export. The first P1 attempt failed because Blender extension online access was disabled; adding `--online-mode` to the extension-install command fixed it.

### P2.0 — PASS

Current agent-oriented Blender workflows were researched and distilled into the local `spatial-forge-3d` skill rather than installed as core dependencies.

The skill establishes:
- a smallest-build contract before creation
- deterministic manifest/Blender-Python source preference
- truthful supported/approximate/unsupported precision handling
- narrow revision and lock semantics
- fixed comparable visual evidence
- independent structural and visual gates
- GLB structural and fresh-import validation when relevant
- a Blender/MPFB evidence hierarchy that prefers proven local runtime and official/version-matched facts
- a late-stage-only MCP boundary

## Current Slice

### P2.1 — Minimal Character Build Schema

Keep this intentionally compact. The manifest must describe only controls the engine can truthfully support.

Read `skills/spatial-forge-3d/SKILL.md` before implementation, then route to its reference files as needed.

Target sequence:
1. define one small versioned character-build JSON schema
2. define one small build-result metadata schema
3. map supported macro fields to MPFB controls
4. report unsupported requested precision explicitly rather than fabricating it
5. add version id plus narrow lock/revision semantics
6. build two generic manifest revisions and prove that the intended field changes while locked fields remain stable

Do not introduce a broad RPG/stat schema, database layer, VPS service, Telegram transport, private canon, or MCP in P2.

## Verification Method

IANEO can inspect GitHub Actions directly. An issue is not required for workflow checking. Use run → jobs/steps → failed logs → artifact list → artifact download → content/structural inspection → fresh import when relevant → visual inspection as applicable. A green run alone is not enough when output correctness matters.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for any 3D/Blender/MPFB work.
- Use `IMPLEMENTATION_PLAN.md` as the canonical checkbox state.
- Keep changes small and directly tied to the current slice.
- Avoid over-engineering and unnecessary tests/guards.
- Preserve the proven Blender `4.5.12 LTS` + MPFB `2.0.17` baseline unless a dedicated upgrade slice proves a replacement.
- Do not claim runtime success without inspecting the actual workflow result/artifacts.
- After each completed slice, synchronize `IMPLEMENTATION_PLAN.md`, `ROADMAP.md` when needed, and this file.
