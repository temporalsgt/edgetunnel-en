#!/usr/bin/env bash
# Deploy _worker.js as a Cloudflare Pages project (direct upload).
#
# Usage:
#   KV_ID=<namespace-id> ./scripts/deploy-pages-worker.sh [project-name]
#
# The project must already exist. Set the ADMIN secret once with:
#   wrangler pages secret put ADMIN --project-name <project-name>
set -euo pipefail

PROJECT="${1:-edgetunnel-en}"
KV_ID="${KV_ID:-}"
PAGES_URL="${PAGES_URL:-https://edgetunnel-en-panel.pages.dev}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/public"
cp "$ROOT/_worker.js" "$TMP/public/_worker.js"

cat > "$TMP/wrangler.toml" <<EOF
name = "$PROJECT"
pages_build_output_dir = "./public"
compatibility_date = "2025-11-04"

[vars]
PAGES_URL = "$PAGES_URL"
EOF

if [ -n "$KV_ID" ]; then
  cat >> "$TMP/wrangler.toml" <<EOF

[[kv_namespaces]]
binding = "KV"
id = "$KV_ID"
EOF
fi

cd "$TMP"
wrangler pages deploy --branch main --no-bundle
