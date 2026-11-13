#!/usr/bin/env bash
# Deploy _worker.js as a Cloudflare Pages project (direct upload).
# Usage: ./scripts/deploy-pages-worker.sh [project-name]
# The project must already exist and have a KV binding named KV.
set -euo pipefail

PROJECT="${1:-edgetunnel-en}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/public"
cp "$ROOT/_worker.js" "$TMP/public/_worker.js"

cat > "$TMP/wrangler.toml" <<EOF
name = "$PROJECT"
pages_build_output_dir = "./public"
compatibility_date = "2025-11-04"
EOF

cd "$TMP"
wrangler pages deploy --branch main --no-bundle
