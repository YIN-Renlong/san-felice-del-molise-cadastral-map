# San Felice del Molise Cadastral Map

Interactive, static, GitHub Pages web map for visualizing cadastral parcels in **San Felice del Molise**, with a focused working area on **Foglio 13** and an overlay for parcels associated with the **Genova family**.

This repository was built as a code-first, reproducible mapping prototype using official Italian cadastral vector data from **Agenzia delle Entrate** and official/national orthophoto imagery where available.

The map is intended as a **technical visualization aid**, not as a final legal survey or cadastral certification.

---

## 1. Published map

If GitHub Pages has been enabled correctly, the live map is available at:

~~~text
https://<github-user>.github.io/san-felice-del-molise-cadastral-map/
~~~

Repository:

~~~text
https://github.com/<github-user>/san-felice-del-molise-cadastral-map
~~~

If the Pages URL returns 404 immediately after deployment, wait a few minutes and refresh.

---

## 2. Current project status

The current map is a static web application under:

~~~text
docs/
~~~

It is intended to be served by GitHub Pages from the `main` branch, `/docs` folder.

The current UI should show:

- Default focus around:
  - longitude: `14.70308095`
  - latitude: `41.89005547`
  - approximate Google Earth focus point provided during development.
- Focus area:
  - **Foglio 13**
- Parcel labels:
  - only the selected target parcel numbers,
  - only in **Foglio 13**.
- Genova family land:
  - selectable green overlay,
  - shown only in **Foglio 13**,
  - checkbox located in a separate bottom section of the legend/panel,
  - clicking a green Genova parcel updates the side information card,
  - no generic popup window.
- Official orthophoto:
  - optional local snapshot from PCN/MASE Ortofoto 2012, if generated.
- AdE WMS comparison:
  - optional local snapshot, if generated.
- OSM and Esri satellite:
  - contextual basemap options.

---

## 3. Repository structure

Expected structure:

~~~text
san-felice-del-molise-cadastral-map/
  README.md
  .gitignore

  docs/
    .nojekyll
    index.html
    data/
      parcels.geojson
      sheets.geojson

      pcn_ortho_2012_manifest.json
      pcn_ortho_2012_tiles/
        pcn_ortho_2012_0000.jpg
        ...

      ade_wms_manifest.json
      ade_wms_tiles/
        ade_wms_0000.png
        ...

      target_parcels.geojson
      genova_family_parcels.geojson
      *.csv

  scripts/
    mvp_ade_gml_map.py
~~~

Notes:

- `docs/index.html` is the current clean/stable frontend.
- `docs/data/parcels.geojson` is the main cadastral parcel layer.
- `docs/data/sheets.geojson` is the cadastral sheet/foglio layer.
- `docs/data/pcn_ortho_2012_*` is optional but recommended for official orthophoto context.
- `docs/data/ade_wms_*` is optional, used for visual comparison with AdE WMS.
- `scripts/mvp_ade_gml_map.py` is the initial GML-to-GeoJSON converter used during the MVP phase. The current final `docs/index.html` includes later UI logic and should not be overwritten without care.

---

## 4. Data sources

### 4.1 Agenzia delle Entrate cadastral vector data

Primary cadastral source:

- Provider: **Agenzia delle Entrate**
- Service/product: **Cartografia catastale**
- Access methods discovered:
  - WMS
  - WFS
  - bulk download GML ZIP by region/province/comune
- License stated by AdE: **CC BY 4.0**
- Municipality used here:
  - **San Felice del Molise**
  - codice catastale: `H833`
- Files used locally during processing:
  - `H833_SAN FELICE DEL MOLISE_map.gml`
  - `H833_SAN FELICE DEL MOLISE_ple.gml`

Important discovery during the project:

Initially we assumed AdE exposed only raster WMS publicly. This was corrected after finding official AdE pages for:

- `Cartografia catastale WFS`
- `Download massivo cartografia catastale`

The official WFS endpoint found:

~~~text
https://wfs.cartografia.agenziaentrate.gov.it/inspire/wfs/owfs01.php
~~~

The official WMS endpoint found:

~~~text
https://wms.cartografia.agenziaentrate.gov.it/inspire/wms/ows01.php
~~~

The bulk download path was used because it is more reproducible than live WFS queries.

---

### 4.2 PCN / MASE official orthophoto 2012

Official orthophoto source investigated and used:

- Provider: **Geoportale Nazionale / MASE / PCN**
- Service: **Ortofoto a colori anno 2012**
- WMS endpoint:

~~~text
http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/WMS_v1.3/raster/ortofoto_colore_12.map
~~~

Capabilities URL:

~~~text
http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/WMS_v1.3/raster/ortofoto_colore_12.map&service=wms&request=getCapabilities&version=1.3.0
~~~

Layer used for Molise:

~~~text
OI.ORTOIMMAGINI.2012.33
~~~

Reason:

The WMS capabilities show that the 2012 orthophoto is split into UTM zone coverage. Molise is in the zone 33 coverage described by the layer:

~~~text
OI.ORTOIMMAGINI.2012.33
~~~

The capabilities describe these as orthophotos with approximately 50 cm pixels.

Important:

- This source is orthophoto imagery.
- It is appropriate for seeing aerial photo context.
- It is not cadastral boundary evidence by itself.
- It may be outdated relative to current ground conditions.

---

### 4.3 LiDAR

A LiDAR service was found:

~~~text
Prodotti LiDAR - Regione Molise
http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/WMS_v1.3/servizi-LiDAR/LIDAR_MOLISE.map
~~~

This is **not** a photo source.

LiDAR is elevation/terrain data, not aerial imagery. It may be useful later for topography or terrain analysis, but it does not replace orthophotos for seeing buildings/houses visually.

---

### 4.4 OSM and Esri satellite basemaps

The map includes contextual basemaps:

- OpenStreetMap raster tiles
- Esri World Imagery

These are useful visually, but not treated as primary legal evidence.

During testing, Esri imagery produced “map data not available” or low-resolution overzooming at high zoom levels. That is a source limitation. It motivated adding the official PCN/MASE orthophoto snapshot.

---

## 5. Cadastral GML data structure

Two official GML files are central.

### 5.1 `*_map.gml`

This file contains cadastral map sheets, i.e. **fogli catastali**.

Feature type:

~~~text
CP:CadastralZoning
~~~

Important fields:

~~~text
CP:LABEL
CP:NATIONALCADASTRALZONINGREFERENCE
CP:ADMINISTRATIVEUNIT
CP:LEVEL
CP:LEVELNAME
CP:msGeometry
~~~

Example conceptual record:

~~~text
LABEL = 13
NATIONALCADASTRALZONINGREFERENCE = H833_001300
ADMINISTRATIVEUNIT = H833
~~~

Meaning:

- `LABEL` is the human-readable foglio number.
- `NATIONALCADASTRALZONINGREFERENCE` is the sheet reference.
- Geometry is the outline of the cadastral sheet.

---

### 5.2 `*_ple.gml`

This file contains individual cadastral parcels, i.e. **particelle catastali**.

Feature type:

~~~text
CP:CadastralParcel
~~~

Important fields:

~~~text
CP:LABEL
CP:NATIONALCADASTRALREFERENCE
CP:msGeometry
~~~

Example conceptual record:

~~~text
LABEL = 594
NATIONALCADASTRALREFERENCE = H833_001300.594
~~~

Meaning:

- `LABEL` is the parcel number.
- `NATIONALCADASTRALREFERENCE` has the form:

~~~text
<ComuneCode>_<FoglioReference>.<Particella>
~~~

Example:

~~~text
H833_001300.594
~~~

The parent sheet reference is everything before the dot:

~~~text
H833_001300
~~~

This joins to:

~~~text
CP:NATIONALCADASTRALZONINGREFERENCE
~~~

in the `*_map.gml` file.

---

### 5.3 Geometry types

Parcel geometries can be:

- `gml:Polygon`
- `gml:MultiSurface`

Some polygons contain internal rings/holes:

- `gml:exterior`
- `gml:interior`

The parser must support both simple and complex geometries.

---

### 5.4 CRS and coordinate order

AdE GML source CRS:

~~~text
EPSG:6706
urn:ogc:def:crs:EPSG::6706
~~~

Observed GML coordinate order:

~~~text
latitude longitude
~~~

Example:

~~~text
41.91249313 14.67409434
~~~

GeoJSON and MapLibre require:

~~~text
longitude latitude
~~~

Therefore the conversion logic must swap axis order when producing GeoJSON.

Correct coordinates for the area should look like:

~~~text
longitude around 14.6–14.8
latitude around 41.8–42.0
~~~

If values appear as:

~~~text
x around 41
y around 14
~~~

then the axis order is wrong.

---

## 6. Processing architecture

The project uses a static-site architecture:

~~~text
AdE GML bulk download
        |
        v
Python parser/converter
        |
        |-- parcels.geojson
        |-- sheets.geojson
        |
        v
MapLibre GL JS static web app
        |
        |-- GitHub Pages
        |-- local image overlays
        |-- interactive layer toggles
~~~

Important design choice:

MapLibre GL JS does **not** read Italian INSPIRE GML directly. Therefore the GML is converted to GeoJSON.

OpenLayers could parse WFS/GML more directly, but the final static GitHub Pages deployment is simpler with GeoJSON and local image overlays.

---

## 7. Frontend design

Library:

~~~text
MapLibre GL JS
~~~

Hosting:

~~~text
GitHub Pages
~~~

Primary frontend file:

~~~text
docs/index.html
~~~

Primary data files:

~~~text
docs/data/parcels.geojson
docs/data/sheets.geojson
~~~

Current important constants inside `docs/index.html`:

~~~text
FOCUS_CENTER = [14.70308095, 41.89005547]
FOCUS_ZOOM = 18.0
FOCUS_FOGLIO = "13"
~~~

The app loads:

- parcel GeoJSON,
- sheet GeoJSON,
- optional local PCN orthophoto image grid,
- optional local AdE WMS image grid,
- OSM raster basemap,
- Esri satellite raster basemap.

---

## 8. Current visual layers

### 8.1 Official PCN Ortofoto 2012

Checkbox:

~~~text
Ortofoto 2012 ufficiale
~~~

This uses locally downloaded image tiles listed in:

~~~text
docs/data/pcn_ortho_2012_manifest.json
~~~

The actual image files are stored in:

~~~text
docs/data/pcn_ortho_2012_tiles/
~~~

The layer is loaded as multiple MapLibre `image` sources.

Reason for local download:

- avoids browser CORS issues,
- avoids mixed HTTP/HTTPS issues,
- makes the GitHub Pages demonstration stable,
- provides an official orthophoto background.

---

### 8.2 OSM and Esri satellite

Checkboxes:

~~~text
Satellite basemap
~~~

OSM is the default raster basemap. Esri satellite is optional.

Known issue:

At high zoom, Esri imagery may be unavailable or blurry due to source limits. Overzooming can avoid missing tiles, but cannot create new resolution. The official orthophoto is the preferred professional background.

---

### 8.3 Particelle catastali

Checkbox:

~~~text
Particelle catastali
~~~

These are from AdE vector GML converted to GeoJSON.

Displayed as blue outlines/fills.

---

### 8.4 Fogli catastali

Checkbox:

~~~text
Fogli catastali
~~~

These are from `*_map.gml`, converted to GeoJSON.

Displayed as orange sheet outlines.

---

### 8.5 Target parcel labels

Checkbox:

~~~text
Target particella labels
~~~

Only a defined list of parcel labels is shown.

The labels are further restricted to:

~~~text
Foglio 13
~~~

This prevents unrelated duplicate parcel numbers in other fogli from cluttering the map.

---

### 8.6 Genova family land

Bottom legend section:

~~~text
Terreni famiglia Genova — Foglio 13
~~~

Checkbox:

~~~text
Mostra terreni famiglia Genova
~~~

Layer behavior:

- green fill and green outline,
- only features where `genova_family = true`,
- only features where `foglio = "13"`,
- hover effect increases opacity/line width,
- clicking a green parcel updates the side information card,
- no popup window is created.

Important:

The Genova family matching is currently based on **parcel number** and then visually filtered to **Foglio 13**. For final legal-grade data, it should be made explicit as `foglio + particella`.

---

## 9. Target parcel-number list

The map labels only these parcel numbers, restricted in the frontend to Foglio 13:

~~~text
173, 383, 391, 555, 556, 557, 558, 559, 560, 561, 562, 563,
564, 565, 566, 567, 569, 570, 571, 572, 573, 575, 576, 580,
581, 582, 583, 584, 585, 586, 587, 591, 592, 594, 595, 597,
598, 600, 601, 604, 605, 606, 607, 611, 612, 613, 614, 616,
617, 619, 622, 623, 624, 625, 626, 627, 628, 635, 636, 637,
640, 641, 642, 650, 651, 669, 700, 701, 703, 707, 725, 726,
727, 736, 739, 790, 802, 834, 835, 836, 837, 838, 839, 840,
841, 842, 843, 844, 852, 853, 854, 855, 856, 857, 862, 887,
888, 889, 890, 891, 892, 893, 894, 895, 896, 925, 926, 927,
928, 929, 930, 931, 932, 934, 941, 947, 1007
~~~

Development note:

When these numbers were first matched against all parcel data without foglio restriction, many duplicates appeared because parcel numbers are not globally unique within the comune. The solution was to restrict display to Foglio 13.

---

## 10. Genova family rights list

The Genova family overlay uses the following user-provided rights table.

Important:

This list is not from the open AdE cadastral GML. It is a separate annotation layer supplied during development.

~~~text
3 - Comproprietà
4 - Livellario
11 - Proprietà 1/1
12 - Proprietà 1/3 e Proprietà 2/3 (Totale 100%)
13 - Proprietà 1/1
18 - Proprietà 1/1
24 - Proprietà 1/1
25 - Proprietà 1/1
28 - Nuda Proprietà e Usufrutto 1/1
31 - Comproprietà
37 - Proprietà 1/1
44 - Proprietà 1/1
45 - Nuda Proprietà e Usufrutto 1/1
48 - Proprietà 1/1
52 - Proprietà 1/1
62 - Nuda Proprietà e Usufrutto 1/1
74 - Livellario e Usufrutto generale di livello
78 - Proprietà 1/1 (Fabbricato)
88 - Proprietà 1/1
103 - Proprietà 1/1
107 - Proprietà 1/1
111 - Proprietà 1/1
115 - Proprietà 1/1
130 - Proprietà 1/1
131 - Proprietà 1/1
134 - Proprietà 1/1
135 - Proprietà 1/1
136 - Proprietà 1/1
138 - Proprietà 1/1
139 - Proprietà 1/1
140 - Proprietà 1/1
141 - Nuda Proprietà e Usufrutto 1/1
145 - Nuda Proprietà e Usufrutto 1/1
146 - Proprietà 1/1
147 - Proprietà 1/1
148 - Proprietà 1/1
149 - Nuda Proprietà e Usufrutto 1/1
150 - Proprietà 1/1
151 - Comproprietà / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
152 - Nuda Proprietà e Usufrutto 1/1 / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
153 - Nuda Proprietà e Usufrutto 1/1 / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
154 - Proprietà 1/3 e Proprietà 2/3 (Totale 100%) / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
155 - Nuda Proprietà e Usufrutto 1/1 / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
156 - Proprietà 1/3 e Proprietà 2/3 (Totale 100%) / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
157 - Proprietà 1/1
159 - Proprietà 1/1
161 - Proprietà 1/1
162 - Proprietà 1/1
164 - Proprietà 1/1
192 - Proprietà 1/1
195 - Proprietà 1/1
200 - Comproprietà
201 - Comproprietà
202 - Comproprietà
203 - Comproprietà
204 - Comproprietà
205 - Comproprietà
207 - Proprietà 1/3 e Proprietà 2/3 (Totale 100%)
212 - Proprietà 1/3 e Proprietà 2/3 (Totale 100%)
232 - Comproprietà
244 - Comproprietà
281 - Comproprietà / Proprietà 1/1 (diritti diversi su fogli catastali diversi)
314 - Proprietà 1/1
343 - Proprietà 1/1
374 - Proprietà 1/1 (Fabbricato)
427 - Proprietà 1/1
436 - Proprietà 1/1
438 - Proprietà 1/1
457 - Proprietà 1/1
458 - Nuda Proprietà e Usufrutto 1/1
460 - Proprietà 1/1
500 - Proprietà 1/2
501 - Proprietà 1/2
502 - Proprietà 1/2
575 - Proprietà 1/1
576 - Proprietà 1/1
582 - Proprietà 1/1 (Fabbricato)
594 - Proprietà 1/1
595 - Proprietà 1/1
600 - Proprietà 1/1
601 - Proprietà 1/1
639 - Proprietà 1/1
647 - Proprietà 1/1
649 - Proprietà 1/1
664 - Nuda Proprietà e Usufrutto 1/1
667 - Proprietà 1/1
685 - Proprietà 1/1
700 - Proprietà 1/1
704 - Proprietà 1/1
736 - Proprietà 1/1
738 - Proprietà 1/1
739 - Proprietà 1/1
742 - Proprietà 1/1
743 - Proprietà 1/1
745 - Proprietà 1/1
754 - Proprietà 1/1
756 - Ciascuno per i propri diritti (Quota indefinita con terzi)
768 - Proprietà 1/1
769 - Proprietà 1/1
778 - Proprietà 1/1
779 - Proprietà 1/1
786 - Nuda Proprietà e Usufrutto 1/1
787 - Nuda Proprietà e Usufrutto 1/1
788 - Nuda Proprietà e Usufrutto 1/1
821 - Nuda Proprietà e Usufrutto 1/1
853 - Proprietà 1/1
927 - Proprietà 1/1
928 - Proprietà 1/1
929 - Proprietà 1/1
~~~

Current frontend behavior:

- the rights list is applied to parcel features by parcel number,
- the map displays only matching parcels in Foglio 13,
- clicking one green parcel shows the associated rights text.

Future improvement:

Create a precise table with:

~~~text
foglio, particella, rights, source_document, source_date
~~~

That would remove ambiguity from duplicated parcel numbers.

---

## 11. Debug and development history

This project went through several important iterations.

### 11.1 Wrong initial assumption about AdE vector access

Initial assumption:

- AdE only offered WMS raster tiles publicly.
- No public/free vector parcel access existed.

Correction:

- AdE provides WFS and bulk GML download under its open-data cadastral cartography services.
- The bulk GML ZIP was used because it is reproducible and avoids repeated WFS queries.

Lesson:

Use bulk GML as the authoritative working source for parcels instead of scraping/vectorizing WMS.

---

### 11.2 MapLibre cannot directly read GML

Problem:

- MapLibre cannot consume AdE GML directly.

Solution:

- Python converted GML to GeoJSON.
- Coordinates were transformed from GML axis order to GeoJSON axis order.

Lesson:

For a static GitHub Pages map, pre-convert to GeoJSON or vector tiles.

---

### 11.3 Coordinate-axis issue

Problem:

- AdE GML with `EPSG:6706` uses latitude/longitude axis order in `gml:posList`.
- GeoJSON requires longitude/latitude.

Symptoms if wrong:

- data appears in the wrong part of the world,
- bounds look like x=41, y=14 instead of x=14, y=41.

Solution:

- conversion logic checks and swaps axes when needed.

---

### 11.4 Parcel labels did not show

Problem:

- MapLibre text labels did not appear.

Causes:

- missing glyphs URL,
- label layer min zoom too high,
- label collision avoidance hiding dense labels.

Solution:

- add glyphs URL,
- reduce min zoom,
- use `text-allow-overlap` and `text-ignore-placement` for the target-only label layer.

---

### 11.5 Live AdE WMS failed in browser

Problem:

Direct AdE WMS in MapLibre failed with CORS errors:

~~~text
No Access-Control-Allow-Origin header
~~~

Also, AdE WMS documentation says it does not support EPSG:3857/Web Mercator.

Earlier erroneous request used:

~~~text
CRS=EPSG:3857
~~~

But AdE WMS supports CRS such as:

~~~text
EPSG:6706
EPSG:4258
EPSG:25832
EPSG:25833
EPSG:25834
EPSG:3044
EPSG:3045
EPSG:3046
~~~

Solution:

- do not request AdE WMS live from browser,
- generate a local image snapshot grid using Python,
- request AdE WMS in EPSG:4258 with correct WMS 1.3.0 axis order,
- serve the resulting PNG files locally through GitHub Pages.

---

### 11.6 WMS snapshot Python bug

Problem:

The first Python WMS download script checked:

~~~text
b"png" not in ctype
~~~

where `ctype` was a Python string, not bytes.

Error:

~~~text
'in <string>' requires string as left operand, not bytes
~~~

Fix:

~~~text
"png" not in ctype
~~~

Lesson:

WMS was likely returning PNG correctly; the local script had a type-check bug.

---

### 11.7 Parcel number duplicates

Problem:

Selecting parcels by parcel number alone matched many features:

- requested numbers: 117
- matched numbers: 117
- selected GeoJSON features: 349
- duplicate parcel-number hits: 100

Cause:

Parcel numbers are not unique without foglio.

Solution for current visualization:

- restrict label and Genova-family display to Foglio 13.

Required legal improvement:

- use `foglio + particella`, not just `particella`.

---

### 11.8 Satellite zoom problem

Problem:

At high zoom, Esri satellite showed:

~~~text
map data not yet available
~~~

or became blurry due to overzooming.

Explanation:

Commercial satellite tiles may not exist at every high zoom level for every place. Overzooming avoids missing tiles but does not add real resolution.

Solution:

- add official PCN/MASE Ortofoto 2012 WMS snapshot,
- use official 50 cm orthophoto imagery for a stable background.

---

### 11.9 Fragile find/replace patches

Problem:

Repeated HTML patches failed because earlier patches changed the structure of `index.html`.

Symptoms:

~~~text
Could not find panel end marker
Could not insert Genova layers before sheet labels
Could not insert Genova/PCN handlers
~~~

Solution:

- replace `docs/index.html` with a clean stable version,
- re-mark GeoJSON properties,
- keep layer logic explicit.

Guidance for future AI/developer:

If more large UI changes are needed, do not keep stacking fragile regex patches. Prefer regenerating or editing a clean structured `index.html`.

---

## 12. How to run locally

From the repository root:

~~~bash
python3 -m http.server 8000 --directory docs
~~~

Open:

~~~text
http://localhost:8000
~~~

If the browser shows stale behavior:

~~~text
Cmd + Shift + R
~~~

on macOS Chrome to hard-refresh.

Do not double-click `index.html` directly. Local file loading can break GeoJSON/image requests.

---

## 13. How to deploy to GitHub Pages

The repository should be configured as:

~~~text
Branch: main
Folder: /docs
~~~

Useful commands:

~~~bash
gh auth status

gh repo view

gh api "repos/$(gh api user --jq .login)/san-felice-del-molise-cadastral-map/pages" --jq '{html_url, status, source}'
~~~

If needed, enable Pages:

~~~bash
GH_OWNER="$(gh api user --jq .login)"
REPO_NAME="san-felice-del-molise-cadastral-map"

gh api \
  -X POST \
  "repos/$GH_OWNER/$REPO_NAME/pages" \
  -f "source[branch]=main" \
  -f "source[path]=/docs"
~~~

If Pages already exists, update instead:

~~~bash
gh api \
  -X PUT \
  "repos/$GH_OWNER/$REPO_NAME/pages" \
  -f "source[branch]=main" \
  -f "source[path]=/docs"
~~~

---

## 14. Local source/workspace used during development

Original local working path:

~~~text
/Users/Renlong/Documents/Visura Catasto Catastale_Cecilie Genova/informatico/Home-Schede informative e servizi-Fabbricati e terreni-Consultazione cartografia catastale-Accedi al servizio/MOLISE/CB/H833_SAN FELICE DEL MOLISE
~~~

Published/copy destination:

~~~text
/Users/Renlong/Projects/GitHub/YIN-Renlong/san-felice-del-molise-cadastral-map
~~~

Recommended workflow:

- keep the original folder as the working/evidence folder,
- publish only the clean static site in this GitHub repo,
- do not publish `_patch_backups`.

---

## 15. Rebuild notes

### 15.1 Initial GML conversion

The initial Python script is:

~~~text
scripts/mvp_ade_gml_map.py
~~~

Original use pattern:

~~~bash
python3 mvp_ade_gml_map.py \
  --ple "/path/to/H833_SAN FELICE DEL MOLISE_ple.gml" \
  --map "/path/to/H833_SAN FELICE DEL MOLISE_map.gml" \
  --out mvp_site
~~~

Then the generated `mvp_site/` was copied to:

~~~text
docs/
~~~

Important:

The current `docs/index.html` contains later custom UI and should not be blindly overwritten by the initial MVP generator.

---

### 15.2 Local WMS snapshots

AdE WMS and PCN orthophoto are not used live in-browser. They are converted to local image grids.

The manifest pattern is:

~~~json
{
  "type": "...",
  "tiles": [
    {
      "url": "data/.../tile_0000.png",
      "coordinates": [
        [west, north],
        [east, north],
        [east, south],
        [west, south]
      ]
    }
  ]
}
~~~

MapLibre loads each tile as an `image` source.

---

## 16. Legal and technical limitations

This project is a visualization aid.

Important limitations:

1. Italian cadastral cartography has positional limits.
   AdE metadata indicates typical absolute positional accuracy around 2 m for much cadastral mapping.

2. Cadastral parcels are not automatically definitive legal boundaries.
   Legal boundary determination may require deeds, survey monuments, historical cadastral maps, professional surveyor analysis, or court-appointed expert review.

3. Parcel matching by number alone is ambiguous.
   Use `foglio + particella` for final legal work.

4. Orthophoto imagery is not cadastral evidence.
   It is context only.

5. The Genova family rights list is user-provided annotation.
   It must be verified against official cadastral/registry documents before legal use.

6. If this repository is public, the parcel/right annotations are public.
   Consider privacy and legal strategy before publishing sensitive ownership information.

---

## 17. Recommended next technical steps

### 17.1 Convert Genova rights to explicit foglio+particella table

Current state:

~~~text
particella -> rights
~~~

Recommended future state:

~~~text
foglio, particella, rights, source_document, source_date, notes
~~~

Example:

~~~text
13,594,Proprietà 1/1,visura/example.pdf,2026-06-30,...
~~~

This will eliminate ambiguity.

---

### 17.2 Add municipal project overlay

For the broader dispute, the next major layer should be the municipality project footprint.

Best source:

- DWG
- DXF
- SHP
- GeoPackage
- GML
- official georeferenced PDF

Avoid relying only on screenshots or non-georeferenced PDFs.

If only PDF is available:

1. rasterize PDF,
2. georeference with GCPs,
3. create local raster tiles,
4. digitize/extract project footprint as vector if possible,
5. compute intersections in a metric CRS.

---

### 17.3 Compute overlap areas

Do not compute legal areas in:

~~~text
EPSG:4326
EPSG:3857
~~~

For Molise, use an appropriate metric CRS, for example:

~~~text
EPSG:6708
RDN2008 / UTM zone 33N
~~~

Suggested Python libraries:

- GeoPandas
- Shapely
- PyProj
- Rasterio/GDAL for rasters

---

## 18. Notes for another AI/developer

If another AI continues this project, preserve these behavioral requirements:

1. Do not remove the bottom legend section:

~~~text
Terreni famiglia Genova — Foglio 13
~~~

2. Do not remove the checkbox:

~~~text
Mostra terreni famiglia Genova
~~~

3. Do not restore generic parcel popups.
   Clicking a green Genova parcel should update the side card, not open a popup.

4. Do not color all target parcels red.
   Earlier red selection was unwanted.

5. Genova family land should be green/gold style.

6. Target parcel labels should be restricted to:

~~~text
Foglio 13
~~~

7. Do not use live AdE WMS directly in the browser.
   It fails because of CORS and CRS/projection limitations.

8. Use local snapshots for WMS/orthophoto layers.

9. If regex patching fails, regenerate a clean `docs/index.html` instead of stacking fragile partial patches.

10. Keep the map focused around:

~~~text
lon 14.70308095
lat 41.89005547
zoom 18.0
~~~

11. For final legal evidence, replace parcel-number-only matching with explicit `foglio + particella` matching.

---

## 19. Attribution draft

When presenting or publishing the map, include attribution similar to:

~~~text
Cadastral cartography: Agenzia delle Entrate, Cartografia catastale, CC BY 4.0.
Orthophoto where shown: Geoportale Nazionale / MASE / PCN, Ortofoto a colori anno 2012.
Basemap where shown: OpenStreetMap contributors and/or Esri World Imagery.
~~~

Also state that the Genova family rights annotation is a user-provided interpretive layer and should be verified against official documents.

---

## 20. Summary

This repository demonstrates a code-first cadastral visualization pipeline:

~~~text
Official AdE cadastral GML
        ->
Python conversion to GeoJSON
        ->
MapLibre static web map
        ->
GitHub Pages publication
        ->
Optional local official WMS/orthophoto image overlays
~~~

The current map is focused on Foglio 13 in San Felice del Molise and highlights Genova family-related parcels in green for visual review.

For legal-grade conclusions, further work should use official project vector data, explicit foglio+particella ownership tables, metric CRS intersection calculations, and professional survey validation.

---

## 21. AI prompt usage

For AI handoff, do **not** include the full generated GeoJSON parcel files by default.

Large generated files currently include:

~~~text
docs/data/parcels.geojson
docs/data/genova_family_parcels.geojson
~~~

They remain necessary for the web map, but they are inefficient for AI prompts because they mostly contain coordinate arrays.

Instead, use:

~~~text
README.md
AI_DATA_SUMMARY.md
docs/index.html
scripts/
docs/data/*manifest.json
~~~

A helper script is provided:

~~~bash
scripts/make_ai_prompt.sh
~~~

It creates:

~~~text
ai_prompt_bundle.xml
~~~

and excludes large generated geometry and raster tile files.

If exact geometry debugging is needed, extract only the specific parcel feature, for example Foglio 13 / Particella 594, rather than sending the entire `parcels.geojson`.
