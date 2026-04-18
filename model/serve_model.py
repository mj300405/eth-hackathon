#!/usr/bin/env python3
"""HTTP service for overload-probability model inference."""

from __future__ import annotations

import os
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException, Query

from model.predict_overload import (
    aggregate_location_rows,
    feeder_predictions,
    generated_at,
    load_artifact,
    matrix,
    read_csv,
)


MODEL_PATH = Path(os.getenv("MODEL_ARTIFACT_PATH", "model/artifacts/overload_probability_model.pkl"))
DEFAULT_INPUT_PATH = Path(os.getenv("MODEL_DEFAULT_INPUT", "data/samples/model_training_gliwice_demo_test.csv"))
TRAIN_ON_STARTUP = os.getenv("MODEL_TRAIN_ON_STARTUP", "true").lower() == "true"
model_artifact: dict[str, Any] | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_model()
    yield


app = FastAPI(
    title="GridFlex OZE Model Service",
    description="Serves overload probability predictions per feeder and location.",
    version="0.1.0",
    lifespan=lifespan,
)


def train_model_if_needed() -> None:
    if MODEL_PATH.exists() or not TRAIN_ON_STARTUP:
        return
    subprocess.run(
        [sys.executable, "-m", "model.train_overload_model", "--output-dir", str(MODEL_PATH.parent)],
        check=True,
    )


def load_model() -> None:
    global model_artifact
    train_model_if_needed()
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model artifact not found: {MODEL_PATH}")
    model_artifact = load_artifact(MODEL_PATH)


def artifact() -> dict[str, Any]:
    if model_artifact is None:
        raise HTTPException(status_code=503, detail="Model artifact is not loaded.")
    return model_artifact


def resolve_input_path(input_path: str | None) -> Path:
    path = Path(input_path) if input_path else DEFAULT_INPUT_PATH
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Input feature table not found: {path}")
    return path


def predict(input_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    current_artifact = artifact()
    rows = read_csv(input_path)
    if not rows:
        raise HTTPException(status_code=400, detail=f"Input feature table is empty: {input_path}")

    feature_columns = current_artifact["feature_columns"]
    threshold = float(current_artifact["threshold"])
    probabilities = np.clip(current_artifact["model"].predict(matrix(rows, feature_columns)), 0.0, 1.0)
    generated_at_ts = generated_at()
    feeder_rows = feeder_predictions(rows, probabilities, threshold, generated_at_ts)
    location_rows = aggregate_location_rows(feeder_rows, generated_at_ts)
    return feeder_rows, location_rows, generated_at_ts


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "model_loaded": model_artifact is not None,
        "model_path": str(MODEL_PATH),
        "default_input_path": str(DEFAULT_INPUT_PATH),
        "train_on_startup": TRAIN_ON_STARTUP,
    }


@app.post("/reload")
def reload_model() -> dict[str, Any]:
    load_model()
    return health()


@app.get("/predictions/location")
def location_predictions(
    input_path: str | None = Query(default=None, description="Optional CSV feature table path inside the container."),
) -> dict[str, Any]:
    resolved_input = resolve_input_path(input_path)
    _, location_rows, generated_at_ts = predict(resolved_input)
    return {
        "generated_at": generated_at_ts,
        "model_path": str(MODEL_PATH),
        "input_path": str(resolved_input),
        "prediction_level": "location",
        "count": len(location_rows),
        "records": location_rows,
    }


@app.get("/predictions/feeder")
def feeder_predictions_endpoint(
    input_path: str | None = Query(default=None, description="Optional CSV feature table path inside the container."),
) -> dict[str, Any]:
    resolved_input = resolve_input_path(input_path)
    feeder_rows, _, generated_at_ts = predict(resolved_input)
    return {
        "generated_at": generated_at_ts,
        "model_path": str(MODEL_PATH),
        "input_path": str(resolved_input),
        "prediction_level": "feeder",
        "count": len(feeder_rows),
        "records": feeder_rows,
    }


@app.get("/metrics")
def metrics() -> dict[str, Any]:
    current_artifact = artifact()
    return current_artifact.get("metrics", {})
