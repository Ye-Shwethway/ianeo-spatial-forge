# IANEO Spatial Forge

IANEO Spatial Forge is a zero-incremental-cost, agent-operated 3D creation pipeline designed for phone-first use.

The development/verification model is:

**Creator → ChatGPT / IANEO → GitHub + proven automation → Spatial Forge artifacts + previews**

After the backend, control plane, and phone delivery path are independently established, a narrow external MCP adapter may expose those proven operations to an IANEO session:

**External IANEO session → MCP → proven Spatial Forge backend → Telegram / Mini App**

MCP is therefore a late control surface, not an early core dependency.

The user should not need to operate Blender directly. Blender and open-source human-generation tooling are treated as headless engines behind automation.

## Current Goal

Prove the smallest useful pipeline first:

1. Run Blender headlessly on GitHub Actions.
2. Create a generic human with MPFB or an equivalent open-source path.
3. Export a `.glb` asset.
4. Produce lightweight preview imagery.
5. Establish a truthful versioned character manifest and revision workflow.
6. Deliver build artifacts for inspection from a phone.

Only after that foundation passes do we add VPS orchestration, Telegram delivery / Mini App viewing, and finally MCP control.

## Architecture Principles

- **Zero incremental cost first.** Prefer open-source software and free public-repository GitHub-hosted runners.
- **Phone-first UX.** The phone is the control and inspection surface, not the heavy compute device.
- **Headless by default.** Blender GUI is not part of the production workflow.
- **3D-aware agent workflow.** `skills/spatial-forge-3d/SKILL.md` routes Blender/MPFB creation and validation work through reproducible generation, truthful precision, scoped revisions, export checks, and fixed visual evidence.
- **Small verified slices.** Finish, run, inspect, document, then move to the next slice.
- **No over-engineering.** Add safeguards and tests only when they protect a real failure mode.
- **Private universe data stays private.** This public repository contains engine code, schemas, workflows, skills, and non-sensitive test fixtures only.
- **MCP is late-stage only.** Do not sacrifice built-in connector access or shape the core backend around MCP during implementation.
- **Bamboo is bootstrap-only.** Any temporary VPS setup performed through Bamboo must not become a permanent runtime dependency.
- **GitHub Actions becomes the normal automation path once the foundation is ready.**

## Security Rule

Never commit credentials, API tokens, SSH material, Telegram bot tokens, private character canon, private generated assets, or persistent user data to this repository.

See `ROADMAP.md`, `IMPLEMENTATION_PLAN.md`, `AGENTS.md`, `NEW_CHAT_BOOTSTRAP.md`, and `skills/spatial-forge-3d/SKILL.md` before implementation work.
