#!/usr/bin/env python3
"""Build a small API-first POC dataset for one Tauron branch area.

The dataset is intentionally small and demonstrational:
- MV line geometry comes from a public/proxy OSM/Overpass sample.
- Weather projection is seeded by an official public IMGW observation when available.
- PV generation shape comes from a public PVGIS/JRC reference profile when available.
- Only the missing OSD context is synthetic: feeder PV capacity, local demand,
  reverse-flow limits and the resulting overload/risk scenario.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


WARSAW_TZ = timezone(timedelta(hours=2))
START_TS = datetime(2026, 4, 18, 0, 0, tzinfo=WARSAW_TZ)
FETCHED_AT = datetime(2026, 4, 17, 18, 0, tzinfo=WARSAW_TZ)


FEEDER_TEMPLATES = {
    "residential": {
        "capacity_kw": 2200,
        "reverse_limit_kw": 330,
        "base_demand_kw": 520,
        "pv_capacity_kwp": 980,
        "oze_density_index": 0.72,
        "south_share": 0.55,
        "east_west_share": 0.30,
        "flat_share": 0.15,
    },
    "mixed": {
        "capacity_kw": 2600,
        "reverse_limit_kw": 260,
        "base_demand_kw": 710,
        "pv_capacity_kwp": 1120,
        "oze_density_index": 0.68,
        "south_share": 0.48,
        "east_west_share": 0.37,
        "flat_share": 0.15,
    },
    "industrial": {
        "capacity_kw": 3100,
        "reverse_limit_kw": 920,
        "base_demand_kw": 1180,
        "pv_capacity_kwp": 1320,
        "oze_density_index": 0.54,
        "south_share": 0.35,
        "east_west_share": 0.25,
        "flat_share": 0.40,
    },
    "rural": {
        "capacity_kw": 1600,
        "reverse_limit_kw": 250,
        "base_demand_kw": 310,
        "pv_capacity_kwp": 760,
        "oze_density_index": 0.77,
        "south_share": 0.58,
        "east_west_share": 0.30,
        "flat_share": 0.12,
    },
}


def classify_area(length_km: float, feature_hash: int) -> str:
    bucket = feature_hash % 10
    if length_km >= 5.0:
        return "rural"
    if length_km >= 1.5:
        return "industrial" if bucket < 3 else "mixed"
    if length_km >= 0.5:
        return "mixed" if bucket < 5 else "residential"
    return "residential"


def jitter(seed: int, salt: int, low: float, high: float) -> float:
    rng = random.Random(seed * 10007 + salt)
    return low + (high - low) * rng.random()


def haversine_km(left: list[float], right: list[float]) -> float:
    lon1, lat1 = map(math.radians, left)
    lon2, lat2 = map(math.radians, right)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(a))


def line_length_km(coordinates: list[list[float]]) -> float:
    return sum(haversine_km(a, b) for a, b in zip(coordinates, coordinates[1:]))


def centroid(coordinates: list[list[float]]) -> tuple[float, float]:
    lon = sum(point[0] for point in coordinates) / len(coordinates)
    lat = sum(point[1] for point in coordinates) / len(coordinates)
    return lat, lon


def read_geojson(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def iso(ts: datetime) -> str:
    return ts.isoformat()


def build_feeders(
    features: list[dict[str, Any]],
    max_feeders: int | None = None,
    location_id: str = "gliwice",
    id_prefix: str = "GLW",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    feeder_rows: list[dict[str, Any]] = []
    orientation_rows: list[dict[str, Any]] = []

    selected = features if max_feeders is None else features[:max_feeders]

    for idx, feature in enumerate(selected, start=1):
        coords = feature["geometry"]["coordinates"]
        lat, lon = centroid(coords)
        length = line_length_km(coords)
        mv_line_id = feature["properties"]["mv_line_id"]
        feature_hash = abs(hash(mv_line_id))
        area_type = classify_area(length, feature_hash)
        template = FEEDER_TEMPLATES[area_type]

        capacity_kw = round(template["capacity_kw"] * jitter(feature_hash, 1, 0.85, 1.20), 1)
        pv_capacity_kwp = round(template["pv_capacity_kwp"] * jitter(feature_hash, 2, 0.75, 1.30), 1)
        base_demand_kw = round(template["base_demand_kw"] * jitter(feature_hash, 3, 0.80, 1.25), 1)
        reverse_limit_kw = round(template["reverse_limit_kw"] * jitter(feature_hash, 4, 0.70, 1.25), 1)
        oze_density_index = round(max(0.1, min(0.98, template["oze_density_index"] * jitter(feature_hash, 5, 0.85, 1.15))), 3)

        feeder_id = f"{location_id}_f{idx:03d}"
        feeder_rows.append(
            {
                "feeder_id": feeder_id,
                "branch_location_id": location_id,
                "mv_line_id": mv_line_id,
                "feeder_name": f"{id_prefix}-DEMO-F{idx:03d}",
                "centroid_lat": f"{lat:.6f}",
                "centroid_lon": f"{lon:.6f}",
                "length_km": f"{length:.3f}",
                "synthetic_capacity_kw": capacity_kw,
                "synthetic_reverse_flow_limit_kw": reverse_limit_kw,
                "synthetic_base_demand_kw": base_demand_kw,
                "synthetic_pv_capacity_kwp": pv_capacity_kwp,
                "area_type": area_type,
                "oze_density_index": oze_density_index,
                "is_synthetic": "true",
                "source_note": "OSM geometry proxy; electrical parameters synthetic for POC",
            }
        )
        orientation_rows.append(
            {
                "feeder_id": feeder_id,
                "south_share": template["south_share"],
                "east_west_share": template["east_west_share"],
                "flat_share": template["flat_share"],
                "south_tilt_deg": 35,
                "east_west_tilt_deg": 20,
                "flat_tilt_deg": 10,
                "assumption_type": "synthetic_rooftop_mix",
            }
        )

    return feeder_rows, orientation_rows


def read_imgw_seed(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else None


def read_pvgis_profile(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def weather_at(hour: int, imgw_seed: dict[str, Any] | None) -> dict[str, Any]:
    daylight = max(0.0, math.sin(math.pi * (hour - 5) / 15))
    base_temperature = 8.5
    base_wind = 2.2
    base_humidity = None
    if imgw_seed:
        base_temperature = float(imgw_seed["temperature_c"])
        base_wind = float(imgw_seed["wind_speed_ms"])
        base_humidity = imgw_seed.get("relative_humidity_pct")

    temperature = base_temperature - 2.0 + 8.0 * max(0.0, math.sin(math.pi * (hour - 6) / 15))
    wind = max(0.1, base_wind + 1.1 * max(0.0, math.sin(math.pi * (hour - 3) / 18)))
    cloud = 68 - 42 * daylight + 8 * math.sin(math.pi * hour / 6)
    radiation = 760 * daylight * (1 - max(0, min(100, cloud)) / 130)
    return {
        "temperature_c": round(temperature, 2),
        "wind_speed_ms": round(wind, 2),
        "relative_humidity_pct": "" if base_humidity in (None, "") else base_humidity,
        "cloud_cover_pct": round(max(5, min(95, cloud)), 1),
        "solar_radiation_wm2": round(max(0, radiation), 1),
    }


def build_weather(imgw_seed: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows = []
    for offset in range(24):
        ts = START_TS + timedelta(hours=offset)
        values = weather_at(ts.hour, imgw_seed)
        if imgw_seed:
            source = "IMGW-PIB public synop API seeded demo projection"
            source_url = imgw_seed["source_url"]
            fetched_at = imgw_seed["fetched_at"]
            data_kind = "forecast_demo_seeded_by_imgw_observation"
            trust_status = "imgw_observation_plus_demo_projection"
        else:
            source = "synthetic_demo_pending_imgw"
            source_url = "https://dane.imgw.pl"
            fetched_at = iso(FETCHED_AT)
            data_kind = "forecast_demo"
            trust_status = "synthetic_demo"
        rows.append(
            {
                "timestamp": iso(ts),
                "location_id": "gliwice",
                **values,
                "source": source,
                "source_station": "" if not imgw_seed else imgw_seed["source_station"],
                "source_station_id": "" if not imgw_seed else imgw_seed["source_station_id"],
                "source_url": source_url,
                "fetched_at": fetched_at,
                "data_kind": data_kind,
                "trust_status": trust_status,
            }
        )
    return rows


def demand_multiplier(area_type: str, hour: int) -> float:
    morning = math.exp(-((hour - 7) / 2.6) ** 2)
    evening = math.exp(-((hour - 19) / 3.0) ** 2)
    workday = 1 if 7 <= hour <= 17 else 0
    if area_type == "industrial":
        return 0.42 + 0.62 * workday + 0.10 * math.exp(-((hour - 12) / 4.5) ** 2)
    if area_type == "mixed":
        return 0.50 + 0.25 * morning + 0.28 * evening + 0.23 * workday
    if area_type == "rural":
        return 0.46 + 0.20 * morning + 0.30 * evening + 0.08 * workday
    return 0.48 + 0.34 * morning + 0.42 * evening + 0.05 * workday


def solar_profile(hour: int, weather: dict[str, Any], orientation: dict[str, Any]) -> float:
    daylight = max(0.0, math.sin(math.pi * (hour - 5) / 15))
    if daylight <= 0:
        return 0.0

    morning = max(0.0, math.sin(math.pi * (hour - 4) / 13)) ** 1.55
    afternoon = max(0.0, math.sin(math.pi * (hour - 7) / 13)) ** 1.55
    south = daylight**1.35
    east_west = 0.5 * morning + 0.5 * afternoon
    flat = 0.86 * daylight**1.12
    cloud_modifier = 1 - 0.0065 * float(weather["cloud_cover_pct"])
    temp_modifier = 1 - 0.004 * max(0.0, float(weather["temperature_c"]) - 25)

    geometry_factor = (
        float(orientation["south_share"]) * south
        + float(orientation["east_west_share"]) * east_west
        + float(orientation["flat_share"]) * flat
    )
    return max(0.0, geometry_factor * cloud_modifier * temp_modifier)


def recommendation(risk_score: int, overload_kw: float, area_type: str) -> str:
    if risk_score >= 75:
        return "activate flexibility or storage; monitor feeder voltage"
    if risk_score >= 50:
        return "shift local demand to PV peak hours; prepare monitoring"
    if overload_kw > 0:
        return "watch repeated reverse-flow peaks"
    if area_type == "industrial":
        return "use daytime industrial demand as local flexibility"
    return "normal monitoring"


def build_hourly_outputs(
    feeders: list[dict[str, Any]],
    orientations: list[dict[str, Any]],
    weather_rows: list[dict[str, Any]],
    pvgis_profile: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    orientation_by_feeder = {row["feeder_id"]: row for row in orientations}
    generation_rows: list[dict[str, Any]] = []
    demand_rows: list[dict[str, Any]] = []
    constraint_rows: list[dict[str, Any]] = []
    risk_rows: list[dict[str, Any]] = []

    for feeder in feeders:
        feeder_id = feeder["feeder_id"]
        orientation = orientation_by_feeder[feeder_id]
        pv_capacity = float(feeder["synthetic_pv_capacity_kwp"])
        base_demand = float(feeder["synthetic_base_demand_kw"])
        reverse_limit = float(feeder["synthetic_reverse_flow_limit_kw"])
        oze_density = float(feeder["oze_density_index"])

        for weather in weather_rows:
            ts = weather["timestamp"]
            hour = datetime.fromisoformat(ts).hour
            if pvgis_profile:
                pvgis_row = pvgis_profile[hour % len(pvgis_profile)]
                pv_kw = pv_capacity * float(pvgis_row["pv_kw_per_kwp"])
                generation_basis = "pvgis_reference_profile_scaled_to_synthetic_feeder_kwp"
            else:
                pv_kw = pv_capacity * 0.86 * solar_profile(hour, weather, orientation)
                generation_basis = "synthetic_pv_model_pending_pvgis"
            demand_kw = base_demand * demand_multiplier(feeder["area_type"], hour)
            reverse_flow_kw = max(0.0, pv_kw - demand_kw)
            overload_kw = max(0.0, reverse_flow_kw - reverse_limit)
            utilization = reverse_flow_kw / reverse_limit if reverse_limit else 0.0
            risk_score = round(
                min(
                    100.0,
                    100.0
                    * (
                        0.58 * min(1.0, utilization)
                        + 0.27 * min(1.0, overload_kw / max(1.0, reverse_limit * 0.35))
                        + 0.15 * oze_density
                    ),
                )
            )
            risk_level = "high" if risk_score >= 70 else "medium" if risk_score >= 40 else "low"

            generation_rows.append(
                {
                    "timestamp": ts,
                    "location_id": "gliwice",
                    "feeder_id": feeder_id,
                    "pv_kw": round(pv_kw, 2),
                    "wind_kw": 0,
                    "confidence": 0.62,
                    "generation_basis": generation_basis,
                }
            )
            demand_rows.append(
                {
                    "timestamp": ts,
                    "location_id": "gliwice",
                    "feeder_id": feeder_id,
                    "demand_index": round(demand_kw / base_demand, 4),
                    "demand_kw": round(demand_kw, 2),
                    "profile_type": f"{feeder['area_type']}_demo",
                    "source_url": "synthetic_demo_profile",
                }
            )
            constraint_rows.append(
                {
                    "scenario_id": "gliwice_sunny_low_demand_v1",
                    "timestamp": ts,
                    "location_id": "gliwice",
                    "feeder_id": feeder_id,
                    "synthetic_constraint_index": round(min(1.0, utilization), 4),
                    "synthetic_overload_flag": str(overload_kw > 0).lower(),
                    "synthetic_overload_mw": round(overload_kw / 1000, 4),
                    "scenario_basis": "sunny spring day, local low-demand PV reverse-flow stress",
                    "is_synthetic": "true",
                    "source_note": "not Tauron operational data",
                }
            )
            risk_rows.append(
                {
                    "timestamp": ts,
                    "location_id": "gliwice",
                    "feeder_id": feeder_id,
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "reverse_flow_kw": round(reverse_flow_kw, 2),
                    "overload_kw": round(overload_kw, 2),
                    "recommendation": recommendation(risk_score, overload_kw, feeder["area_type"]),
                }
            )

    return generation_rows, demand_rows, constraint_rows, risk_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mv-lines",
        default="data/processed/mv_line_geometries_gliwice.geojson",
        help="Input MV line GeoJSON file.",
    )
    parser.add_argument(
        "--max-feeders",
        type=int,
        default=None,
        help="Optional cap on feeder count (default: one feeder per line in the input).",
    )
    parser.add_argument(
        "--output-dir",
        default="data/samples",
        help="Directory for generated sample CSVs.",
    )
    parser.add_argument(
        "--imgw-weather",
        default="data/samples/weather_hourly_gliwice_imgw.csv",
        help="Optional trusted IMGW weather CSV used to seed the 24h demo projection.",
    )
    parser.add_argument(
        "--pvgis-profile",
        default="data/samples/pvgis_profile_gliwice.csv",
        help="Optional PVGIS reference profile CSV used for PV generation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    geojson = read_geojson(Path(args.mv_lines))
    imgw_seed = read_imgw_seed(Path(args.imgw_weather))
    pvgis_profile = read_pvgis_profile(Path(args.pvgis_profile))
    feeders, orientations = build_feeders(geojson["features"], max_feeders=args.max_feeders)
    weather_rows = build_weather(imgw_seed)
    generation, demand, constraints, risk = build_hourly_outputs(
        feeders,
        orientations,
        weather_rows,
        pvgis_profile,
    )

    write_csv(
        output_dir / "synthetic_mv_feeders_gliwice.csv",
        [
            "feeder_id",
            "branch_location_id",
            "mv_line_id",
            "feeder_name",
            "centroid_lat",
            "centroid_lon",
            "length_km",
            "synthetic_capacity_kw",
            "synthetic_reverse_flow_limit_kw",
            "synthetic_base_demand_kw",
            "synthetic_pv_capacity_kwp",
            "area_type",
            "oze_density_index",
            "is_synthetic",
            "source_note",
        ],
        feeders,
    )
    write_csv(
        output_dir / "pv_orientation_mix_gliwice.csv",
        [
            "feeder_id",
            "south_share",
            "east_west_share",
            "flat_share",
            "south_tilt_deg",
            "east_west_tilt_deg",
            "flat_tilt_deg",
            "assumption_type",
        ],
        orientations,
    )
    write_csv(
        output_dir / "weather_hourly_gliwice_demo.csv",
        [
            "timestamp",
            "location_id",
            "temperature_c",
            "wind_speed_ms",
            "relative_humidity_pct",
            "cloud_cover_pct",
            "solar_radiation_wm2",
            "source",
            "source_station",
            "source_station_id",
            "source_url",
            "fetched_at",
            "data_kind",
            "trust_status",
        ],
        weather_rows,
    )
    write_csv(
        output_dir / "generation_forecast_gliwice_demo.csv",
        ["timestamp", "location_id", "feeder_id", "pv_kw", "wind_kw", "confidence", "generation_basis"],
        generation,
    )
    write_csv(
        output_dir / "demand_proxy_gliwice_demo.csv",
        ["timestamp", "location_id", "feeder_id", "demand_index", "demand_kw", "profile_type", "source_url"],
        demand,
    )
    write_csv(
        output_dir / "synthetic_grid_constraints_gliwice_demo.csv",
        [
            "scenario_id",
            "timestamp",
            "location_id",
            "feeder_id",
            "synthetic_constraint_index",
            "synthetic_overload_flag",
            "synthetic_overload_mw",
            "scenario_basis",
            "is_synthetic",
            "source_note",
        ],
        constraints,
    )
    write_csv(
        output_dir / "risk_hourly_gliwice_demo.csv",
        [
            "timestamp",
            "location_id",
            "feeder_id",
            "risk_score",
            "risk_level",
            "reverse_flow_kw",
            "overload_kw",
            "recommendation",
        ],
        risk,
    )

    print(f"Generated {len(feeders)} feeders and {len(risk)} hourly risk rows in {output_dir}")


if __name__ == "__main__":
    main()
