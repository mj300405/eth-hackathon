#!/usr/bin/env python3
"""Fetch public/proxy medium-voltage line geometries from OpenStreetMap.

The output is a GeoJSON file that can be used as spatial context for the MVP.
It is not official Tauron Dystrybucja topology. Operational parameters, loads
and overload labels must stay synthetic unless formally provided by the OSD.
"""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


OVERPASS_URL = "https://overpass-api.de/api/interpreter"
MV_VOLTAGES = ("6000", "10000", "15000", "20000", "30000")


def build_query(bbox: str) -> str:
    """Build an Overpass query for likely Polish MV lines in a bbox."""
    return f"""
[out:json][timeout:60];
(
  way["power"~"^(line|minor_line|cable)$"]["voltage"~"^({'|'.join(MV_VOLTAGES)})$"]({bbox});
);
out tags geom;
""".strip()


def fetch_overpass(query: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({"data": query}).encode("utf-8")
    request = urllib.request.Request(
        OVERPASS_URL,
        data=params,
        headers={"User-Agent": "gridflex-oze-mvp/0.1"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def overpass_to_geojson(payload: dict[str, Any], source_label: str) -> dict[str, Any]:
    features: list[dict[str, Any]] = []

    for element in payload.get("elements", []):
        geometry = element.get("geometry") or []
        if element.get("type") != "way" or len(geometry) < 2:
            continue

        tags = element.get("tags") or {}
        voltage = tags.get("voltage")
        try:
            voltage_v = int(voltage) if voltage is not None else None
        except ValueError:
            voltage_v = None

        feature = {
            "type": "Feature",
            "properties": {
                "mv_line_id": f"osm_way_{element['id']}",
                "source_feature_id": str(element["id"]),
                "source": "osm",
                "source_url": OVERPASS_URL,
                "source_label": source_label,
                "voltage_v": voltage_v,
                "power": tags.get("power"),
                "operator_tag": tags.get("operator"),
                "name": tags.get("name"),
                "quality_flag": "medium",
                "is_official_tauron_topology": False,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[point["lon"], point["lat"]] for point in geometry],
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "name": source_label,
        "features": features,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bbox",
        required=True,
        help="Bounding box as south,west,north,east, e.g. 50.22,18.55,50.38,18.82",
    )
    parser.add_argument(
        "--output",
        default="data/processed/mv_line_geometries.geojson",
        help="Output GeoJSON path.",
    )
    parser.add_argument(
        "--raw-output",
        default=None,
        help="Optional path for raw Overpass JSON.",
    )
    parser.add_argument(
        "--source-label",
        default="osm_mv_lines",
        help="Human-readable label stored in GeoJSON metadata.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    query = build_query(args.bbox)
    payload = fetch_overpass(query)

    if args.raw_output:
        raw_path = Path(args.raw_output)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    geojson = overpass_to_geojson(payload, args.source_label)
    output.write_text(json.dumps(geojson, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved {len(geojson['features'])} MV line features to {output}")


if __name__ == "__main__":
    main()
