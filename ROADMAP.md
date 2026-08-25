# IANEO Spatial Forge Roadmap

## Mission

Build a zero-incremental-cost, phone-first 3D creation system that IANEO can operate through tools instead of requiring the Creator to learn or manually drive desktop 3D software.

## Target Interaction

During development and verification:

**Creator → IANEO → built-in repository/connectors + proven automation → Spatial Forge → preview / GLB / scene assets**

Phone inspection is intentionally pulled forward before the full control plane:

**GitHub Actions artifact → lightweight web viewer → Creator's phone**

After the underlying backend, control plane, and phone delivery are independently established:

**External IANEO session → MCP → proven Spatial Forge backend → Telegram / web viewer / Mini App**

Telegram is the notification and delivery surface. The first interactive 3D inspection surface is a lightweight mobile web viewer that can later run inside a Telegram Mini App without being rewritten. A dedicated Flutter client is optional later, only if the web/Mini App path proves insufficient.

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
- feature-lock semantics can express changes such as `face-only` without silently modifying approved body settings
- two generic revisions prove intended change plus lock preservation

## Phase P2V — Phone Viewer Foundation

Goal: give the Creator an immediate phone-first inspection surface before finishing revision semantics or the full VPS control plane.

Architecture:

**mobile browser → static Spatial Forge Viewer → GLB + preview + build-result metadata**

Initial deployment target:
- static viewer files are versioned in this repository
- preferred public UI hostname is `forge.drthorne.uk`
- Cloudflare Pages is the preferred static hosting target once connected
- the viewer must not require the VPS merely to render a GLB
- the VPS will later provide protected/private build assets and metadata through the P3 control plane

Success:
- mobile-first static viewer shell exists
- viewer can load a GLB URL and rotate/zoom/reset it
- front and three-quarter evidence can be displayed when URLs are supplied
- build-result metadata can be displayed without fabricating unsupported precision
- no database, account system, or large frontend framework is required
- architecture is compatible with later Telegram Mini App embedding

## Phase P3 — VPS Control Plane

Goal: use the existing VPS as a lightweight coordinator and temporary private file store, not as a render farm.

Success:
- authenticated job submission
- temporary job directories
- build/result status
- signed or otherwise protected asset retrieval
- cleanup/expiry policy
- the viewer can consume protected build URLs without becoming tightly coupled to the VPS implementation

Bamboo may be used once to bootstrap the VPS foundation. It is not a runtime dependency and should disappear from the normal workflow after automated deployment is established.

## Phase P4 — Telegram Delivery + Mini App

Goal: connect the already-proven web viewer to the phone delivery loop before adding MCP.

Success:
- Telegram bot sends build completion/status and preview
- `Open 3D` opens the existing viewer as a Telegram Mini App/web view
- viewer supports rotate/zoom/reset plus metadata/download actions
- private assets are not exposed as permanent public URLs
- Android phone end-to-end delivery/inspection works without MCP

## Phase P5 — MCP External Control

Goal: expose already-proven Spatial Forge backend operations to an external IANEO session through a narrow MCP adapter without making MCP a core backend dependency.

Entry gate:
- P2 manifest/revision semantics proven
- P3 control plane proven
- P4 phone delivery proven independently of MCP
- development/verification does not need to sacrifice built-in connector access

Initial tool family may include:
- `create_character`
- `get_character`
- `build_character`
- `get_build`
- `list_assets`
- `request_revision`

Start with read/status operations, then add narrow build/create operations. Do not create a large tool surface before the underlying operations are proven. MCP must not determine core schemas, file formats, generation scripts, or validation semantics.

## Phase P6 — Revision and Canon Workflow

Goal: turn one-off generation into a controlled iterative character workflow.

Success:
- versioned character builds
- approved parameter locks
- scoped revisions
- reusable poses
- canonical vs temporary asset distinction

## Phase P7 — Spatial Scene Forge

Goal: expand from characters to reproducible spatial scenes.

Potential capabilities:
- place characters and props
- preserve relative heights and positions
- camera/lens control
- lighting presets
- pose libraries
- composition reference renders for downstream image generation

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
- building a heavy SPA or account/database system just to inspect a GLB

## 3D Creation Intelligence Rule

For Blender, MPFB, character, scene, rigging, GLB, rendering, or 3D validation work, read `skills/spatial-forge-3d/SKILL.md` and its routed references. External Blender-agent skills are methodology sources only; the project keeps its own proven runtime and minimal workflow.

## Documentation Rule

After every completed slice, update `IMPLEMENTATION_PLAN.md`, this roadmap when scope/status changes, and `NEW_CHAT_BOOTSTRAP.md` with the exact current handoff state.
