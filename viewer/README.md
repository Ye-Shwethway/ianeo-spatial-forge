# Spatial Forge Viewer

This directory contains the first phone-first inspection surface for IANEO Spatial Forge.

It is intentionally framework-free and stateless. The viewer does not own builds, accounts, or storage. It renders assets supplied through explicit URLs.

## URL contract

Open the viewer with any subset of these query parameters:

- `model` — GLB URL
- `meta` — Spatial Forge `build-result.json` URL
- `front` — front preview image URL
- `threeQuarter` — three-quarter preview image URL
- `title` — display label

Example shape:

```text
/?model=<glb-url>&meta=<json-url>&front=<png-url>&threeQuarter=<png-url>&title=Generic%20Character
```

The asset host must permit browser access from the viewer origin. In particular, cross-origin GLB/JSON/image delivery may require appropriate CORS headers.

## Hosting direction

Preferred UI hostname: `forge.drthorne.uk`.

Preferred static host: Cloudflare Pages, serving this `viewer/` directory.

The static viewer and the build asset backend are deliberately separate:

```text
forge.drthorne.uk
  -> static viewer

protected build asset URLs
  -> later VPS/control-plane storage
```

The VPS is not required merely to render a GLB. P3 will add protected/private asset delivery and expiry semantics.

## Telegram compatibility

The same web viewer should later open from Telegram as a Mini App/web view. Do not create a second independent 3D viewer unless a concrete Telegram limitation requires it.

## Current dependency

The viewer pins `@google/model-viewer` `4.3.1` from a CDN. Keep the version explicit; do not silently float to latest.

## Security boundary

Do not commit private GLBs, private previews, private character metadata, tokens, signed URLs, or credentials here. Test with generic non-canonical assets only until protected asset delivery exists.
