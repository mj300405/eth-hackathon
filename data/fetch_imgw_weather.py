#!/usr/bin/env python3
"""Fetch trusted public weather observations from IMGW-PIB API.

This script writes a small CSV in the `weather_hourly` schema used by the POC.
For Gliwice we use the nearest available synoptic station from the public API:
Katowice. This is official IMGW-PIB public data, not a synthetic weather row.
"""

from __future__ import annotations

import argparse
import csv
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


IMGW_SYNOP_STATION_URL = "https://danepubliczne.imgw.pl/api/data/synop/station/{station}"
WARSAW_TZ = timezone(timedelta(hours=2))


def fetch_station(station: str) -> dict[str, Any]:
    url = IMGW_SYNOP_STATION_URL.format(station=station)
    request = urllib.request.Request(url, headers={"User-Agent": "gridflex-oze-mvp/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def measurement_timestamp(row: dict[str, Any]) -> datetime:
    date = row["data_pomiaru"]
    hour = int(row["godzina_pomiaru"])
    return datetime.fromisoformat(f"{date}T{hour:02d}:00:00").replace(tzinfo=WARSAW_TZ)


def to_weather_row(row: dict[str, Any], location_id: str, station_slug: str) -> dict[str, Any]:
    timestamp = measurement_timestamp(row)
    temperature = parse_float(row.get("temperatura"))
    wind_speed_kmh = parse_float(row.get("predkosc_wiatru"))
    precipitation = parse_float(row.get("suma_opadu"))

    return {
        "timestamp": timestamp.isoformat(),
        "location_id": location_id,
        "temperature_c": "" if temperature is None else temperature,
        "wind_speed_ms": "" if wind_speed_kmh is None else round(wind_speed_kmh / 3.6, 3),
        "wind_direction_deg": row.get("kierunek_wiatru", ""),
        "relative_humidity_pct": row.get("wilgotnosc_wzgledna", ""),
        "precipitation_mm": "" if precipitation is None else precipitation,
        "pressure_hpa": row.get("cisnienie", ""),
        "cloud_cover_pct": "",
        "solar_radiation_wm2": "",
        "source": "IMGW-PIB public synop API",
        "source_station": row.get("stacja", station_slug),
        "source_station_id": row.get("id_stacji", ""),
        "source_url": IMGW_SYNOP_STATION_URL.format(station=station_slug),
        "fetched_at": datetime.now(WARSAW_TZ).replace(microsecond=0).isoformat(),
        "data_kind": "observation",
        "trust_status": "official_public_imgw",
    }


def write_csv(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "timestamp",
        "location_id",
        "temperature_c",
        "wind_speed_ms",
        "wind_direction_deg",
        "relative_humidity_pct",
        "precipitation_mm",
        "pressure_hpa",
        "cloud_cover_pct",
        "solar_radiation_wm2",
        "source",
        "source_station",
        "source_station_id",
        "source_url",
        "fetched_at",
        "data_kind",
        "trust_status",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--station", default="katowice", help="IMGW station slug.")
    parser.add_argument("--location-id", default="gliwice", help="POC location id.")
    parser.add_argument(
        "--output",
        default="data/samples/weather_hourly_gliwice_imgw.csv",
        help="Output CSV path.",
    )
    parser.add_argument(
        "--raw-output",
        default="data/raw/imgw_synop_katowice_latest.json",
        help="Raw JSON output path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = fetch_station(args.station)

    raw_output = Path(args.raw_output)
    raw_output.parent.mkdir(parents=True, exist_ok=True)
    raw_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    weather_row = to_weather_row(payload, args.location_id, args.station)
    write_csv(Path(args.output), weather_row)
    print(f"Saved IMGW weather row for {weather_row['source_station']} to {args.output}")


if __name__ == "__main__":
    main()
