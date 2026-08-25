# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → proven Spatial Forge backend → 3D assets / previews → web viewer → Telegram/Mini App**

MCP is intentionally deferred until the backend and delivery path are independently established. It will later act as a narrow external control adapter, not as an early implementation dependency.

## Current Architecture Decisions

- Repository is intentionally **public** so standard public-repository GitHub-hosted runners can be used under GitHub's public-repo Actions policy.
- Public repo contains engine code, workflow definitions, schemas, skills, viewer code, and non-sensitive generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Blender runs headlessly in Actions.
- P0 proved Blender `4.5.12 LTS` can generate `.blend`, `.glb`, and a preview on `ubuntu-latest` after installing `libegl1`.
- P1 proved MPFB `2.0.17` can be installed non-interactively, generate a generic human from script, apply macro phenotype parameters, attach the built-in `game_engine` rig, export GLB, and render previews headlessly.
- P2 has compact versioned character-build and build-result schemas plus a manifest-driven runtime path for the six proven MPFB macro controls.
- P2.4 proved exact real-world measurement intent can be preserved and explicitly reported unsupported instead of being silently fabricated as an MPFB control.
- The manifest builder reads `mpfb.VERSION` at runtime and fails if it is not `2.0.17`, preventing silent extension drift.
- Exported GLB is validated both structurally and by clean-Blender fresh import when relevant.
- `skills/spatial-forge-3d/SKILL.md` is the project-specific 3D creation intelligence router.
- Phone inspection is deliberately pulled forward as P2V before P2.5/P2.6 because the Creator currently has no PC access and needs to inspect real 3D outputs from Android.
- The first viewer is framework-free/static and URL-driven. It must not require a database or VPS merely to render a model.
- `@google/model-viewer` is pinned to `4.3.1`; do not silently float the dependency.
- Preferred future UI hostname: `forge.drthorne.uk`.
- Cloudflare Pages is the preferred static hosting target once connected. The VPS will later provide protected/private build assets and control APIs, not the viewer rendering engine itself.
- Telegram will later send build notifications/previews and open the same web viewer as a Mini App/web view rather than requiring a second viewer implementation.
- Dedicated Flutter client is deferred until web/Mini App usage demonstrates a concrete need.
- MCP is deferred until underlying build/control operations and phone delivery are proven without it.
- Bamboo is temporary bootstrap help only and must not become a permanent system dependency.

## Security Boundary

Never commit credentials, `.env` files, API keys, SSH keys, Telegram tokens, VPS passwords/config secrets, private character manifests, private meshes/textures/renders, or persistent user data.

Current P2/P2V work uses generic non-canonical data only.

## Proven Runtime State

### P0 — PASS

Successful workflow run: `32859113238`
Commit: `f5d3ebf5bef58d6f445dd4f68a91d6b153cabe34`
Blender: `4.5.12 LTS`

### P1 — PASS

Successful rigged workflow run: `32860562804`
Commit: `691939711d29e552d8920a48b6df8b7e091f7c84`
Blender: `4.5.12 LTS`
MPFB: `2.0.17`

GLB inspection found 1 mesh definition, 1 skin, and 53 joints; previews were visually inspected.

### P2.1–P2.3 — PASS

Successful manifest workflow run: `32864360900`
Commit: `53c5e16bb68a4b588409cb524c0904fbb324225a`

The build-result metadata contained exactly the six requested normalized MPFB controls. GLB structural inspection found 1 mesh definition, 1 skin, and 53 joints. Clean-Blender fresh import succeeded with 2 mesh objects, 1 armature, and 53 bones.

### P2.4 — PASS

Successful workflow run: `32864975879`
Commit: `595bcb5b9768d1f341fac93c803237a0029f3f39`

The downloaded artifact preserved `chest_circumference = 110 cm` in `unsupported_fields` with an explicit reason and did not add it to engine controls. The generated GLB remained structurally valid and fresh-imported successfully.

### P2V.1 — PASS

Viewer files:
- `viewer/index.html`
- `viewer/app.js`
- `viewer/styles.css`
- `viewer/README.md`

Verification workflow:
- `.github/workflows/viewer-smoke.yml`
- successful run `32866763601`
- commit `580048d40ec5189317a30698305faa4956b45514`

The workflow served the static viewer with a local HTTP server and successfully fetched/verified the HTML, JavaScript, CSS, pinned `model-viewer@4.3.1` reference, and URL-driven app wiring. This proves the shell is serveable. It does **not** yet prove a real GLB renders on Android; that remains the next viewer work.

## Current Slice

### P2V.2 — Real GLB Loading + Phone Interaction

The viewer already accepts this explicit URL contract:

- `model` — GLB URL
- `meta` — `build-result.json` URL
- `front` — front preview URL
- `threeQuarter` — three-quarter preview URL
- `title` — display label

Next target sequence:
1. establish a static deployment path for the viewer
2. provide a generic Spatial Forge GLB and metadata through browser-accessible URLs
3. open the deployed viewer with those URLs
4. verify rotate/zoom/reset and metadata rendering
5. verify from the Creator's Android phone
6. only then mark P2V.2/P2V.3/P2V.4/P2V.7 complete as actually proven

Preferred final UI hostname remains `forge.drthorne.uk`.

Do not add a database, account system, large SPA framework, VPS render dependency, Telegram bot, private canon, or MCP in this viewer foundation.

After P2V is usable, return to P2.5 version/lock semantics and P2.6 two-revision runtime proof, then build the VPS protected asset/control path.

## Verification Method

IANEO can inspect GitHub Actions directly. An issue is not required for workflow checking. Use run → jobs/steps → failed logs → artifact list → artifact download → content/structural inspection → fresh import when relevant → visual inspection as applicable.

For the web viewer, verify the smallest real behavior: page loads, supplied GLB renders, touch interaction works, metadata is truthful, and no private asset is accidentally committed or permanently exposed.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for any 3D/Blender/MPFB work.
- Use `IMPLEMENTATION_PLAN.md` as the canonical checkbox state.
- Keep changes small and directly tied to the current slice.
- Avoid over-engineering and unnecessary tests/guards.
- Preserve the proven Blender `4.5.12 LTS` + MPFB `2.0.17` baseline unless a dedicated upgrade slice proves a replacement.
- Do not claim runtime success without inspecting the actual workflow result/artifacts.
- After each completed slice, synchronize `IMPLEMENTATION_PLAN.md`, `ROADMAP.md` when needed, and this file.
