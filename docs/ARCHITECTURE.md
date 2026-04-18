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

- `data/fetch_imgw_weather.py`
- `data/fetch_mv_lines.py`
- `data/fetch_pvgis.py`
- `data/build_sample_datasets.py`
- `data/generate_training_dataset.py`
- `data/split_training_dataset.py`

Kolejne adaptery danych, jesli beda potrzebne po POC:

- `data/fetch_tauron_capacity.py`
- `data/fetch_tauron_flexibility.py`
- `data/fetch_pse.py`
- `data/fetch_ure_gus_context.py`

### 2. Forecasting

Odpowiada za:

- przygotowanie cech do predykcji przeciazenia,
- trening baseline modelu tabularnego,
- predykcje `target_overload_probability`,
- walidacje na temporalnym train/validation/test split.

Aktualne pliki:

- `model/train_overload_model.py`
- `model/predict_overload.py`
- `model/serve_model.py`
- `model/Dockerfile`
- `model/requirements.txt`
- `model/README.md`

### 3. Risk scoring

Odpowiada za zamiane prognozy generacji i popytu na prawdopodobienstwo przeciazenia oraz poziom ryzyka.

Proponowany wzor MVP:

```text
reverse_flow_kw = max(0, pv_generation_kw - local_demand_kw)
overload_kw = max(0, reverse_flow_kw - synthetic_reverse_flow_limit_kw)
target_overload_probability = f(overload_kw, duration, confidence, oze_density_index)
```

Gdzie:

- `pv_generation_kw` - symulowana produkcja OZE dla syntetycznego feedera SN,
- `local_demand_kw` - syntetyczny/proxy popyt lokalny,
- `synthetic_reverse_flow_limit_kw` - syntetyczny limit przeplywu zwrotnego dla feedera,
- `oze_density_index` - lokalna gestosc OZE,
- `confidence` - jakosc wejsc: meteo, geometria, zalozenia PV i popytu.

Aktualny baseline:

- `HistGradientBoostingRegressor` ze `scikit-learn`,
- trening CPU na macOS bez CUDA,
- artefakty lokalne w `model/artifacts/`, ignorowane przez Git,
- predykcje per feeder i agregacja per lokalizacja w `latest_location_predictions.json`.

### 4. Runtime API i dashboard

Aktualny runtime kontenerowy:

- `model` - FastAPI service na porcie `8001`, laduje albo trenuje artefakt ML,
- `api` - FastAPI backend na porcie `8000`, wystawia dashboard-friendly endpointy,
- `frontend` - Next.js z katalogu `app/` na porcie `3000`.

Uruchomienie:

```bash
docker compose up --build
```

Aktualne endpointy API:

```text
GET /locations
GET /dashboard
GET /predictions/locations
GET /predictions/feeders
GET /metrics
GET /health
```

Aktualne endpointy model service:

```text
GET /predictions/location
GET /predictions/feeder
GET /metrics
GET /health
POST /reload
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
│   ├── samples/
│   ├── fetch_mv_lines.py
│   ├── generate_training_dataset.py
│   ├── split_training_dataset.py
│   ├── build_sample_datasets.py
│   └── README.md
├── model/
│   ├── README.md
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── serve_model.py
│   ├── predict_overload.py
│   └── train_overload_model.py
├── api/
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   └── main.py
├── app/
│   ├── Dockerfile
│   └── Next.js dashboard
├── notebooks/
│   ├── 01_baseline_forecast.ipynb
│   └── README.md
```

## Minimalna wersja demo

Najmniejszy sensowny wariant:

- jeden plik `locations.csv` z 11 lokalizacjami oddzialow Tauron Dystrybucja,
- jedna probka `mv_line_geometries.geojson` z publicznym/proxy przebiegiem linii SN,
- jeden plik `synthetic_mv_feeders.csv` z parametrami demo,
- jeden skrypt pobierajacy pogode z IMGW-PIB,
- jeden skrypt pobierajacy profil PV z PVGIS/JRC,
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
