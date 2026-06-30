#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-ai_prompt_bundle.xml}"

python3 "$(dirname "$0")/make_ai_prompt.py" "$OUT"
