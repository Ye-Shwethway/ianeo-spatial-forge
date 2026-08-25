# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → MCP → Spatial Forge → 3D assets / previews → Telegram + Mini App**

## Current Architecture Decisions

- Repository is intentionally **public** so standard public-repository GitHub-hosted runners can be used under GitHub's public-repo Actions policy.
- Public repo contains engine code, workflow definitions, schemas, and non-sensitive generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Blender runs headlessly in Actions.
- P0 proved Blender `4.5.12 LTS` can generate `.blend`, `.glb`, and a preview on `ubuntu-latest` after installing `libegl1`.
- MPFB is the initial open-source human-generation engine for P1.
- VPS will later be a lightweight control plane and temporary private asset store, not the heavy rendering machine.
- Telegram bot will be the notification/delivery layer.
- Telegram Mini App is the first planned interactive 3D viewer.
- Dedicated Flutter client is deferred until Mini App usage demonstrates a concrete need.
- MCP is deferred until underlying build/control operations are proven.
- Bamboo is temporary bootstrap help only and must not become a permanent system dependency. After foundation/deployment automation is stable, GitHub Actions is the normal path.

## Security Boundary

Never commit credentials, `.env` files, API keys, SSH keys, Telegram tokens, VPS passwords/config secrets, private character manifests, private meshes/textures/renders, or persistent user data.

P1 remains a **zero-secret** phase using a generic non-canonical human only.

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

## Current Slice

### P1 — Human Generation Proof

Use MPFB with the smallest reliable headless path. Current preferred MPFB release is `2.0.17`, compatible with Blender 4.2 LTS and newer. Start with a generic human only.

Target sequence:
1. install/enable MPFB non-interactively in the Actions runner
2. prove the scripting API loads in background Blender
3. create one generic human basemesh
4. apply a small phenotype set such as gender/age/muscle/weight/height
5. export GLB
6. render front and three-quarter lightweight previews
7. inspect actual artifacts
8. add a built-in rig only after the unrigged human path is reliable

Do not add VPS, Telegram, MCP, canonical characters, or private data until the P1 gate passes.

## Verification Method

IANEO can inspect GitHub Actions directly. An issue is not required for workflow checking. Use run → jobs/steps → failed logs → artifact list → artifact download → content/visual inspection as applicable. A green run alone is not enough when output correctness matters.

## Working Rules

- Read `AGENTS.md` before implementation.
- Use `IMPLEMENTATION_PLAN.md` as the canonical checkbox state.
- Keep changes small and directly tied to the current slice.
- Avoid over-engineering and unnecessary tests/guards.
- Do not claim runtime success without inspecting the actual workflow result/artifacts.
- After each completed slice, synchronize `IMPLEMENTATION_PLAN.md`, `ROADMAP.md` when needed, and this file.
