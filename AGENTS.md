# AGENTS.md — IANEO Spatial Forge

## Working Style

This repository is built in small, runtime-verified slices. Prefer the simplest implementation that proves the current slice. Do not widen scope while a current gate is failing.

## Core Rules

1. Read `ROADMAP.md`, `IMPLEMENTATION_PLAN.md`, and `NEW_CHAT_BOOTSTRAP.md` before changing implementation.
2. Work only on the current unchecked slice unless a prerequisite is genuinely missing.
3. Keep code and folder structure obvious to a human reader.
4. Avoid speculative abstraction, generic frameworks, large guard layers, and test matrices that slow iteration without protecting a demonstrated failure mode.
5. Use meaningful smoke/integration checks that verify real outputs.
6. Never mark a slice complete from static reasoning alone when it has a runtime success criterion.
7. After a slice passes, update implementation status and the new-chat handoff before advancing.

## Zero-Cost Constraint

Do not add paid services, paid APIs, paid runners, or dependencies that require payment for the intended workflow without explicit Creator approval.

## Public Repository / Privacy Boundary

This repository is public. Treat everything committed here as world-readable.

Never commit:
- `.env` files or environment dumps
- API keys or access tokens
- SSH/private keys, certificates, credentials, passwords
- Telegram bot tokens
- VPS credentials or private host configuration containing secrets
- private character canon/manifests
- private generated meshes, textures, renders, or scene assets
- persistent user data

Use repository/environment secrets only when later slices genuinely require them. Early P0/P1 work should use no secrets.

## 3D Pipeline Rules

- Blender should be used headlessly in production automation.
- Pin important tool versions once a combination is proven.
- Prefer GLB/glTF for phone/runtime inspection unless a slice explicitly needs another format.
- Keep previews lightweight.
- Never report unsupported character precision as if the engine reproduced exact anthropometric values. Record approximations and unsupported controls explicitly.
- Generic test characters must remain non-canonical and non-private.

## Compute Policy

GitHub Actions is the normal build/automation compute path after the foundation is proven. Do not turn the VPS into a heavy render farm. The VPS should eventually coordinate jobs, temporary private assets, auth, and delivery.

Do not use GitHub Actions as a bulk animation/render farm. Keep jobs aligned with build, export, validation, and lightweight preview workflows.

## Bamboo Policy

Bamboo is a temporary bootstrap/helper agent only. It may assist with one-time VPS foundation setup or emergency repair. Do not build Bamboo into APIs, runtime control flow, schemas, long-term deployment, or recurring implementation steps. Once automated GitHub Actions deployment works, normal operation must not depend on Bamboo.

## Testing Policy

Favor:
- command launches
- output file existence and non-zero size
- format/import validation where cheap and meaningful
- one or two representative end-to-end smoke paths
- actual artifact inspection

Avoid by default:
- exhaustive unit tests for glue code
- large fixture suites
- duplicate guards across layers
- slow visual regression systems during early POC stages

Add a stronger test only when a real regression or risk justifies it.

## Documentation Discipline

`IMPLEMENTATION_PLAN.md` is the slice checklist.
`ROADMAP.md` is the high-level direction and phase boundaries.
`NEW_CHAT_BOOTSTRAP.md` is the exact handoff for another chat/agent.

Keep all three synchronized with real runtime state. Documentation must never claim a workflow passes when the latest inspected run fails.
