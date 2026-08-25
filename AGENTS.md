# AGENTS.md — IANEO Spatial Forge

## Working Style

This repository is built in small, runtime-verified slices. Prefer the simplest implementation that proves the current slice. Do not widen scope while a current gate is failing.

## Core Rules

1. Read `ROADMAP.md`, `IMPLEMENTATION_PLAN.md`, and `NEW_CHAT_BOOTSTRAP.md` before changing implementation.
2. For Blender, MPFB, character, scene, GLB, rigging, rendering, or 3D validation work, read `skills/spatial-forge-3d/SKILL.md` and only the routed references needed for the task.
3. For web UI, mobile web, Telegram Mini App, layout, interaction, visual design, accessibility, or future Flutter UI work, read `skills/spatial-forge-ui/SKILL.md` and the relevant routed references.
4. Work only on the current unchecked slice unless a prerequisite is genuinely missing.
5. Keep code and folder structure obvious to a human reader.
6. Avoid speculative abstraction, generic frameworks, large guard layers, and test matrices that slow iteration without protecting a demonstrated failure mode.
7. Use meaningful smoke/integration checks that verify real outputs.
8. Never mark a slice complete from static reasoning alone when it has a runtime success criterion.
9. After a slice passes, update implementation status and the new-chat handoff before advancing.

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

Use repository/environment secrets only when later slices genuinely require them. Early P0/P1/P2 work should use no secrets.

## 3D Pipeline Rules

- Blender should be used headlessly in production automation.
- The proven baseline is Blender `4.5.12 LTS` with MPFB `2.0.17` for current human-generation work. Do not upgrade simply because an external skill uses a newer version.
- Pin important tool versions once a combination is proven.
- Prefer GLB/glTF for phone/runtime inspection unless a slice explicitly needs another format.
- Keep previews lightweight and comparable across revisions.
- Prefer deterministic manifests + Blender Python as durable source when the generated asset can be reproducibly rebuilt.
- Never report unsupported character precision as if the engine reproduced exact anthropometric values. Record real controls, approximations, and unsupported fields explicitly.
- Generic test characters must remain non-canonical and non-private.
- Structural validation and visual validation are separate gates. Metrics do not replace visual inspection.
- When GLB is the deliverable, inspect the exported artifact and fresh-import it when that meaningfully tests the claim.

## UI Rules

- Spatial Forge is an inspection/creation tool, not a marketing site. Keep the model/preview visually dominant.
- Phone and touch behavior are first-class. Do not design a desktop dashboard and shrink it down.
- Use shared semantic design tokens and a small spacing/type system rather than per-screen styling.
- Preserve the same product language and conceptual tokens between web and future Flutter implementations.
- Keep core actions visible; do not hide required behavior behind hover or gesture-only interaction.
- Review actual rendered UI at representative phone widths before claiming a visual slice is complete.
- Fix meaningful Blocker/High issues from `skills/spatial-forge-ui/references/QUALITY.md`; do not delay useful slices for low-value cosmetic perfection.

## Compute Policy

GitHub Actions is the normal build/automation compute path after the foundation is proven. Do not turn the VPS into a heavy render farm. The VPS should eventually coordinate jobs, temporary private assets, auth, and delivery.

Do not use GitHub Actions as a bulk animation/render farm. Keep jobs aligned with build, export, validation, and lightweight preview workflows.

## MCP Policy

Do not introduce MCP during early implementation just to operate Blender or the build pipeline. The development and verification workflow still benefits from built-in repository/connectors, and custom MCP sessions may not expose those built-in connectors.

First establish the build pipeline, manifests, validation semantics, VPS control plane, and phone delivery independently. MCP is a later narrow external control adapter that lets IANEO operate already-proven backend operations. It must not dictate core schemas, file formats, generation scripts, or validation rules.

## Bamboo Policy

Bamboo is a temporary bootstrap/helper agent only. It may assist with one-time VPS foundation setup or emergency repair. Do not build Bamboo into APIs, runtime control flow, schemas, long-term deployment, or recurring implementation steps. Once automated GitHub Actions deployment works, normal operation must not depend on Bamboo.

## Testing Policy

Favor:
- command launches
- output file existence and non-zero size
- format/import validation where cheap and meaningful
- one or two representative end-to-end smoke paths
- actual artifact inspection
- fixed low-cost multiview evidence when visual comparison matters
- representative phone-width UI checks for user-facing surfaces

Avoid by default:
- exhaustive unit tests for glue code
- large fixture suites
- duplicate guards across layers
- slow visual regression systems during early POC stages
- rendering after every tiny adjustment
- large device/viewport matrices without a demonstrated need

Add a stronger test only when a real regression or risk justifies it.

## GitHub Actions Verification Loop

IANEO should inspect Actions directly through the GitHub connector. Do not create a GitHub issue merely to learn whether a workflow passed.

For a runtime-backed slice, use the smallest relevant portion of this loop:
1. identify the workflow run for the relevant commit
2. inspect jobs and step conclusions
3. if failed, fetch the failed job log and repair the concrete root cause
4. if successful, fetch the artifact list
5. download the relevant artifact when output inspection matters
6. inspect filenames, non-zero sizes, and format/content as appropriate
7. fresh-import exported 3D assets when that tests downstream correctness
8. visually inspect generated previews or rendered UI when the slice makes a visual claim
9. only then mark the runtime slice complete and sync docs

A green workflow icon alone is not proof of correct output.

## Documentation Discipline

`IMPLEMENTATION_PLAN.md` is the slice checklist.
`ROADMAP.md` is the high-level direction and phase boundaries.
`NEW_CHAT_BOOTSTRAP.md` is the exact handoff for another chat/agent.
`skills/spatial-forge-3d/SKILL.md` is the project-specific 3D creation/validation intelligence router.
`skills/spatial-forge-ui/SKILL.md` is the project-specific web/mobile/Flutter UI design intelligence router.

Keep all of them synchronized with real runtime state. Documentation must never claim a workflow passes when the latest inspected run fails.
