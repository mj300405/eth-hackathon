# Dane

Ten katalog jest przeznaczony na dane lokalne uzywane w demo.

Proponowana struktura:

```text
data/
├── raw/        # dane pobrane z API bez zmian
├── processed/  # dane oczyszczone i polaczone
└── samples/    # male probki do demo i testow
```

## Zasady

- Nie commitowac duzych plikow.
- Nie commitowac danych osobowych.
- Probki demo trzymac male i opisane.
- Przy kazdym zbiorze zapisac zrodlo i date pobrania.

## Minimalne pliki demo

Na start warto dodac:

- `locations.csv` - lokalizacje oddzialow Tauron Dystrybucja,
- `pv_installation_assumptions.csv` - jawne zalozenia mocy i geometrii instalacji PV, dostepne jako probka w `data/samples/`,
- `weather_hourly.csv` - pogoda godzinowa,
- `generation_forecast.csv` - prognoza PV/wiatr,
- `tauron_flexibility_constraints.csv` - publiczne proxy ograniczen sieciowych z map elastycznosci Taurona,
- `tauron_connection_capacity.csv` - publiczne moce przylaczeniowe Taurona,
- `demand_proxy.csv` - demonstracyjny profil popytu lokalnego,
- `grid_proxy.csv` - polaczone proxy sieciowe dla lokalizacji,
- `risk_hourly.csv` - wynikowy risk score.
