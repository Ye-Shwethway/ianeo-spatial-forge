# Spatial Forge Private Asset Control Plane

This document defines the smallest P3 interface needed to keep canonical/private Spatial Forge work off the public repository and off static Cloudflare Pages assets.

## Architecture Boundary

```text
forge.drthorne.uk
  -> public static viewer shell on Cloudflare Pages

private Spatial Forge VPS
  -> authenticated control API
  -> private build storage
  -> short-lived viewer sessions
  -> protected GLB / preview / metadata delivery
```

The public repository may contain code, schemas, workflows, skills, and generic fixtures. Private character canon, references, manifests, GLBs, previews, and metadata must remain outside the repository and outside the Pages deployment.

## P3 Design Goals

- one Creator / operator; no user-account system yet
- no database requirement
- no heavy framework requirement
- private assets stored outside any public web root
- short-lived read-only viewer access
- explicit expiry and cleanup
- control credentials never appear in viewer URLs
- routine deployment comes from GitHub Actions after one-time VPS bootstrap

## Minimal Filesystem Contract

Preferred service root:

```text
/srv/ianeo-spatial-forge/
  app/                 # deployed control-plane release
  private/
    builds/            # private build directories, never directly web-served
    sessions/          # temporary read-only session metadata/links
  state/               # small local runtime state if needed
```

Ownership should belong to a dedicated least-privilege service account such as `spatialforge`. The deploy account may update `app/` through the controlled deployment path but should not gain unrelated VPS privileges.

## Minimal HTTP Contract

### `GET /health`

Purpose: deployment/runtime verification.

Authentication: none.

Response shape:

```json
{
  "status": "ok",
  "service": "ianeo-spatial-forge",
  "version": "<deployed commit or release id>"
}
```

No private build information is returned.

### `GET /v1/builds/{build_id}`

Purpose: read private build status/metadata for control-plane clients.

Authentication: `Authorization: Bearer <control token>`.

Initial status values may remain deliberately small: `ready`, `failed`, `expired`.

This endpoint is not exposed to the public viewer.

### `POST /v1/builds/{build_id}/viewer-session`

Purpose: create a temporary read-only browser session for one already-existing private build.

Authentication: `Authorization: Bearer <control token>`.

Request body may optionally contain:

```json
{
  "ttl_seconds": 7200
}
```

Default TTL: 2 hours.
Hard maximum for early P3: 24 hours.

Response shape:

```json
{
  "expires_at": "<UTC ISO-8601>",
  "viewer_url": "https://forge.drthorne.uk/?model=<temporary-model-url>&meta=<temporary-meta-url>&front=<temporary-front-url>&threeQuarter=<temporary-three-quarter-url>&title=<label>"
}
```

The returned asset URLs use a high-entropy opaque session identifier. Possession of the temporary link grants read-only access until expiry. The long-lived control token must never be embedded in the viewer URL.

### `GET /s/{session_id}/{asset}`

Purpose: serve one temporary read-only build asset to the public viewer.

Authentication: possession of an unexpired high-entropy `session_id`.

Allowed early assets only:
- `model.glb`
- `build-result.json`
- `front.png`
- `three-quarter.png`

Do not expose `.blend`, source manifests, private references, arbitrary filesystem paths, directory listings, or unrelated build files through viewer sessions.

Expired or unknown sessions return `404` rather than revealing whether a private build exists.

## HTTP Safety Headers

Private asset responses should use at least:

```text
Cache-Control: private, no-store
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
```

CORS for viewer assets should allow only the production viewer origin:

```text
Access-Control-Allow-Origin: https://forge.drthorne.uk
```

The authenticated control API should not enable browser CORS unless a concrete control UI later requires it.

## Session Semantics

Early P3 should use server-side random session IDs rather than building a generic JWT/auth platform.

Requirements:
- generated from a cryptographically secure random source
- at least 256 bits of entropy
- read-only
- linked to exactly one private build
- explicit expiry
- deleted by cleanup after expiry
- never committed or logged in full when avoidable

A viewer link is therefore temporary capability access, not a permanent public URL.

## Secrets

Initial control-plane secret set should remain small:

- `SF_CONTROL_TOKEN` — long-lived operator/control bearer token, stored only on VPS and in whichever trusted automation client later needs it

GitHub Actions deployment should use a separate SSH deploy credential. Do not reuse `SF_CONTROL_TOKEN` as an SSH credential.

Do not put secret values in this repository, workflow YAML, chat messages, viewer query parameters, or static Pages files.

## Deployment Boundary

One-time bootstrap may be performed manually from Termux or by Bamboo to establish:
- dedicated service/deploy users
- directories and ownership
- SSH deploy public key
- system service/runtime prerequisites
- initial secret file with correct permissions

After this bootstrap succeeds:

```text
GitHub Actions
  -> SSH/SCP or rsync over SSH
  -> staged release on VPS
  -> atomic/safe service restart
  -> /health verification
```

Routine code deployment must not require Termux or Bamboo.

## Explicit Non-Goals for P3

Do not add yet:
- user registration/login
- database server
- OAuth provider
- permanent public asset URLs
- S3/R2 dependency
- build queue/orchestration framework
- Blender rendering on the VPS
- Telegram logic
- MCP server
- generic file browser

## P3 Proof Sequence

1. Bootstrap the VPS service/deploy boundary once.
2. Deploy a tiny control-plane service through GitHub Actions.
3. Verify `/health` remotely.
4. Stage one generic-but-private test build under `private/builds/`.
5. Create a temporary viewer session.
6. Verify public viewer can read only the allowed temporary assets.
7. Verify the same URLs fail after expiry/cleanup.
8. Only after this privacy path works should canonical character assets use it.
