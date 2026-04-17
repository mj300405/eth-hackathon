#!/usr/bin/env python3
"""Fetch PVGIS hourly PV production profile for a point.

PVGIS is used here as a public reference generator for PV production shape.
The downloaded profile is not Tauron/prosumer measurement data.
"""

from __future__ import annotations

import argparse
import csv
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PVGIS_URL = "https://re.jrc.ec.europa.eu/api/v5_3/seriescalc"


def fetch_pvgis(
    lat: float,
    lon: float,
    year: int,
    peakpower_kwp: float,
    loss_pct: float,
    angle_deg: float,
    aspect_deg: float,
) -> dict[str, Any]:
    params = {
        "lat": lat,
        "lon": lon,
        "startyear": year,
        "endyear": year,
        "pvcalculation": 1,
        "peakpower": peakpower_kwp,
        "loss": loss_pct,
        "angle": angle_deg,
        "aspect": aspect_deg,
        "outputformat": "json",
    }
    url = PVGIS_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "gridflex-oze-mvp/0.1"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_pvgis_time(value: str) -> str:
    parsed = datetime.strptime(value, "%Y%m%d:%H%M")
    return parsed.replace(tzinfo=timezone.utc).isoformat()


def hourly_rows(payload: dict[str, Any], limit: int, sample_date: str) -> list[dict[str, Any]]:
    rows = []
    selected = [
        item
        for item in payload["outputs"]["hourly"]
        if item["time"].startswith(sample_date.replace("-", ""))
    ]
    if not selected:
        selected = payload["outputs"]["hourly"]

    for item in selected[:limit]:
        rows.append(
            {
                "timestamp": parse_pvgis_time(item["time"]),
                "pv_kw_per_kwp": round(float(item["P"]) / 1000, 6),
                "global_irradiance_wm2": item.get("G(i)", ""),
                "sun_height_deg": item.get("H_sun", ""),
                "temperature_c": item.get("T2m", ""),
                "wind_speed_ms": item.get("WS10m", ""),
                "source": "PVGIS JRC seriescalc",
                "source_url": PVGIS_URL,
                "data_kind": "reference_profile",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "timestamp",
        "pv_kw_per_kwp",
        "global_irradiance_wm2",
        "sun_height_deg",
        "temperature_c",
        "wind_speed_ms",
        "source",
        "source_url",
        "data_kind",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, default=50.2945)
    parser.add_argument("--lon", type=float, default=18.6714)
    parser.add_argument("--year", type=int, default=2020)
    parser.add_argument("--peakpower-kwp", type=float, default=1.0)
    parser.add_argument("--loss-pct", type=float, default=14.0)
    parser.add_argument("--angle-deg", type=float, default=35.0)
    parser.add_argument("--aspect-deg", type=float, default=0.0)
    parser.add_argument("--sample-date", default="2020-04-18", help="Date to sample from the PVGIS year.")
    parser.add_argument("--limit-hours", type=int, default=24)
    parser.add_argument("--output", default="data/samples/pvgis_profile_gliwice.csv")
    parser.add_argument("--raw-output", default="data/raw/pvgis_gliwice_2020.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = fetch_pvgis(
        lat=args.lat,
        lon=args.lon,
        year=args.year,
        peakpower_kwp=args.peakpower_kwp,
        loss_pct=args.loss_pct,
        angle_deg=args.angle_deg,
        aspect_deg=args.aspect_deg,
    )

    raw_output = Path(args.raw_output)
    raw_output.parent.mkdir(parents=True, exist_ok=True)
    raw_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = hourly_rows(payload, args.limit_hours, args.sample_date)
    write_csv(Path(args.output), rows)
    print(f"Saved {len(rows)} PVGIS hourly rows to {args.output}")


if __name__ == "__main__":
    main()
