#!/usr/bin/env python3
"""Create time-based train/validation/test splits for the ML dataset.

For hourly forecasting, a random split would leak very similar timestamps across
train and test. This script splits by ordered unique timestamps, keeping all
feeders for the same hour in the same split.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


SPLIT_ORDER = ("train", "validation", "test")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)


def split_counts(total_timestamps: int, train_ratio: float, validation_ratio: float) -> tuple[int, int, int]:
    if total_timestamps < 3:
        raise ValueError("Need at least 3 unique timestamps to create train/validation/test splits.")
    if not 0 < train_ratio < 1:
        raise ValueError("--train-ratio must be between 0 and 1.")
    if not 0 < validation_ratio < 1:
        raise ValueError("--validation-ratio must be between 0 and 1.")
    if train_ratio + validation_ratio >= 1:
        raise ValueError("--train-ratio plus --validation-ratio must be below 1.")

    train_count = max(1, round(total_timestamps * train_ratio))
    validation_count = max(1, round(total_timestamps * validation_ratio))
    test_count = total_timestamps - train_count - validation_count
    if test_count < 1:
        test_count = 1
        validation_count = max(1, total_timestamps - train_count - test_count)
    return train_count, validation_count, test_count


def assign_splits(
    rows: list[dict[str, Any]],
    train_ratio: float,
    validation_ratio: float,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    unique_timestamps = sorted({row["timestamp"] for row in rows}, key=parse_timestamp)
    train_count, validation_count, _ = split_counts(len(unique_timestamps), train_ratio, validation_ratio)

    train_timestamps = set(unique_timestamps[:train_count])
    validation_timestamps = set(unique_timestamps[train_count : train_count + validation_count])
    split_by_timestamp = {
        timestamp: "train"
        for timestamp in train_timestamps
    }
    split_by_timestamp.update({timestamp: "validation" for timestamp in validation_timestamps})
    split_by_timestamp.update(
        {
            timestamp: "test"
            for timestamp in unique_timestamps[train_count + validation_count :]
        }
    )

    split_rows = {split: [] for split in SPLIT_ORDER}
    for row in rows:
        split = split_by_timestamp[row["timestamp"]]
        row_with_split = dict(row)
        row_with_split["split"] = split
        split_rows[split].append(row_with_split)

    return split_rows, split_by_timestamp


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def split_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "rows": 0,
            "timestamps": 0,
            "start_timestamp": "",
            "end_timestamp": "",
            "target_event_count": 0,
            "target_event_rate": 0,
            "avg_target_overload_probability": 0,
            "risk_level_counts": {},
        }

    timestamps = sorted({row["timestamp"] for row in rows}, key=parse_timestamp)
    event_count = sum(int(row.get("target_overload_event", 0)) for row in rows)
    probabilities = [as_float(row.get("target_overload_probability")) for row in rows]
    risk_counts = Counter(row.get("risk_level", "") for row in rows)
    return {
        "rows": len(rows),
        "timestamps": len(timestamps),
        "start_timestamp": timestamps[0],
        "end_timestamp": timestamps[-1],
        "target_event_count": event_count,
        "target_event_rate": round(event_count / len(rows), 4),
        "avg_target_overload_probability": round(sum(probabilities) / len(probabilities), 4),
        "risk_level_counts": dict(sorted(risk_counts.items())),
    }


def write_metadata(
    path: Path,
    input_path: Path,
    split_rows: dict[str, list[dict[str, Any]]],
    train_ratio: float,
    validation_ratio: float,
) -> None:
    metadata = {
        "input": str(input_path),
        "split_strategy": "time_ordered_unique_timestamp",
        "reason": "avoid leakage between neighboring hourly observations and feeder rows from the same hour",
        "ratios": {
            "train": train_ratio,
            "validation": validation_ratio,
            "test": round(1 - train_ratio - validation_ratio, 6),
        },
        "target_columns": ["target_overload_probability", "target_overload_event"],
        "splits": {split: split_summary(rows) for split, rows in split_rows.items()},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/samples/model_training_gliwice_demo.csv")
    parser.add_argument("--output-dir", default="data/samples")
    parser.add_argument("--output-prefix", default="model_training_gliwice_demo")
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--validation-ratio", type=float, default=0.15)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    rows = read_csv(input_path)
    if not rows:
        raise ValueError(f"No rows found in {input_path}")

    split_rows, _ = assign_splits(rows, args.train_ratio, args.validation_ratio)
    output_dir = Path(args.output_dir)
    fieldnames = list(rows[0].keys()) + ["split"]

    for split in SPLIT_ORDER:
        write_csv(output_dir / f"{args.output_prefix}_{split}.csv", fieldnames, split_rows[split])

    metadata_path = output_dir / f"{args.output_prefix}_splits.json"
    write_metadata(metadata_path, input_path, split_rows, args.train_ratio, args.validation_ratio)

    summary = {split: split_summary(split_rows[split]) for split in SPLIT_ORDER}
    print(
        "Created time-based splits: "
        + ", ".join(
            f"{split}={summary[split]['rows']} rows/{summary[split]['target_event_count']} events"
            for split in SPLIT_ORDER
        )
        + f"; metadata={metadata_path}"
    )


if __name__ == "__main__":
    main()
