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

## Why not MLX/PyTorch first

MLX or PyTorch/MPS makes sense later if we add sequence models, spatial graph
features or a larger real OSD dataset. For this MVP, the strongest baseline is
a calibrated tabular model. It gives a defensible probability of overload with
less engineering risk.
