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

- pobieranie pogody,
- pobieranie danych generacji,
- normalizacje czasu do jednej strefy,
- walidacje brakow,
- zapis danych przetworzonych.

Proponowane pliki:

- `src/data/fetch_weather.py`
- `src/data/fetch_pvgis.py`
- `src/data/fetch_pse.py`
- `src/data/fetch_tauron_grid_proxy.py`
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
risk_score = 100 * normalized_generation * oze_density_index * constraint_index * demand_modifier
```

Gdzie:

- `normalized_generation` - prognoza OZE przeskalowana do 0-1,
- `oze_density_index` - lokalna gestosc OZE,
- `constraint_index` - im wyzszy, tym mniejszy margines sieci,
- `demand_modifier` - korekta na lokalny popyt.

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
