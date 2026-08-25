#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENV_FILE = Path("/srv/ianeo-spatial-forge/state/control.env")
BUILD_ID = "p3-private-proof"
SESSION_URL = f"http://127.0.0.1:18792/v1/builds/{BUILD_ID}/viewer-session"
VIEWER_HOST = "forge.drthorne.uk"
ASSET_HOST = "assets.drthorne.uk"
TTL_SECONDS = 7200
EXPECTED_ASSETS = {
    "model": "model.glb",
    "meta": "build-result.json",
    "front": "front.png",
    "threeQuarter": "three-quarter.png",
}
SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{40,}$")


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def read_control_token():
    if not ENV_FILE.is_file():
        fail("control environment file is missing")
    token = ""
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "SF_CONTROL_TOKEN":
            token = value.strip().strip('"').strip("'")
            break
    if not token:
        fail("SF_CONTROL_TOKEN is missing")
    return token


def validate_viewer_url(viewer_url):
    parsed = urllib.parse.urlparse(viewer_url)
    if parsed.scheme != "https" or parsed.netloc != VIEWER_HOST or parsed.path != "/":
        fail("unexpected viewer origin")
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if query.get("title") != [BUILD_ID]:
        fail("unexpected viewer title")

    session_id = None
    for key, asset_name in EXPECTED_ASSETS.items():
        values = query.get(key)
        if not values or len(values) != 1:
            fail(f"missing viewer asset parameter: {key}")
        asset_url = urllib.parse.urlparse(values[0])
        if asset_url.scheme != "https" or asset_url.netloc != ASSET_HOST:
            fail(f"unexpected asset origin for {key}")
        parts = asset_url.path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "s" or parts[2] != asset_name:
            fail(f"unexpected protected asset path for {key}")
        if not SESSION_ID_RE.fullmatch(parts[1]):
            fail("invalid session identifier")
        if session_id is None:
            session_id = parts[1]
        elif parts[1] != session_id:
            fail("viewer assets do not share one session")


def main():
    if os.geteuid() != 0:
        fail("proof session helper must run as root")

    token = read_control_token()
    request = urllib.request.Request(
        SESSION_URL,
        data=json.dumps({"ttl_seconds": TTL_SECONDS}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 201:
                fail(f"viewer-session creation returned HTTP {response.status}")
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        fail(f"viewer-session creation returned HTTP {exc.code}")
    except Exception as exc:
        fail(f"viewer-session creation failed: {type(exc).__name__}")

    viewer_url = payload.get("viewer_url")
    expires_at = payload.get("expires_at")
    if not isinstance(viewer_url, str) or not isinstance(expires_at, str):
        fail("viewer-session response is incomplete")
    validate_viewer_url(viewer_url)

    print(f"expires_at={expires_at}")
    print(f"viewer_url={viewer_url}")


if __name__ == "__main__":
    main()
