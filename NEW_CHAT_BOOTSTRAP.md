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
- Blender is intended to run **headlessly**.
- MPFB is the initial preferred open-source human-generation candidate, but it is not introduced until plain Blender headless P0 passes.
- VPS will later be a lightweight control plane and temporary private asset store, not the heavy rendering machine.
- Telegram bot will be the notification/delivery layer.
- Telegram Mini App is the first planned interactive 3D viewer.
- Dedicated Flutter client is deferred until Mini App usage demonstrates a concrete need.
- MCP is deferred until underlying build/control operations are proven.
- Bamboo is temporary bootstrap help only and must not become a permanent system dependency. After foundation/deployment automation is stable, GitHub Actions is the normal path.

## Security Boundary

Never commit credentials, `.env` files, API keys, SSH keys, Telegram tokens, VPS passwords/config secrets, private character manifests, private meshes/textures/renders, or persistent user data.

P0 and preferably P1 should require **zero secrets**.

## Current Slice

Foundation documentation is being established first. After foundation verification, the next implementation target is:

### P0.1 — Minimal manual GitHub Actions workflow

Then:
1. provision/pin Blender on `ubuntu-latest`
2. run a tiny Python smoke script
3. generate deterministic primitive scene
4. save `.blend`
5. export `.glb`
6. render one lightweight preview
7. upload outputs as Actions artifacts
8. inspect real outputs before marking P0 complete

Do **not** add MPFB, VPS, Telegram, MCP, or private data before the P0 gate passes.

## Working Rules

- Read `AGENTS.md` before implementation.
- Use `IMPLEMENTATION_PLAN.md` as the canonical checkbox state.
- Keep changes small and directly tied to the current slice.
- Avoid over-engineering and unnecessary tests/guards.
- Do not claim runtime success without inspecting the actual workflow result/artifacts.
- After each completed slice, synchronize `IMPLEMENTATION_PLAN.md`, `ROADMAP.md` when needed, and this file.
