#!/usr/bin/env python3

import argparse
import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET


ITALY_LAT = (35.0, 48.5)
ITALY_LON = (5.0, 20.0)


def local_name(tag):
    """Strip XML namespace."""
    if tag is None:
        return ""
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    if ":" in tag:
        return tag.rsplit(":", 1)[1]
    return tag


def first_text(elem, wanted_name):
    """Find first descendant text by local tag name."""
    for e in elem.iter():
        if local_name(e.tag) == wanted_name and e.text and e.text.strip():
            return e.text.strip()
    return None


def first_elem(elem, wanted_name):
    for e in elem.iter():
        if local_name(e.tag) == wanted_name:
            return e
    return None


def get_gml_id(elem):
    for k, v in elem.attrib.items():
        if local_name(k) == "id":
            return v
    return None


def should_flip_axis(pairs):
    """
    Your AdE EPSG:6706 GML appears as latitude longitude.
    GeoJSON needs longitude latitude.

    This function detects whether pairs look like:
      41.9 14.6 -> lat lon -> flip
    or:
      14.6 41.9 -> lon lat -> do not flip
    """
    latlon_score = 0
    lonlat_score = 0

    for a, b in pairs[:30]:
        if ITALY_LAT[0] <= a <= ITALY_LAT[1] and ITALY_LON[0] <= b <= ITALY_LON[1]:
            latlon_score += 1
        if ITALY_LON[0] <= a <= ITALY_LON[1] and ITALY_LAT[0] <= b <= ITALY_LAT[1]:
            lonlat_score += 1

    # Default to flipping because EPSG:6706 GML commonly comes as lat/lon.
    return latlon_score >= lonlat_score


def parse_poslist(text):
    if not text:
        return []

    vals = [float(x) for x in text.replace("\n", " ").split()]
    pairs = []

    for i in range(0, len(vals) - 1, 2):
        pairs.append((vals[i], vals[i + 1]))

    flip = should_flip_axis(pairs)

    coords = []
    for a, b in pairs:
        if flip:
            # lat/lon -> lon/lat
            coords.append([b, a])
        else:
            # already lon/lat
            coords.append([a, b])

    # GeoJSON rings should be closed.
    if coords and coords[0] != coords[-1]:
        coords.append(coords[0])

    return coords


def ring_from_container(container):
    for e in container.iter():
        if local_name(e.tag) == "posList":
            return parse_poslist(e.text)
    return None


def parse_polygon(poly_elem):
    exterior = None
    interiors = []

    # Normal GML structure:
    # Polygon
    #   exterior
    #   interior
    #   interior
    for child in list(poly_elem):
        ln = local_name(child.tag)

        if ln == "exterior":
            exterior = ring_from_container(child)

        elif ln == "interior":
            ring = ring_from_container(child)
            if ring and len(ring) >= 4:
                interiors.append(ring)

    # Fallback if exterior was nested unusually.
    if exterior is None:
        for e in poly_elem.iter():
            if local_name(e.tag) == "exterior":
                exterior = ring_from_container(e)
                break

    if not exterior or len(exterior) < 4:
        return None

    return [exterior] + interiors


def geometry_from_feature(feature_elem):
    geom_elem = first_elem(feature_elem, "msGeometry")
    if geom_elem is None:
        return None

    polygons = []

    for e in geom_elem.iter():
        if local_name(e.tag) == "Polygon":
            rings = parse_polygon(e)
            if rings:
                polygons.append(rings)

    if not polygons:
        return None

    if len(polygons) == 1:
        return {
            "type": "Polygon",
            "coordinates": polygons[0],
        }

    return {
        "type": "MultiPolygon",
        "coordinates": polygons,
    }


def parse_gml(path, feature_kind):
    """
    feature_kind:
      parcel -> CP:CadastralParcel
      sheet  -> CP:CadastralZoning
    """
    path = Path(path)
    root = ET.parse(path).getroot()

    if feature_kind == "parcel":
        wanted_feature = "CadastralParcel"
    elif feature_kind == "sheet":
        wanted_feature = "CadastralZoning"
    else:
        raise ValueError(feature_kind)

    features = []

    for elem in root.iter():
        if local_name(elem.tag) != wanted_feature:
            continue

        geom = geometry_from_feature(elem)
        if geom is None:
            continue

        gml_id = get_gml_id(elem)

        if feature_kind == "parcel":
            label = first_text(elem, "LABEL")
            national_ref = first_text(elem, "NATIONALCADASTRALREFERENCE")

            props = {
                "kind": "parcel",
                "gml_id": gml_id,
                "label": label,
                "particella": label,
                "national_ref": national_ref,
                "NATIONALCADASTRALREFERENCE": national_ref,
            }

            if national_ref:
                # Example: H833_002400.10 -> H833_002400
                if "." in national_ref:
                    props["sheet_ref"] = national_ref.rsplit(".", 1)[0]
                else:
                    props["sheet_ref"] = None

                # Example: H833_002400.10 -> H833
                props["comune_code"] = national_ref.split("_", 1)[0]

        else:
            label = first_text(elem, "LABEL")
            zoning_ref = first_text(elem, "NATIONALCADASTRALZONINGREFERENCE")

            props = {
                "kind": "sheet",
                "gml_id": gml_id,
                "label": label,
                "foglio": label,
                "zoning_ref": zoning_ref,
                "NATIONALCADASTRALZONINGREFERENCE": zoning_ref,
                "ADMINISTRATIVEUNIT": first_text(elem, "ADMINISTRATIVEUNIT"),
                "LEVEL": first_text(elem, "LEVEL"),
                "LEVELNAME": first_text(elem, "LEVELNAME"),
            }

        features.append({
            "type": "Feature",
            "properties": props,
            "geometry": geom,
        })

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def add_sheet_labels_to_parcels(parcels_fc, sheets_fc):
    sheet_index = {}

    for f in sheets_fc["features"]:
        p = f["properties"]
        zoning_ref = p.get("zoning_ref")
        foglio = p.get("foglio")
        if zoning_ref:
            sheet_index[zoning_ref] = foglio

    for f in parcels_fc["features"]:
        p = f["properties"]
        sheet_ref = p.get("sheet_ref")
        p["foglio"] = sheet_index.get(sheet_ref)


def apply_targets(parcels_fc, targets_csv):
    """
    Optional CSV format:

    foglio,particella,role,notes
    1,10,private,test parcel
    24,5,private,another

    Or:

    national_ref,role,notes
    H833_002400.10,private,test parcel
    """
    for f in parcels_fc["features"]:
        f["properties"]["selected"] = False

    if not targets_csv:
        return 0, 0

    targets_csv = Path(targets_csv)

    rows = []
    with targets_csv.open("r", encoding="utf-8-sig", newline="") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            clean = {
                (k or "").strip().lower(): (v or "").strip()
                for k, v in row.items()
            }
            rows.append(clean)

    by_ref = {}
    by_foglio_particella = {}

    for row in rows:
        national_ref = row.get("national_ref") or row.get("nationalcadastalreference") or row.get("nationalcadastralreference")
        foglio = row.get("foglio")
        particella = row.get("particella")

        if national_ref:
            by_ref[national_ref] = row

        if foglio and particella:
            by_foglio_particella[(foglio, particella)] = row

    matched = 0

    for f in parcels_fc["features"]:
        p = f["properties"]

        national_ref = p.get("national_ref") or ""
        foglio = str(p.get("foglio") or "")
        particella = str(p.get("particella") or "")

        row = by_ref.get(national_ref) or by_foglio_particella.get((foglio, particella))

        if row:
            p["selected"] = True
            matched += 1

            # Copy useful target CSV columns into popup properties.
            for k, v in row.items():
                if k not in {"foglio", "particella", "national_ref"} and v:
                    p[k] = v

    return matched, len(rows)


def iter_coords(geom):
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            for xy in ring:
                yield xy

    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                for xy in ring:
                    yield xy


def fc_bounds(fc):
    xs = []
    ys = []

    for f in fc["features"]:
        for x, y in iter_coords(f["geometry"]):
            xs.append(x)
            ys.append(y)

    if not xs:
        return None

    return [min(xs), min(ys), max(xs), max(ys)]


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, separators=(",", ":"))


def write_html(out_dir, bounds, n_parcels, n_sheets, n_selected):
    out_dir = Path(out_dir)

    bounds_js = json.dumps([
        [bounds[0], bounds[1]],
        [bounds[2], bounds[3]],
    ])

    html = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AdE Catasto GML MVP</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link
    href="https://unpkg.com/maplibre-gl@5.9.0/dist/maplibre-gl.css"
    rel="stylesheet"
  >
  <script src="https://unpkg.com/maplibre-gl@5.9.0/dist/maplibre-gl.js"></script>

  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    #map {
      position: absolute;
      inset: 0;
    }

    #panel {
      position: absolute;
      z-index: 10;
      top: 12px;
      left: 12px;
      background: rgba(255,255,255,0.94);
      padding: 12px;
      border-radius: 10px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.25);
      max-width: 320px;
      font-size: 13px;
      line-height: 1.35;
    }

    #panel h2 {
      margin: 0 0 8px 0;
      font-size: 15px;
    }

    #panel label {
      display: block;
      margin: 5px 0;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      margin: 4px 0;
    }

    .swatch {
      width: 16px;
      height: 12px;
      border: 1px solid #333;
      display: inline-block;
    }

    .popup-table {
      border-collapse: collapse;
      font-size: 12px;
    }

    .popup-table td {
      border-bottom: 1px solid #ddd;
      padding: 2px 4px;
      vertical-align: top;
    }

    .popup-table td:first-child {
      font-weight: 700;
      white-space: nowrap;
    }
  </style>
</head>

<body>
  <div id="map"></div>

  <div id="panel">
    <h2>AdE Catasto GML MVP</h2>

    <div id="stats"></div>

    <hr>

    <label>
      <input id="chk-satellite" type="checkbox">
      Satellite basemap
    </label>

    <label>
      <input id="chk-parcels" type="checkbox" checked>
      Parcels / particelle
    </label>

    <label>
      <input id="chk-sheets" type="checkbox" checked>
      Sheets / fogli
    </label>

    <label>
      <input id="chk-labels" type="checkbox" checked>
      Target particella labels
    </label>

    <label>
      <input id="chk-wms" type="checkbox">
      AdE WMS comparison layer (local snapshot)
    </label>

    <button id="btn-focus-place" type="button" style="
      width: 100%;
      margin: 8px 0;
      padding: 7px 9px;
      border: 1px solid #999;
      border-radius: 7px;
      background: #fff;
      cursor: pointer;
      font-size: 13px;
    ">
      Go to focus area
    </button>

    <hr>

    <div class="legend-item">
      <span class="swatch" style="background: rgba(33,150,243,0.18); border-color: #1565c0;"></span>
      All parcels
    </div>

    <div class="legend-item">
      <span class="swatch" style="background: rgba(255,23,68,0.45); border-color: #b00020;"></span>
      Selected target parcels
    </div>

    <div class="legend-item">
      <span class="swatch" style="background: rgba(255,152,0,0.12); border-color: #ff9800;"></span>
      Fogli / map sheets
    </div>

    <p style="margin-bottom:0;">
      Click a parcel to inspect metadata.
    </p>
  </div>

  <script>
    const INITIAL_BOUNDS = __BOUNDS__;
    const N_PARCELS = __N_PARCELS__;
    const N_SHEETS = __N_SHEETS__;
    const N_SELECTED = __N_SELECTED__;

    // Focus/target label configuration: start
    // Google Earth URL location:
    // lat 41.89005547, lon 14.70308095
    const FOCUS_CENTER = [14.70308095, 41.89005547];
    const FOCUS_ZOOM = 17;

    // Only these particella numbers will be shown as parcel-number labels.
    const TARGET_LABEL_PARTICELLE = ["173", "383", "391", "555", "556", "557", "558", "559", "560", "561", "562", "563", "564", "565", "566", "567", "569", "570", "571", "572", "573", "575", "576", "580", "581", "582", "583", "584", "585", "586", "587", "591", "592", "594", "595", "597", "598", "600", "601", "604", "605", "606", "607", "611", "612", "613", "614", "616", "617", "619", "622", "623", "624", "625", "626", "627", "628", "635", "636", "637", "640", "641", "642", "650", "651", "669", "700", "701", "703", "707", "725", "726", "727", "736", "739", "790", "802", "834", "835", "836", "837", "838", "839", "840", "841", "842", "843", "844", "852", "853", "854", "855", "856", "857", "862", "887", "888", "889", "890", "891", "892", "893", "894", "895", "896", "925", "926", "927", "928", "929", "930", "931", "932", "934", "941", "947", "1007"];
    // Focus/target label configuration: end

    document.getElementById("stats").innerHTML =
      `<b>${N_PARCELS}</b> parcels<br>` +
      `<b>${N_SHEETS}</b> fogli / sheets<br>` +
      `<b>${N_SELECTED}</b> selected targets`;

    const center = [
      (INITIAL_BOUNDS[0][0] + INITIAL_BOUNDS[1][0]) / 2,
      (INITIAL_BOUNDS[0][1] + INITIAL_BOUNDS[1][1]) / 2,
    ];

    const map = new maplibregl.Map({
      container: "map",
      center,
      zoom: 13,
      style: {
        version: 8,

        // Required for text labels.
        glyphs: "https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",

        sources: {
          osm: {
            type: "raster",
            tiles: [
              "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            ],
            tileSize: 256,
            attribution: "© OpenStreetMap contributors"
          },

          satellite: {
            type: "raster",
            tiles: [
              "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            ],
            tileSize: 256,
            attribution: "Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community"
          }
        },

        layers: [
          {
            id: "satellite",
            type: "raster",
            source: "satellite",
            layout: {
              visibility: "none"
            }
          },
          {
            id: "osm",
            type: "raster",
            source: "osm"
          }
        ]
      }
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");
    map.addControl(new maplibregl.ScaleControl({ unit: "metric" }));

    function esc(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function popupHtml(props) {
      const preferred = [
        "foglio",
        "particella",
        "national_ref",
        "NATIONALCADASTRALREFERENCE",
        "sheet_ref",
        "comune_code",
        "selected",
        "role",
        "notes",
        "label",
        "gml_id"
      ];

      const used = new Set();
      const rows = [];

      for (const k of preferred) {
        if (props[k] !== undefined && props[k] !== null && props[k] !== "") {
          used.add(k);
          rows.push(`<tr><td>${esc(k)}</td><td>${esc(props[k])}</td></tr>`);
        }
      }

      for (const k of Object.keys(props).sort()) {
        if (!used.has(k)) {
          rows.push(`<tr><td>${esc(k)}</td><td>${esc(props[k])}</td></tr>`);
        }
      }

      const title = props.foglio && props.particella
        ? `Foglio ${esc(props.foglio)} - Particella ${esc(props.particella)}`
        : "Cadastral parcel";

      return `
        <div>
          <b>${title}</b>
          <table class="popup-table">${rows.join("")}</table>
        </div>
      `;
    }

    function setVis(layerIds, visible) {
      for (const id of layerIds) {
        if (map.getLayer(id)) {
          map.setLayoutProperty(id, "visibility", visible ? "visible" : "none");
        }
      }
    }

    map.on("load", () => {
      // Local static AdE WMS comparison snapshot.
      // Why not live WMS?
      // 1) AdE WMS does not send browser CORS headers.
      // 2) AdE WMS does not support EPSG:3857/WebMercator.
      // This local snapshot is generated into:
      //   data/ade_wms_manifest.json
      let adeWmsComparisonLoaded = false;
      const adeWmsComparisonLayerIds = [];

      async function ensureAdeWmsComparisonLoaded() {
        if (adeWmsComparisonLoaded) {
          return true;
        }

        let manifest;

        try {
          const response = await fetch("data/ade_wms_manifest.json", {
            cache: "no-cache"
          });

          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }

          manifest = await response.json();
        } catch (err) {
          console.error("Could not load local AdE WMS manifest:", err);
          alert(
            "Local AdE WMS snapshot not found or unreadable. " +
            "Re-run the WMS download patch from the project folder."
          );
          return false;
        }

        const tiles = manifest.tiles || [];

        if (!tiles.length) {
          alert("Local AdE WMS manifest contains no tiles.");
          return false;
        }

        for (let i = 0; i < tiles.length; i++) {
          const tile = tiles[i];
          const sourceId = `ade-wms-local-${i}`;
          const layerId = `ade-wms-local-${i}`;

          if (!map.getSource(sourceId)) {
            map.addSource(sourceId, {
              type: "image",
              url: tile.url,
              coordinates: tile.coordinates
            });
          }

          if (!map.getLayer(layerId)) {
            const layerDef = {
              id: layerId,
              type: "raster",
              source: sourceId,
              layout: {
                visibility: "none"
              },
              paint: {
                "raster-opacity": 0.58
              }
            };

            // Put WMS snapshot above basemap but below vector parcel lines.
            const beforeId = map.getLayer("sheets-fill") ? "sheets-fill" : undefined;

            if (beforeId) {
              map.addLayer(layerDef, beforeId);
            } else {
              map.addLayer(layerDef);
            }

            adeWmsComparisonLayerIds.push(layerId);
          }
        }

        adeWmsComparisonLoaded = true;
        console.log(
          `Loaded local AdE WMS snapshot: ${adeWmsComparisonLayerIds.length} image tiles`
        );

        return true;
      }

      function setAdeWmsComparisonVisible(visible) {
        for (const layerId of adeWmsComparisonLayerIds) {
          if (map.getLayer(layerId)) {
            map.setLayoutProperty(
              layerId,
              "visibility",
              visible ? "visible" : "none"
            );
          }
        }
      }

      map.addSource("sheets", {
        type: "geojson",
        data: "data/sheets.geojson"
      });

      map.addSource("parcels", {
        type: "geojson",
        data: "data/parcels.geojson"
      });

      map.addLayer({
        id: "sheets-fill",
        type: "fill",
        source: "sheets",
        paint: {
          "fill-color": "#ff9800",
          "fill-opacity": 0.08
        }
      });

      map.addLayer({
        id: "sheets-line",
        type: "line",
        source: "sheets",
        paint: {
          "line-color": "#ff9800",
          "line-width": 2.5
        }
      });

      map.addLayer({
        id: "parcels-fill",
        type: "fill",
        source: "parcels",
        paint: {
          "fill-color": "#2196f3",
          "fill-opacity": 0.10
        }
      });

      map.addLayer({
        id: "parcels-line",
        type: "line",
        source: "parcels",
        paint: {
          "line-color": "#1565c0",
          "line-width": 0.7
        }
      });

      map.addLayer({
        id: "selected-fill",
        type: "fill",
        source: "parcels",
        filter: ["==", ["get", "selected"], true],
        paint: {
          "fill-color": "#ff1744",
          "fill-opacity": 0.45
        }
      });

      map.addLayer({
        id: "selected-line",
        type: "line",
        source: "parcels",
        filter: ["==", ["get", "selected"], true],
        paint: {
          "line-color": "#b00020",
          "line-width": 3
        }
      });

      map.addLayer({
        id: "sheet-labels",
        type: "symbol",
        source: "sheets",
        minzoom: 11,
        layout: {
          "text-field": ["concat", "Foglio ", ["coalesce", ["get", "foglio"], ""]],
          "text-size": 14,
          "text-font": ["Noto Sans Regular"],
          "text-allow-overlap": false
        },
        paint: {
          "text-color": "#e65100",
          "text-halo-color": "#ffffff",
          "text-halo-width": 2
        }
      });

      map.addLayer({
        id: "parcel-labels",
        type: "symbol",
        source: "parcels",
        minzoom: 14,
        filter: [
          "in",
          ["to-string", ["coalesce", ["get", "particella"], ["get", "label"], ""]],
          ["literal", TARGET_LABEL_PARTICELLE]
        ],
        layout: {
          "text-field": ["to-string", ["coalesce", ["get", "particella"], ["get", "label"], ""]],
          "text-size": [
            "interpolate",
            ["linear"],
            ["zoom"],
            14, 10,
            16, 12,
            18, 15,
            20, 18
          ],
          "text-font": ["Noto Sans Regular"],

          // We intentionally show only the requested target numbers.
          "text-allow-overlap": true,
          "text-ignore-placement": true
        },
        paint: {
          "text-color": "#111111",
          "text-halo-color": "#ffffff",
          "text-halo-width": 2.0
        }
      });
      // Start directly at requested focus location.
      map.jumpTo({ center: FOCUS_CENTER, zoom: FOCUS_ZOOM });

      map.on("click", (e) => {
        const features = map.queryRenderedFeatures(e.point, {
          layers: ["selected-fill", "parcels-fill"]
        });

        if (!features.length) return;

        const feature = features[0];

        new maplibregl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(popupHtml(feature.properties))
          .addTo(map);
      });

      map.on("mousemove", (e) => {
        const features = map.queryRenderedFeatures(e.point, {
          layers: ["selected-fill", "parcels-fill"]
        });

        map.getCanvas().style.cursor = features.length ? "pointer" : "";
      });

      document.getElementById("chk-satellite").addEventListener("change", (e) => {
        if (e.target.checked) {
          map.setLayoutProperty("satellite", "visibility", "visible");
          map.setLayoutProperty("osm", "visibility", "none");
        } else {
          map.setLayoutProperty("satellite", "visibility", "none");
          map.setLayoutProperty("osm", "visibility", "visible");
        }
      });

      const focusPlaceButton = document.getElementById("btn-focus-place");
      if (focusPlaceButton) {
        focusPlaceButton.addEventListener("click", () => {
          map.flyTo({
            center: FOCUS_CENTER,
            zoom: FOCUS_ZOOM,
            duration: 650
          });
        });
      }

      document.getElementById("chk-parcels").addEventListener("change", (e) => {
        setVis(
          ["parcels-fill", "parcels-line", "selected-fill", "selected-line"],
          e.target.checked
        );
      });

      document.getElementById("chk-sheets").addEventListener("change", (e) => {
        setVis(["sheets-fill", "sheets-line"], e.target.checked);
      });

            document.getElementById("chk-labels").addEventListener("change", (e) => {
        setVis(["parcel-labels"], e.target.checked);
      });

      document.getElementById("chk-wms").addEventListener("change", async (e) => {
        if (e.target.checked) {
          const ok = await ensureAdeWmsComparisonLoaded();

          if (!ok) {
            e.target.checked = false;
            return;
          }

          setAdeWmsComparisonVisible(true);
        } else {
          setAdeWmsComparisonVisible(false);
        }
      });
    });
  </script>
</body>
</html>
"""

    html = html.replace("__BOUNDS__", bounds_js)
    html = html.replace("__N_PARCELS__", str(n_parcels))
    html = html.replace("__N_SHEETS__", str(n_sheets))
    html = html.replace("__N_SELECTED__", str(n_selected))

    (out_dir / "index.html").write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ple", required=True, help="Path to *_ple.gml")
    parser.add_argument("--map", required=True, help="Path to *_map.gml")
    parser.add_argument("--out", default="mvp_site", help="Output folder")
    parser.add_argument("--targets", help="Optional CSV of parcels to highlight")
    parser.add_argument(
        "--only-targets",
        action="store_true",
        help="Export/show only selected target parcels. Requires --targets."
    )

    args = parser.parse_args()

    out_dir = Path(args.out)
    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Reading sheets/fogli GML...")
    sheets_fc = parse_gml(args.map, "sheet")

    print("Reading parcels/particelle GML...")
    parcels_fc = parse_gml(args.ple, "parcel")

    print("Joining parcel sheet_ref -> foglio label...")
    add_sheet_labels_to_parcels(parcels_fc, sheets_fc)

    matched, total_targets = apply_targets(parcels_fc, args.targets)

    if args.only_targets:
        if not args.targets:
            raise SystemExit("--only-targets requires --targets")
        parcels_fc["features"] = [
            f for f in parcels_fc["features"]
            if f["properties"].get("selected") is True
        ]

    if not parcels_fc["features"]:
        raise SystemExit("No parcel features found/exported.")

    bounds = fc_bounds(parcels_fc)
    if bounds is None:
        bounds = fc_bounds(sheets_fc)

    if bounds is None:
        raise SystemExit("Could not compute bounds.")

    write_json(data_dir / "parcels.geojson", parcels_fc)
    write_json(data_dir / "sheets.geojson", sheets_fc)

    n_parcels = len(parcels_fc["features"])
    n_sheets = len(sheets_fc["features"])
    n_selected = sum(
        1 for f in parcels_fc["features"]
        if f["properties"].get("selected") is True
    )

    write_html(out_dir, bounds, n_parcels, n_sheets, n_selected)

    print()
    print("Done.")
    print(f"Sheets:   {n_sheets}")
    print(f"Parcels:  {n_parcels}")
    print(f"Selected: {n_selected}")

    if args.targets:
        print(f"Targets matched: {matched} / {total_targets}")

    print()
    print("Open the MVP map with:")
    print(f"  cd {out_dir}")
    print("  python3 -m http.server 8000")
    print()
    print("Then open:")
    print("  http://localhost:8000")
    print()
    print("If the map appears in the wrong place, inspect data/parcels.geojson.")
    print("Coordinates should look like [14.x, 41.x], not [41.x, 14.x].")


if __name__ == "__main__":
    main()