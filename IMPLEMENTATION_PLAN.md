# IANEO Spatial Forge Implementation Plan

Work one slice at a time. A slice is complete only when its runtime result has been inspected and the handoff docs are updated.

## Foundation

- [x] F0.1 Create public repository.
- [x] F0.2 Add README and architecture/security principles.
- [x] F0.3 Add roadmap.
- [x] F0.4 Add implementation plan, AGENTS.md, bootstrap handoff, and `.gitignore`.
- [x] F0.5 Verify repository foundation from `main`.

## P0 — Headless Blender Proof

- [x] P0.1–P0.9 Headless Blender build/export/preview/artifact proof.

**Proof:** Blender `4.5.12 LTS`; run `32859113238`; commit `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`.

## P1 — Human Generation Proof

- [x] P1.1–P1.8 MPFB human generation, rig, GLB and preview proof.

**Proof:** Blender `4.5.12 LTS`, MPFB `2.0.17`; run `32860562804`; GLB contained 1 mesh definition, 1 skin, 53 joints.

## P2 — Minimal Character Manifest

- [x] P2.0 Spatial Forge 3D skill.
- [x] P2.1 Character build schema.
- [x] P2.2 Build-result schema.
- [x] P2.3 Proven manifest-to-engine controls.
- [x] P2.4 Explicit unsupported-field reporting.
- [x] P2.5 Version/lock semantics.
- [x] P2.6 Scoped revision proof.

**Proof:** runs `32864360900`, `32864975879`, and revision run `32877860898`. Six MPFB controls are proven. Unsupported exact measurements are reported rather than fabricated. v1→v2 changed only `muscle` `0.72→0.52`; five declared locks stayed exact; fresh import remained valid with 2 mesh objects, 1 armature, 53 joints.

## P2V — Phone Viewer Foundation

- [x] P2V.1–P2V.7 Framework-free mobile viewer, URL contract, Pages deployment, Android verification.

**Proof:** Viewer Smoke `32866763601`; Direct Upload `32876020417` / `32876094428`; demo `32876486511`; Android rendering/touch/previews/metadata confirmed.

**Privacy boundary:** `/demo/` is generic public-safe only. Canonical/private manifests, GLBs, previews, references, and metadata must never be deployed as public Pages files.

## P3 — VPS Control Plane

- [x] P3.1 Define minimal authenticated HTTP/job interface.
- [x] P3.2 Bootstrap service directories and least-privilege service account on VPS.
- [x] P3.3 Add temporary session storage with expiry/cleanup.
- [ ] P3.4 Complete protected asset retrieval through a real HTTPS private asset origin.
- [x] P3.5 Establish GitHub Actions deployment as the normal update path.
- [x] P3.6 Remove Bamboo/Termux from normal operational workflow.

### P3.1 contract

`docs/PRIVATE_ASSET_CONTROL_PLANE.md` and `control-plane/server.py` define:
- public `/health`
- bearer-authenticated build status and viewer-session creation
- read-only temporary `/s/{session_id}/{asset}` capability access
- allowed assets only: `model.glb`, `build-result.json`, `front.png`, `three-quarter.png`
- high-entropy server-side sessions
- default 2h TTL, max 24h
- private/no-store delivery and viewer-origin CORS
- no account/database/JWT platform
- control token never enters viewer URLs.

### P3.2 VPS bootstrap proof

Dedicated runtime user `spatialforge` and `/srv/ianeo-spatial-forge/{app,private/builds,private/sessions,state}` are installed with separated ownership/modes. `SF_CONTROL_TOKEN` is locally generated, non-printed, and stored `0600`. Service binds only `127.0.0.1:18792`. `eidolon-deploy` sudo is restricted to restart/status/is-active for this service. No packages, firewall, DNS, tunnel, cloudflared, or unrelated `/srv/eidolon` changes were made.

Final root verification confirmed:
- service active/running
- enabled at boot
- listening only `127.0.0.1:18792`
- public IPv4 connection to port `18792` refused
- `/health` returns 200
- no journal errors.

### P3.3 runtime proof

`control-plane/server.py` now performs expired-session cleanup at startup and request boundaries. Corrupt/expired session records are removed. Expired capability URLs return 404. `SF_ASSET_ORIGIN` support was added so the public Pages viewer can receive absolute private asset URLs once HTTPS ingress exists.

Control Plane Smoke runs `32885401030` and `32885482676` passed:
- proactive expired-session removal
- bearer auth boundary
- session creation
- absolute asset-origin viewer URL contract
- protected GLB GET
- actual GET response headers (`Access-Control-Allow-Origin`, `Cache-Control`, `Referrer-Policy`, `X-Content-Type-Options`)
- expired capability 404 + session-file removal.

### P3.5 / P3.6 runtime proof

Initial VPS deploy run `32884206891` passed SSH key validation, pinned host-key SSH, code deployment, service restart, and localhost health verification.

Normal deployment is now smoke-gated:
`control-plane change → Control Plane Smoke PASS → Deploy Control Plane to VPS workflow_run → SSH deploy → restart → localhost /health`.

Fresh chain proof:
- smoke run `32885482676` PASS
- automatically spawned deploy run `32885510216` PASS
- deploy steps all passed: checkout, decoded-key validation, SSH transport, code deploy, restart, localhost health.

Bamboo/Termux are now bootstrap/emergency-only, not normal deployment dependencies.

### Current P3 target

P3.4 remains open because the service intentionally has no public ingress yet. Next establish one protected HTTPS asset origin (without exposing port `18792` directly), set `SF_ASSET_ORIGIN`, then prove the live `forge.drthorne.uk` viewer can retrieve a temporary protected asset with correct CORS/expiry behavior.

## P4 — Telegram Delivery + Mini App

- [ ] P4.1 Create Telegram bot delivery path using secrets outside the repository.
- [ ] P4.2 Send build status and lightweight preview.
- [ ] P4.3 Open the existing web viewer from Telegram as a Mini App/web view.
- [ ] P4.4 Add protected download action when P3 asset delivery exists.
- [ ] P4.5 Verify end-to-end from Android phone.

## P5 — MCP Control

- [ ] P5.1 Introduce MCP only after build, manifest semantics, control plane, and phone delivery are independently proven.
- [ ] P5.2 Implement a minimal MCP server over proven backend operations.
- [ ] P5.3 Expose read/status tools first.
- [ ] P5.4 Add narrow build/create actions.
- [ ] P5.5 Add revision only after version/lock semantics pass.
- [ ] P5.6 Verify external IANEO → MCP → Spatial Forge → Telegram/web viewer.

## P6 — Character Canon and Revisions

- [ ] P6.1 Separate temporary builds from approved canonical assets.
- [ ] P6.2 Persist approved manifests privately.
- [ ] P6.3 Add reusable pose assets.
- [ ] P6.4 Add side-by-side version comparison.
- [ ] P6.5 Prove scoped revisions without unrelated drift.

## P7 — Spatial Scene Forge

- [ ] P7.1 Scene manifest.
- [ ] P7.2 Multi-character placement and scale consistency.
- [ ] P7.3 Camera/lens controls.
- [ ] P7.4 Lighting presets.
- [ ] P7.5 Spatial reference renders.

## P8 — Optional Flutter Client

- [ ] P8.1 Re-evaluate after web/Mini App usage proves a need.
- [ ] P8.2 If justified, create a small inspection/download client rather than another orchestration system.

## Permanent Rules

- Never commit secrets, credentials, tokens, private keys, private canon, or private generated assets.
- Never introduce a paid dependency without explicit Creator approval.
- Keep production path simple; avoid broad test matrices and speculative guards.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Do not claim a slice passed until actual runtime output has been inspected.
- Update docs after every completed slice before moving on.
