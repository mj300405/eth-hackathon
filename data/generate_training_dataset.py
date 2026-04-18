#!/usr/bin/env python3
"""Generate an API-first training dataset for overload probability.

This script creates one flat CSV for ML experiments. It uses public/API-backed
inputs where available and synthesizes only the OSD context that is not public:
PV capacity per feeder, local demand, reverse-flow limits and the target
probability of overload.
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
AREA_TYPE_ID = {
    "residential": 0,
    "mixed": 1,
    "industrial": 2,
    "rural": 3,
}


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return default


def parse_start_date(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=WARSAW_TZ)
    return parsed.astimezone(WARSAW_TZ)


def parse_pvgis_time(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%d:%H%M").replace(tzinfo=timezone.utc)


def load_pvgis_raw(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in payload["outputs"]["hourly"]:
        rows.append(
            {
                "source_timestamp": parse_pvgis_time(item["time"]).isoformat(),
                "pv_kw_per_kwp": round(as_float(item.get("P")) / 1000, 6),
                "global_irradiance_wm2": as_float(item.get("G(i)")),
                "temperature_c": as_float(item.get("T2m")),
                "wind_speed_ms": as_float(item.get("WS10m")),
                "source": "PVGIS JRC seriescalc raw yearly profile",
            }
        )
    return rows


def load_pvgis_profile(path: Path) -> list[dict[str, Any]]:
    rows = []
    for item in read_csv(path):
        rows.append(
            {
                "source_timestamp": item.get("timestamp", ""),
                "pv_kw_per_kwp": as_float(item.get("pv_kw_per_kwp")),
                "global_irradiance_wm2": as_float(item.get("global_irradiance_wm2")),
                "temperature_c": as_float(item.get("temperature_c")),
                "wind_speed_ms": as_float(item.get("wind_speed_ms")),
                "source": item.get("source", "PVGIS JRC seriescalc sample profile"),
            }
        )
    return rows


def load_pvgis_source(raw_path: Path | None, profile_path: Path) -> tuple[list[dict[str, Any]], str]:
    if raw_path and raw_path.exists():
        return load_pvgis_raw(raw_path), "pvgis_raw_year"
    return load_pvgis_profile(profile_path), "pvgis_sample_profile"


def load_weather_profile(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for item in read_csv(path):
        rows.append(
            {
                "source_timestamp": item.get("timestamp", ""),
                "temperature_c": as_float(item.get("temperature_c")),
                "wind_speed_ms": as_float(item.get("wind_speed_ms")),
                "cloud_cover_pct": as_float(item.get("cloud_cover_pct")),
                "solar_radiation_wm2": as_float(item.get("solar_radiation_wm2")),
                "source": item.get("source", "weather_profile"),
                "trust_status": item.get("trust_status", ""),
            }
        )
    return rows


def weather_row_for_timestamp(rows: list[dict[str, Any]], offset_hour: int) -> dict[str, Any] | None:
    if not rows:
        return None
    return rows[offset_hour % len(rows)]


def pvgis_row_for_timestamp(
    rows: list[dict[str, Any]],
    source_kind: str,
    ts: datetime,
    offset_hour: int,
) -> dict[str, Any]:
    if not rows:
        raise ValueError("PVGIS profile is empty.")
    if source_kind == "pvgis_raw_year":
        source_index = ((ts.timetuple().tm_yday - 1) * 24 + ts.hour) % len(rows)
    else:
        source_index = offset_hour % len(rows)
    return rows[source_index]


def demand_multiplier(area_type: str, hour: int, is_weekend: bool, temperature_c: float) -> float:
    morning = math.exp(-((hour - 7) / 2.6) ** 2)
    evening = math.exp(-((hour - 19) / 3.0) ** 2)
    workday = 1 if 7 <= hour <= 17 else 0

    if area_type == "industrial":
        value = 0.42 + 0.62 * workday + 0.10 * math.exp(-((hour - 12) / 4.5) ** 2)
        value *= 0.62 if is_weekend else 1.0
    elif area_type == "mixed":
        value = 0.50 + 0.25 * morning + 0.28 * evening + 0.23 * workday
        value *= 0.92 if is_weekend else 1.0
    elif area_type == "rural":
        value = 0.46 + 0.20 * morning + 0.30 * evening + 0.08 * workday
        value *= 1.04 if is_weekend else 1.0
    else:
        value = 0.48 + 0.34 * morning + 0.42 * evening + 0.05 * workday
        value *= 1.06 if is_weekend else 1.0

    weather_load = 1 + 0.012 * max(0.0, 22 - temperature_c) + 0.018 * max(0.0, temperature_c - 26)
    return max(0.18, value * weather_load)


def deterministic_factor(seed: int, day_index: int, feeder_index: int, salt: int, low: float, high: float) -> float:
    rng = random.Random(seed + day_index * 10007 + feeder_index * 997 + salt)
    return low + (high - low) * rng.random()


def logistic(value: float) -> float:
    value = max(-30.0, min(30.0, value))
    return 1 / (1 + math.exp(-value))


def overload_probability(
    overload_ratio: float,
    overload_margin_kw: float,
    reverse_limit_kw: float,
    oze_density_index: float,
    hour: int,
    is_weekend: bool,
) -> float:
    positive_margin_ratio = max(0.0, overload_margin_kw) / max(1.0, reverse_limit_kw)
    near_limit = overload_ratio - 0.82
    midday_stress = 1.0 if 10 <= hour <= 15 else 0.0
    weekend_stress = 1.0 if is_weekend else 0.0
    logit = (
        -2.95
        + 5.35 * near_limit
        + 2.65 * positive_margin_ratio
        + 0.95 * oze_density_index
        + 0.32 * midday_stress
        + 0.24 * weekend_stress
    )
    return round(max(0.005, min(0.995, logistic(logit))), 4)


def risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "high"
    if probability >= 0.35:
        return "medium"
    return "low"


def synthetic_event(probability: float, seed: int, offset_hour: int, feeder_index: int) -> int:
    rng = random.Random(seed + offset_hour * 7919 + feeder_index * 104729)
    return int(rng.random() < probability)


def build_rows(
    feeders: list[dict[str, Any]],
    pvgis_rows: list[dict[str, Any]],
    pvgis_source_kind: str,
    weather_rows: list[dict[str, Any]],
    start_ts: datetime,
    days: int,
    seed: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    total_hours = days * 24

    for offset_hour in range(total_hours):
        ts = start_ts + timedelta(hours=offset_hour)
        day_index = offset_hour // 24
        is_weekend = ts.weekday() >= 5
        pvgis = pvgis_row_for_timestamp(pvgis_rows, pvgis_source_kind, ts, offset_hour)
        weather = weather_row_for_timestamp(weather_rows, offset_hour)

        for feeder_index, feeder in enumerate(feeders, start=1):
            area_type = feeder["area_type"]
            feeder_id = feeder["feeder_id"]
            pv_capacity_kwp = as_float(feeder["synthetic_pv_capacity_kwp"])
            base_demand_kw = as_float(feeder["synthetic_base_demand_kw"])
            reverse_limit_kw = as_float(feeder["synthetic_reverse_flow_limit_kw"])
            oze_density_index = as_float(feeder["oze_density_index"])

            pv_scenario_factor = deterministic_factor(seed, day_index, feeder_index, 11, 0.90, 1.06)
            demand_scenario_factor = deterministic_factor(seed, day_index, feeder_index, 23, 0.88, 1.16)
            limit_scenario_factor = deterministic_factor(seed, 0, feeder_index, 37, 0.94, 1.04)

            pv_kw_per_kwp = as_float(pvgis["pv_kw_per_kwp"])
            pvgis_temperature_c = as_float(pvgis["temperature_c"], 12.0)
            pvgis_wind_speed_ms = as_float(pvgis["wind_speed_ms"])
            temperature_c = as_float(weather["temperature_c"], pvgis_temperature_c) if weather else pvgis_temperature_c
            wind_speed_ms = as_float(weather["wind_speed_ms"], pvgis_wind_speed_ms) if weather else pvgis_wind_speed_ms
            cloud_cover_pct = as_float(weather["cloud_cover_pct"]) if weather else 0.0
            solar_radiation_wm2 = as_float(weather["solar_radiation_wm2"]) if weather else 0.0
            demand_index = demand_multiplier(area_type, ts.hour, is_weekend, temperature_c)
            pv_generation_kw = pv_kw_per_kwp * pv_capacity_kwp * pv_scenario_factor
            local_demand_kw = base_demand_kw * demand_index * demand_scenario_factor
            effective_reverse_limit_kw = reverse_limit_kw * limit_scenario_factor
            reverse_flow_kw = max(0.0, pv_generation_kw - local_demand_kw)
            overload_margin_kw = reverse_flow_kw - effective_reverse_limit_kw
            overload_kw = max(0.0, overload_margin_kw)
            overload_ratio = reverse_flow_kw / effective_reverse_limit_kw if effective_reverse_limit_kw else 0.0
            probability = overload_probability(
                overload_ratio=overload_ratio,
                overload_margin_kw=overload_margin_kw,
                reverse_limit_kw=effective_reverse_limit_kw,
                oze_density_index=oze_density_index,
                hour=ts.hour,
                is_weekend=is_weekend,
            )
            event = synthetic_event(probability, seed, offset_hour, feeder_index)

            rows.append(
                {
                    "timestamp": ts.isoformat(),
                    "location_id": feeder["branch_location_id"],
                    "feeder_id": feeder_id,
                    "mv_line_id": feeder["mv_line_id"],
                    "area_type": area_type,
                    "area_type_id": AREA_TYPE_ID.get(area_type, -1),
                    "hour": ts.hour,
                    "day_of_week": ts.weekday(),
                    "is_weekend": int(is_weekend),
                    "month": ts.month,
                    "centroid_lat": feeder["centroid_lat"],
                    "centroid_lon": feeder["centroid_lon"],
                    "line_length_km": feeder["length_km"],
                    "pv_kw_per_kwp": round(pv_kw_per_kwp, 6),
                    "global_irradiance_wm2": round(as_float(pvgis["global_irradiance_wm2"]), 2),
                    "temperature_c": round(temperature_c, 2),
                    "wind_speed_ms": round(wind_speed_ms, 2),
                    "cloud_cover_pct": round(cloud_cover_pct, 2),
                    "solar_radiation_wm2": round(solar_radiation_wm2, 2),
                    "synthetic_pv_capacity_kwp": round(pv_capacity_kwp * pv_scenario_factor, 2),
                    "synthetic_base_demand_kw": round(base_demand_kw, 2),
                    "synthetic_local_demand_kw": round(local_demand_kw, 2),
                    "synthetic_reverse_flow_limit_kw": round(effective_reverse_limit_kw, 2),
                    "oze_density_index": round(oze_density_index, 4),
                    "pv_generation_kw": round(pv_generation_kw, 2),
                    "reverse_flow_kw": round(reverse_flow_kw, 2),
                    "overload_margin_kw": round(overload_margin_kw, 2),
                    "overload_kw": round(overload_kw, 2),
                    "overload_ratio": round(overload_ratio, 4),
                    "target_overload_probability": probability,
                    "target_overload_event": event,
                    "risk_level": risk_level(probability),
                    "risk_score": round(probability * 100),
                    "pvgis_source_kind": pvgis_source_kind,
                    "pvgis_source_timestamp": pvgis["source_timestamp"],
                    "weather_source": "" if not weather else weather["source"],
                    "weather_source_timestamp": "" if not weather else weather["source_timestamp"],
                    "weather_trust_status": "" if not weather else weather["trust_status"],
                    "target_source": "synthetic_probability_from_reverse_flow_model",
                    "source_note": "public PVGIS/OSM and IMGW-seeded weather inputs plus synthetic OSD context; not Tauron operational data",
                }
            )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feeders", default="data/samples/synthetic_mv_feeders_gliwice.csv")
    parser.add_argument("--pvgis-profile", default="data/samples/pvgis_profile_gliwice.csv")
    parser.add_argument("--weather-profile", default="data/samples/weather_hourly_gliwice_demo.csv")
    parser.add_argument(
        "--pvgis-raw",
        default="",
        help="Optional raw PVGIS yearly JSON. If omitted, the tracked 24h sample profile is reused.",
    )
    parser.add_argument("--output", default="data/samples/model_training_gliwice_demo.csv")
    parser.add_argument("--start-date", default="2026-04-01")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    feeders = read_csv(Path(args.feeders))
    raw_path = Path(args.pvgis_raw) if args.pvgis_raw else None
    pvgis_rows, pvgis_source_kind = load_pvgis_source(raw_path, Path(args.pvgis_profile))
    weather_rows = load_weather_profile(Path(args.weather_profile))
    rows = build_rows(
        feeders=feeders,
        pvgis_rows=pvgis_rows,
        pvgis_source_kind=pvgis_source_kind,
        weather_rows=weather_rows,
        start_ts=parse_start_date(args.start_date),
        days=args.days,
        seed=args.seed,
    )
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(Path(args.output), fieldnames, rows)

    events = sum(int(row["target_overload_event"]) for row in rows)
    high_risk = sum(1 for row in rows if row["risk_level"] == "high")
    print(
        f"Generated {len(rows)} rows to {args.output} "
        f"({events} synthetic overload events, {high_risk} high-risk rows)."
    )


if __name__ == "__main__":
    main()
