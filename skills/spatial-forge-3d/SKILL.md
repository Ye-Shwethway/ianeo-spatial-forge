---
name: spatial-forge-3d
description: Use for IANEO Spatial Forge 3D creation, Blender/MPFB character generation, scene building, GLB export, visual evidence, revision control, and artifact validation. Routes work through the smallest reproducible workflow and treats generated Python/manifests as durable source rather than opaque .blend files. Not for unrelated UI/app design.
---

# Spatial Forge 3D

A project-specific 3D creation intelligence layer for IANEO Spatial Forge.

This skill exists to let an agent make reliable 3D decisions without requiring the Creator to manually operate Blender. It combines reproducible generation, truthful parameter handling, fixed visual evidence, and export validation while keeping the implementation deliberately small.

## Runtime Baseline

Until a later slice explicitly changes and re-proves it, use the repository's proven stack:

- Blender `4.5.12 LTS`
- MPFB `2.0.17` for current human-generation work
- headless Blender on GitHub Actions
- GLB/glTF as the primary phone/runtime inspection format

Do not upgrade tools merely because another project validates a newer version.

## Route the Task

Read only the references needed for the request.

- Any asset/character/scene creation or revision: read `references/CREATION_WORKFLOW.md`.
- Any claim that an output is correct, game-ready, unchanged, rigged, export-safe, or visually satisfactory: read `references/VALIDATION.md`.
- Any Blender/MPFB API name, operator, enum, parameter, version-sensitive behavior, or undocumented assumption: read `references/REFERENCE_POLICY.md`.

Character work uses creation + validation by default.

## Core Contract

Before implementation, reduce the request to the smallest explicit contract that matters:

1. subject and intended use
2. required geometry/body/face controls
3. scale and spatial relationships
4. rig/animation requirement, if any
5. material/appearance requirement, if any
6. required outputs
7. required visual evidence
8. fields/features that must remain locked during revision
9. unsupported or approximate requirements

Do not expand a narrow request into a broad character system, renderer, database, or framework.

## Durable Source Rule

Prefer deterministic, reviewable source inputs:

- JSON manifests for user intent and versioned parameters
- Blender Python for deterministic generated scene/asset construction
- explicit referenced source assets when a later phase allows them

`.blend`, `.glb`, renders, and previews are build outputs. They are not the only durable source of truth when a reproducible source can exist.

## Truthful Precision Rule

Never present an engine approximation as exact anthropometric or visual reproduction.

For every requested parameter, classify it as one of:

- `supported_exact` — only when the engine/API truly guarantees the requested semantics
- `supported_control` — a real engine control exists, but its normalized value is not an exact real-world measurement
- `derived` — computed from supported source values
- `approximate` — intentionally approximated and disclosed
- `unsupported` — no honest mapping exists

Do not silently invent a control to satisfy a schema.

## Revision Rule

A revision must be scoped.

- Carry forward the prior approved manifest/version.
- Change only requested fields plus unavoidable derived metadata.
- Locked fields must be compared before/after.
- If the engine cannot preserve a requested lock reliably, report the limitation before declaring success.
- Never regenerate unrelated approved properties merely because regeneration is convenient.

## Visual Judgment Rule

Structural validation and visual quality are separate gates.

Automated metrics can prove facts such as file existence, mesh/skin/joint counts, transform ranges, or successful fresh import. They cannot prove that a face looks right, proportions read naturally, composition works, or a revision preserved visual identity.

Use fixed comparable previews and inspect them before making a visual-quality claim.

## Export Rule

When GLB is an intended deliverable:

1. build the authored scene
2. export GLB
3. inspect the GLB structurally
4. when practical, fresh-import the exported GLB into a clean Blender scene
5. compare the imported result against the authored intent

Do not call `.blend` success sufficient proof of a GLB deliverable.

## Efficiency Rule

Validation must protect demonstrated risks without becoming a render/test farm.

Prefer:

- one representative end-to-end build
- cheap structural checks
- fixed low-cost preview views
- targeted fresh-import validation
- one focused revision comparison

Avoid exhaustive unit-test matrices, rendering every tiny iteration, speculative validators, or broad benchmark infrastructure during early phases.

## MCP Policy

MCP is not required for this skill and must not be introduced during early implementation simply to drive Blender.

Use built-in repository/connectors and GitHub Actions while those are required for implementation and verification. Add MCP only after the underlying build/control plane is independently established, as a narrow external control adapter for IANEO.

Never let MCP availability determine the core file formats, schemas, generation scripts, or validation semantics.

## Privacy Boundary

This repository is public. Generic non-canonical fixtures only during public pipeline development.

Never commit private character canon, private manifests, private generated meshes/renders/textures, credentials, tokens, or persistent private user data.

## Completion Standard

A 3D slice is complete only when the evidence required by that slice is inspected.

Typical order:

`contract → deterministic source → headless build → structural checks → export → fresh-import check when relevant → fixed visual evidence → human/IANEO visual judgment → docs sync`

A green workflow icon alone is never visual proof.
