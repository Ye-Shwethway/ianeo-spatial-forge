#!/usr/bin/env bash
set -euo pipefail

ROOT=/srv/ianeo-spatial-forge
RUNTIME_USER=spatialforge
DEPLOY_USER=eidolon-deploy
SERVICE=ianeo-spatial-forge.service

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "bootstrap must run as root" >&2
  exit 1
fi

if ! id "$DEPLOY_USER" >/dev/null 2>&1; then
  echo "required existing deploy user $DEPLOY_USER not found" >&2
  exit 1
fi

if ! id "$RUNTIME_USER" >/dev/null 2>&1; then
  useradd --system --home-dir "$ROOT" --shell /usr/sbin/nologin "$RUNTIME_USER"
fi

install -d -m 0750 -o "$DEPLOY_USER" -g "$RUNTIME_USER" "$ROOT" "$ROOT/app"
install -d -m 0700 -o "$RUNTIME_USER" -g "$RUNTIME_USER" \
  "$ROOT/private" "$ROOT/private/builds" "$ROOT/private/sessions" "$ROOT/state"

ENV_FILE="$ROOT/state/control.env"
if [[ ! -f "$ENV_FILE" ]]; then
  TOKEN=$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)
  umask 077
  printf 'SF_CONTROL_TOKEN=%s\n' "$TOKEN" > "$ENV_FILE"
  unset TOKEN
fi
chown "$RUNTIME_USER:$RUNTIME_USER" "$ENV_FILE"
chmod 0600 "$ENV_FILE"

cat >/etc/systemd/system/$SERVICE <<'UNIT'
[Unit]
Description=IANEO Spatial Forge Private Asset Control Plane
After=network.target

[Service]
Type=simple
User=spatialforge
Group=spatialforge
WorkingDirectory=/srv/ianeo-spatial-forge/app
EnvironmentFile=/srv/ianeo-spatial-forge/state/control.env
Environment=SF_HOST=127.0.0.1
Environment=SF_PORT=18792
Environment=SF_ROOT=/srv/ianeo-spatial-forge
Environment=SF_VIEWER_ORIGIN=https://forge.drthorne.uk
ExecStart=/usr/bin/python3 /srv/ianeo-spatial-forge/app/control-plane/server.py
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/ianeo-spatial-forge/private /srv/ianeo-spatial-forge/state

[Install]
WantedBy=multi-user.target
UNIT
chmod 0644 /etc/systemd/system/$SERVICE

cat >/etc/sudoers.d/ianeo-spatial-forge-deploy <<'SUDOERS'
eidolon-deploy ALL=(root) NOPASSWD: /usr/bin/systemctl restart ianeo-spatial-forge.service, /usr/bin/systemctl status ianeo-spatial-forge.service, /usr/bin/systemctl is-active ianeo-spatial-forge.service
SUDOERS
chmod 0440 /etc/sudoers.d/ianeo-spatial-forge-deploy
visudo -cf /etc/sudoers.d/ianeo-spatial-forge-deploy >/dev/null

systemctl daemon-reload

# Do not enable or start until the first GitHub Actions deployment places app code.

echo "Spatial Forge VPS bootstrap complete"
echo "runtime_user=$RUNTIME_USER"
echo "deploy_user=$DEPLOY_USER"
echo "root=$ROOT"
echo "listen=127.0.0.1:18792"
echo "service_installed=yes"
echo "service_started=no"
echo "control_token_generated=yes (value not printed)"
