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
- [x] P1.8 Inspect downloaded artifacts and record runtime/file-structure observations.

**P1 runtime proof:** Blender `4.5.12 LTS` with MPFB `2.0.17`; successful rigged workflow run `32860562804` on commit `691939711d29e552d8920a48b6df8b7e091f7c84`. Artifact `spatial-forge-mpfb-human` was downloaded and inspected. It contained `generic-human.blend` (8,438,771 bytes), `generic-human.glb` (8,689,428 bytes), `front.png` (355,928 bytes), and `three-quarter.png` (357,028 bytes). Both previews were visually inspected and showed the expected generic human. The GLB JSON chunk was inspected directly and contained 1 mesh, 1 skin, and 53 rig joints. MPFB's built-in `game_engine` rig therefore survived GLB export. The first P1 attempt failed because Blender extension sync was blocked by online-access preference; using Blender's `--online-mode` on the extension-install command fixed the install path.

**P1 privacy gate:** PASS — only a generic non-canonical human and non-sensitive parameters were used.

## P2 — Minimal Character Manifest

- [x] P2.0 Research current agent-oriented Blender creation patterns and add a project-specific `spatial-forge-3d` skill covering reproducible creation, truthful precision, scoped revisions, structural + visual validation, export/fresh-import checks, version-aware reference policy, and late-stage-only MCP policy.
- [x] P2.1 Define compact JSON schema for character build input.
- [x] P2.2 Define build-result metadata schema.
- [x] P2.3 Map supported manifest fields to engine controls.
- [x] P2.4 Add explicit unsupported-field reporting; never silently fake precision.
- [ ] P2.5 Add version identifier and scoped revision/lock semantics.
- [ ] P2.6 Build two versions of a generic test character and verify scoped changes.

**P2 workflow intelligence:** `skills/spatial-forge-3d/SKILL.md` is the routing layer for Blender/MPFB/3D work. Its references define the smallest-build contract, deterministic manifest/Python source rule, fixed visual evidence, structural-vs-visual gates, GLB fresh-import validation when relevant, and Blender/MPFB reference hierarchy. The proven baseline remains Blender `4.5.12 LTS` + MPFB `2.0.17`; external skills are methodology references, not runtime dependencies.

**P2.1–P2.3 runtime proof:** `schemas/character-build.schema.json` and `schemas/build-result.schema.json` passed Draft 2020-12 static validation. `fixtures/generic-character-v1.json` contains only the six runtime-proven normalized MPFB controls: gender, age, muscle, weight, height, and proportions. Character Manifest Proof run `32864360900` on commit `53c5e16bb68a4b588409cb524c0904fbb324225a` passed every step. The inspected artifact reported Blender `4.5.12 LTS`, MPFB `2.0.17`, exactly the six requested applied controls, 1 GLB mesh definition, 1 skin, and 53 joints. Front and three-quarter previews were visually inspected and showed the expected generic human. A separate clean-Blender fresh import of `generic-character-v1.glb` succeeded with 2 imported mesh objects, 1 armature, and 53 bones. The manifest builder asserts `mpfb.VERSION == 2.0.17`, so extension drift now fails visibly instead of silently changing the proven runtime.

**P2.4 runtime proof:** Character Manifest Proof run `32864975879` on commit `595bcb5b9768d1f341fac93c803237a0029f3f39` completed successfully. The downloaded artifact preserved the requested `chest_circumference = 110 cm` only in `unsupported_fields`, with a clear reason that MPFB `2.0.17` has no proven direct control guaranteeing that exact real-world measurement. `applied_controls` still contained only the six proven MPFB macros. The build produced a valid GLB with 1 mesh definition, 1 skin, and 53 joints; clean fresh import succeeded with 2 mesh objects, 1 armature, and 53 joints. This proves unsupported exact measurements are reported rather than silently fabricated.

## P2V — Phone Viewer Foundation (pulled forward)

Reason: the Creator currently needs a phone-first inspection surface before the remaining P2 revision work. This is a deliberate usability slice, not a replacement for P2.5/P2.6.

- [x] P2V.1 Add a framework-free mobile viewer shell under `viewer/`.
- [ ] P2V.2 Load a GLB from an explicit URL and support rotate/zoom/reset on phone.
- [ ] P2V.3 Display optional front and three-quarter preview URLs.
- [ ] P2V.4 Load and render `build-result.json` metadata including unsupported fields truthfully.
- [ ] P2V.5 Define the minimal build asset URL contract without adding a database or account system.
- [ ] P2V.6 Establish a static deployment path suitable for `forge.drthorne.uk`.
- [ ] P2V.7 Verify the viewer from an Android browser with a real generic Spatial Forge GLB.

**P2V.1 runtime proof:** `viewer/index.html`, `viewer/app.js`, `viewer/styles.css`, and `viewer/README.md` now define a framework-free, stateless mobile viewer. `@google/model-viewer` is explicitly pinned to `4.3.1`. Viewer Smoke run `32866763601` on commit `580048d40ec5189317a30698305faa4956b45514` completed successfully: the workflow served `viewer/` through a local HTTP server and fetched/verified the HTML, JavaScript, CSS, pinned viewer dependency reference, and URL-driven app wiring. This proves the static shell is serveable; real GLB rendering/touch behavior remains P2V.2/P2V.7 and is not yet claimed.

**Viewer boundary:** The initial viewer is static and must not require the VPS merely to render a model. The VPS becomes the later protected/private asset and control backend. Prefer a small web component/vanilla JavaScript implementation over a large SPA framework. Keep the viewer compatible with later Telegram Mini App embedding.

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
- [ ] P4.3 Open the existing web viewer from Telegram as a Mini App/web view.
- [ ] P4.4 Add protected download action when P3 asset delivery exists.
- [ ] P4.5 Verify end-to-end from Android phone.

## P5 — MCP Control

- [ ] P5.1 Introduce MCP only after the build pipeline, manifest semantics, control plane, and phone delivery are independently proven without MCP.
- [ ] P5.2 Implement a minimal MCP server over already-proven backend operations.
- [ ] P5.3 Expose read/status tools first.
- [ ] P5.4 Add narrow build/create actions.
- [ ] P5.5 Add revision action only after version/lock semantics pass.
- [ ] P5.6 Verify Creator → external IANEO session → MCP → proven Spatial Forge backend → Telegram/web viewer loop.

**MCP boundary:** During implementation and verification, preserve access to built-in repository/connectors. MCP is a late external control adapter, not a core implementation dependency, and must not dictate schemas, file formats, generation scripts, or validation semantics.

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

- [ ] P8.1 Re-evaluate only after web/Mini App usage proves a concrete need.
- [ ] P8.2 If justified, create a small inspection/download client rather than a second orchestration system.

## Permanent Rules

- Never commit secrets, credentials, tokens, private keys, private canon, or private generated assets.
- Never rely on repository secrecy; this repository is intentionally public.
- Never introduce a paid dependency without explicit Creator approval.
- Keep production path simple; avoid broad test matrices and speculative guards.
- Read `skills/spatial-forge-3d/SKILL.md` for Blender/MPFB/3D creation or validation work.
- Do not claim a slice passed until its actual runtime output has been inspected.
- For Actions-backed slices, verify in this order when available: workflow run → jobs/steps → failed job logs → artifact list → downloaded artifact contents → fresh-import validation when relevant → visual output inspection.
- Issues are for durable project discussion/tracking, not a required mechanism for checking workflow state.
- Update docs after every completed slice before moving on.
