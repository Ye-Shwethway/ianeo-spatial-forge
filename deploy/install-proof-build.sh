#!/usr/bin/env bash
set -euo pipefail

PATH=/usr/sbin:/sbin:/usr/bin:/bin
export PATH

ROOT=/srv/ianeo-spatial-forge
STAGING="$ROOT/app/build-staging/current"
TARGET="$ROOT/private/builds/p3-private-proof"
RUNTIME_USER=spatialforge

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "install-proof-build must run as root" >&2
  exit 1
fi

required=(model.glb build-result.json front.png three-quarter.png)
for name in "${required[@]}"; do
  test -f "$STAGING/$name" || { echo "missing staged asset: $name" >&2; exit 1; }
  test -s "$STAGING/$name" || { echo "empty staged asset: $name" >&2; exit 1; }
done

# Reject unexpected regular files. The proof installer has one narrow payload shape.
mapfile -t staged_files < <(find "$STAGING" -maxdepth 1 -type f -printf '%f\n' | sort)
mapfile -t expected_files < <(printf '%s\n' "${required[@]}" | sort)
[[ "${staged_files[*]}" == "${expected_files[*]}" ]] || {
  echo "unexpected file set in staging" >&2
  exit 1
}

python3 -m json.tool "$STAGING/build-result.json" >/dev/null

rm -rf "$TARGET"
install -d -m 0700 -o "$RUNTIME_USER" -g "$RUNTIME_USER" "$TARGET"
for name in "${required[@]}"; do
  install -m 0600 -o "$RUNTIME_USER" -g "$RUNTIME_USER" "$STAGING/$name" "$TARGET/$name"
done

rm -rf "$STAGING"

echo "Spatial Forge private proof build installed"
echo "build_id=p3-private-proof"
echo "assets=4"
