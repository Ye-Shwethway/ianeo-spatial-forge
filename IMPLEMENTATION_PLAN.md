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

**P0 runtime proof:** Blender `4.5.12 LTS`; successful workflow run `32859113238` on commit `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`. Artifact `spatial-forge-blender-smoke` contained an inspected `.blend`, `.glb`, and preview.

## P1 — Human Generation Proof

- [x] P1.1 Determine the smallest reliable MPFB installation path for headless Blender.
- [x] P1.2 Pin MPFB/tool versions and document licenses/source.
- [x] P1.3 Generate one generic non-canonical human from script.
- [x] P1.4 Control a small set of body/phenotype parameters.
- [x] P1.5 Attach a supported rig if the headless path is reliable.
- [x] P1.6 Export GLB with mesh + skin + joints.
- [x] P1.7 Render front and three-quarter lightweight previews.
- [x] P1.8 Inspect downloaded artifacts and record runtime/file-structure observations.

**P1 runtime proof:** Blender `4.5.12 LTS` with MPFB `2.0.17`; run `32860562804`; GLB contained 1 mesh definition, 1 skin, and 53 joints.

## P2 — Minimal Character Manifest

- [x] P2.0 Research current agent-oriented Blender creation patterns and add `skills/spatial-forge-3d/`.
- [x] P2.1 Define compact JSON schema for character build input.
- [x] P2.2 Define build-result metadata schema.
- [x] P2.3 Map supported manifest fields to engine controls.
- [x] P2.4 Add explicit unsupported-field reporting; never silently fake precision.
- [ ] P2.5 Add version identifier and scoped revision/lock semantics.
- [ ] P2.6 Build two versions of a generic test character and verify scoped changes.

**P2.1–P2.3 runtime proof:** run `32864360900`; exactly six normalized MPFB controls applied; clean fresh import succeeded with 2 mesh objects, 1 armature, and 53 bones.

**P2.4 runtime proof:** run `32864975879`; exact `chest_circumference = 110 cm` was preserved only in `unsupported_fields`, not fabricated as an engine control; GLB remained valid.

**P2.5/P2.6 implementation in progress:** `revision.parent_version` plus a deliberately narrow `locked_fields` list now supports only the six proven `phenotype.*` controls. `scripts/build_character.py` requires `SF_PARENT_MANIFEST` for revisions, rejects parent/version/character mismatches, and fails before generation if any locked control drifts. `fixtures/generic-character-v2.json` changes only `muscle` from `0.72` to `0.52` while locking the other five phenotype controls. Runtime proof workflow: `.github/workflows/character-revision.yml`.

## P2V — Phone Viewer Foundation (pulled forward)

- [x] P2V.1 Add a framework-free mobile viewer shell under `viewer/`.
- [x] P2V.2 Load a GLB from an explicit URL and support rotate/zoom/reset on phone.
- [x] P2V.3 Display optional front and three-quarter preview URLs.
- [x] P2V.4 Load and render `build-result.json` metadata including unsupported fields truthfully.
- [x] P2V.5 Define the minimal build asset URL contract without adding a database or account system.
- [x] P2V.6 Establish a static deployment path suitable for `forge.drthorne.uk`.
- [x] P2V.7 Verify the viewer from an Android browser with a real generic Spatial Forge GLB.

**P2V runtime proof:** Viewer Smoke run `32866763601` proved the static shell. Direct Upload runs `32876020417` and `32876094428` proved GitHub Actions → Wrangler → Cloudflare Pages plus HTTPS on both Pages and custom-domain URLs. Generic demo run `32876486511` reused the proven P2.4 artifact, deployed GLB/previews/metadata under `/demo/`, and verified the live files. The Creator then confirmed on Android that the real GLB rendered, touch interaction worked, front and three-quarter evidence displayed, and build metadata including the unsupported `chest_circumference = 110 cm` request rendered correctly.

**Privacy boundary:** The current `/demo/` files are generic public-safe fixtures. Canonical/private character manifests, GLBs, previews, references, and metadata must never be deployed as static public Pages assets.

## P3 — VPS Control Plane

- [ ] P3.1 Define minimal authenticated HTTP/job interface.
- [ ] P3.2 Bootstrap service directories and least-privilege service account on VPS.
- [ ] P3.3 Add temporary job storage with expiry/cleanup.
- [ ] P3.4 Add build status and protected asset retrieval.
- [ ] P3.5 Establish GitHub Actions deployment as the normal update path.
- [ ] P3.6 Remove Bamboo from the normal operational workflow.

**VPS operating rule:** Manual/Termux/Bamboo access is permitted only for one-time bootstrap, connection establishment, secret installation, or emergency repair. Once the VPS deployment connection is established, normal updates must flow from GitHub Actions to the VPS. Do not make recurring production operation depend on manual Termux commands or Bamboo.

## P4 — Telegram Delivery + Mini App

- [ ] P4.1 Create Telegram bot delivery path using secrets outside the repository.
- [ ] P4.2 Send build status and lightweight preview.
- [ ] P4.3 Open the existing web viewer from Telegram as a Mini App/web view.
- [ ] P4.4 Add protected download action when P3 asset delivery exists.
- [ ] P4.5 Verify end-to-end from Android phone.

## P5 — MCP Control

- [ ] P5.1 Introduce MCP only after build, manifest semantics, control plane, and phone delivery are independently proven.
- [ ] P5.2 Implement a minimal MCP server over already-proven backend operations.
- [ ] P5.3 Expose read/status tools first.
- [ ] P5.4 Add narrow build/create actions.
- [ ] P5.5 Add revision action only after version/lock semantics pass.
- [ ] P5.6 Verify the full external IANEO → MCP → Spatial Forge → Telegram/web viewer loop.

## P6 — Character Canon and Revisions

- [ ] P6.1 Separate temporary builds from approved canonical assets.
- [ ] P6.2 Persist approved manifests privately.
- [ ] P6.3 Add reusable pose assets.
- [ ] P6.4 Add side-by-side version metadata/preview comparison.
- [ ] P6.5 Prove scoped revisions without unrelated drift.

## P7 — Spatial Scene Forge

- [ ] P7.1 Scene manifest.
- [ ] P7.2 Multi-character placement and scale consistency.
- [ ] P7.3 Camera/lens controls.
- [ ] P7.4 Lighting presets.
- [ ] P7.5 Spatial reference renders.

## P8 — Optional Flutter Client

- [ ] P8.1 Re-evaluate only after web/Mini App usage proves a concrete need.
- [ ] P8.2 If justified, create a small inspection/download client rather than a second orchestration system.

## Permanent Rules

- Never commit secrets, credentials, tokens, private keys, private canon, or private generated assets.
- Never introduce a paid dependency without explicit Creator approval.
- Keep production path simple; avoid broad test matrices and speculative guards.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Do not claim a slice passed until actual runtime output has been inspected.
- Update docs after every completed slice before moving on.
