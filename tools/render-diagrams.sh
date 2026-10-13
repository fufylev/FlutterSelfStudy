#!/usr/bin/env bash
# Рендерит все diagrams/*.mmd в PNG рядом с исходником.
# По умолчанию — только новые/изменённые; с флагом --all — все.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MMDC="$ROOT/tools/node_modules/.bin/mmdc"
ALL="${1:-}"
find "$ROOT" -path "$ROOT/tools" -prune -o -path '*/diagrams/*.mmd' -print | sort | while read -r src; do
  out="${src%.mmd}.png"
  if [[ "$ALL" == "--all" || ! -f "$out" || "$src" -nt "$out" ]]; then
    echo "→ ${src#$ROOT/}"
    "$MMDC" -i "$src" -o "$out" -c "$ROOT/tools/mermaid-config.json" -b white -s 2 -q
  fi
done
