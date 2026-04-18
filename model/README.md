# Model

This directory contains the local training pipeline for overload probability.

## Recommended first model

Use a tabular gradient boosting model, not PyTorch/MLX, for the first MVP.
The current dataset is structured tabular data: feeder parameters, PV forecast,
weather features, demand proxy and reverse-flow context. A tree-based model is
fast on a Mac CPU, returns probabilities, handles non-linear thresholds well,
and is easier to explain in the pitch than a neural network.

Primary target:

```text
target_overload_probability
```

Secondary target for event metrics:

```text
target_overload_event
```

## Local venv

Create and activate the local virtual environment from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r model/requirements.txt
```

No CUDA is required. This baseline trains on CPU and works on macOS.

## Data pipeline

Regenerate the API-first training dataset and temporal splits:

```bash
python data/generate_training_dataset.py
python data/split_training_dataset.py
```

## Train

```bash
python model/train_overload_model.py
```

Outputs are written to `model/artifacts/` and are ignored by Git:

- `overload_probability_model.pkl`
- `metrics.json`
- `validation_predictions.csv`
- `test_predictions.csv`

## Predict

Run inference on a feature table:

```bash
python model/predict_overload.py
```

Default input:

```text
data/samples/model_training_gliwice_demo_test.csv
```

Default outputs:

- `model/artifacts/latest_feeder_predictions.csv`
- `model/artifacts/latest_location_predictions.csv`
- `model/artifacts/latest_location_predictions.json`

The feeder-level output has one row per timestamp and feeder:

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

The location-level output aggregates feeder rows into one row per timestamp and
location:

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

For API/dashboard use, `latest_location_predictions.json` is the cleanest shape:
one list of prediction records per location and timestamp.

## Model service

Run the model as a local HTTP service:

```bash
uvicorn model.serve_model:app --host 127.0.0.1 --port 8001
```

Endpoints:

```text
GET /health
GET /predictions/location
GET /predictions/feeder
GET /metrics
POST /reload
```

The service uses `MODEL_DEFAULT_INPUT` as the default feature table and
`MODEL_ARTIFACT_PATH` as the model artifact path. If `MODEL_TRAIN_ON_STARTUP` is
`true`, the service trains the model at startup only when the artifact is
missing.

## Near real-time shape

In production or a stronger demo, run the following cycle every 15-60 minutes:

```bash
python data/fetch_imgw_weather.py
python data/build_sample_datasets.py
python data/generate_training_dataset.py --days 1 --output data/samples/latest_prediction_features.csv
python model/predict_overload.py --input data/samples/latest_prediction_features.csv
```

PVGIS and OSM/Overpass do not need to be refreshed every few minutes. Weather is
the source that should refresh frequently. Real OSD measurements, if formally
available, would replace the synthetic demand/limit/overload context.

## Why not MLX/PyTorch first

MLX or PyTorch/MPS makes sense later if we add sequence models, spatial graph
features or a larger real OSD dataset. For this MVP, the strongest baseline is
a calibrated tabular model. It gives a defensible probability of overload with
less engineering risk.
