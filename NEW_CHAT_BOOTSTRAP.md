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
- The viewer is framework-free/static, URL-driven, and uses pinned `@google/model-viewer` `4.3.1`.
- Cloudflare native Git integration was abandoned after repeated failures. Do not retry it unless explicitly requested.
- Canonical viewer deployment is **GitHub Actions → Wrangler → Cloudflare Pages Direct Upload**.
- Cloudflare Pages project: `ianeo-spatial-forge`.
- Live URLs: `https://ianeo-spatial-forge.pages.dev/` and `https://forge.drthorne.uk/`.
- VPS provides protected/private build assets and control APIs, not Blender rendering and not viewer rendering.
- Canonical/private GLBs, previews, manifests, references, and metadata must never be deployed as plain public Pages files.
- Telegram later opens the same viewer; Flutter remains optional later; MCP remains late-stage only.
- VPS bootstrap/manual access is one-time only. Termux or Bamboo may establish the connection, directories, service user, and secrets or perform emergency repair. After the deployment connection exists, normal VPS updates must come from GitHub Actions.

## Proven Runtime State

### P0 — PASS
Run `32859113238`, Blender `4.5.12 LTS`.

### P1 — PASS
Run `32860562804`, Blender `4.5.12 LTS`, MPFB `2.0.17`; GLB contained 1 mesh definition, 1 skin, 53 joints.

### P2.1–P2.4 — PASS
Runs `32864360900` and `32864975879`; six proven MPFB controls are truthful and exact unsupported real-world measurement intent is reported rather than fabricated.

### P2.5 / P2.6 — PASS
Character Revision Proof run `32877860898`, commit `137dafa67823894a1dfc95d3aa96370996d3739b`.

The workflow built generic-character v1 and v2. Only `muscle` changed from `0.72` to `0.52`; declared locks for gender, age, weight, height, and proportions remained exact. v2 fresh import succeeded with 2 mesh objects, 1 armature, and 53 joints. The uploaded revision artifact was downloaded and both front/three-quarter preview pairs were visually inspected with no obvious corruption. The appearance delta is subtle under the neutral material, so no stronger visual claim is made.

### P2V — PASS
Viewer hosting, Direct Upload deployment, real GLB/preview/metadata delivery, and Android touch/visual inspection are proven. The `/demo/` assets are generic public-safe only.

## P3 Private Asset Contract — PASS

`docs/PRIVATE_ASSET_CONTROL_PLANE.md` defines the initial private delivery boundary:
- public Cloudflare Pages viewer shell
- private VPS build storage outside any public web root
- unauthenticated `GET /health`
- bearer-authenticated private build status
- bearer-authenticated creation of temporary viewer sessions
- temporary read-only `/s/{session_id}/{asset}` delivery limited to model GLB, build-result JSON, front PNG, and three-quarter PNG
- high-entropy server-side session IDs
- default 2-hour TTL, 24-hour hard maximum
- `Cache-Control: private, no-store`, `Referrer-Policy: no-referrer`, and `X-Content-Type-Options: nosniff`
- viewer-asset CORS limited to `https://forge.drthorne.uk`
- no database/account system/JWT platform required
- long-lived control token never appears in viewer URLs

## Current Slice

### P3.2 — VPS Bootstrap

Before modifying the VPS, perform one read-only environment survey so the bootstrap does not collide with existing services.

Need to establish only:
- OS/version/architecture
- whether systemd is available
- Python 3 and Node versions if installed
- existing reverse proxy/web server (nginx, Caddy, Apache, other)
- whether cloudflared is installed/running
- listening ports relevant to HTTP/HTTPS and the proposed local app port
- current SSH service/port and whether a dedicated deploy/service-user path is practical
- existing `/srv` conventions/directories that must not be disturbed

Do not print passwords, private keys, API tokens, tunnel credentials, environment secrets, or unrelated application configuration.

After the survey, IANEO will prepare one minimal bootstrap action. Manual/Termux/Bamboo use ends once GitHub Actions can deploy and verify the VPS service.

## VPS Manual/Automation Boundary

1. Manual/Bamboo/Termux is bootstrap or emergency-only.
2. Never ask the Creator to paste secret values into chat.
3. If secret setup is required, provide a one-shot command or exact GitHub UI secret step.
4. Once GitHub Actions can reach the VPS, use Actions for routine deployment/update/verification.
5. Bamboo must not become a permanent runtime dependency.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Use `IMPLEMENTATION_PLAN.md` as canonical checkbox state.
- Keep changes small; avoid over-engineering.
- Do not claim runtime success without inspecting actual output.
- Sync docs after completed slices.
