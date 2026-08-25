# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Current direction:

**Creator → Cloudflare Access → `forge.drthorne.uk` → same-origin `/api` → protected VPS control/assets**

Build work remains:

**Creator → IANEO → GitHub Actions → Blender/MPFB → validated outputs → VPS private build storage → web viewer**

MCP remains deferred until the underlying 3D quality, backend, and delivery paths are independently proven.

## Current Architecture

- Public repo contains engine code, workflows, schemas, skills, viewer code, Pages Function proxy, and generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Proven 3D baseline: Blender `4.5.12 LTS` + MPFB `2.0.17`.
- `skills/spatial-forge-3d/SKILL.md` is the 3D creation/validation router.
- `skills/spatial-forge-ui/SKILL.md` is the UI/UX router.
- Viewer is framework-free and uses pinned `@google/model-viewer` `4.3.1`.
- Cloudflare native Git integration is abandoned. Canonical viewer deployment is GitHub Actions → Wrangler → Cloudflare Pages Direct Upload.
- Pages project: `ianeo-spatial-forge`.
- Primary viewer: `https://forge.drthorne.uk/`.
- VPS control plane is localhost-only at `127.0.0.1:18792` and does not render Blender jobs.
- `assets.drthorne.uk` reaches the VPS only through Cloudflare Tunnel.
- Browser control calls are same-origin through `forge.drthorne.uk/api/*`; the Pages Function forwards the authenticated Cloudflare Access assertion server-side to the protected asset/control origin.
- Browser cross-origin Access cookie/login bouncing is not canonical and must not be reintroduced.
- Cloudflare Access uses Email OTP, exact-owner-email Allow, deny-by-default behavior, and a 30-day session. Eager redirect cookie is disabled.
- Bamboo/Termux/root are bootstrap/emergency-only.

## Proven Runtime State

### P0 — PASS
Run `32859113238`; Blender `4.5.12 LTS`.

### P1 — PASS
Run `32860562804`; Blender `4.5.12 LTS`; MPFB `2.0.17`; GLB 1 mesh definition, 1 skin, 53 joints.

### P2 — PASS
Runs `32864360900`, `32864975879`, `32877860898`. Six MPFB controls are proven; unsupported precision is reported rather than fabricated; scoped revision/locks passed.

### P2V — PASS
Viewer smoke, Pages Direct Upload, generic GLB delivery, and Android touch/visual inspection passed.

### P3 — PASS
- service active/enabled
- localhost-only `127.0.0.1:18792`
- public direct port access refused
- temporary sessions + expiry/cleanup proven
- GitHub Actions normal deploy path proven
- `assets.drthorne.uk` tunnel route → `http://127.0.0.1:18792`
- `SF_ASSET_ORIGIN=https://assets.drthorne.uk` active
- Cloudflare Access OTP login/logout verified on Android
- real generic Blender/MPFB private build promoted into VPS private storage
- protected model + previews rendered on Android
- direct authenticated `forge.drthorne.uk/api/v1/builds` returned the private build JSON
- Asset Library root page rendered the `p3-private-proof` build card on Android
- same-origin Pages Function proxy is the canonical browser→VPS control path.

## Current Slice — P3Q.1 Character Quality Baseline

P3Q is the next active phase. The current proof character is structurally valid but visually crude. The project must now improve actual character quality before Telegram or MCP.

P3Q sequence:
1. P3Q.1 clean baseline + fixed front/3-quarter/profile/full-body evidence
2. P3Q.2 mesh presentation/smoothing/normals/mobile-appropriate surface quality
3. P3Q.3 expanded real MPFB face controls + scoped face revision proof
4. P3Q.4 GLB-safe PBR skin/eyes/mouth appearance
5. P3Q.5 hair/brow/facial-hair asset path
6. P3Q.6 clean replaceable clothing path
7. P3Q.7 representative rig deformation cleanup
8. P3Q.8 flattering but honest viewer/render presentation defaults
9. P3Q.9 final generic quality character proof on Android.

Do not call a visual-quality slice complete from structure/tests alone. Fixed comparable visual evidence and actual inspection are required.

## Immediate P3Q.1 Goal

Create one deliberate generic quality-baseline character from deterministic source. Do not try to solve skin, hair, clothes, face, and deformation all at once. First produce fixed comparable evidence and identify the visible defects that matter most.

Required evidence:
- front full-body
- three-quarter full-body
- profile
- face close-up
- GLB in `forge.drthorne.uk`
- current material/asset/mesh summary.

Then choose the smallest next visual improvement based on that evidence.

## VPS Operating Boundary

1. GitHub Actions is the normal deployment/update/verification path.
2. Bamboo/Termux/root access is bootstrap or emergency-only.
3. Never ask the Creator to paste secret values into chat.
4. Do not expose `127.0.0.1:18792` directly to the Internet.
5. Do not modify unrelated `/srv/eidolon`, tunnels, services, firewall rules, or container ports.

## Working Rules

- Read `AGENTS.md` before implementation.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Read `skills/spatial-forge-ui/SKILL.md` for UI work.
- Use `IMPLEMENTATION_PLAN.md` as canonical checkbox state.
- Keep changes small; avoid over-engineering.
- Do not claim runtime success without inspecting actual output.
- Sync docs after completed slices.
