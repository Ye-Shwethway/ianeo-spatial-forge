#!/usr/bin/env python3
import json
import mimetypes
import os
import secrets
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

HOST = os.environ.get("SF_HOST", "127.0.0.1")
PORT = int(os.environ.get("SF_PORT", "18792"))
ROOT = Path(os.environ.get("SF_ROOT", "/srv/ianeo-spatial-forge"))
BUILDS = ROOT / "private" / "builds"
SESSIONS = ROOT / "private" / "sessions"
CONTROL_TOKEN = os.environ.get("SF_CONTROL_TOKEN", "")
VERSION = os.environ.get("SF_VERSION", "dev")
VIEWER_ORIGIN = os.environ.get("SF_VIEWER_ORIGIN", "https://forge.drthorne.uk").rstrip("/")
ASSET_ORIGIN = os.environ.get("SF_ASSET_ORIGIN", "").rstrip("/")
DEFAULT_TTL = 7200
MAX_TTL = 86400
ALLOWED_ASSETS = {
    "model.glb": "model.glb",
    "build-result.json": "build-result.json",
    "front.png": "front.png",
    "three-quarter.png": "three-quarter.png",
}


def utc_iso(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)


def cleanup_expired_sessions(now=None):
    now = int(time.time()) if now is None else int(now)
    removed = 0
    if not SESSIONS.is_dir():
        return removed
    for session_path in SESSIONS.glob("*.json"):
        try:
            session = read_json(session_path)
            expired = int(session.get("expires_at", 0)) <= now
        except Exception:
            expired = True
        if expired:
            try:
                session_path.unlink()
                removed += 1
            except FileNotFoundError:
                pass
    return removed


def asset_url(path):
    return f"{ASSET_ORIGIN}{path}" if ASSET_ORIGIN else path


class Handler(BaseHTTPRequestHandler):
    server_version = "SpatialForge/0.2"

    def log_message(self, fmt, *args):
        # Never log Authorization headers or opaque session IDs from paths.
        print(f"{self.client_address[0]} {self.command} {self._safe_path()} {fmt % args}")

    def _safe_path(self):
        if self.path.startswith("/s/"):
            parts = self.path.split("/")
            return f"/s/<redacted>/{parts[-1] if parts else ''}"
        return self.path.split("?", 1)[0]

    def _json(self, status, payload, extra_headers=None):
        body = (json.dumps(payload, separators=(",", ":")) + "\n").encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        if not CONTROL_TOKEN:
            return False
        return secrets.compare_digest(self.headers.get("Authorization", ""), f"Bearer {CONTROL_TOKEN}")

    def _require_auth(self):
        if self._authorized():
            return True
        self._json(401, {"error": "unauthorized"})
        return False

    def do_GET(self):
        cleanup_expired_sessions()
        path = self.path.split("?", 1)[0]
        if path == "/health":
            return self._json(200, {"status": "ok", "service": "ianeo-spatial-forge", "version": VERSION})

        if path.startswith("/v1/builds/"):
            if not self._require_auth():
                return
            build_id = path.removeprefix("/v1/builds/")
            if not build_id or "/" in build_id or build_id.startswith("."):
                return self._json(404, {"error": "not_found"})
            build_dir = BUILDS / build_id
            metadata = build_dir / "build-result.json"
            if not metadata.is_file():
                return self._json(404, {"error": "not_found"})
            return self._json(200, {"build_id": build_id, "status": "ready", "metadata": read_json(metadata)})

        if path.startswith("/s/"):
            return self._serve_session_asset(path)

        self._json(404, {"error": "not_found"})

    def do_POST(self):
        cleanup_expired_sessions()
        path = self.path.split("?", 1)[0]
        prefix = "/v1/builds/"
        suffix = "/viewer-session"
        if not (path.startswith(prefix) and path.endswith(suffix)):
            return self._json(404, {"error": "not_found"})
        if not self._require_auth():
            return

        build_id = path[len(prefix):-len(suffix)]
        if not build_id or "/" in build_id or build_id.startswith("."):
            return self._json(404, {"error": "not_found"})
        build_dir = BUILDS / build_id
        if not (build_dir / "model.glb").is_file() or not (build_dir / "build-result.json").is_file():
            return self._json(404, {"error": "not_found"})

        length = int(self.headers.get("Content-Length", "0") or "0")
        if length > 4096:
            return self._json(413, {"error": "request_too_large"})
        payload = {}
        if length:
            try:
                payload = json.loads(self.rfile.read(length))
            except Exception:
                return self._json(400, {"error": "invalid_json"})
        ttl = payload.get("ttl_seconds", DEFAULT_TTL)
        if not isinstance(ttl, int) or isinstance(ttl, bool) or not 60 <= ttl <= MAX_TTL:
            return self._json(400, {"error": "invalid_ttl"})

        session_id = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + ttl
        SESSIONS.mkdir(parents=True, exist_ok=True)
        write_json_atomic(SESSIONS / f"{session_id}.json", {"build_id": build_id, "expires_at": expires_at})

        base = f"/s/{session_id}"
        viewer_url = (
            f"{VIEWER_ORIGIN}/?model={quote(asset_url(base + '/model.glb'), safe='/:')}"
            f"&meta={quote(asset_url(base + '/build-result.json'), safe='/:')}"
            f"&front={quote(asset_url(base + '/front.png'), safe='/:')}"
            f"&threeQuarter={quote(asset_url(base + '/three-quarter.png'), safe='/:')}"
            f"&title={quote(build_id)}"
        )
        self._json(201, {"expires_at": utc_iso(expires_at), "viewer_url": viewer_url})

    def _serve_session_asset(self, path):
        parts = path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "s":
            return self._json(404, {"error": "not_found"})
        _, session_id, asset = parts
        if asset not in ALLOWED_ASSETS or len(session_id) < 40:
            return self._json(404, {"error": "not_found"})

        session_path = SESSIONS / f"{session_id}.json"
        try:
            session = read_json(session_path)
        except Exception:
            return self._json(404, {"error": "not_found"})
        if int(session.get("expires_at", 0)) <= int(time.time()):
            try:
                session_path.unlink()
            except FileNotFoundError:
                pass
            return self._json(404, {"error": "not_found"})

        build_id = session.get("build_id", "")
        if not isinstance(build_id, str) or not build_id or "/" in build_id or build_id.startswith("."):
            return self._json(404, {"error": "not_found"})
        source = BUILDS / build_id / ALLOWED_ASSETS[asset]
        if not source.is_file():
            return self._json(404, {"error": "not_found"})

        content_type = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
        if source.suffix == ".glb":
            content_type = "model/gltf-binary"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(source.stat().st_size))
        self.send_header("Cache-Control", "private, no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Access-Control-Allow-Origin", VIEWER_ORIGIN)
        self.end_headers()
        with source.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                self.wfile.write(chunk)


def main():
    if not CONTROL_TOKEN:
        raise SystemExit("SF_CONTROL_TOKEN is required")
    BUILDS.mkdir(parents=True, exist_ok=True)
    SESSIONS.mkdir(parents=True, exist_ok=True)
    cleanup_expired_sessions()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"IANEO Spatial Forge control plane listening on {HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
