"""Public API service for the GridFlex OZE demo."""

from __future__ import annotations

import asyncio
import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://localhost:8001").rstrip("/")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
CORS_ALLOW_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]
MV_LINE_GEOMETRY_PATH = os.getenv("MV_LINE_GEOMETRY_PATH", "data/processed/mv_line_geometries_gliwice.geojson")
MV_LINE_GEOMETRY_FALLBACK_PATH = os.getenv(
    "MV_LINE_GEOMETRY_FALLBACK_PATH", "data/samples/mv_line_geometries_gliwice_sample.geojson"
)

app = FastAPI(
    title="GridFlex OZE API",
    description="Backend API that exposes model predictions to the dashboard.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


async def model_get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{MODEL_SERVICE_URL}{path}"
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Model service unavailable: {exc}") from exc


def as_float(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return default


def timestamp_key(value: str) -> datetime:
    return datetime.fromisoformat(value)


def hour_label(value: str) -> str:
    return timestamp_key(value).strftime("%H:%M")


def display_name(location_id: str) -> str:
    return location_id.replace("_", " ").replace("-", " ").title()


def ui_risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "WYSOKIE"
    if probability >= 0.35:
        return "SREDNIE"
    return "NISKIE"


def load_mv_line_geometries() -> dict[str, dict[str, Any]]:
    for candidate in (MV_LINE_GEOMETRY_PATH, MV_LINE_GEOMETRY_FALLBACK_PATH):
        if not candidate:
            continue
        path = Path(candidate)
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        geometries: dict[str, dict[str, Any]] = {}
        for feature in data.get("features", []):
            props = feature.get("properties") or {}
            mv_line_id = props.get("mv_line_id")
            geometry = feature.get("geometry") or {}
            if not mv_line_id or geometry.get("type") != "LineString":
                continue
            coordinates = geometry.get("coordinates") or []
            if len(coordinates) < 2:
                continue
            geometries[mv_line_id] = {
                "coordinates": coordinates,
                "voltage_v": props.get("voltage_v"),
                "power": props.get("power"),
                "operator_tag": props.get("operator_tag"),
                "name": props.get("name"),
                "source": props.get("source"),
                "is_official_tauron_topology": bool(props.get("is_official_tauron_topology", False)),
            }
        return geometries
    return {}


MV_LINE_GEOMETRIES: dict[str, dict[str, Any]] = load_mv_line_geometries()


def recommendations_for(risk_level: str, constrained_feeders: int) -> list[str]:
    if risk_level == "WYSOKIE":
        return [
            "Wymagany monitoring w czasie rzeczywistym",
            "Rozważ lokalne magazynowanie energii",
            "Kandydat do analizy modernizacji sieci",
        ]
    if risk_level == "SREDNIE" or constrained_feeders > 0:
        return [
            "Przesuń zużycie na godziny wysokiej generacji",
            "Monitoruj feedery z najwyższym przepływem zwrotnym",
        ]
    return []


def build_mv_line_payload(feeder_rows: list[dict[str, Any]], horizon_hours: int = 24) -> list[dict[str, Any]]:
    timestamps = sorted({row["timestamp"] for row in feeder_rows if row.get("timestamp")}, key=timestamp_key)[:horizon_hours]
    timestamp_set = set(timestamps)
    scoped_rows = [row for row in feeder_rows if row.get("timestamp") in timestamp_set]

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scoped_rows:
        mv_line_id = row.get("mv_line_id")
        if not mv_line_id:
            continue
        groups[mv_line_id].append(row)

    payload: list[dict[str, Any]] = []
    for mv_line_id, rows in sorted(groups.items()):
        geometry = MV_LINE_GEOMETRIES.get(mv_line_id)
        if not geometry:
            continue
        sorted_rows = sorted(rows, key=lambda r: timestamp_key(r["timestamp"]) if r.get("timestamp") else datetime.min)
        peak_row = max(sorted_rows, key=lambda r: as_float(r.get("predicted_overload_probability")))
        max_probability = as_float(peak_row.get("predicted_overload_probability"))
        limit_kw = as_float(peak_row.get("reverse_flow_limit_kw"))
        reverse_flow_kw = as_float(peak_row.get("reverse_flow_kw"))
        utilization = reverse_flow_kw / limit_kw if limit_kw > 0 else 0.0
        overload_hours = sum(1 for r in sorted_rows if int(r.get("predicted_overload_event", 0) or 0) == 1)

        forecast = []
        for row in sorted_rows:
            timestamp = row.get("timestamp")
            if not timestamp:
                continue
            row_limit_kw = as_float(row.get("reverse_flow_limit_kw"))
            row_reverse_flow_kw = as_float(row.get("reverse_flow_kw"))
            generation_mw = (
                as_float(row.get("pv_generation_kw")) + as_float(row.get("wind_generation_kw"))
            ) / 1000.0
            forecast.append(
                {
                    "hour": hour_label(timestamp),
                    "generation_mw": round(generation_mw, 3),
                    "probability": round(as_float(row.get("predicted_overload_probability")), 4),
                    "reverse_flow_kw": round(row_reverse_flow_kw, 2),
                    "reverse_flow_limit_kw": round(row_limit_kw, 2),
                }
            )

        payload.append(
            {
                "mv_line_id": mv_line_id,
                "location_id": peak_row.get("location_id", ""),
                "feeder_id": peak_row.get("feeder_id", ""),
                "coordinates": geometry["coordinates"],
                "voltage_v": geometry.get("voltage_v"),
                "power": geometry.get("power"),
                "operator_tag": geometry.get("operator_tag"),
                "name": geometry.get("name"),
                "is_official_tauron_topology": geometry.get("is_official_tauron_topology", False),
                "risk_score": round(max_probability * 100),
                "risk_level": ui_risk_level(max_probability),
                "max_probability": round(max_probability, 4),
                "peak_hour": hour_label(peak_row["timestamp"]) if peak_row.get("timestamp") else "00:00",
                "reverse_flow_kw": round(reverse_flow_kw, 2),
                "reverse_flow_limit_kw": round(limit_kw, 2),
                "utilization": round(min(1.5, utilization), 3),
                "overload_hours": overload_hours,
                "horizon_hours": len(sorted_rows),
                "forecast": forecast,
            }
        )

    payload.sort(key=lambda row: row["risk_score"], reverse=True)
    return payload


def build_dashboard_payload(location_records: list[dict[str, Any]], feeder_records: list[dict[str, Any]]) -> dict[str, Any]:
    timestamps = sorted({row["timestamp"] for row in location_records}, key=timestamp_key)[:24]
    timestamp_set = set(timestamps)
    location_rows = [row for row in location_records if row["timestamp"] in timestamp_set]
    feeder_rows = [row for row in feeder_records if row["timestamp"] in timestamp_set]

    feeder_by_location: dict[str, list[dict[str, Any]]] = defaultdict(list)
    feeder_by_timestamp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    feeder_by_location_timestamp: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in feeder_rows:
        location_id = row["location_id"]
        timestamp = row["timestamp"]
        feeder_by_location[location_id].append(row)
        feeder_by_timestamp[timestamp].append(row)
        feeder_by_location_timestamp[(location_id, timestamp)].append(row)

    hourly_generation = []
    for timestamp in timestamps:
        rows = feeder_by_timestamp[timestamp]
        solar_mw = sum(as_float(row.get("pv_generation_kw")) for row in rows) / 1000.0
        wind_mw = sum(as_float(row.get("wind_generation_kw")) for row in rows) / 1000.0
        hourly_generation.append(
            {
                "hour": hour_label(timestamp),
                "solar": round(solar_mw, 2),
                "wind": round(wind_mw, 2),
                "total": round(solar_mw + wind_mw, 2),
            }
        )

    location_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in location_rows:
        location_groups[row["location_id"]].append(row)

    locations = []
    risky_areas = []
    for location_id, rows in sorted(location_groups.items()):
        top_risk = max(rows, key=lambda row: as_float(row.get("max_overload_probability")))
        max_probability = as_float(top_risk.get("max_overload_probability"))
        risk_score = round(max_probability * 100)
        risk_level = ui_risk_level(max_probability)
        location_feeders = feeder_by_location[location_id]

        latitudes = [as_float(row.get("centroid_lat")) for row in location_feeders if row.get("centroid_lat")]
        longitudes = [as_float(row.get("centroid_lon")) for row in location_feeders if row.get("centroid_lon")]
        coordinates = [
            round(sum(latitudes) / len(latitudes), 6) if latitudes else 50.2945,
            round(sum(longitudes) / len(longitudes), 6) if longitudes else 18.6714,
        ]

        forecast = []
        peak_generation_mw = 0.0
        peak_hour = hour_label(timestamps[0]) if timestamps else "00:00"
        max_generation_kw = 0.0
        max_demand_kw = 0.0
        max_grid_constraint = 0.0
        max_overload_pct = 0

        for timestamp in timestamps:
            rows_for_timestamp = feeder_by_location_timestamp[(location_id, timestamp)]
            generation_kw = sum(
                as_float(row.get("pv_generation_kw")) + as_float(row.get("wind_generation_kw"))
                for row in rows_for_timestamp
            )
            demand_kw = sum(as_float(row.get("local_demand_kw")) for row in rows_for_timestamp)
            reverse_flow_kw = sum(as_float(row.get("reverse_flow_kw")) for row in rows_for_timestamp)
            reverse_flow_limit_kw = sum(as_float(row.get("reverse_flow_limit_kw")) for row in rows_for_timestamp)
            generation_mw = round(generation_kw / 1000.0, 2)
            forecast.append({"hour": hour_label(timestamp), "generation_mw": generation_mw})

            if generation_mw > peak_generation_mw:
                peak_generation_mw = generation_mw
                peak_hour = hour_label(timestamp)
            max_generation_kw = max(max_generation_kw, generation_kw)
            max_demand_kw = max(max_demand_kw, demand_kw)
            if reverse_flow_limit_kw > 0:
                max_grid_constraint = max(max_grid_constraint, reverse_flow_kw / reverse_flow_limit_kw)
            overload_pct = max(
                (round((as_float(row.get("overload_ratio")) - 1.0) * 100) for row in rows_for_timestamp),
                default=0,
            )
            max_overload_pct = max(max_overload_pct, overload_pct)

        oze_density = 0.0
        if max_generation_kw + max_demand_kw > 0:
            oze_density = min(1.0, max_generation_kw / (max_generation_kw + max_demand_kw))

        total_feeders = int(top_risk.get("total_feeder_count", 0))
        constrained_feeders = int(top_risk.get("predicted_overload_feeder_count", 0))
        locations.append(
            {
                "location_id": location_id,
                "name": display_name(location_id),
                "risk_score": risk_score,
                "risk_level": risk_level,
                "peak_hour": peak_hour,
                "peak_generation_mw": peak_generation_mw,
                "oze_density": round(oze_density, 2),
                "grid_constraint": round(min(1.0, max_grid_constraint), 2),
                "coordinates": coordinates,
                "forecast": forecast,
                "recommendations": recommendations_for(risk_level, constrained_feeders),
                "predicted_overload_feeder_count": constrained_feeders,
                "total_feeder_count": total_feeders,
            }
        )
        risky_areas.append(
            {
                "location": display_name(location_id),
                "risk_score": risk_score,
                "risk_level": risk_level,
                "peak_hour": peak_hour,
                "expected_overload": max(0, max_overload_pct),
            }
        )

    risky_areas.sort(key=lambda row: row["risk_score"], reverse=True)
    locations.sort(key=lambda row: row["risk_score"], reverse=True)

    mv_lines = build_mv_line_payload(feeder_rows)

    return {
        "generated_at": location_records[0].get("generated_at") if location_records else None,
        "source": "api_proxy_to_model_service",
        "horizon_hours": len(timestamps),
        "locations": locations,
        "hourly_generation": hourly_generation,
        "risky_areas": risky_areas[:5],
        "mv_lines": mv_lines,
    }


@app.get("/health")
async def health() -> dict[str, Any]:
    model_health = await model_get("/health")
    return {
        "status": "ok",
        "model_service_url": MODEL_SERVICE_URL,
        "model": model_health,
    }


@app.get("/predictions/locations")
async def location_predictions(
    input_path: str | None = Query(default=None, description="Optional feature table path inside the model container."),
) -> dict[str, Any]:
    params = {"input_path": input_path} if input_path else None
    return await model_get("/predictions/location", params=params)


@app.get("/predictions/feeders")
async def feeder_predictions(
    input_path: str | None = Query(default=None, description="Optional feature table path inside the model container."),
) -> dict[str, Any]:
    params = {"input_path": input_path} if input_path else None
    return await model_get("/predictions/feeder", params=params)


@app.get("/metrics")
async def metrics() -> dict[str, Any]:
    return await model_get("/metrics")


@app.get("/locations")
async def locations() -> dict[str, Any]:
    predictions = await model_get("/predictions/location")
    location_ids = sorted({record["location_id"] for record in predictions.get("records", [])})
    return {
        "count": len(location_ids),
        "records": [{"location_id": location_id} for location_id in location_ids],
    }


@app.get("/dashboard")
async def dashboard() -> dict[str, Any]:
    location_predictions, feeder_predictions = await asyncio.gather(
        model_get("/predictions/location"),
        model_get("/predictions/feeder"),
    )
    return build_dashboard_payload(
        location_records=location_predictions.get("records", []),
        feeder_records=feeder_predictions.get("records", []),
    )


@app.get("/mv_lines")
async def mv_lines(
    input_path: str | None = Query(default=None, description="Optional feature table path inside the model container."),
) -> dict[str, Any]:
    params = {"input_path": input_path} if input_path else None
    feeder_response = await model_get("/predictions/feeder", params=params)
    records = build_mv_line_payload(feeder_response.get("records", []))
    return {
        "generated_at": feeder_response.get("generated_at"),
        "count": len(records),
        "geometry_source": MV_LINE_GEOMETRY_PATH if Path(MV_LINE_GEOMETRY_PATH).exists() else MV_LINE_GEOMETRY_FALLBACK_PATH,
        "records": records,
    }
