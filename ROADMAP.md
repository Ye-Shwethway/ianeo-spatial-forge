# IANEO Spatial Forge Roadmap

## Mission

Build a zero-incremental-cost, phone-first 3D creation system that IANEO can operate through tools instead of requiring the Creator to learn or manually drive desktop 3D software.

## Target Interaction

**Creator → IANEO → MCP → Spatial Forge → preview / GLB / scene assets**

Telegram is the notification and delivery surface. A Telegram Mini App is the first interactive 3D inspection surface. A dedicated Flutter client is optional later, only if the Mini App proves insufficient.

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

Goal: establish a small canonical input format without building a huge character system.

Success:
- JSON manifest identifies a character and version.
- Supported body/face parameters map predictably to generation controls.
- Build metadata records engine/tool versions and outputs.
- Feature-lock semantics can express changes such as `face-only` without silently modifying approved body settings.

## Phase P3 — VPS Control Plane

Goal: use the existing VPS as a lightweight coordinator and temporary private file store, not as a render farm.

Success:
- authenticated job submission
- temporary job directories
- build/result status
- signed or otherwise protected asset retrieval
- cleanup/expiry policy

Bamboo may be used once to bootstrap the VPS foundation. It is not a runtime dependency and should disappear from the normal workflow after automated deployment is established.

## Phase P4 — Telegram Delivery + Mini App Viewer

Goal: make the full loop usable from a phone.

Success:
- Telegram bot sends build completion/status and preview.
- `Open 3D` opens a Mini App viewer.
- Viewer loads GLB, supports rotate/zoom, and exposes metadata/download actions.
- Private assets are not exposed as permanent public URLs.

## Phase P5 — MCP Control

Goal: let IANEO operate the system through narrow, explicit tools.

Initial tool family may include:
- `create_character`
- `get_character`
- `build_character`
- `get_build`
- `list_assets`
- `request_revision`

Do not create a large tool surface before the underlying pipeline is proven.

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

Build only if the Telegram Mini App is no longer sufficient. Possible future functions include offline cache, richer asset browsing, side-by-side version comparison, scene inspection, and Simiverse integration.

## Non-Goals for Early Phases

- photorealistic render-farm workloads
- high-end sculpting from scratch
- complex cloth/hair simulation
- large test matrices
- premature distributed architecture
- paid AI 3D APIs
- storing private character canon in this public repository

## Documentation Rule

After every completed slice, update `IMPLEMENTATION_PLAN.md`, this roadmap when scope/status changes, and `NEW_CHAT_BOOTSTRAP.md` with the exact current handoff state.
