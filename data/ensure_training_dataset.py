#!/usr/bin/env python3
"""Regenerate the training dataset + splits if they are missing.

Idempotent bootstrap: if the split CSVs exist, it returns immediately.
Otherwise it runs data/generate_training_dataset.py and
data/split_training_dataset.py with their defaults.

The three inputs (synthetic_mv_feeders_gliwice.csv, pvgis_profile_gliwice.csv,
weather_hourly_gliwice_demo.csv) are tracked in git, so this works on a fresh
clone without any extra setup.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SAMPLES_DIR = Path("data/samples")
FULL_DATASET = SAMPLES_DIR / "model_training_gliwice_demo.csv"
SPLIT_PREFIX = "model_training_gliwice_demo"
SPLIT_SUFFIXES = ("_train.csv", "_validation.csv", "_test.csv")

REQUIRED_INPUTS = (
    SAMPLES_DIR / "synthetic_mv_feeders_gliwice.csv",
    SAMPLES_DIR / "pvgis_profile_gliwice.csv",
    SAMPLES_DIR / "weather_hourly_gliwice_demo.csv",
)


def split_paths() -> list[Path]:
    return [SAMPLES_DIR / f"{SPLIT_PREFIX}{suffix}" for suffix in SPLIT_SUFFIXES]


def splits_present() -> bool:
    return all(path.exists() for path in split_paths())


def run(cmd: list[str]) -> None:
    print(f"[ensure_training_dataset] running: {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True)


def ensure_training_dataset(force: bool = False) -> bool:
    """Return True if regeneration happened, False if nothing to do."""
    if not force and splits_present():
        return False

    missing_inputs = [str(p) for p in REQUIRED_INPUTS if not p.exists()]
    if missing_inputs:
        raise FileNotFoundError(
            "Cannot regenerate training dataset — missing tracked inputs: "
            + ", ".join(missing_inputs)
        )

    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    if force or not FULL_DATASET.exists():
        run([sys.executable, "-m", "data.generate_training_dataset"])

    run([sys.executable, "-m", "data.split_training_dataset"])
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even if split CSVs already exist.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    regenerated = ensure_training_dataset(force=args.force)
    if regenerated:
        print("[ensure_training_dataset] done.", flush=True)
    else:
        print("[ensure_training_dataset] split CSVs already present, skipping.", flush=True)


if __name__ == "__main__":
    main()
