# API

FastAPI backend for the GridFlex OZE demo.

The API container is intentionally thin. It exposes dashboard-friendly endpoints
and proxies prediction requests to the model service.

## Endpoints

```text
GET /health
GET /locations
GET /predictions/locations
GET /predictions/feeders
GET /metrics
```

`/predictions/locations` returns one record per `timestamp + location_id`.
`/predictions/feeders` returns one record per `timestamp + feeder_id`.

The model service URL is configured with:

```text
MODEL_SERVICE_URL=http://model:8001
CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

For local development without Docker:

```bash
MODEL_SERVICE_URL=http://127.0.0.1:8001 uvicorn api.main:app --host 127.0.0.1 --port 8000
```

In Docker Compose this service waits for the model service healthcheck and then
listens on `http://localhost:8000`.
