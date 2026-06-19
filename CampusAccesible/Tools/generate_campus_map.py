#!/usr/bin/env python3
"""
generate_campus_map.py
======================
Genera un mapa HTML (Leaflet + OpenStreetMap) con TODOS los nodos, caminos y
entradas de edificio del campus, leyendo directamente los tres .plist que usa
la app. Sirve como ayuda visual para depurar/dar seguimiento a los datos del
grafo de navegacion.

Lee:
  - Coords.plist          -> nodos (lat/lon)
  - ListaCaminos.plist    -> aristas (accesibles vs. regulares)
  - ListaEdificios.plist  -> nombres de las entradas de edificio

OJO con los datos originales: en Coords.plist los nombres de las llaves estan
invertidos a proposito (se conservan asi en la app):
    longitud = latitud  (~25.6x)
    latitud  = longitud (~-100.2x)

Uso basico (desde la carpeta Tools/, usa los plists del proyecto por defecto):
    python3 generate_campus_map.py

Con rutas personalizadas:
    python3 generate_campus_map.py --data /ruta/a/carpeta/con/plists --out /ruta/salida/mapa.html

Requisitos: solo Python 3 (plistlib viene incluido). Necesita internet al ABRIR
el HTML porque carga Leaflet y los tiles de OpenStreetMap desde la web.
"""
import argparse
import json
import plistlib
import sys
from pathlib import Path

# Por defecto: los plists viven en ../Data respecto a este script (Tools/).
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = SCRIPT_DIR.parent / "Data"
DEFAULT_OUT = SCRIPT_DIR / "campus_map.html"


def load_plist(path: Path):
    if not path.exists():
        sys.exit(f"ERROR: no se encontro {path}")
    with open(path, "rb") as f:
        return plistlib.load(f)


def build(data_dir: Path, out_path: Path):
    raw_coords = load_plist(data_dir / "Coords.plist")
    raw_paths = load_plist(data_dir / "ListaCaminos.plist")
    raw_buildings = load_plist(data_dir / "ListaEdificios.plist")

    # --- nodos ---
    coords = []
    for i, c in enumerate(raw_coords):
        lat = c.get("longitud", 0)   # nombres invertidos en la fuente (ver docstring)
        lon = c.get("latitud", 0)
        valid = not (lat == 0 and lon == 0)
        coords.append({"index": i, "lat": lat, "lon": lon, "valid": valid})

    def pt(i):
        if 0 <= i < len(coords) and coords[i]["valid"]:
            return [coords[i]["lat"], coords[i]["lon"]]
        return None

    # --- aristas ---
    edges, acc_edges = [], []
    for p in raw_paths:
        a, b = pt(p.get("punto1", -1)), pt(p.get("punto2", -1))
        if a is None or b is None:
            continue
        (acc_edges if p.get("accesible") else edges).append([a, b])

    # --- edificios: indice de coord -> nombre (el ultimo gana en duplicados) ---
    building_coords = {}
    for bld in raw_buildings:
        name = bld.get("nombre", "")
        for idx in bld.get("coord", []) or []:
            building_coords[str(idx)] = name

    html = TEMPLATE.format(
        coords=json.dumps(coords),
        edges=json.dumps(edges),
        acc_edges=json.dumps(acc_edges),
        buildings=json.dumps(building_coords, ensure_ascii=False),
    )
    out_path.write_text(html, encoding="utf-8")

    valid = sum(c["valid"] for c in coords)
    print(f"nodos:        {len(coords)} (validos: {valid}, en 0,0: {len(coords) - valid})")
    print(f"caminos:      {len(acc_edges)} accesibles + {len(edges)} regulares")
    print(f"edificios:    {len(building_coords)} indices etiquetados")
    print(f"HTML escrito: {out_path}")


# {{ }} = llaves literales para CSS/JS; {coords} etc = se rellenan con .format()
TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"><title>Campus Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body {{ margin: 0; font-family: sans-serif; }}
  #map {{ height: 100vh; }}
  #legend {{ position: fixed; top: 10px; right: 10px; z-index: 1000; background: white; padding: 12px 16px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); font-size: 13px; line-height: 1.8; }}
  #legend label {{ display: flex; align-items: center; gap: 8px; cursor: pointer; }}
  .swatch {{ width: 24px; height: 4px; border-radius: 2px; display: inline-block; }}
</style>
</head>
<body>
<div id="map"></div>
<div id="legend">
  <b>Campus Node Map</b><br>
  <label><input type="checkbox" id="chk-acc" checked> <span class="swatch" style="background:#2196F3"></span> Accessible path</label>
  <label><input type="checkbox" id="chk-reg" checked> <span class="swatch" style="background:#FF9800"></span> Regular path</label>
  <label><input type="checkbox" id="chk-nodes" checked> &#9679; All nodes</label>
  <label><input type="checkbox" id="chk-buildings" checked> &#127963; Building entrances</label>
</div>
<script>
const coords = {coords};
const edges = {edges};
const accEdges = {acc_edges};
const buildingCoords = {buildings};

const map = L.map('map').setView([25.6520, -100.2910], 16);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{attribution: '© OpenStreetMap', maxZoom: 20}}).addTo(map);

const accLayer = L.layerGroup(), regLayer = L.layerGroup(), nodeLayer = L.layerGroup(), buildingLayer = L.layerGroup();
accEdges.forEach(e => L.polyline(e, {{color: '#2196F3', weight: 3, opacity: 0.8}}).addTo(accLayer));
edges.forEach(e => L.polyline(e, {{color: '#FF9800', weight: 2, opacity: 0.7}}).addTo(regLayer));
coords.forEach(c => {{
  if (!c.valid) return;
  const isBuilding = buildingCoords[c.index] !== undefined;
  const label = isBuilding ? `${{c.index}}: ${{buildingCoords[c.index]}}` : `${{c.index}}`;
  if (isBuilding) {{
    L.circleMarker([c.lat, c.lon], {{radius: 7, color: '#C62828', fillColor: '#EF5350', fillOpacity: 1, weight: 2}}).bindPopup(label).addTo(buildingLayer);
  }} else {{
    L.circleMarker([c.lat, c.lon], {{radius: 4, color: '#1B5E20', fillColor: '#66BB6A', fillOpacity: 0.9, weight: 1.5}}).bindPopup(label).addTo(nodeLayer);
  }}
}});
[accLayer, regLayer, nodeLayer, buildingLayer].forEach(l => l.addTo(map));
document.getElementById('chk-acc').addEventListener('change', e => e.target.checked ? accLayer.addTo(map) : map.removeLayer(accLayer));
document.getElementById('chk-reg').addEventListener('change', e => e.target.checked ? regLayer.addTo(map) : map.removeLayer(regLayer));
document.getElementById('chk-nodes').addEventListener('change', e => e.target.checked ? nodeLayer.addTo(map) : map.removeLayer(nodeLayer));
document.getElementById('chk-buildings').addEventListener('change', e => e.target.checked ? buildingLayer.addTo(map) : map.removeLayer(buildingLayer));
</script>
</body>
</html>"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Genera un mapa HTML del campus desde los .plist de la app.")
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA,
                    help=f"Carpeta con los 3 .plist (por defecto: {DEFAULT_DATA})")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"Ruta del HTML de salida (por defecto: {DEFAULT_OUT})")
    args = ap.parse_args()
    build(args.data, args.out)
