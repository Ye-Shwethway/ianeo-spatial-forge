# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → proven Spatial Forge backend → 3D assets / previews → web viewer → Telegram/Mini App**

MCP is intentionally deferred until the backend and delivery path are independently established. It will later act as a narrow external control adapter, not as an early implementation dependency.

## Current Architecture Decisions

- Repository is intentionally public; public repo contains engine code, workflows, schemas, skills, viewer code, and generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Blender runs headlessly in Actions.
- Proven baseline: Blender `4.5.12 LTS` + MPFB `2.0.17`.
- P2.4 proved exact unsupported real-world measurement intent is reported rather than fabricated as an MPFB control.
- `skills/spatial-forge-3d/SKILL.md` is the 3D creation/validation router.
- `skills/spatial-forge-ui/SKILL.md` is the UI/UX router for web, Telegram Mini App, and future Flutter work.
- Phone inspection is deliberately pulled forward as P2V before P2.5/P2.6.
- The viewer is framework-free/static, URL-driven, and uses pinned `@google/model-viewer` `4.3.1`.
- Preferred UI hostname is `forge.drthorne.uk`.
- Cloudflare Pages is the static host. The VPS later provides protected/private build assets and control APIs, not viewer rendering.
- Telegram will later open the same web viewer rather than requiring a second viewer implementation.
- Dedicated Flutter client remains deferred until a concrete need exists.
- MCP remains late-stage only.

## Proven Runtime State

### P0 — PASS
Run `32859113238`, Blender `4.5.12 LTS`.

### P1 — PASS
Run `32860562804`, Blender `4.5.12 LTS`, MPFB `2.0.17`; GLB contained 1 mesh definition, 1 skin, 53 joints.

### P2.1–P2.3 — PASS
Run `32864360900`; exact six normalized MPFB controls applied; clean fresh import succeeded with 2 mesh objects, 1 armature, 53 bones.

### P2.4 — PASS
Run `32864975879`; `chest_circumference = 110 cm` preserved in `unsupported_fields` with explicit reason and not added to engine controls; GLB remained valid.

### P2V.1 — PASS
Viewer files under `viewer/`; Viewer Smoke run `32866763601` passed serving/fetch verification of HTML/JS/CSS and pinned `model-viewer@4.3.1` wiring.

### P2V.5 — PASS
`viewer/README.md` defines the stateless URL contract:
- `model` — GLB URL
- `meta` — `build-result.json` URL
- `front` — front preview URL
- `threeQuarter` — three-quarter preview URL
- `title` — display label
The asset host must permit browser access/CORS. The viewer owns no database or storage.

## Cloudflare Pages Foundation — CREATED, DEPLOYMENT PENDING

Cloudflare Pages project:
- project: `ianeo-spatial-forge`
- project ID: `58dfc37e-10a4-459a-811f-565001cc473b`
- default Pages URL: `https://ianeo-spatial-forge.pages.dev`
- production branch: `main`
- framework: none
- root directory: `viewer`
- build command: empty
- output directory: `.`
- build caching: disabled

Custom domain:
- `forge.drthorne.uk`
- Pages custom-domain ID: `acfbe3f1-1e98-4954-b1a3-a7ddc4b4f86f`
- proxied CNAME points to `ianeo-spatial-forge.pages.dev`

No Worker, D1, KV, R2, Tunnel, database, or other service was created for this viewer foundation.

There is **no Pages deployment yet** because GitHub source binding is still pending. Therefore do not claim `forge.drthorne.uk` is live or HTTPS-verified yet. The temporary custom-domain pending state is expected until source/deployment exists and Cloudflare validation settles.

## Current Slice

### P2V.6 — First Static Deployment

Use the existing Cloudflare Pages project; do not create another project and do not add a GitHub Actions direct-deploy path unless source integration proves impossible.

Required source config:
- repository: `Ye-Shwethway/ianeo-spatial-forge`
- production branch: `main`
- root directory: `viewer`
- framework: none
- build command: empty
- output directory: `.`

Next target sequence:
1. attach the existing Pages project to the GitHub repository through Cloudflare/GitHub source integration
2. trigger/observe first production deployment
3. verify `https://ianeo-spatial-forge.pages.dev`
4. verify `https://forge.drthorne.uk` after custom-domain validation/TLS settles
5. then provide a real generic Spatial Forge GLB/metadata/previews through browser-accessible URLs
6. verify rotate/zoom/reset, preview rendering, metadata truthfulness, and Android use

Do not add Cloudflare API tokens/GitHub Actions secrets merely to duplicate native Pages Git integration unless native integration cannot be established.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Use `IMPLEMENTATION_PLAN.md` as canonical checkbox state.
- Keep changes small; avoid over-engineering.
- Do not claim runtime success without inspecting actual output.
- Sync docs after completed slices.
