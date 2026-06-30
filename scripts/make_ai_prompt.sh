#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-ai_prompt_bundle.xml}"

if ! command -v files-to-prompt >/dev/null 2>&1; then
  echo "ERROR: files-to-prompt is not installed."
  echo ""
  echo "Install with one of:"
  echo "  python3 -m pip install files-to-prompt"
  echo "  pipx install files-to-prompt"
  echo ""
  exit 1
fi

files-to-prompt . \
  --cxml \
  --ignore ".git/*" \
  --ignore ".git/**" \
  --ignore ".DS_Store" \
  --ignore "_patch_backups/*" \
  --ignore "_patch_backups/**" \
  --ignore "ai_prompt_bundle.xml" \
  --ignore "ai_prompt_bundle.txt" \
  --ignore "docs/data/parcels.geojson" \
  --ignore "docs/data/genova_family_parcels.geojson" \
  --ignore "docs/data/target_parcels.geojson" \
  --ignore "docs/data/pcn_ortho_2012_tiles/*" \
  --ignore "docs/data/pcn_ortho_2012_tiles/**" \
  --ignore "docs/data/ade_wms_tiles/*" \
  --ignore "docs/data/ade_wms_tiles/**" \
  --ignore "*.png" \
  --ignore "*.jpg" \
  --ignore "*.jpeg" \
  --ignore "*.tif" \
  --ignore "*.tiff" \
  --ignore "*.zip" \
  --ignore "*.gml" \
  > "$OUT"

echo "Wrote AI prompt bundle:"
echo "  $OUT"
echo ""
echo "Approx size:"
wc -c "$OUT"
echo ""
echo "To copy to clipboard on macOS:"
echo "  pbcopy < \"$OUT\""
