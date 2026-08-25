# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

Target direction:

**Creator → ChatGPT / IANEO → proven Spatial Forge backend → 3D assets / previews → web viewer → Telegram/Mini App**

MCP remains intentionally deferred until backend and delivery paths are independently proven.

## Current Architecture

- Public repo contains engine code, workflows, schemas, skills, viewer code, and generic fixtures only.
- Private character canon and private generated assets must never be committed.
- Proven 3D baseline: Blender `4.5.12 LTS` + MPFB `2.0.17`.
- `skills/spatial-forge-3d/SKILL.md` is the 3D creation/validation router.
- `skills/spatial-forge-ui/SKILL.md` is the UI/UX router.
- Viewer is framework-free/static, URL-driven, and uses pinned `@google/model-viewer` `4.3.1`.
- Cloudflare native Git integration is abandoned. Canonical viewer deployment is GitHub Actions → Wrangler → Cloudflare Pages Direct Upload.
- Pages project: `ianeo-spatial-forge`.
- Viewer URLs: `https://ianeo-spatial-forge.pages.dev/` and `https://forge.drthorne.uk/`.
- VPS stores protected/private build assets and serves control/temporary-asset APIs. It does not render Blender jobs or host the public viewer shell.
- Canonical/private GLBs, previews, manifests, references, and metadata must never be deployed as plain public Pages files.
- Telegram later opens the same viewer. Flutter remains optional. MCP remains late-stage.

## Proven Runtime State

### P0 — PASS
Run `32859113238`; Blender `4.5.12 LTS`.

### P1 — PASS
Run `32860562804`; Blender `4.5.12 LTS`; MPFB `2.0.17`; GLB 1 mesh definition, 1 skin, 53 joints.

### P2 — PASS
Runs `32864360900`, `32864975879`, `32877860898`. Six MPFB controls are proven; unsupported precision is reported rather than fabricated; scoped revision/locks passed.

### P2V — PASS
Viewer smoke, Pages Direct Upload, generic real GLB delivery, and Android touch/visual inspection passed. `/demo/` is generic public-safe only.

### P3.1 — PASS
Private control-plane contract and stdlib Python service implemented.

### P3.2 — PASS
VPS bootstrap is complete:
- runtime user `spatialforge`
- deploy user `eidolon-deploy`
- root `/srv/ianeo-spatial-forge`
- service bind `127.0.0.1:18792`
- private/state directories separated from deploy-owned app code
- local non-printed `SF_CONTROL_TOKEN`
- narrow restart/status/is-active sudo rules only
- service active and enabled at boot
- public IPv4 connection to `18792` refused
- `/health` returns 200
- no tunnel/DNS/firewall/package changes were required for bootstrap.

### P3.3 — PASS
Temporary server-side sessions now have cleanup at service startup and request boundaries. Expired/corrupt session records are removed and expired capability URLs return 404.

Smoke runs `32885401030` and `32885482676` proved cleanup, bearer auth, session creation, protected asset GET, real security/CORS headers, absolute `SF_ASSET_ORIGIN` URL generation, and expired capability deletion.

### P3.5 / P3.6 — PASS
GitHub Actions is the normal VPS deployment path. Bamboo/Termux are bootstrap/emergency-only.

Initial deploy proof: run `32884206891`.

Normal smoke-gated chain is now:

**control-plane change → Control Plane Smoke PASS → Deploy Control Plane to VPS → pinned SSH → code deploy → service restart → localhost health**

Fresh chain proof:
- Control Plane Smoke `32885482676` PASS
- automatic VPS deploy `32885510216` PASS.

## Current Slice — P3.4 Protected HTTPS Asset Origin

P3.4 is the only remaining P3 item.

Current service is intentionally localhost-only; there is no public ingress to port `18792`.

Next goal:
1. Inspect the existing `cloudflared` setup without modifying unrelated ingress.
2. Choose one dedicated HTTPS asset hostname for Spatial Forge.
3. Route only that hostname to `http://127.0.0.1:18792` through Cloudflare Tunnel; never expose port `18792` directly.
4. Set `SF_ASSET_ORIGIN` to that HTTPS hostname.
5. Stage/provide a private-safe test build through an approved path.
6. Create a temporary viewer session and prove `https://forge.drthorne.uk` can fetch GLB/JSON/PNG through the temporary capability URL with correct CORS, no-store headers, and expiry behavior.
7. Keep control-token APIs out of browser CORS.

Do not mark P3.4 complete until this end-to-end live proof exists.

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
