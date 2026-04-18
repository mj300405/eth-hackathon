FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LOKY_MAX_CPU_COUNT=2

WORKDIR /workspace

COPY model/requirements.txt model/requirements.txt
RUN pip install --no-cache-dir -r model/requirements.txt

COPY data data
COPY model model

EXPOSE 8001

CMD ["uvicorn", "model.serve_model:app", "--host", "0.0.0.0", "--port", "8001"]
