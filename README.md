# IANEO Spatial Forge

IANEO Spatial Forge is a zero-incremental-cost, agent-operated 3D creation pipeline designed for phone-first use.

The development/verification model is:

**Creator → ChatGPT / IANEO → GitHub + proven automation → Spatial Forge artifacts + previews → mobile web viewer**

After the backend, control plane, and phone delivery path are independently established, a narrow external MCP adapter may expose those proven operations to an IANEO session:

**External IANEO session → MCP → proven Spatial Forge backend → Telegram / web viewer / Mini App**

MCP is therefore a late control surface, not an early core dependency.

The user should not need to operate Blender directly. Blender and open-source human-generation tooling are treated as headless engines behind automation.

## Current Goal

Prove the smallest useful pipeline first:

1. Run Blender headlessly on GitHub Actions.
2. Create a generic human with MPFB or an equivalent open-source path.
3. Export a `.glb` asset.
4. Produce lightweight preview imagery.
5. Establish a truthful versioned character manifest and revision workflow.
6. Give the Creator an immediate phone-first web viewer for real GLB/preview/metadata inspection.
7. Add the VPS as a protected asset/control backend.
8. Add Telegram delivery and reuse the web viewer as the Mini App/web-view surface.
9. Add MCP only after the underlying operations are independently proven.

The phone viewer is deliberately pulled forward before the remaining revision work because immediate visual inspection is more useful than continuing blind backend development.

## Viewer Direction

The initial viewer is intentionally small:

- framework-free static HTML/CSS/JavaScript
- GLB loaded from an explicit URL
- touch rotate/zoom and camera reset
- optional front and three-quarter preview images
- `build-result.json` metadata display
- no database or account system
- no VPS requirement merely to render a model
- compatible with later Telegram Mini App embedding

Preferred future hostname: `forge.drthorne.uk`.

Cloudflare Pages is the preferred static hosting target once connected. The VPS will later serve protected/private build assets and control APIs rather than running the viewer rendering engine.

## Architecture Principles

- **Zero incremental cost first.** Prefer open-source software and free public-repository GitHub-hosted runners.
- **Phone-first UX.** The phone is the control and inspection surface, not the heavy compute device.
- **Headless by default.** Blender GUI is not part of the production workflow.
- **3D-aware agent workflow.** `skills/spatial-forge-3d/SKILL.md` routes Blender/MPFB creation and validation work through reproducible generation, truthful precision, scoped revisions, export checks, and fixed visual evidence.
- **Small verified slices.** Finish, run, inspect, document, then move to the next slice.
- **No over-engineering.** Add safeguards and tests only when they protect a real failure mode.
- **Private universe data stays private.** This public repository contains engine code, schemas, workflows, skills, viewer code, and non-sensitive test fixtures only.
- **MCP is late-stage only.** Do not sacrifice built-in connector access or shape the core backend around MCP during implementation.
- **Bamboo is bootstrap-only.** Any temporary VPS setup performed through Bamboo must not become a permanent runtime dependency.
- **GitHub Actions becomes the normal automation path once the foundation is ready.**

## Security Rule

Never commit credentials, API tokens, SSH material, Telegram bot tokens, private character canon, private generated assets, or persistent user data to this repository.

See `ROADMAP.md`, `IMPLEMENTATION_PLAN.md`, `AGENTS.md`, `NEW_CHAT_BOOTSTRAP.md`, and `skills/spatial-forge-3d/SKILL.md` before implementation work.
