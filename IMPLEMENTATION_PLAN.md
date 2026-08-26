# IANEO Spatial Forge Implementation Plan

Work one slice at a time. A slice is complete only after runtime evidence is inspected and docs are synchronized.

## Foundation

- [x] F0 Repository, architecture rules, AGENTS.md, roadmap, implementation plan, bootstrap handoff.

## P0 — Headless Blender Proof

- [x] P0 Headless Blender build/export/preview/artifact proof.

**Proof:** Blender `4.5.12 LTS`; run `32859113238`.

## P1 — Human Generation Proof

- [x] P1 MPFB human generation, rig, GLB and preview proof.

**Proof:** Blender `4.5.12 LTS`, MPFB `2.0.17`; run `32860562804`; 1 mesh definition, 1 skin, 53 joints.

## P2 — Character Manifest + Revision

- [x] P2.0 Spatial Forge 3D skill.
- [x] P2.1 Character/build-result schemas.
- [x] P2.2 Six proven MPFB macro controls.
- [x] P2.3 Unsupported precision reporting.
- [x] P2.4 Version/lock semantics.
- [x] P2.5 Scoped revision proof.

**Proof:** runs `32864360900`, `32864975879`, `32877860898`.

## P2V — Phone Viewer Foundation

- [x] P2V Framework-free mobile viewer, Pages deployment, Android rendering/touch verification.

**Proof:** Viewer Smoke `32866763601`; Direct Upload `32876020417` / `32876094428`; demo `32876486511`.

## P3 — Private Web Control Plane

- [x] P3.1 Minimal control/session API.
- [x] P3.2 VPS service bootstrap and localhost-only runtime.
- [x] P3.3 Session expiry/cleanup.
- [x] P3.4 Protected HTTPS asset retrieval.
- [x] P3.5 GitHub Actions normal deployment path.
- [x] P3.6 Bamboo/Termux removed from normal operation.
- [x] P3.7 Phone-first Asset Library with authenticated same-origin `/api` proxy.

**Runtime state:** protected web login, private VPS build storage, temporary asset delivery, Android 3D viewing, web build listing/open/delete path, and explicit logout are proven. Bamboo/Termux remain bootstrap/emergency-only.

## P3Q — Character Quality & Visual Fidelity

**Goal:** progress from a structurally valid generic MPFB human to a visually convincing, detailed, attractive character while preserving deterministic builds and phone-friendly GLB output.

- [x] P3Q.1 Establish a fixed visual baseline.
  - Generic v1 fixture, unchanged for quality.
  - Fixed evidence: front, three-quarter, profile, face/upper-body close view.
  - Structural + fresh-import validation retained.
  - Visual defects inspected and recorded.

**P3Q.1 proof:** Character Quality Baseline run `32932834097` PASS. Artifact `9593852812`, digest `sha256:513f432ee25037b8bb0555f851bb3f2954e153a217f70137d894ae0b20b57737`. Blender `4.5.12 LTS`, MPFB `2.0.17`; GLB 1 mesh / 1 skin / 53 joints; fresh import 2 mesh objects / 1 armature / 53 joints. The artifact contained `.blend`, `.glb`, four PNG evidence views, `build-result.json`, and `fresh-import.json`; all four images were visually inspected.

**Baseline defects:**
- body silhouette is usable but generic
- face is the largest bottleneck: weak eye/nose/lip/jaw/chin definition
- pale single material creates a clay/mannequin appearance
- production skin/eyes/brows/hair are absent
- hands/feet and profile torso/hip forms remain basic
- current face view is usable for comparison but should become a tighter portrait later.

- [ ] P3Q.2 Improve mesh/surface presentation.
  - shading, normals, seams
  - smallest useful subdivision/surface treatment
  - GLB + fresh-import comparison.

- [ ] P3Q.3 Expand face-shape control.
  - [x] P3Q.3A **Technical face-control proof.**
    - MPFB `2.0.17` runtime target inventory was probed instead of inventing schema fields.
    - Probe found 530 bundled targets, including 270 face/head-related targets.
    - A small 11-target generic face profile was applied, baked, rigged, exported to GLB, and fresh-imported successfully.
    - Final face workflow run `32934697014` PASS; artifact `9594484821`.
    - Private VPS install path was proven with build ID `generic-face-quality-v1`; install run `32938078210` PASS.
    - Creator opened the private build from the authenticated Asset Library on Android and confirmed it renders in the web viewer.
    - **Result:** transport/control is proven, but visible quality gain is too subtle. This is a technical proof, not a visual-quality pass.
  - [ ] P3Q.3B **Visible face sculpt pass — ACTIVE.**
    - Temporarily remove/disable the current hair asset in face-review builds because it obscures the face.
    - Keep body macro phenotype locked.
    - Use stronger but still human-looking supported MPFB face targets for head/jaw/chin/cheek/nose/eye-region/lips.
    - Tighten portrait framing so head/shoulders dominate the comparison.
    - Produce baseline vs revised fixed evidence and require an obvious visual difference before calling the slice visually successful.
    - Do not add skin/material complexity yet; first prove readable facial form.

**P3Q.3 visual finding:** the first 11-target build is structurally healthy and web-deliverable, but the Creator correctly judged that it looks almost the same as the baseline. The current blocky hair also hides much of the face. Continue with P3Q.3B rather than claiming face quality is complete.

- [ ] P3Q.4 Production-quality PBR skin/eyes/mouth appearance.
- [ ] P3Q.5 Hair/brows/facial-hair asset path.
- [ ] P3Q.6 Clean replaceable clothing asset path.
- [ ] P3Q.7 Representative deformation/pose quality.
- [ ] P3Q.8 Presentation-grade viewer/render defaults.
- [ ] P3Q.9 Final generic quality proof against P3Q.1 baseline.

### P3Q evidence-driven order

Current order is **P3Q.3B visible face form → P3Q.4 skin/eyes/mouth → P3Q.5 hair/brows → P3Q.2 mesh/surface polish → clothing/deformation/presentation** unless new visual evidence justifies a change. P3Q.2 remains required; it is simply not the highest-value next move.

### P3Q quality rule

Structural validity and visual quality are separate gates. Green Actions runs, valid targets, successful GLB export, mesh/joint counts, and successful web delivery do not prove that a character looks good. Each visual slice requires fixed comparable evidence and actual Creator inspection.

## P4 — Telegram Delivery + Mini App

- [ ] P4.1 Bot delivery path.
- [ ] P4.2 Build status + lightweight preview.
- [ ] P4.3 Open existing viewer as Mini App/web view.
- [ ] P4.4 Protected download action.
- [ ] P4.5 Android end-to-end proof.

## P5 — MCP Control

- [ ] P5.1 Introduce MCP only after proven backend/delivery.
- [ ] P5.2 Minimal MCP adapter over proven operations.
- [ ] P5.3 Read/status first.
- [ ] P5.4 Narrow build/create actions.
- [ ] P5.5 Revision after lock semantics remain proven.
- [ ] P5.6 External IANEO end-to-end proof.

## P6 — Character Canon and Revisions

- [ ] P6.1 Temporary vs canonical assets.
- [ ] P6.2 Private approved manifests.
- [ ] P6.3 Reusable poses.
- [ ] P6.4 Version comparison.
- [ ] P6.5 Scoped revision proof without unrelated drift.

## P7 — Spatial Scene Forge

- [ ] P7.1 Scene manifest.
- [ ] P7.2 Multi-character placement/scale.
- [ ] P7.3 Camera/lens.
- [ ] P7.4 Lighting presets.
- [ ] P7.5 Spatial reference renders.

## P8 — Optional Flutter Client

- [ ] P8 Re-evaluate only if web/Mini App becomes insufficient.

## Permanent Rules

- Public repo contains generic/public-safe development material only.
- No paid dependency without explicit approval.
- Keep production simple; avoid broad test matrices and speculative guards.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work and `skills/spatial-forge-ui/SKILL.md` for UI work.
- Do not claim success until required runtime and visual evidence is inspected.
- Update docs after every completed slice or material scope/status change.
