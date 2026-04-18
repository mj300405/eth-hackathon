# Inteligentne bilansowanie OZE - hackathon

Roboczy projekt hackathonowy: predykcyjna mapa ryzyka lokalnych nadwyzek energii z OZE dla obszaru Tauron Dystrybucja.

## Teza projektu

Publiczne dane pogodowe, dane o generacji OZE i publiczne informacje sieciowe daja wystarczajaca baze do zbudowania demonstratora, ktory:

- prognozuje produkcje PV i wiatru dla wybranych lokalizacji,
- wskazuje godziny wysokiego ryzyka lokalnej nadprodukcji dla publicznych/proxy linii SN w scenariuszu syntetycznym,
- laczy prognoze z publicznymi proxy ograniczen sieciowych,
- pokazuje, jak model moglby zejsc do poziomu stacji SN/nN po podlaczeniu danych OSD.

To nie jest system operacyjnego sterowania siecia. To MVP warstwy predykcyjnej dla OSD, bez danych sprzedazowych i bez rzeczywistych danych o przeciazeniach sieci.

## Zalozenia krytyczne

- Projekt jest kierowany do Tauron Dystrybucja jako operatora systemu dystrybucyjnego, nie do spolek sprzedazy energii.
- Ze wzgledu na unbundling nie zakladamy wymiany danych pomiedzy dystrybucja i sprzedaza.
- Dane pogodowe dla wersji prezentowanej OSD musza pochodzic z IMGW-PIB albo innego certyfikowanego/zatwierdzonego dostawcy.
- Dane o przeciazeniach i ograniczeniach operacyjnych sa syntetyczne. Publiczne dane Taurona slużą tylko jako kontekst i proxy, nie jako prawdziwa historia pracy sieci.
- Szczegoly sa opisane w [docs/ASSUMPTIONS.md](docs/ASSUMPTIONS.md).

## Proponowana nazwa

GridFlex OZE

Alternatywy:

- OZE Balance AI
- FlexGrid Tauron
- ProsumerFlow
- GreenGrid Forecaster

## Najwazniejsze pliki

- [PLAN.md](PLAN.md) - plan prac i harmonogram hackathonu.
- [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md) - zakres MVP, zalozenia i ograniczenia.
- [docs/ASSUMPTIONS.md](docs/ASSUMPTIONS.md) - zalozenia regulacyjne, pogodowe i bezpieczenstwa.
- [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) - publiczne zrodla danych i braki danych.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - proponowana architektura techniczna.
- [docs/PITCH.md](docs/PITCH.md) - krotki opis do prezentacji.
- [docs/DEMO_SCENARIO.md](docs/DEMO_SCENARIO.md) - scenariusz pokazania projektu.
- [BACKLOG.md](BACKLOG.md) - lista zadan do implementacji.
- [data/samples/locations.csv](data/samples/locations.csv) - startowa probka 11 lokalizacji oddzialow Tauron Dystrybucja.

## MVP w jednym zdaniu

Dashboard mapowy, ktory na podstawie zaufanych danych pogodowych, publicznych/proxy przebiegow linii SN, prognozy generacji OZE i syntetycznych scenariuszy ograniczen pokazuje, gdzie i kiedy w kolejnym dniu moze pojawic sie wysokie ryzyko dla dalszej integracji prosumentow.

## Jak odpalic pipeline krok po kroku

Ponizsze komendy uruchamiamy z katalogu repo:

```bash
cd /Users/michal/Desktop/eth-hackathon
```

### 1. Przygotuj lokalne srodowisko

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r model/requirements.txt
```

Venv `.venv/` jest lokalny i ignorowany przez Git.

### 2. Odswiez dane z publicznych API

IMGW-PIB, czyli zaufane publiczne meteo:

```bash
python data/fetch_imgw_weather.py
```

Wynik:

```text
data/samples/weather_hourly_gliwice_imgw.csv
data/raw/imgw_synop_katowice_latest.json
```

PVGIS/JRC, czyli referencyjny profil produkcji PV:

```bash
python data/fetch_pvgis.py
```

Wynik:

```text
data/samples/pvgis_profile_gliwice.csv
data/raw/pvgis_gliwice_2020.json
```

OSM/Overpass, czyli publiczne/proxy linie SN. Do normalnego demo nie trzeba tego odpalac, bo w repo jest juz mala probka:

```bash
python data/fetch_mv_lines.py \
  --bbox 50.22,18.55,50.38,18.82 \
  --output data/processed/mv_line_geometries_gliwice.geojson \
  --raw-output data/raw/osm_mv_lines_gliwice.overpass.json \
  --source-label osm_mv_lines_gliwice
```

Wynik lokalny:

```text
data/processed/mv_line_geometries_gliwice.geojson
data/raw/osm_mv_lines_gliwice.overpass.json
```

Pliki `data/raw/` i `data/processed/` sa ignorowane przez Git.

### 3. Zbuduj male demo 24h

```bash
python data/build_sample_datasets.py
```

Wynik:

```text
data/samples/synthetic_mv_feeders_gliwice.csv
data/samples/weather_hourly_gliwice_demo.csv
data/samples/generation_forecast_gliwice_demo.csv
data/samples/demand_proxy_gliwice_demo.csv
data/samples/synthetic_grid_constraints_gliwice_demo.csv
data/samples/risk_hourly_gliwice_demo.csv
```

Ten krok pokazuje mechanike demo: geometria feederow z publicznego/proxy OSM, ksztalt PV z PVGIS, seed meteo z IMGW, a brakujace dane OSD syntetyczne.

### 4. Wygeneruj dataset ML

```bash
python data/generate_training_dataset.py
```

Wynik:

```text
data/samples/model_training_gliwice_demo.csv
```

Domyslnie powstaje 30 dni danych godzinowych dla 5 feederow, czyli 3600 rekordow. Najwazniejsze targety:

```text
target_overload_probability
target_overload_event
```

Model ma uczyc sie prawdopodobienstwa przeciazenia w danej godzinie i lokalizacji/feedrze.

### 5. Zrob train/validation/test split

```bash
python data/split_training_dataset.py
```

Wynik:

```text
data/samples/model_training_gliwice_demo_train.csv
data/samples/model_training_gliwice_demo_validation.csv
data/samples/model_training_gliwice_demo_test.csv
data/samples/model_training_gliwice_demo_splits.json
```

Split jest czasowy, nie losowy:

```text
train:      2026-04-01 00:00 -> 2026-04-21 23:00
validation: 2026-04-22 00:00 -> 2026-04-26 11:00
test:       2026-04-26 12:00 -> 2026-04-30 23:00
```

Nie mieszamy tych samych godzin miedzy zbiorami, zeby ograniczyc leakage.

### 6. Wytrenuj model

```bash
python model/train_overload_model.py
```

Wynik lokalny:

```text
model/artifacts/overload_probability_model.pkl
model/artifacts/metrics.json
model/artifacts/validation_predictions.csv
model/artifacts/test_predictions.csv
```

`model/artifacts/` jest ignorowane przez Git, bo to lokalne artefakty treningu.

Aktualny baseline to `HistGradientBoostingRegressor` ze `scikit-learn`, trenowany na CPU. Nie wymaga CUDA, PyTorch ani MLX. Na obecnej probce wynik jest rzedu:

```text
validation_mae ~= 0.0030
validation_f1  ~= 0.8455
test_mae       ~= 0.0024
test_f1        ~= 0.8595
```

### 7. Wygeneruj predykcje per feeder i lokalizacja

```bash
python model/predict_overload.py
```

Domyslne wejscie:

```text
data/samples/model_training_gliwice_demo_test.csv
```

Wynik lokalny:

```text
model/artifacts/latest_feeder_predictions.csv
model/artifacts/latest_location_predictions.csv
model/artifacts/latest_location_predictions.json
```

Format per feeder ma jeden wiersz na `timestamp + feeder_id`:

```text
timestamp
location_id
feeder_id
predicted_overload_probability
predicted_overload_event
risk_level
pv_generation_kw
local_demand_kw
reverse_flow_kw
reverse_flow_limit_kw
```

Format per lokalizacja agreguje feedery do jednego wiersza na `timestamp + location_id`:

```text
timestamp
location_id
max_overload_probability
avg_overload_probability
predicted_overload_feeder_count
high_risk_feeder_count
risk_level
top_feeder_id
```

Do API/dashboardu najlepszy jest `latest_location_predictions.json`, bo daje gotowe rekordy per lokalizacja i godzina.

### 8. Co faktycznie przewiduje model

Docelowo model ma przewidywac:

```text
P(przeciazenie | prognoza pogody, generacja PV, lokalizacja/feeder, historia przeciazen, popyt, limity sieci)
```

W MVP nie mamy prawdziwej historii przeciazen ani limitow Tauron Dystrybucja, wiec trenujemy odpowiednik demonstracyjny:

```text
P(syntetyczne przeciazenie | IMGW/PVGIS/OSM + syntetyczny popyt i syntetyczny limit feedera)
```

Czyli pipeline jest gotowy pod produkcyjne dane OSD, ale obecny target przeciazenia jest syntetyczny i jawnie oznaczony jako demo.

### 9. Jak to wyglada w prawie real-time

W produkcji albo mocniejszym demo uruchamiamy cykl co 15-60 minut:

```bash
python data/fetch_imgw_weather.py
python data/build_sample_datasets.py
python data/generate_training_dataset.py --days 1 --output data/samples/latest_prediction_features.csv
python model/predict_overload.py --input data/samples/latest_prediction_features.csv
```

Najczesciej odswiezamy pogode. PVGIS i geometria linii nie musza byc pobierane co kilka minut. Jesli kiedys dostaniemy formalne dane OSD, to w tym miejscu podmieniamy syntetyczny popyt, limity i historie przeciazen na realne dane operatora.

### 10. Najkrotsze odpalenie, gdy dane API juz sa w repo

```bash
source .venv/bin/activate
python data/build_sample_datasets.py
python data/generate_training_dataset.py
python data/split_training_dataset.py
python model/train_overload_model.py
python model/predict_overload.py
```

## Co pokazujemy jury

1. Wybor obszaru: wojewodztwo, powiat, gmina albo punkt/stacja.
2. Prognoza produkcji PV/wiatru na kolejne 24-48 godzin.
3. Wskazanie godzin szczytu generacji OZE.
4. Mapa ryzyka: niski / sredni / wysoki poziom ryzyka.
5. Rekomendacja: magazynowanie, przesuniecie zuzycia, lokalna elastycznosc, potrzeba inwestycji.

## Najwieksza uczciwosc projektowa

Z danych publicznych i syntetycznych scenariuszy da sie zbudowac dobry demonstrator i model predykcyjny. Nie da sie jednak wiarygodnie policzyc rzeczywistych przeciazen konkretnych transformatorow bez chronionych danych OSD:

- topologii sieci,
- obciazen transformatorow,
- pomiarow napiec,
- profili prosumentow,
- stanow lacznikow,
- danych SCADA/AMI.

W pitchu mowimy to wprost: publiczne dane wystarczaja do MVP, a dane Taurona odblokowuja wersje operacyjna.

## Proponowany stack

- Python: przetwarzanie danych, modele, notebooki.
- Pandas / Polars: pipeline danych.
- Scikit-learn / LightGBM / XGBoost: baseline ML.
- FastAPI: API backendu.
- React / Next.js: dashboard.
- Leaflet / MapLibre: mapa.
- SQLite / DuckDB / Postgres: dane demonstracyjne.

Na start wystarczy prosty wariant: notebook + CSV + Streamlit albo FastAPI + frontend.


## Licencja
Projekt udostępniany jest na licencji GPLv3. Szczegóły znajdziesz w pliku [LICENSE](LICENSE).
