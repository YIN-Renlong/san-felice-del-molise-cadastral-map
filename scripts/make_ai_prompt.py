#!/usr/bin/env python3
from pathlib import Path
from xml.sax.saxutils import escape
import sys

ROOT = Path(__file__).resolve().parents[1]

INCLUDE = [
    ".gitignore",
    "README.md",
    "AI_DATA_SUMMARY.md",

    "docs/index.html",

    "scripts/make_ai_prompt.sh",
    "scripts/make_ai_prompt.py",
    "scripts/mvp_ade_gml_map.py",

    "docs/data/ade_wms_manifest.json",
    "docs/data/pcn_ortho_2012_manifest.json",

    "docs/data/genova_family_report.csv",
    "docs/data/target_parcels_duplicates.csv",
    "docs/data/target_parcels_missing.csv",
    "docs/data/target_parcels_report.csv",
]

def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace")

def main():
    out = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "ai_prompt_bundle.xml")

    existing = []

    for rel in INCLUDE:
        path = ROOT / rel
        if path.exists() and path.is_file():
            existing.append(rel)
        else:
            print(f"WARNING: missing file skipped: {rel}", file=sys.stderr)

    if not existing:
        raise SystemExit("ERROR: no files to include")

    parts = ["<documents>"]

    for i, rel in enumerate(existing, start=1):
        text = read_text(ROOT / rel)

        parts.append(f'<document index="{i}">')
        parts.append(f"<source>{escape(rel)}</source>")
        parts.append("<document_content>")
        parts.append(escape(text))
        parts.append("</document_content>")
        parts.append("</document>")

    parts.append("</documents>")
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")

    print("Wrote AI prompt bundle:")
    print(f"  {out}")
    print("")
    print("Included files:")
    for rel in existing:
        print(f"  {rel}")

    print("")
    print("Approx size:")
    print(f"  {out.stat().st_size} bytes")

    forbidden_sources = [
        "<source>docs/data/parcels.geojson</source>",
        "<source>./docs/data/parcels.geojson</source>",
        "<source>docs/data/genova_family_parcels.geojson</source>",
        "<source>./docs/data/genova_family_parcels.geojson</source>",
        "<source>docs/data/target_parcels.geojson</source>",
        "<source>./docs/data/target_parcels.geojson</source>",
    ]

    bundle = out.read_text(encoding="utf-8", errors="replace")

    bad = [s for s in forbidden_sources if s in bundle]

    if bad:
        print("")
        print("ERROR: forbidden generated GeoJSON source included:")
        for s in bad:
            print(f"  {s}")
        raise SystemExit(1)

    print("")
    print("OK: large generated GeoJSON files are not included as documents.")
    print("")
    print("To copy to clipboard on macOS:")
    print(f"  pbcopy < {out.name}")

if __name__ == "__main__":
    main()
