#!/usr/bin/env python3
"""Run overload-probability inference and aggregate results per location."""

from __future__ import annotations

import argparse
import csv
import json
import os
import pickle
import warnings
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

logical_cpus = os.cpu_count() or 1
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(max(1, logical_cpus - 1)))
warnings.filterwarnings("ignore", category=UserWarning, module=r"joblib\.externals\.loky\.backend\.context")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return 0.0


def matrix(rows: list[dict[str, Any]], feature_columns: list[str]) -> np.ndarray:
    return np.array(
        [[as_float(row.get(column)) for column in feature_columns] for row in rows],
        dtype=np.float64,
    )


def risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "high"
    if probability >= 0.35:
        return "medium"
    return "low"


def generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_artifact(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return pickle.load(handle)


def feeder_predictions(
    rows: list[dict[str, Any]],
    probabilities: np.ndarray,
    threshold: float,
    generated_at_ts: str,
) -> list[dict[str, Any]]:
    output = []
    for row, probability in zip(rows, probabilities):
        probability_value = float(probability)
        output.append(
            {
                "generated_at": generated_at_ts,
                "timestamp": row.get("timestamp", ""),
                "location_id": row.get("location_id", ""),
                "feeder_id": row.get("feeder_id", ""),
                "mv_line_id": row.get("mv_line_id", ""),
                "centroid_lat": row.get("centroid_lat", ""),
                "centroid_lon": row.get("centroid_lon", ""),
                "predicted_overload_probability": round(probability_value, 6),
                "predicted_overload_event": int(probability_value >= threshold),
                "risk_level": risk_level(probability_value),
                "risk_score": round(probability_value * 100),
                "pv_generation_kw": row.get("pv_generation_kw", ""),
                "local_demand_kw": row.get("synthetic_local_demand_kw", ""),
                "reverse_flow_kw": row.get("reverse_flow_kw", ""),
                "reverse_flow_limit_kw": row.get("synthetic_reverse_flow_limit_kw", ""),
                "overload_ratio": row.get("overload_ratio", ""),
                "model_threshold": round(threshold, 4),
                "source_note": "model prediction from API-first features plus synthetic OSD context",
            }
        )
    return output


def aggregate_location_rows(feeder_rows: list[dict[str, Any]], generated_at_ts: str) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in feeder_rows:
        groups[(row["timestamp"], row["location_id"])].append(row)

    output = []
    for (timestamp, location_id), rows in sorted(groups.items()):
        probabilities = [as_float(row["predicted_overload_probability"]) for row in rows]
        events = [int(row["predicted_overload_event"]) for row in rows]
        top = max(rows, key=lambda row: as_float(row["predicted_overload_probability"]))
        high_count = sum(1 for row in rows if row["risk_level"] == "high")
        medium_count = sum(1 for row in rows if row["risk_level"] == "medium")
        max_probability = max(probabilities)
        output.append(
            {
                "generated_at": generated_at_ts,
                "timestamp": timestamp,
                "location_id": location_id,
                "max_overload_probability": round(max_probability, 6),
                "avg_overload_probability": round(sum(probabilities) / len(probabilities), 6),
                "predicted_overload_feeder_count": sum(events),
                "high_risk_feeder_count": high_count,
                "medium_risk_feeder_count": medium_count,
                "total_feeder_count": len(rows),
                "risk_level": risk_level(max_probability),
                "top_feeder_id": top["feeder_id"],
                "top_feeder_probability": top["predicted_overload_probability"],
                "top_feeder_reverse_flow_kw": top["reverse_flow_kw"],
                "top_feeder_limit_kw": top["reverse_flow_limit_kw"],
            }
        )
    return output


def write_location_json(
    path: Path,
    rows: list[dict[str, Any]],
    model_path: Path,
    input_path: Path,
    generated_at_ts: str,
) -> None:
    payload = {
        "generated_at": generated_at_ts,
        "model_path": str(model_path),
        "input_path": str(input_path),
        "prediction_level": "location",
        "records": rows,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="model/artifacts/overload_probability_model.pkl")
    parser.add_argument("--input", default="data/samples/model_training_gliwice_demo_test.csv")
    parser.add_argument("--output-dir", default="model/artifacts")
    parser.add_argument("--feeder-output", default="latest_feeder_predictions.csv")
    parser.add_argument("--location-output", default="latest_location_predictions.csv")
    parser.add_argument("--location-json-output", default="latest_location_predictions.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_path = Path(args.model)
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    artifact = load_artifact(model_path)
    rows = read_csv(input_path)
    feature_columns = artifact["feature_columns"]
    threshold = float(artifact["threshold"])

    probabilities = np.clip(artifact["model"].predict(matrix(rows, feature_columns)), 0.0, 1.0)
    generated_at_ts = generated_at()
    feeder_rows = feeder_predictions(rows, probabilities, threshold, generated_at_ts)
    location_rows = aggregate_location_rows(feeder_rows, generated_at_ts)

    feeder_fieldnames = list(feeder_rows[0].keys()) if feeder_rows else []
    location_fieldnames = list(location_rows[0].keys()) if location_rows else []
    feeder_path = output_dir / args.feeder_output
    location_path = output_dir / args.location_output
    location_json_path = output_dir / args.location_json_output

    write_csv(feeder_path, feeder_fieldnames, feeder_rows)
    write_csv(location_path, location_fieldnames, location_rows)
    write_location_json(location_json_path, location_rows, model_path, input_path, generated_at_ts)

    max_probability = max((as_float(row["max_overload_probability"]) for row in location_rows), default=0.0)
    high_locations = sum(1 for row in location_rows if row["risk_level"] == "high")
    print(
        f"Predicted {len(feeder_rows)} feeder rows and {len(location_rows)} location rows. "
        f"max_location_probability={max_probability:.4f}, high_location_rows={high_locations}. "
        f"Outputs: {feeder_path}, {location_path}, {location_json_path}"
    )


if __name__ == "__main__":
    main()
