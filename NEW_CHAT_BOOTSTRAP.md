# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → proven Spatial Forge backend → 3D assets / previews → web viewer → Telegram/Mini App**

MCP is intentionally deferred until the backend and delivery path are independently established.

## Current Architecture Decisions

- Public repo contains engine code, workflows, schemas, skills, viewer code, and generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Proven 3D baseline: Blender `4.5.12 LTS` + MPFB `2.0.17`.
- `skills/spatial-forge-3d/SKILL.md` is the 3D creation/validation router.
- `skills/spatial-forge-ui/SKILL.md` is the UI/UX router for web, Telegram Mini App, and future Flutter work.
- Phone inspection is deliberately pulled forward as P2V before P2.5/P2.6.
- The viewer is framework-free/static, URL-driven, and uses pinned `@google/model-viewer` `4.3.1`.
- Cloudflare native Git integration was abandoned after repeated failures. Do not retry it unless explicitly requested.
- Canonical viewer deployment is **GitHub Actions → Wrangler → Cloudflare Pages Direct Upload**.
- Cloudflare Pages project: `ianeo-spatial-forge`.
- Live URLs: `https://ianeo-spatial-forge.pages.dev/` and `https://forge.drthorne.uk/`.
- VPS later provides protected/private build assets and control APIs, not viewer rendering.
- Telegram will later open the same web viewer rather than requiring a second implementation.
- Flutter remains optional later; MCP remains late-stage only.

## Proven Runtime State

### P0 — PASS
Run `32859113238`, Blender `4.5.12 LTS`.

### P1 — PASS
Run `32860562804`, Blender `4.5.12 LTS`, MPFB `2.0.17`; GLB contained 1 mesh definition, 1 skin, 53 joints.

### P2.1–P2.3 — PASS
Run `32864360900`; exact six normalized MPFB controls applied; clean fresh import succeeded with 2 mesh objects, 1 armature, 53 bones.

### P2.4 — PASS
Run `32864975879`; exact `chest_circumference = 110 cm` preserved in `unsupported_fields` and not fabricated as an engine control.

### P2V.1 — PASS
Viewer Smoke run `32866763601` passed serving/fetch verification for the static shell and pinned viewer dependency.

### P2V.5 — PASS
`viewer/README.md` defines stateless URL inputs: `model`, `meta`, `front`, `threeQuarter`, `title`.

### P2V.6 — PASS
Workflow: `.github/workflows/deploy-pages.yml`

First successful deployment:
- commit `4901727e1b72a29ba5ec2692afdbf3da8cf85d39`
- run `32876020417`

Live-URL verification:
- commit `411036bcf9e57cd5faec4ee69fa32725ec2e7bce`
- run `32876094428`
- deploy PASS
- HTTPS/content PASS for both Pages and custom-domain URLs

No Worker, D1, KV, R2, Tunnel, database, or unrelated Cloudflare resource was added.

### Real Generic Viewer Demo — LIVE, ANDROID CONFIRMATION PENDING

Workflow: `.github/workflows/deploy-viewer-demo.yml`

The workflow intentionally reuses the already-proven P2.4 artifact instead of re-running Blender. It stages these generic public-safe assets under `viewer/demo/` at runtime and Direct Upload deploys them without committing the binaries:
- `generic-unsupported-v1.glb`
- `front.png`
- `three-quarter.png`
- `build-result.json`

Successful proof:
- commit `f3ebe566d26fa1bdaff2ba6287261a4f0d2778e0`
- run `32876486511`
- artifact download PASS
- staged metadata assertions PASS
- Wrangler Pages deployment PASS
- live `build-result.json` PASS
- live GLB download PASS and >8 MB
- live preview PNG PASS
- live viewer URL PASS

First real demo URL:
`https://forge.drthorne.uk/?model=/demo/generic-unsupported-v1.glb&meta=/demo/build-result.json&front=/demo/front.png&threeQuarter=/demo/three-quarter.png&title=Generic%20Character%20P2.4`

## Current Slice

### P2V.2 / P2V.3 / P2V.4 / P2V.7 — Android Viewer Confirmation

The real generic assets are live and browser-accessible. The Creator should open the demo URL on Android and confirm:
1. the real GLB visibly renders
2. drag rotates the model
3. pinch zoom works
4. Reset view works
5. front and three-quarter previews are visible
6. build metadata renders, including Blender `4.5.12 LTS`, MPFB `2.0.17`, six applied controls, structural counts, and the unsupported `chest_circumference = 110 cm` request/reason

Do not mark P2V.2/P2V.3/P2V.4/P2V.7 complete until the actual phone behavior is confirmed. HTTP/file verification alone is not a visual/touch proof.

After Android confirmation, sync docs and return to P2.5 version/lock semantics and P2.6 two-revision proof, then proceed toward protected VPS asset delivery and Telegram.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Use `IMPLEMENTATION_PLAN.md` as canonical checkbox state.
- Keep changes small; avoid over-engineering.
- Do not claim runtime success without inspecting actual output.
- Sync docs after completed slices.
