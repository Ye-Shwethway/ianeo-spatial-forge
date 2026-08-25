# IANEO Spatial Forge Roadmap

## Mission

Build a zero-incremental-cost, phone-first 3D creation system that IANEO can operate through tools instead of requiring the Creator to learn or manually drive desktop 3D software.

## Target Interaction

During development and verification:

**Creator → IANEO → built-in repository/connectors + proven automation → Spatial Forge → preview / GLB / scene assets**

Phone inspection is intentionally pulled forward before the full control plane:

**GitHub Actions artifact → lightweight web viewer → Creator's phone**

The current web path is now:

**Creator → Cloudflare Access → `forge.drthorne.uk` → same-origin `/api` proxy → protected VPS assets/control**

After character quality, backend, control plane, and phone delivery are independently established:

**External IANEO session → MCP → proven Spatial Forge backend → Telegram / web viewer / Mini App**

Telegram remains a later notification/delivery surface. The web viewer is the primary current inspection/control surface. A dedicated Flutter client remains optional later.

## Phase P0 — Headless Blender Proof

Goal: prove GitHub Actions can run Blender headlessly and return useful artifacts at zero incremental cost.

Success:
- Blender launches on `ubuntu-latest`.
- A deterministic smoke scene is created by Python.
- A `.blend`, `.glb`, and lightweight preview image are uploaded as workflow artifacts.
- No secrets or VPS access are required.

## Phase P1 — Human Generation Proof

Goal: add MPFB or the simplest maintainable open-source human-generation path.

Success:
- A generic human is generated programmatically.
- Basic phenotype/body parameters are script-controlled.
- A rig can be attached where supported.
- `.glb` export and preview rendering succeed.

## Phase P2 — Character Manifest

Goal: establish a small canonical input format without building a huge character system, guided by the local `spatial-forge-3d` creation/validation skill.

Success:
- agent workflow intelligence is documented for reproducible creation, truthful precision, validation, and scoped revisions
- JSON manifest identifies a character and version
- supported body/face parameters map predictably to real generation controls
- unsupported or approximate precision is reported explicitly
- build metadata records engine/tool versions and outputs
- feature-lock semantics can express scoped revisions
- two generic revisions prove intended change plus lock preservation.

## Phase P2V — Phone Viewer Foundation

Goal: give the Creator an immediate phone-first inspection surface.

Architecture:

**mobile browser → Spatial Forge Viewer → protected GLB + previews + build-result metadata**

Success:
- mobile-first viewer shell exists
- viewer can load a GLB and rotate/zoom/reset it
- front and three-quarter evidence can be displayed
- build-result metadata can be displayed without fabricating unsupported precision
- no heavy frontend framework is required
- architecture remains compatible with later Telegram Mini App embedding.

## Phase P3 — VPS Control Plane

Goal: use the existing VPS as a lightweight coordinator and private file store, not as a render farm.

Success:
- authenticated control surface
- temporary session URLs with expiry/cleanup
- protected HTTPS asset retrieval through Cloudflare Tunnel
- localhost-only VPS app
- GitHub Actions as normal deployment path
- Bamboo/Termux removed from normal operation
- Cloudflare Access protects viewer and asset hostnames
- same-origin Pages Function proxy lets the authenticated web app list/manage protected builds without cross-origin browser-auth redirects
- Android runtime proves protected private build retrieval and web Asset Library listing.

## Phase P3Q — Character Quality & Visual Fidelity

Goal: turn the structurally valid generic MPFB human into a visually convincing, detailed, attractive character while preserving reproducibility, truthful controls, rig/export safety, and phone-friendly GLB delivery.

This is the next active phase before Telegram or MCP.

Quality ladder:
1. establish a clean baseline and fixed visual evidence views
2. improve mesh presentation, smoothing/normals and mobile-appropriate surface quality
3. expand only genuinely supported face controls and prove scoped face revision
4. add GLB-safe PBR skin/eye/mouth materials
5. add a disciplined hair/brow/facial-hair asset path
6. add a clean replaceable clothing asset path with skinning/clipping checks
7. improve demonstrated rig deformation problems only
8. improve neutral viewer/render lighting, framing and inspection modes
9. produce one deterministic complete generic quality character and compare it against the baseline on Android.

Success is visual as well as structural. A green workflow, mesh count, or valid rig does not prove beauty or believable appearance; fixed comparable previews and actual inspection are required.

Early P3Q is intentionally not:
- high-end sculpting from scratch
- a render farm
- heavy cloth/hair simulation
- huge texture libraries
- paid AI 3D services
- premature LOD/asset-management frameworks.

## Phase P4 — Telegram Delivery + Mini App

Goal: connect the already-proven web viewer to the phone delivery loop before adding MCP.

Success:
- Telegram bot sends build completion/status and preview
- `Open 3D` opens the existing viewer as a Telegram Mini App/web view
- viewer supports rotate/zoom/reset plus metadata/download actions
- private assets are not exposed as permanent public URLs
- Android phone end-to-end delivery/inspection works without MCP.

## Phase P5 — MCP External Control

Goal: expose already-proven Spatial Forge backend operations to an external IANEO session through a narrow MCP adapter without making MCP a core backend dependency.

Entry gate:
- P2 manifest/revision semantics proven
- P3 control plane proven
- P3Q generic character quality path proven
- P4 phone delivery proven independently of MCP.

Start with read/status operations, then add narrow build/create operations. MCP must not determine core schemas, file formats, generation scripts, or validation semantics.

## Phase P6 — Revision and Canon Workflow

Goal: turn one-off generation into a controlled iterative character workflow.

Success:
- versioned character builds
- approved parameter locks
- scoped revisions
- reusable poses
- canonical vs temporary asset distinction.

## Phase P7 — Spatial Scene Forge

Goal: expand from characters to reproducible spatial scenes.

Potential capabilities:
- place characters and props
- preserve relative heights and positions
- camera/lens control
- lighting presets
- pose libraries
- composition reference renders for downstream image generation.

## Phase P8 — Optional Dedicated Flutter Client

Build only if the Telegram/web viewer path is no longer sufficient. Possible future functions include offline cache, richer asset browsing, side-by-side version comparison, scene inspection, and Simiverse integration.

## Non-Goals for Early Phases

- MCP-driven Blender control during early implementation
- photorealistic render-farm workloads
- high-end sculpting from scratch
- complex cloth/hair simulation
- large test matrices
- premature distributed architecture
- paid AI 3D APIs
- storing private character canon in this public repository
- building a heavy SPA or account/database system just to inspect a GLB.

## 3D Creation Intelligence Rule

For Blender, MPFB, character, scene, rigging, GLB, rendering, or 3D validation work, read `skills/spatial-forge-3d/SKILL.md` and its routed references. External Blender-agent skills are methodology sources only; the project keeps its own proven runtime and minimal workflow.

## Documentation Rule

After every completed slice, update `IMPLEMENTATION_PLAN.md`, this roadmap when scope/status changes, and `NEW_CHAT_BOOTSTRAP.md` with the exact current handoff state.
