# Kod zrodlowy

Proponowana struktura po rozpoczeciu implementacji:

```text
src/
├── data/
│   ├── fetch_weather.py
│   ├── fetch_pvgis.py
│   ├── fetch_pse.py
│   └── build_dataset.py
├── models/
│   ├── pv_baseline.py
│   └── wind_baseline.py
└── scoring/
    ├── risk_score.py
    └── recommendations.py
```

Na start nie trzeba budowac duzej architektury. Najpierw powinien dzialac jeden przeplyw:

```text
lokalizacje -> pogoda -> prognoza generacji -> risk score -> dashboard
```

