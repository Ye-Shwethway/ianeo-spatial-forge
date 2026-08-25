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

**P0 runtime proof:** Blender `4.5.12 LTS`; successful workflow run `32859113238` on commit `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`.

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
- [x] P2.5 Add version identifier and scoped revision/lock semantics.
- [x] P2.6 Build two versions of a generic test character and verify scoped changes.

**P2.1–P2.4 proof:** runs `32864360900` and `32864975879` proved six normalized MPFB controls, fresh-import validity, and explicit unsupported exact-measurement reporting.

**P2.5/P2.6 runtime proof:** Character Revision Proof run `32877860898` on commit `137dafa67823894a1dfc95d3aa96370996d3739b` completed successfully. Only `muscle` changed from `0.72` to `0.52`; five declared phenotype locks remained exact. v2 fresh import succeeded with 2 mesh objects, 1 armature, and 53 joints. Preview pairs were inspected; no stronger appearance claim is made beyond the proven scoped engine change.

## P2V — Phone Viewer Foundation (pulled forward)

- [x] P2V.1 Add a framework-free mobile viewer shell under `viewer/`.
- [x] P2V.2 Load a GLB from an explicit URL and support rotate/zoom/reset on phone.
- [x] P2V.3 Display optional front and three-quarter preview URLs.
- [x] P2V.4 Load and render `build-result.json` metadata including unsupported fields truthfully.
- [x] P2V.5 Define the minimal build asset URL contract without adding a database or account system.
- [x] P2V.6 Establish a static deployment path suitable for `forge.drthorne.uk`.
- [x] P2V.7 Verify the viewer from an Android browser with a real generic Spatial Forge GLB.

**P2V runtime proof:** Viewer Smoke run `32866763601`, Direct Upload runs `32876020417` / `32876094428`, and generic demo run `32876486511` proved the mobile viewer and live delivery. The Creator confirmed real Android rendering, touch interaction, previews, and truthful metadata.

**Privacy boundary:** `/demo/` is generic public-safe only. Canonical/private character manifests, GLBs, previews, references, and metadata must never be deployed as static public Pages assets.

## P3 — VPS Control Plane

- [x] P3.1 Define minimal authenticated HTTP/job interface.
- [x] P3.2 Bootstrap service directories and least-privilege service account on VPS.
- [ ] P3.3 Add temporary job storage with expiry/cleanup.
- [ ] P3.4 Add build status and protected asset retrieval.
- [x] P3.5 Establish GitHub Actions deployment as the normal update path.
- [ ] P3.6 Remove Bamboo from the normal operational workflow.

**P3.1 contract:** `docs/PRIVATE_ASSET_CONTROL_PLANE.md` defines the public viewer/private VPS split. `control-plane/server.py` implements the first stdlib-only service: public `/health`, bearer-authenticated private build status + viewer-session creation, and temporary read-only `/s/{session_id}/{asset}` delivery limited to GLB, build-result JSON, front PNG, and three-quarter PNG. Session IDs are high entropy; control credentials never enter viewer URLs.

**P3 pre-VPS proof:** Control Plane Smoke run `32880493854` passed syntax, health, bearer authorization, temporary session creation, and protected asset retrieval in an isolated runner root. After the first VPS bootstrap attempt revealed a non-interactive PATH issue before any mutation, `deploy/bootstrap-vps.sh` was corrected to set `PATH=/usr/sbin:/sbin:/usr/bin:/bin`; verification run `32881012007` on commit `0292d8e286838e4823b681009cac04252cd4e57c` passed again.

**P3.2 VPS bootstrap proof:** Bamboo performed a read-only survey first, then fetched and reviewed the exact pinned bootstrap before execution. The successful bootstrap created dedicated runtime user `spatialforge`; `/srv/ianeo-spatial-forge/{app,private/builds,private/sessions,state}` with separated ownership/modes; locally generated non-printed `SF_CONTROL_TOKEN` in `state/control.env` mode `0600`; a localhost-only systemd unit for `127.0.0.1:18792`; and a sudoers drop-in giving existing `eidolon-deploy` only `restart`, `status`, and `is-active` for `ianeo-spatial-forge.service`. No packages, firewall rules, DNS, tunnels, cloudflared changes, or unrelated `/srv/eidolon` changes were made.

**P3.5 runtime proof:** Deploy Control Plane to VPS run `32884206891` succeeded end-to-end after replacing fragile multiline private-key pasting with a single-line Base64 repository secret. The workflow validated the decoded key with `ssh-keygen -y`, verified pinned-host-key SSH as `eidolon-deploy`, deployed `control-plane/server.py` into `/srv/ianeo-spatial-forge/app/control-plane/server.py`, restarted `ianeo-spatial-forge.service` through the narrow sudo rule, and verified `http://127.0.0.1:18792/health` from the VPS. The workflow was then restored to manual-only dispatch. Routine code deployment no longer requires Bamboo/Termux.

**P3.6 remaining bootstrap-only item:** the service is active but was intentionally not enabled during the initial bootstrap. Close P3.6 after one final one-time enable-on-boot verification; after that Bamboo/Termux remain emergency-only.

**Current P3 order:** perform the one-time enable-on-boot check, then prove P3.3/P3.4 on the real VPS through GitHub Actions. Bamboo/Termux are no longer part of normal deployment.

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
