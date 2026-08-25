# IANEO Spatial Forge Implementation Plan

Work one slice at a time. A slice is complete only when its runtime result has been inspected and the handoff docs are updated.

## Foundation

- [x] F0.1 Create public repository.
- [x] F0.2 Add README and architecture/security principles.
- [x] F0.3 Add roadmap.
- [x] F0.4 Add implementation plan, AGENTS.md, bootstrap handoff, and `.gitignore`.
- [x] F0.5 Verify repository foundation from `main`.

## P0 — Headless Blender Proof

- [x] P0.1 Add minimal GitHub Actions workflow with manual dispatch.
- [x] P0.2 Install or provision a pinned Blender version on `ubuntu-latest`.
- [x] P0.3 Add one tiny Blender Python smoke script.
- [x] P0.4 Generate a deterministic primitive test scene.
- [x] P0.5 Export `.blend` and `.glb`.
- [x] P0.6 Render one lightweight preview image.
- [x] P0.7 Upload outputs as GitHub Actions artifacts.
- [x] P0.8 Run workflow and inspect actual artifact outputs.
- [x] P0.9 Record exact Blender version, workflow run, outputs, and any limitations in docs.

**P0 runtime proof:** Blender `4.5.12 LTS`; successful workflow run `32859113238` on commit `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`. Artifact `spatial-forge-blender-smoke` contained an inspected `spatial-forge-smoke.blend` (441,202 bytes), `spatial-forge-smoke.glb` (3,016 bytes), and `preview.png` (291,816 bytes). The preview was visually inspected and showed the expected cube/ground test scene. First run failed only because `libEGL.so.1` was absent on the runner; installing `libegl1` fixed the headless render runtime.

## P1 — Human Generation Proof

- [x] P1.1 Determine the smallest reliable MPFB installation path for headless Blender.
- [x] P1.2 Pin MPFB/tool versions and document licenses/source.
- [x] P1.3 Generate one generic non-canonical human from script.
- [x] P1.4 Control a small set of body/phenotype parameters.
- [x] P1.5 Attach a supported rig if the headless path is reliable.
- [x] P1.6 Export GLB with mesh + skin + joints.
- [x] P1.7 Render front and three-quarter lightweight previews.
- [x] P1.8 Inspect downloaded artifacts and record runtime/file-structure observations. Phone delivery/viewing remains a P4 concern.

**P1 runtime proof:** Blender `4.5.12 LTS` with MPFB `2.0.17`; successful rigged workflow run `32860562804` on commit `691939711d29e552d8920a48b6df8b7e091f7c84`. Artifact `spatial-forge-mpfb-human` was downloaded and inspected. It contained `generic-human.blend` (8,438,771 bytes), `generic-human.glb` (8,689,428 bytes), `front.png` (355,928 bytes), and `three-quarter.png` (357,028 bytes). Both previews were visually inspected and showed the expected generic human. The GLB JSON chunk was inspected directly and contained 1 mesh, 1 skin, and 53 rig joints. MPFB's built-in `game_engine` rig therefore survived GLB export. The first P1 attempt failed because Blender extension sync was blocked by online-access preference; using Blender's `--online-mode` on the extension-install command fixed the install path.

**P1 privacy gate:** PASS — only a generic non-canonical human and non-sensitive parameters were used.

## P2 — Minimal Character Manifest

- [ ] P2.1 Define compact JSON schema for character build input.
- [ ] P2.2 Define build-result metadata schema.
- [ ] P2.3 Map supported manifest fields to engine controls.
- [ ] P2.4 Add explicit unsupported-field reporting; never silently fake precision.
- [ ] P2.5 Add version identifier and scoped revision/lock semantics.
- [ ] P2.6 Build two versions of a generic test character and verify scoped changes.

## P3 — VPS Control Plane

- [ ] P3.1 Define minimal authenticated HTTP/job interface.
- [ ] P3.2 Bootstrap service directories and least-privilege service account on VPS.
- [ ] P3.3 Add temporary job storage with expiry/cleanup.
- [ ] P3.4 Add build status and protected asset retrieval.
- [ ] P3.5 Establish GitHub Actions deployment as the normal update path.
- [ ] P3.6 Remove Bamboo from the normal operational workflow.

**Bamboo note:** Bamboo may be used only as a temporary bootstrap helper for P3.2 or emergency repair. Do not encode Bamboo as a permanent component, dependency, or recurring implementation step.

## P4 — Telegram Delivery + Mini App

- [ ] P4.1 Create Telegram bot delivery path using secrets outside the repository.
- [ ] P4.2 Send build status and lightweight preview.
- [ ] P4.3 Add `Open 3D` Mini App entry point.
- [ ] P4.4 Implement minimal GLB viewer with rotate, zoom, reset, and metadata.
- [ ] P4.5 Add protected download action.
- [ ] P4.6 Verify end-to-end from Android phone.

## P5 — MCP Control

- [ ] P5.1 Implement minimal MCP server over proven backend operations.
- [ ] P5.2 Expose read/status tools first.
- [ ] P5.3 Add narrow build/create actions.
- [ ] P5.4 Add revision action only after version/lock semantics pass.
- [ ] P5.5 Verify Creator → IANEO → MCP → build → Telegram/Mini App loop.

## P6 — Character Canon and Revisions

- [ ] P6.1 Separate temporary builds from approved canonical assets.
- [ ] P6.2 Persist approved manifests privately.
- [ ] P6.3 Add reusable pose assets.
- [ ] P6.4 Add side-by-side version metadata/preview comparison.
- [ ] P6.5 Prove `body locked, face only` style revisions without unrelated drift.

## P7 — Spatial Scene Forge

- [ ] P7.1 Scene manifest.
- [ ] P7.2 Multi-character placement and scale consistency.
- [ ] P7.3 Camera/lens controls.
- [ ] P7.4 Lighting presets.
- [ ] P7.5 Spatial reference renders for downstream image generation.

## P8 — Optional Flutter Client

- [ ] P8.1 Re-evaluate only after Mini App usage proves a concrete need.
- [ ] P8.2 If justified, create a small inspection/download client rather than a second orchestration system.

## Permanent Rules

- Never commit secrets, credentials, tokens, private keys, private canon, or private generated assets.
- Never rely on repository secrecy; this repository is intentionally public.
- Never introduce a paid dependency without explicit Creator approval.
- Keep production path simple; avoid broad test matrices and speculative guards.
- Do not claim a slice passed until its actual runtime output has been inspected.
- For Actions-backed slices, verify in this order when available: workflow run → jobs/steps → failed job logs → artifact list → downloaded artifact contents → visual output inspection.
- Issues are for durable project discussion/tracking, not a required mechanism for checking workflow state.
- Update docs after every completed slice before moving on.
