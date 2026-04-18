"""Public API service for the GridFlex OZE demo."""

from __future__ import annotations

import os
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
