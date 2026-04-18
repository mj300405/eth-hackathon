#!/usr/bin/env python3
"""Train a tabular overload-probability baseline.

The model predicts `target_overload_probability` from API-first forecast
features and the minimal synthetic OSD context. It also reports event metrics
against `target_overload_event`.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import pickle
import warnings
from pathlib import Path
from typing import Any

logical_cpus = os.cpu_count() or 1
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(max(1, logical_cpus - 1)))
warnings.filterwarnings("ignore", message="Could not find the number of physical cores.*")
warnings.filterwarnings("ignore", category=UserWarning, module=r"joblib\.externals\.loky\.backend\.context")

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor


FEATURE_COLUMNS = [
    "area_type_id",
    "hour",
    "day_of_week",
    "is_weekend",
    "month",
    "centroid_lat",
    "centroid_lon",
    "line_length_km",
    "pv_kw_per_kwp",
    "global_irradiance_wm2",
    "temperature_c",
    "wind_speed_ms",
    "cloud_cover_pct",
    "solar_radiation_wm2",
    "synthetic_pv_capacity_kwp",
    "synthetic_wind_capacity_kw",
    "synthetic_base_demand_kw",
    "synthetic_local_demand_kw",
    "synthetic_reverse_flow_limit_kw",
    "oze_density_index",
    "pv_generation_kw",
    "wind_generation_kw",
    "reverse_flow_kw",
]

IDENTITY_COLUMNS = [
    "timestamp",
    "location_id",
    "feeder_id",
    "split",
]


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


def target_probability(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.array([as_float(row["target_overload_probability"]) for row in rows], dtype=np.float64)


def target_event(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.array([int(as_float(row["target_overload_event"])) for row in rows], dtype=np.int64)


def clipped_predictions(values: np.ndarray) -> np.ndarray:
    return np.clip(values, 0.0, 1.0)


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    error = y_pred - y_true
    mae = float(np.mean(np.abs(error)))
    rmse = float(math.sqrt(np.mean(error**2)))
    return {
        "mae_probability": round(mae, 6),
        "rmse_probability": round(rmse, 6),
    }


def event_metrics(y_event: np.ndarray, y_pred_probability: np.ndarray, threshold: float) -> dict[str, float]:
    predicted_event = (y_pred_probability >= threshold).astype(np.int64)
    tp = int(np.sum((predicted_event == 1) & (y_event == 1)))
    fp = int(np.sum((predicted_event == 1) & (y_event == 0)))
    tn = int(np.sum((predicted_event == 0) & (y_event == 0)))
    fn = int(np.sum((predicted_event == 0) & (y_event == 1)))

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = (tp + tn) / len(y_event) if len(y_event) else 0.0
    brier = float(np.mean((y_pred_probability - y_event) ** 2)) if len(y_event) else 0.0

    return {
        "threshold": round(threshold, 4),
        "event_rate": round(float(np.mean(y_event)), 6) if len(y_event) else 0.0,
        "predicted_event_rate": round(float(np.mean(predicted_event)), 6) if len(y_event) else 0.0,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "accuracy": round(accuracy, 6),
        "brier_event": round(brier, 6),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
    }


def choose_threshold(y_event: np.ndarray, y_pred_probability: np.ndarray) -> float:
    best_threshold = 0.5
    best_f1 = -1.0
    for threshold in np.arange(0.05, 0.96, 0.01):
        f1 = event_metrics(y_event, y_pred_probability, float(threshold))["f1"]
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = float(threshold)
    return best_threshold


def prediction_rows(
    rows: list[dict[str, Any]],
    y_probability: np.ndarray,
    y_event: np.ndarray,
    y_pred_probability: np.ndarray,
    threshold: float,
) -> list[dict[str, Any]]:
    output = []
    for row, target_prob, target_evt, pred_prob in zip(rows, y_probability, y_event, y_pred_probability):
        predicted_event = int(pred_prob >= threshold)
        output.append(
            {
                **{column: row.get(column, "") for column in IDENTITY_COLUMNS},
                "target_overload_probability": round(float(target_prob), 6),
                "predicted_overload_probability": round(float(pred_prob), 6),
                "target_overload_event": int(target_evt),
                "predicted_overload_event": predicted_event,
                "absolute_probability_error": round(abs(float(pred_prob) - float(target_prob)), 6),
            }
        )
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/samples/model_training_gliwice_demo_train.csv")
    parser.add_argument("--validation", default="data/samples/model_training_gliwice_demo_validation.csv")
    parser.add_argument("--test", default="data/samples/model_training_gliwice_demo_test.csv")
    parser.add_argument("--output-dir", default="model/artifacts")
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_rows = read_csv(Path(args.train))
    validation_rows = read_csv(Path(args.validation))
    test_rows = read_csv(Path(args.test))

    x_train = matrix(train_rows, FEATURE_COLUMNS)
    y_train = target_probability(train_rows)

    model = HistGradientBoostingRegressor(
        max_iter=500,
        learning_rate=0.08,
        max_leaf_nodes=7,
        l2_regularization=0.03,
        random_state=args.random_state,
    )
    model.fit(x_train, y_train)

    split_payloads = {
        "train": train_rows,
        "validation": validation_rows,
        "test": test_rows,
    }
    predictions: dict[str, np.ndarray] = {}
    probabilities: dict[str, np.ndarray] = {}
    events: dict[str, np.ndarray] = {}

    for split, rows in split_payloads.items():
        predictions[split] = clipped_predictions(model.predict(matrix(rows, FEATURE_COLUMNS)))
        probabilities[split] = target_probability(rows)
        events[split] = target_event(rows)

    threshold = choose_threshold(events["validation"], predictions["validation"])

    metrics = {
        "model_type": "HistGradientBoostingRegressor",
        "target": "target_overload_probability",
        "event_target": "target_overload_event",
        "feature_columns": FEATURE_COLUMNS,
        "threshold_selected_on": "validation_f1",
        "selected_threshold": round(threshold, 4),
        "splits": {},
    }
    for split in split_payloads:
        metrics["splits"][split] = {
            **regression_metrics(probabilities[split], predictions[split]),
            **event_metrics(events[split], predictions[split], threshold),
            "rows": len(split_payloads[split]),
        }

    artifact = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "threshold": threshold,
        "metrics": metrics,
    }
    with (output_dir / "overload_probability_model.pkl").open("wb") as handle:
        pickle.dump(artifact, handle)

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    prediction_fieldnames = [
        *IDENTITY_COLUMNS,
        "target_overload_probability",
        "predicted_overload_probability",
        "target_overload_event",
        "predicted_overload_event",
        "absolute_probability_error",
    ]
    write_csv(
        output_dir / "validation_predictions.csv",
        prediction_fieldnames,
        prediction_rows(
            validation_rows,
            probabilities["validation"],
            events["validation"],
            predictions["validation"],
            threshold,
        ),
    )
    write_csv(
        output_dir / "test_predictions.csv",
        prediction_fieldnames,
        prediction_rows(
            test_rows,
            probabilities["test"],
            events["test"],
            predictions["test"],
            threshold,
        ),
    )

    validation = metrics["splits"]["validation"]
    test = metrics["splits"]["test"]
    print(
        "Trained overload probability model. "
        f"threshold={threshold:.2f}, "
        f"validation_mae={validation['mae_probability']:.4f}, "
        f"validation_f1={validation['f1']:.4f}, "
        f"test_mae={test['mae_probability']:.4f}, "
        f"test_f1={test['f1']:.4f}. "
        f"Artifacts: {output_dir}"
    )


if __name__ == "__main__":
    main()
