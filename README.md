# IANEO Spatial Forge

IANEO Spatial Forge is a zero-incremental-cost, agent-operated 3D creation pipeline designed for phone-first use.

The long-term interaction model is:

**Creator → ChatGPT / IANEO → MCP → Spatial Forge → 3D assets + previews**

The user should not need to operate Blender directly. Blender and open-source human-generation tooling are treated as headless engines behind automation.

## Current Goal

Prove the smallest useful pipeline first:

1. Run Blender headlessly on GitHub Actions.
2. Create a generic human with MPFB or an equivalent open-source path.
3. Export a `.glb` asset.
4. Produce lightweight preview imagery.
5. Deliver build artifacts for inspection from a phone.

Only after that foundation passes do we add VPS orchestration, Telegram delivery / Mini App viewing, and MCP control.

## Architecture Principles

- **Zero incremental cost first.** Prefer open-source software and free public-repository GitHub-hosted runners.
- **Phone-first UX.** The phone is the control and inspection surface, not the heavy compute device.
- **Headless by default.** Blender GUI is not part of the production workflow.
- **Small verified slices.** Finish, run, inspect, document, then move to the next slice.
- **No over-engineering.** Add safeguards and tests only when they protect a real failure mode.
- **Private universe data stays private.** This public repository contains engine code, schemas, workflows, and non-sensitive test fixtures only.
- **Bamboo is bootstrap-only.** Any temporary VPS setup performed through Bamboo must not become a permanent runtime dependency.
- **GitHub Actions becomes the normal automation path once the foundation is ready.**

## Security Rule

Never commit credentials, API tokens, SSH material, Telegram bot tokens, private character canon, private generated assets, or persistent user data to this repository.

See `ROADMAP.md`, `IMPLEMENTATION_PLAN.md`, `AGENTS.md`, and `NEW_CHAT_BOOTSTRAP.md` before implementation work.
