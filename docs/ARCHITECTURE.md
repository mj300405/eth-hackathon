# Architektura

## Cel architektury

System ma byc prosty do zbudowania podczas hackathonu, ale pokazac sciezke do wersji produkcyjnej.

## Wariant rekomendowany na start

```text
Publiczne API / CSV
        |
        v
Data ingestion scripts
        |
        v
Processed Parquet/CSV
        |
        v
Forecast model
        |
        v
Risk scoring
        |
        v
Dashboard / API
```

## Moduly

### 1. Data ingestion

Odpowiada za:

- pobieranie publicznych/proxy geometrii linii SN,
- pobieranie pogody,
- pobieranie danych generacji,
- budowanie syntetycznych feederow SN,
- normalizacje czasu do jednej strefy,
- walidacje brakow,
- zapis danych przetworzonych.

Proponowane pliki:

- `src/data/fetch_weather.py`
- `src/data/fetch_mv_lines.py`
- `src/data/fetch_pvgis.py`
- `src/data/fetch_pse.py`
- `src/data/build_synthetic_mv_feeders.py`
- `src/data/build_dataset.py`

### 2. Forecasting

Odpowiada za:

- baseline prognozy PV,
- opcjonalna prognoze wiatru,
- walidacje historyczna,
- zapis prognoz godzinowych.

Proponowane pliki:

- `src/models/pv_baseline.py`
- `src/models/wind_baseline.py`
- `notebooks/01_baseline_forecast.ipynb`

### 3. Risk scoring

Odpowiada za zamiane prognozy na wskaznik ryzyka.

Proponowany wzor MVP:

```text
reverse_flow_kw = max(0, pv_generation_kw - local_demand_kw)
overload_kw = max(0, reverse_flow_kw - synthetic_reverse_flow_limit_kw)
risk_score = f(overload_kw, duration, confidence, oze_density_index)
```

Gdzie:

- `pv_generation_kw` - symulowana produkcja OZE dla syntetycznego feedera SN,
- `local_demand_kw` - syntetyczny/proxy popyt lokalny,
- `synthetic_reverse_flow_limit_kw` - syntetyczny limit przeplywu zwrotnego dla feedera,
- `oze_density_index` - lokalna gestosc OZE,
- `confidence` - jakosc wejsc: meteo, geometria, zalozenia PV i popytu.

Proponowane pliki:

- `src/scoring/risk_score.py`
- `src/scoring/build_grid_proxy.py`
- `src/scoring/recommendations.py`

### 4. API albo dashboard

Wariant szybki:

- Streamlit czyta pliki CSV/Parquet i pokazuje mape.

Wariant bardziej produktowy:

- FastAPI udostepnia endpointy,
- frontend React/Next.js pokazuje mape i wykresy.

Endpointy:

```text
GET /locations
GET /mv-lines?branch_id=...
GET /forecast?location_id=...
GET /risk?timestamp=...
GET /recommendations?location_id=...
```

## Struktura przyszlego repo

```text
.
├── README.md
├── PLAN.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_SOURCES.md
│   ├── MVP_SCOPE.md
│   └── PITCH.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── notebooks/
│   ├── 01_baseline_forecast.ipynb
│   └── README.md
├── src/
│   ├── data/
│   ├── models/
│   ├── scoring/
│   └── README.md
└── app/
    └── dashboard or frontend
```

## Minimalna wersja demo

Najmniejszy sensowny wariant:

- jeden plik `locations.csv` z 11 lokalizacjami oddzialow Tauron Dystrybucja,
- jedna probka `mv_line_geometries.geojson` z publicznym/proxy przebiegiem linii SN,
- jeden plik `synthetic_mv_feeders.csv` z parametrami demo,
- jeden skrypt pobierajacy pogode,
- jeden notebook trenujacy baseline,
- jeden skrypt liczacy `risk_score`,
- Streamlit dashboard z mapa.

## Wersja produkcyjna

Wersja produkcyjna wymaga:

- hurtowni danych czasowych,
- automatycznego harmonogramu pobierania danych,
- danych OSD,
- monitoringu jakosci prognoz,
- kontroli dostepu,
- integracji z narzedziami operatora,
- audytowalnosci decyzji i rekomendacji.
