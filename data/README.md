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
- `mv_line_geometries.geojson` - publiczne/proxy geometrie linii sredniego napiecia z BDOT10k albo OSM,
- `synthetic_mv_feeders.csv` - syntetyczne feedery SN zbudowane na publicznej geometrii linii,
- `pv_installation_assumptions.csv` - jawne zalozenia mocy i geometrii instalacji PV, dostepne jako probka w `data/samples/`,
- `weather_hourly.csv` - pogoda godzinowa z IMGW-PIB albo zatwierdzonego dostawcy meteo,
- `generation_forecast.csv` - symulowana prognoza PV/wiatr dla feederow SN,
- `synthetic_grid_constraints.csv` - jawnie syntetyczne scenariusze przeciazen/ograniczen,
- `tauron_flexibility_context.csv` - publiczny kontekst z map elastycznosci Taurona, nie etykiety realnych przeciazen,
- `tauron_connection_capacity.csv` - publiczne moce przylaczeniowe Taurona,
- `demand_proxy.csv` - demonstracyjny profil popytu lokalnego,
- `grid_proxy.csv` - polaczone proxy sieciowe dla lokalizacji,
- `risk_hourly.csv` - wynikowy risk score.

Open-Meteo, NASA POWER i podobne serwisy moga byc uzyte do szybkiego developmentu, ale nie jako glowne zrodlo danych pogodowych dla wersji prezentowanej OSD.

Geometrie linii SN z BDOT10k/OSM traktujemy jako publiczny proxy przebiegu linii, a nie oficjalna topologie Tauron Dystrybucja. Limity, obciazenia, generacja lokalna i przeciazenia pozostaja syntetyczne w MVP.

W `data/samples/mv_line_geometries_gliwice_sample.geojson` jest mala probka publicznych linii SN pobrana z OSM/Overpass dla obszaru Gliwic. Pelny lokalny wynik testu moze lezec w `data/processed/`, ale nie powinien byc commitowany jako duzy plik.
