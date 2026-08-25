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
- [x] P3.4 Complete protected asset retrieval through a real HTTPS private asset origin.
- [x] P3.5 Establish GitHub Actions deployment as the normal update path.
- [x] P3.6 Remove Bamboo/Termux from normal operational workflow.
- [x] P3.7 Add phone-first web Asset Library with same-origin authenticated API proxy.

### P3 runtime state

- VPS service is active/enabled and binds only `127.0.0.1:18792`.
- `assets.drthorne.uk` routes through the existing remotely-managed Cloudflare Tunnel to `http://127.0.0.1:18792`; port `18792` remains non-public.
- Cloudflare Access protects `forge.drthorne.uk`, Pages fallback/preview hostnames, and `assets.drthorne.uk` with Email OTP, exact-owner-email Allow, deny-by-default behavior, and 30-day session.
- `SF_ASSET_ORIGIN=https://assets.drthorne.uk` is active in the live service.
- A real generic Blender/MPFB build was staged and promoted into VPS private storage and retrieved on Android through the protected viewer with model + previews visible.
- Web control now uses a same-origin Pages Function proxy: browser calls `forge.drthorne.uk/api/*`; the function forwards the authenticated Access assertion server-side to `assets.drthorne.uk`. Browser cross-origin Access login/cookie bouncing is not part of the canonical flow.
- Android runtime verified `forge.drthorne.uk/api/v1/builds` returning the private build JSON and the Asset Library rendering the `p3-private-proof` build card.
- Bamboo/Termux/root access are bootstrap/emergency-only.

### Web Access security runtime proof

Android runtime verified:
- unauthenticated `forge.drthorne.uk` reaches the Cloudflare Access login page
- OTP verification reaches Spatial Forge
- explicit `/cdn-cgi/access/logout` logs out and requires login again
- Eager redirect cookie is disabled
- direct anonymous `assets.drthorne.uk` access remains Access-blocked
- same-origin `/api` proxy works with authenticated Access context.

## P3Q — Character Quality & Visual Fidelity

**Goal:** move from a structurally valid generic MPFB human to a visually convincing, detailed, attractive character while preserving deterministic builds, mobile-friendly GLB output, and honest support boundaries.

This is the next active phase. Do not jump to Telegram or MCP until the quality ladder is proven on at least one generic character.

- [ ] P3Q.1 Establish a clean visual baseline.
  - Build one generic body/face fixture specifically for quality work.
  - Remove accidental/placeholder-looking assets from the baseline.
  - Use fixed front, three-quarter, profile, and full-body evidence views.
  - Record current visible defects instead of redesigning everything at once.

- [ ] P3Q.2 Improve base mesh presentation and surface quality.
  - smooth shading / normals / seam sanity
  - verify body topology survives rig + GLB export
  - choose the smallest subdivision/surface treatment that materially improves appearance without making phone GLBs unnecessarily heavy
  - compare authored Blender output against fresh-imported GLB.

- [ ] P3Q.3 Expand face-shape control.
  - identify real MPFB-supported head/face controls before adding schema fields
  - add a small useful set for head shape, jaw/chin, nose, eyes, brows, mouth/lips where genuinely supported
  - create a fixed face close-up evidence sheet
  - prove one scoped face revision without body drift.

- [ ] P3Q.4 Add production-quality PBR appearance.
  - skin material that survives GLB/glTF export
  - distinct eye materials with believable cornea/iris/sclera appearance where supported
  - mouth/teeth/tongue materials only if present and export-safe
  - no Blender-only shader tricks that disappear in the phone viewer
  - inspect in the real `forge.drthorne.uk` viewer, not Blender alone.

- [ ] P3Q.5 Add hair / brows / facial-hair asset path.
  - start with one permissively usable generic hairstyle
  - prove fit, scalp coverage, material, rig/head attachment, and GLB export
  - add eyebrows/facial hair only through the same asset discipline
  - avoid heavy hair simulation in this phase.

- [ ] P3Q.6 Add clean clothing asset path.
  - prove one fitted top + bottom or one simple outfit
  - verify skinning/deformation with the game-engine rig
  - eliminate obvious clipping in neutral and one representative pose
  - keep clothing as replaceable assets rather than hard-wiring one costume into the character generator.

- [ ] P3Q.7 Improve deformation and pose quality.
  - verify shoulder, elbow, hip, knee, neck, and wrist deformation on representative poses
  - correct only demonstrated weight/deformation problems
  - preserve the proven rig/export contract.

- [ ] P3Q.8 Add presentation-grade viewer/render defaults.
  - neutral flattering lighting/environment
  - sensible exposure/background/camera framing
  - face close-up + full-body inspection modes
  - presentation changes must not hide geometry/material defects.

- [ ] P3Q.9 Final generic quality proof.
  - build one complete generic quality character from deterministic source
  - inspect Blender output, GLB structure, fresh import, fixed renders, and Android viewer
  - record asset/material/tool versions
  - compare against the P3Q.1 baseline and close only after visible improvement is confirmed.

### P3Q quality rule

Visual quality is a separate gate from structural validity. Mesh counts, joints, successful exports, and green Actions runs do not prove that a character looks good. Every visual-quality slice requires fixed comparable evidence and actual inspection.

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
