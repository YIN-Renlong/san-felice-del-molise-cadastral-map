# San Felice del Molise Cadastral Map

Interactive cadastral web map for San Felice del Molise.

## Published map

After GitHub Pages is enabled, the map will be available at:

```
https://$(gh api user --jq .login).github.io/san-felice-del-molise-cadastral-map/
```

## Contents

- `docs/` — GitHub Pages static web map
- `docs/data/parcels.geojson` — processed cadastral parcel data
- `docs/data/sheets.geojson` — cadastral sheet/foglio data
- `docs/data/pcn_ortho_2012_*` — local official orthophoto snapshot, if generated
- `docs/data/ade_wms_*` — local AdE WMS comparison snapshot, if generated
- `scripts/` — processing/rebuild scripts

## Data sources

- Agenzia delle Entrate — Cartografia catastale, CC BY 4.0
- Geoportale Nazionale / MASE / PCN — Ortofoto 2012 WMS, where used
- OpenStreetMap / Esri basemaps where displayed

## Note

This is a technical visualization aid. For legal/court use, preserve original source files, metadata, hashes, CRS information, and obtain professional survey validation where necessary.
