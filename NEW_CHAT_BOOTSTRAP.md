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
- VPS later provides protected/private build assets and control APIs, not viewer rendering.
- Canonical/private GLBs, previews, manifests, references, and metadata must never be deployed as plain public Pages files.
- Telegram will later open the same web viewer rather than requiring a second implementation.
- Flutter remains optional later; MCP remains late-stage only.
- VPS bootstrap/manual access is one-time only. Termux or Bamboo may establish the connection, directories, service user, and secrets or perform emergency repair. After the deployment connection exists, normal VPS updates must come from GitHub Actions.

## Proven Runtime State

### P0 — PASS
Run `32859113238`, Blender `4.5.12 LTS`.

### P1 — PASS
Run `32860562804`, Blender `4.5.12 LTS`, MPFB `2.0.17`; GLB contained 1 mesh definition, 1 skin, 53 joints.

### P2.1–P2.3 — PASS
Run `32864360900`; exact six normalized MPFB controls applied; clean fresh import succeeded with 2 mesh objects, 1 armature, 53 bones.

### P2.4 — PASS
Run `32864975879`; exact `chest_circumference = 110 cm` preserved in `unsupported_fields` and not fabricated as an engine control.

### P2V — PASS
Viewer Smoke run `32866763601` proved the static shell. Direct Upload runs `32876020417` and `32876094428` proved the production deploy path and HTTPS on both Pages/custom-domain URLs. Generic demo run `32876486511` reused the proven P2.4 artifact, deployed browser-accessible generic assets, and verified the live JSON, GLB, preview, and viewer URL.

The Creator then verified the real demo on Android: the GLB rendered, touch interaction worked, front and three-quarter previews displayed, and build details correctly showed Blender `4.5.12 LTS`, MPFB `2.0.17`, six applied controls, 53 joints, and the unsupported `chest_circumference = 110 cm` request/reason.

The `/demo/` files are generic public-safe only. They are not a pattern for canonical/private asset delivery.

## Current Slice

### P2.5 / P2.6 — Scoped Revision Proof

Implemented foundation:
- character manifest schema now accepts optional `revision`
- `revision.parent_version` identifies the parent manifest version
- `revision.locked_fields` is deliberately limited to the six proven `phenotype.*` controls rather than arbitrary paths
- `scripts/build_character.py` requires `SF_PARENT_MANIFEST` for a revision
- builder rejects wrong character, wrong parent version, non-increasing version, and any locked-field drift before generation
- build-result metadata records the enforced revision relationship
- `fixtures/generic-character-v2.json` changes only `muscle` from `0.72` to `0.52` and locks gender, age, weight, height, and proportions
- `.github/workflows/character-revision.yml` builds v1 and v2, compares applied controls, fresh-imports v2, and uploads both versions for inspection

Current runtime proof run:
- workflow: `Character Revision Proof`
- run ID: `32877860898`
- commit: `137dafa67823894a1dfc95d3aa96370996d3739b`

Do not mark P2.5/P2.6 complete until this run finishes successfully and the uploaded revision artifact/previews are inspected. If it fails, repair only the concrete failure.

After P2.5/P2.6 pass, begin P3 with the smallest private asset/control contract. Do not put Darian/private canon into the public repo or static Pages deployment.

## VPS Manual/Automation Boundary

When P3 reaches the VPS:
1. IANEO should prepare the exact bootstrap requirements first.
2. If a secret or initial connection must be installed manually, provide the Creator one minimal one-shot Termux command or a narrowly scoped Bamboo instruction.
3. Never ask the Creator to paste secret values into chat.
4. Once GitHub Actions can reach the VPS, use Actions for routine deploy/update/verification.
5. Bamboo remains bootstrap/emergency-only and must not become the runtime orchestrator.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Use `IMPLEMENTATION_PLAN.md` as canonical checkbox state.
- Keep changes small; avoid over-engineering.
- Do not claim runtime success without inspecting actual output.
- Sync docs after completed slices.
