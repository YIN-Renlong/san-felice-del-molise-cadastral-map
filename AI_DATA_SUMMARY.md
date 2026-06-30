# AI Data Summary

This file is generated to help AI tools understand the repository without loading large generated GeoJSON or raster tile files.

The full geometry files remain in the repository for the web map, but should normally be excluded from `files-to-prompt`.

Generated data files intentionally summarized here include:

- `docs/data/parcels.geojson`
- `docs/data/genova_family_parcels.geojson`
- `docs/data/sheets.geojson`
- `docs/data/target_parcels.geojson`
- local WMS/orthophoto manifests

Important: this summary omits full coordinate arrays. It includes schemas, counts, sample properties, bounding boxes, and geometry types.

## Why large data files are excluded from AI prompts

The large GeoJSON files are generated data. They contain thousands of coordinate pairs and consume many tokens, but usually add little value for code review or architectural reasoning.

For most AI handoff/debugging tasks, include:

- `README.md`
- `AI_DATA_SUMMARY.md`
- `docs/index.html`
- `scripts/`

Only include full GeoJSON if debugging exact geometry or a specific coordinate issue.

## GeoJSON file summaries

### `docs/data/parcels.geojson`

- Size: `6.339 MB`
- Feature count: `8329`
- Genova family true count: `1337`
- Selected true count: `0`

Geometry types:

~~~json
{
  "Polygon": 8329
}
~~~

Collection bbox, lon/lat:

~~~json
{
  "west": 14.66367133,
  "south": 41.85956499,
  "east": 14.74040655,
  "north": 41.92800981
}
~~~

Property keys:

~~~text
NATIONALCADASTRALREFERENCE
comune_code
foglio
genova_family
genova_particella
genova_rights
gml_id
kind
label
national_ref
particella
selected
sheet_ref
~~~

Property key counts:

~~~json
{
  "NATIONALCADASTRALREFERENCE": 8329,
  "comune_code": 8329,
  "foglio": 8329,
  "genova_family": 8329,
  "genova_particella": 1337,
  "genova_rights": 1337,
  "gml_id": 8329,
  "kind": 8329,
  "label": 8329,
  "national_ref": 8329,
  "particella": 8329,
  "selected": 8329,
  "sheet_ref": 8329
}
~~~

Top foglio counts:

~~~text
10: 829
14: 642
12: 567
13A: 547
24: 478
16: 455
9: 417
7: 369
17: 335
5: 334
13: 328
23: 291
15: 288
4: 288
20: 276
18: 271
19: 245
11: 238
21: 195
22: 182
~~~

Property value examples:

~~~json
{
  "NATIONALCADASTRALREFERENCE": [
    "H833_000100.1",
    "H833_002400.1",
    "H833_002300.1",
    "H833_002200.1",
    "H833_002100.1",
    "H833_001900.1",
    "H833_001800.1",
    "H833_001600.1"
  ],
  "comune_code": [
    "H833"
  ],
  "foglio": [
    "1",
    "24",
    "23",
    "22",
    "21",
    "19",
    "18",
    "16"
  ],
  "genova_family": [
    "False",
    "True"
  ],
  "genova_particella": [
    "103",
    "107",
    "11",
    "111",
    "115",
    "12",
    "13",
    "130"
  ],
  "genova_rights": [
    "Proprietà 1/1",
    "Proprietà 1/3 e Proprietà 2/3 (Totale 100%)",
    "Nuda Proprietà e Usufrutto 1/1",
    "Comproprietà / Proprietà 1/1 (diritti diversi su fogli catastali diversi)",
    "Nuda Proprietà e Usufrutto 1/1 / Proprietà 1/1 (diritti diversi su fogli cata...",
    "Proprietà 1/3 e Proprietà 2/3 (Totale 100%) / Proprietà 1/1 (diritti diversi ...",
    "Comproprietà",
    "Proprietà 1/1 (Fabbricato)"
  ],
  "gml_id": [
    "CadastralParcel.IT.AGE.PLA.H833_000100.1",
    "CadastralParcel.IT.AGE.PLA.H833_002400.1",
    "CadastralParcel.IT.AGE.PLA.H833_002300.1",
    "CadastralParcel.IT.AGE.PLA.H833_002200.1",
    "CadastralParcel.IT.AGE.PLA.H833_002100.1",
    "CadastralParcel.IT.AGE.PLA.H833_001900.1",
    "CadastralParcel.IT.AGE.PLA.H833_001800.1",
    "CadastralParcel.IT.AGE.PLA.H833_001600.1"
  ],
  "kind": [
    "parcel"
  ],
  "label": [
    "1",
    "10",
    "100",
    "1007",
    "1008",
    "101",
    "102",
    "103"
  ],
  "national_ref": [
    "H833_000100.1",
    "H833_002400.1",
    "H833_002300.1",
    "H833_002200.1",
    "H833_002100.1",
    "H833_001900.1",
    "H833_001800.1",
    "H833_001600.1"
  ],
  "particella": [
    "1",
    "10",
    "100",
    "1007",
    "1008",
    "101",
    "102",
    "103"
  ],
  "selected": [
    "False"
  ],
  "sheet_ref": [
    "H833_000100",
    "H833_002400",
    "H833_002300",
    "H833_002200",
    "H833_002100",
    "H833_001900",
    "H833_001800",
    "H833_001600"
  ]
}
~~~

Sample features with geometry omitted:

~~~json
[
  {
    "sample_label": "Foglio 13, particella 594 if present",
    "feature_id": "H833_001300.594",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.70286962,
      "south": 41.88959001,
      "east": 14.70366481,
      "north": 41.89030798
    },
    "properties": {
      "foglio": "13",
      "particella": "594",
      "label": "594",
      "national_ref": "H833_001300.594",
      "NATIONALCADASTRALREFERENCE": "H833_001300.594",
      "sheet_ref": "H833_001300",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_001300.594",
      "genova_family": true,
      "genova_rights": "Proprietà 1/1",
      "genova_particella": "594",
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  },
  {
    "sample_label": "First Genova family feature in Foglio 13",
    "feature_id": "H833_001300.11",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.6990813,
      "south": 41.89215629,
      "east": 14.69935054,
      "north": 41.89282065
    },
    "properties": {
      "foglio": "13",
      "particella": "11",
      "label": "11",
      "national_ref": "H833_001300.11",
      "NATIONALCADASTRALREFERENCE": "H833_001300.11",
      "sheet_ref": "H833_001300",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_001300.11",
      "genova_family": true,
      "genova_rights": "Proprietà 1/1",
      "genova_particella": "11",
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  },
  {
    "sample_label": "First Foglio 13 feature",
    "feature_id": "H833_001300.10",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.69895912,
      "south": 41.89219239,
      "east": 14.69915861,
      "north": 41.89267036
    },
    "properties": {
      "foglio": "13",
      "particella": "10",
      "label": "10",
      "national_ref": "H833_001300.10",
      "NATIONALCADASTRALREFERENCE": "H833_001300.10",
      "sheet_ref": "H833_001300",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_001300.10",
      "genova_family": false,
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  },
  {
    "sample_label": "First feature in file",
    "feature_id": "H833_000100.1",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.6748392,
      "south": 41.92027499,
      "east": 14.6759861,
      "north": 41.92096391
    },
    "properties": {
      "foglio": "1",
      "particella": "1",
      "label": "1",
      "national_ref": "H833_000100.1",
      "NATIONALCADASTRALREFERENCE": "H833_000100.1",
      "sheet_ref": "H833_000100",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_000100.1",
      "genova_family": false,
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  }
]
~~~

### `docs/data/genova_family_parcels.geojson`

- Size: `1.036 MB`
- Feature count: `1337`
- Genova family true count: `1337`
- Selected true count: `0`

Geometry types:

~~~json
{
  "Polygon": 1337
}
~~~

Collection bbox, lon/lat:

~~~json
{
  "west": 14.66543248,
  "south": 41.86055311,
  "east": 14.73997447,
  "north": 41.92767335
}
~~~

Property keys:

~~~text
NATIONALCADASTRALREFERENCE
comune_code
foglio
genova_family
genova_particella
genova_rights
gml_id
kind
label
national_ref
particella
selected
sheet_ref
~~~

Property key counts:

~~~json
{
  "NATIONALCADASTRALREFERENCE": 1337,
  "comune_code": 1337,
  "foglio": 1337,
  "genova_family": 1337,
  "genova_particella": 1337,
  "genova_rights": 1337,
  "gml_id": 1337,
  "kind": 1337,
  "label": 1337,
  "national_ref": 1337,
  "particella": 1337,
  "selected": 1337,
  "sheet_ref": 1337
}
~~~

Top foglio counts:

~~~text
10: 106
14: 78
12: 74
16: 67
9: 63
7: 63
17: 62
5: 60
18: 58
11: 58
24: 57
23: 57
13A: 52
21: 49
20: 49
4: 49
1: 46
22: 46
19: 46
15: 45
~~~

Property value examples:

~~~json
{
  "NATIONALCADASTRALREFERENCE": [
    "H833_000100.103",
    "H833_002400.103",
    "H833_002300.103",
    "H833_002200.103",
    "H833_002100.103",
    "H833_002000.103",
    "H833_001900.103",
    "H833_001800.103"
  ],
  "comune_code": [
    "H833"
  ],
  "foglio": [
    "1",
    "24",
    "23",
    "22",
    "21",
    "20",
    "19",
    "18"
  ],
  "genova_family": [
    "True"
  ],
  "genova_particella": [
    "103",
    "107",
    "11",
    "111",
    "115",
    "12",
    "13",
    "130"
  ],
  "genova_rights": [
    "Proprietà 1/1",
    "Proprietà 1/3 e Proprietà 2/3 (Totale 100%)",
    "Nuda Proprietà e Usufrutto 1/1",
    "Comproprietà / Proprietà 1/1 (diritti diversi su fogli catastali diversi)",
    "Nuda Proprietà e Usufrutto 1/1 / Proprietà 1/1 (diritti diversi su fogli cata...",
    "Proprietà 1/3 e Proprietà 2/3 (Totale 100%) / Proprietà 1/1 (diritti diversi ...",
    "Comproprietà",
    "Proprietà 1/1 (Fabbricato)"
  ],
  "gml_id": [
    "CadastralParcel.IT.AGE.PLA.H833_000100.103",
    "CadastralParcel.IT.AGE.PLA.H833_002400.103",
    "CadastralParcel.IT.AGE.PLA.H833_002300.103",
    "CadastralParcel.IT.AGE.PLA.H833_002200.103",
    "CadastralParcel.IT.AGE.PLA.H833_002100.103",
    "CadastralParcel.IT.AGE.PLA.H833_002000.103",
    "CadastralParcel.IT.AGE.PLA.H833_001900.103",
    "CadastralParcel.IT.AGE.PLA.H833_001800.103"
  ],
  "kind": [
    "parcel"
  ],
  "label": [
    "103",
    "107",
    "11",
    "111",
    "115",
    "12",
    "13",
    "130"
  ],
  "national_ref": [
    "H833_000100.103",
    "H833_002400.103",
    "H833_002300.103",
    "H833_002200.103",
    "H833_002100.103",
    "H833_002000.103",
    "H833_001900.103",
    "H833_001800.103"
  ],
  "particella": [
    "103",
    "107",
    "11",
    "111",
    "115",
    "12",
    "13",
    "130"
  ],
  "selected": [
    "False"
  ],
  "sheet_ref": [
    "H833_000100",
    "H833_002400",
    "H833_002300",
    "H833_002200",
    "H833_002100",
    "H833_002000",
    "H833_001900",
    "H833_001800"
  ]
}
~~~

Sample features with geometry omitted:

~~~json
[
  {
    "sample_label": "Foglio 13, particella 594 if present",
    "feature_id": "H833_001300.594",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.70286962,
      "south": 41.88959001,
      "east": 14.70366481,
      "north": 41.89030798
    },
    "properties": {
      "foglio": "13",
      "particella": "594",
      "label": "594",
      "national_ref": "H833_001300.594",
      "NATIONALCADASTRALREFERENCE": "H833_001300.594",
      "sheet_ref": "H833_001300",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_001300.594",
      "genova_family": true,
      "genova_rights": "Proprietà 1/1",
      "genova_particella": "594",
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  },
  {
    "sample_label": "First Genova family feature in Foglio 13",
    "feature_id": "H833_001300.11",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.6990813,
      "south": 41.89215629,
      "east": 14.69935054,
      "north": 41.89282065
    },
    "properties": {
      "foglio": "13",
      "particella": "11",
      "label": "11",
      "national_ref": "H833_001300.11",
      "NATIONALCADASTRALREFERENCE": "H833_001300.11",
      "sheet_ref": "H833_001300",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_001300.11",
      "genova_family": true,
      "genova_rights": "Proprietà 1/1",
      "genova_particella": "11",
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  },
  {
    "sample_label": "First feature in file",
    "feature_id": "H833_000100.103",
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.66952987,
      "south": 41.91493992,
      "east": 14.67271446,
      "north": 41.91596262
    },
    "properties": {
      "foglio": "1",
      "particella": "103",
      "label": "103",
      "national_ref": "H833_000100.103",
      "NATIONALCADASTRALREFERENCE": "H833_000100.103",
      "sheet_ref": "H833_000100",
      "gml_id": "CadastralParcel.IT.AGE.PLA.H833_000100.103",
      "genova_family": true,
      "genova_rights": "Proprietà 1/1",
      "genova_particella": "103",
      "selected": false,
      "kind": "parcel",
      "comune_code": "H833"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  }
]
~~~

### `docs/data/sheets.geojson`

- Size: `0.249 MB`
- Feature count: `26`
- Genova family true count: `0`
- Selected true count: `0`

Geometry types:

~~~json
{
  "Polygon": 26
}
~~~

Collection bbox, lon/lat:

~~~json
{
  "west": 14.66367133,
  "south": 41.85956499,
  "east": 14.74040655,
  "north": 41.92800981
}
~~~

Property keys:

~~~text
ADMINISTRATIVEUNIT
LEVEL
LEVELNAME
NATIONALCADASTRALZONINGREFERENCE
foglio
gml_id
kind
label
zoning_ref
~~~

Property key counts:

~~~json
{
  "ADMINISTRATIVEUNIT": 26,
  "LEVEL": 26,
  "LEVELNAME": 26,
  "NATIONALCADASTRALZONINGREFERENCE": 26,
  "foglio": 26,
  "gml_id": 26,
  "kind": 26,
  "label": 26,
  "zoning_ref": 26
}
~~~

Top foglio counts:

~~~text
1: 1
2: 1
3: 1
4: 1
5: 1
6: 1
7: 1
8: 1
9: 1
10: 1
11: 1
12: 1
13: 1
13A: 1
14B: 1
14: 1
15: 1
16: 1
17: 1
18: 1
~~~

Property value examples:

~~~json
{
  "ADMINISTRATIVEUNIT": [
    "H833"
  ],
  "LEVEL": [
    "3rdOrder"
  ],
  "LEVELNAME": [
    "Mappa Catastale"
  ],
  "NATIONALCADASTRALZONINGREFERENCE": [
    "H833_000100",
    "H833_000200",
    "H833_000300",
    "H833_000400",
    "H833_000500",
    "H833_000600",
    "H833_000700",
    "H833_000800"
  ],
  "foglio": [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8"
  ],
  "gml_id": [
    "CadastralZoning.IT.AGE.MAP.H833_000100",
    "CadastralZoning.IT.AGE.MAP.H833_000200",
    "CadastralZoning.IT.AGE.MAP.H833_000300",
    "CadastralZoning.IT.AGE.MAP.H833_000400",
    "CadastralZoning.IT.AGE.MAP.H833_000500",
    "CadastralZoning.IT.AGE.MAP.H833_000600",
    "CadastralZoning.IT.AGE.MAP.H833_000700",
    "CadastralZoning.IT.AGE.MAP.H833_000800"
  ],
  "kind": [
    "sheet"
  ],
  "label": [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8"
  ],
  "zoning_ref": [
    "H833_000100",
    "H833_000200",
    "H833_000300",
    "H833_000400",
    "H833_000500",
    "H833_000600",
    "H833_000700",
    "H833_000800"
  ]
}
~~~

Sample features with geometry omitted:

~~~json
[
  {
    "sample_label": "First Foglio 13 feature",
    "feature_id": null,
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.69650225,
      "south": 41.88906559,
      "east": 14.70595963,
      "north": 41.89438375
    },
    "properties": {
      "foglio": "13",
      "label": "13",
      "gml_id": "CadastralZoning.IT.AGE.MAP.H833_001300",
      "kind": "sheet",
      "ADMINISTRATIVEUNIT": "H833",
      "LEVEL": "3rdOrder",
      "LEVELNAME": "Mappa Catastale",
      "NATIONALCADASTRALZONINGREFERENCE": "H833_001300",
      "zoning_ref": "H833_001300"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  },
  {
    "sample_label": "First feature in file",
    "feature_id": null,
    "geometry_type": "Polygon",
    "geometry_bbox": {
      "west": 14.66367133,
      "south": 41.91237828,
      "east": 14.68158813,
      "north": 41.92184187
    },
    "properties": {
      "foglio": "1",
      "label": "1",
      "gml_id": "CadastralZoning.IT.AGE.MAP.H833_000100",
      "kind": "sheet",
      "ADMINISTRATIVEUNIT": "H833",
      "LEVEL": "3rdOrder",
      "LEVELNAME": "Mappa Catastale",
      "NATIONALCADASTRALZONINGREFERENCE": "H833_000100",
      "zoning_ref": "H833_000100"
    },
    "geometry_note": "Full coordinate array intentionally omitted from AI prompt summary."
  }
]
~~~

### `docs/data/target_parcels.geojson`

- Size: `0.0 MB`
- Feature count: `0`
- Genova family true count: `0`
- Selected true count: `0`

Geometry types:

~~~json
{}
~~~

Collection bbox, lon/lat:

~~~json
null
~~~

Property keys:

~~~text
~~~

Property key counts:

~~~json
{}
~~~

Property value examples:

~~~json
{}
~~~

Sample features with geometry omitted:

~~~json
[]
~~~

## Local image manifest summaries

### `docs/data/pcn_ortho_2012_manifest.json`

~~~json
{
  "path": "docs/data/pcn_ortho_2012_manifest.json",
  "exists": true,
  "size_mb": 0.003,
  "type": "pcn_mase_ortofoto_2012_local_grid",
  "source": "http://wms.pcn.minambiente.it/ogc",
  "layer": "OI.ORTOIMMAGINI.2012.33",
  "request_crs": "EPSG:3857",
  "bbox_lonlat": [
    14.69600225,
    41.88856559,
    14.706459630000001,
    41.894883750000005
  ],
  "grid": {
    "nx": 3,
    "ny": 2
  },
  "tile_count": 6,
  "first_tile_example": {
    "url": "data/pcn_ortho_2012_tiles/pcn_ortho_2012_0000.jpg",
    "coordinates": [
      [
        14.69600225,
        41.89172474811876
      ],
      [
        14.699488043333334,
        41.89172474811876
      ],
      [
        14.699488043333334,
        41.888565590000006
      ],
      [
        14.69600225,
        41.888565590000006
      ]
    ]
  },
  "note": "Official PCN/MASE orthophoto 2012, downloaded locally to avoid CORS/mixed-content issues."
}
~~~

### `docs/data/ade_wms_manifest.json`

~~~json
{
  "path": "docs/data/ade_wms_manifest.json",
  "exists": true,
  "size_mb": 0.027,
  "type": "local_ade_wms_snapshot_grid",
  "source": "https://wms.cartografia.agenziaentrate.gov.it/inspire/wms/ows01.php",
  "layer": null,
  "request_crs": "EPSG:4258",
  "bbox_lonlat": [
    14.6621366256,
    41.8581960936,
    14.741941254399999,
    41.9293787064
  ],
  "grid": {
    "nx": 8,
    "ny": 9
  },
  "tile_count": 72,
  "first_tile_example": {
    "url": "data/ade_wms_tiles/ade_wms_0000.png",
    "coordinates": [
      [
        14.6621366256,
        41.8661052728
      ],
      [
        14.672112204200001,
        41.8661052728
      ],
      [
        14.672112204200001,
        41.8581960936
      ],
      [
        14.6621366256,
        41.8581960936
      ]
    ]
  },
  "note": "Generated locally to avoid browser CORS and because AdE WMS does not support EPSG:3857."
}
~~~

## Recommended `files-to-prompt` exclusion policy

Exclude full generated data and raster tile folders:

~~~text
docs/data/parcels.geojson
docs/data/genova_family_parcels.geojson
docs/data/target_parcels.geojson
docs/data/pcn_ortho_2012_tiles/*
docs/data/ade_wms_tiles/*
*.png
*.jpg
*.jpeg
*.tif
*.tiff
~~~

Keep summaries and source logic:

~~~text
README.md
AI_DATA_SUMMARY.md
docs/index.html
scripts/
docs/data/*manifest.json
~~~

