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

## API i zrodla uzyte teraz

Aktualna probka POC korzysta z trzech publicznych zrodel/API:

- `data/fetch_imgw_weather.py` pobiera oficjalna publiczna obserwacje z IMGW-PIB public synop API.
- `data/fetch_pvgis.py` pobiera referencyjny profil PV z PVGIS/JRC `seriescalc` API.
- `data/fetch_mv_lines.py` pobiera publiczne/proxy geometrie linii SN z OSM/Overpass API.

Tauron dostepne moce, Tauron uslugi elastycznosci, PSE, URE i GUS/TERYT sa opisane jako kolejne zrodla kontekstowe, ale nie sa jeszcze uzyte w aktualnej probce POC.

## Skrypty generowania danych

| Skrypt | Co robi | Typ danych |
|---|---|---|
| `data/fetch_imgw_weather.py` | pobiera obserwacje meteo IMGW-PIB dla stacji Katowice jako najblizszy publiczny synop dla POC Gliwice | realne publiczne API |
| `data/fetch_pvgis.py` | pobiera godzinowy profil PVGIS/JRC dla Gliwic i zapisuje produkcje w `pv_kw_per_kwp` | realne publiczne API |
| `data/fetch_mv_lines.py` | pobiera publiczne/proxy przebiegi linii SN z OSM/Overpass dla podanego bbox | realne publiczne API/proxy |
| `data/build_sample_datasets.py` | buduje kompletna probke POC: feedery, projekcje meteo, generacje PV, popyt, limity, przeciazenia i risk score | API-first + minimalna syntetyka OSD |
| `data/generate_training_dataset.py` | buduje plaski dataset ML z cechami, `target_overload_probability` i `target_overload_event` | API-first + syntetyczny target OSD |
| `data/split_training_dataset.py` | tworzy czasowy podzial train/validation/test bez mieszania tych samych godzin miedzy zbiorami | walidacja modelu |

`build_sample_datasets.py` nie wymysla recznie etykiet ryzyka. Liczy je deterministycznie z danych wejsciowych:

```text
pv_generation_kw = pvgis_kw_per_kwp * synthetic_pv_capacity_kwp
reverse_flow_kw = max(0, pv_generation_kw - synthetic_local_demand_kw)
overload_kw = max(0, reverse_flow_kw - synthetic_reverse_flow_limit_kw)
```

Syntetyczne sa tylko brakujace dane OSD: moc PV przypisana do feedera, lokalny popyt i limit przeplywu zwrotnego. Geometria feedera pochodzi z publicznego/proxy OSM, ksztalt generacji z PVGIS, a seed meteo z IMGW-PIB.

Do trenowania modelu prawdopodobienstwa przeciazenia uzywamy:

```bash
python3 data/generate_training_dataset.py
```

Domyslnie powstaje `data/samples/model_training_gliwice_demo.csv` z 30 dniami danych godzinowych dla 5 feederow. Target `target_overload_probability` jest syntetyczny, ale liczony z fizycznie zrozumialych zmiennych: generacji PV, lokalnego popytu i limitu przeplywu zwrotnego. Jesli lokalnie jest pelny surowy plik PVGIS, mozna wygenerowac dataset z rocznego profilu:

```bash
python3 data/generate_training_dataset.py \
  --pvgis-raw data/raw/pvgis_gliwice_2020.json \
  --days 90
```

Po wygenerowaniu datasetu ML robimy czasowy split:

```bash
python3 data/split_training_dataset.py
```

Domyslny podzial to 70/15/15 po unikalnych timestampach:

- `data/samples/model_training_gliwice_demo_train.csv` - trening,
- `data/samples/model_training_gliwice_demo_validation.csv` - walidacja i dobor progow/modelu,
- `data/samples/model_training_gliwice_demo_test.csv` - finalny test,
- `data/samples/model_training_gliwice_demo_splits.json` - metadane splitu, zakres dat i liczba zdarzen.

Nie robimy losowego splitu, bo w predykcji godzinowej mieszalby sasiednie godziny i feedery z tej samej godziny miedzy train/test.

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

## Aktualna probka POC: Gliwice

Pierwszy kompletny, maly dataset demonstracyjny jest oparty o Gliwice:

- `mv_line_geometries_gliwice_sample.geojson` - 5 publicznych/proxy odcinkow linii SN z OSM.
- `synthetic_mv_feeders_gliwice.csv` - 5 syntetycznych feederow SN z limitami i mocami demo.
- `pv_orientation_mix_gliwice.csv` - syntetyczny miks orientacji PV per feeder.
- `weather_hourly_gliwice_imgw.csv` - oficjalna publiczna obserwacja IMGW-PIB ze stacji Katowice dla POC Gliwice.
- `weather_hourly_gliwice_demo.csv` - 24 godziny projekcji demo opartej o obserwacje IMGW-PIB; promieniowanie i zachmurzenie sa nadal modelowane do POC.
- `pvgis_profile_gliwice.csv` - publiczny profil PVGIS/JRC dla Gliwic, uzyty jako ksztalt produkcji PV.
- `generation_forecast_gliwice_demo.csv` - 24h generacji PV per feeder, skalowanej z profilu PVGIS.
- `demand_proxy_gliwice_demo.csv` - 24h syntetycznego popytu per feeder.
- `synthetic_grid_constraints_gliwice_demo.csv` - 24h syntetycznych ograniczen/przeciazen.
- `risk_hourly_gliwice_demo.csv` - wynikowy risk score per feeder i godzina.

Pliki mozna odtworzyc komenda:

```bash
python3 data/fetch_imgw_weather.py
python3 data/fetch_pvgis.py
python3 data/build_sample_datasets.py
```

Pelne odswiezenie publicznych/proxy linii SN z Overpass dla okolic Gliwic mozna uruchomic lokalnie tak:

```bash
python3 data/fetch_mv_lines.py \
  --bbox 50.22,18.55,50.38,18.82 \
  --output data/processed/mv_line_geometries_gliwice.geojson \
  --raw-output data/raw/osm_mv_lines_gliwice.overpass.json \
  --source-label osm_mv_lines_gliwice
```

Do commitowanych probek uzywamy malego pliku `data/samples/mv_line_geometries_gliwice_sample.geojson`, zeby repo pozostalo lekkie.
