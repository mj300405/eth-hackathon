# Plan projektu

Stan dokumentu: 2026-04-17

## Cel

Zbudowac hackathonowy demonstrator systemu, ktory prognozuje produkcje energii z PV i wiatru oraz wyznacza lokalny wskaznik ryzyka problemow z integracja OZE w sieci dystrybucyjnej.

## Hipoteza

Jesli polaczymy prognozy meteorologiczne, historyczna generacje OZE i publiczne informacje o dostepnych mocach przylaczeniowych, mozemy pokazac Tauronowi uzyteczny model predykcyjny. Po dolaczeniu danych wewnetrznych OSD ten sam model moze zostac rozszerzony do poziomu operacyjnego.

## Zakres MVP

MVP ma odpowiedziec na pytanie:

> Gdzie i w jakich godzinach jutro lokalna produkcja OZE moze najbardziej obciazyc siec?

Minimalny zakres:

- pobranie lub przygotowanie danych pogodowych dla wybranego obszaru,
- oszacowanie produkcji PV i/lub wiatru na najblizsze 24-48 godzin,
- zbudowanie prostego wskaznika ryzyka,
- pokazanie wynikow na mapie lub w dashboardzie,
- przygotowanie jasnej narracji: publiczne dane teraz, dane OSD w wersji produkcyjnej.

## Harmonogram 48h

### Godziny 0-3: doprecyzowanie problemu

- Wybrac obszar testowy, np. Slask / Malopolska / wybrane powiaty z obszaru Tauron.
- Wybrac tryb MVP: PV-only albo PV + wiatr.
- Ustalic, czy robimy dashboard mapowy, czy notebook z wizualizacja.
- Zdefiniowac prosta metryke ryzyka.

Rezultat: zamkniety zakres, brak rozmywania projektu.

### Godziny 3-8: dane

- Pobranie danych pogodowych: temperatura, zachmurzenie/promieniowanie, predkosc wiatru.
- Pobranie danych produkcji PV/wiatr lub przygotowanie syntetycznego targetu z PVGIS.
- Zebranie publicznych informacji o mocach przylaczeniowych i planowanych przylaczeniach.
- Przygotowanie jednego wspolnego formatu danych godzinowych.

Rezultat: dzialajacy dataset demo.

### Godziny 8-16: baseline modelu

- Baseline PV: regresja z promieniowania, godziny dnia, dnia roku i temperatury.
- Baseline wiatr: regresja z predkosci wiatru, kierunku i sezonowosci.
- Alternatywnie: bez ML, model fizyczno-statystyczny jako punkt odniesienia.
- Walidacja na historycznych dniach.

Rezultat: prognoza produkcji na wykresie.

### Godziny 16-24: wskaznik ryzyka

Przykladowy wzor:

```text
risk_score = forecast_generation_index * local_oze_density_index * connection_constraint_index - local_demand_proxy
```

Gdzie:

- `forecast_generation_index` - przewidywana produkcja OZE w danej godzinie,
- `local_oze_density_index` - przyblizona gestosc mikroinstalacji/OZE,
- `connection_constraint_index` - proxy ograniczen na podstawie dostepnych mocy przylaczeniowych,
- `local_demand_proxy` - przyblizone zuzycie lub profil popytu.

Rezultat: ryzyko niskie/srednie/wysokie dla kazdej lokalizacji i godziny.

### Godziny 24-34: dashboard

- Mapa z punktami/obszarami.
- Timeline godzinowy.
- Wykres prognozy PV/wiatr.
- Panel rekomendacji.
- Widok "co daje dolaczenie danych Taurona".

Rezultat: demo, ktore da sie pokazac w 2 minuty.

### Godziny 34-42: dopracowanie i testy

- Sprawdzenie skrajnych przypadkow.
- Uporzadkowanie danych demo.
- Dodanie opisow do wykresow.
- Przygotowanie prostego scenariusza prezentacji.

Rezultat: stabilna prezentacja.

### Godziny 42-48: pitch

- Slajd problemu.
- Slajd danych.
- Slajd demo.
- Slajd architektury.
- Slajd wartosci biznesowej.
- Slajd: czego potrzebujemy od Taurona, aby przejsc do produkcji.

Rezultat: spojna historia, bez udawania dostepu do niepublicznych danych.

## Decyzje techniczne na start

Rekomendowany wariant na hackathon:

- Python + notebook do modelu.
- CSV/Parquet jako format posredni.
- Streamlit jako dashboard, jesli liczy sie szybkosc.
- FastAPI + React, jesli zespol ma frontendowca i chce pokazac bardziej produktowy UI.

## Podzial rol

- Data/ML: dane pogodowe, model PV/wiatr, walidacja.
- Backend/Data engineering: pipeline pobierania i normalizacji danych.
- Frontend/Data viz: mapa, wykresy, timeline.
- Product/Pitch: narracja, biznes, ograniczenia danych, prezentacja.

## Definition of Done

Projekt jest gotowy do pokazania, gdy:

- da sie uruchomic demo jednym poleceniem lub przez jeden notebook,
- jest jeden wybrany obszar testowy,
- dashboard pokazuje prognoze godzinowa,
- kazdy punkt/obszar ma risk score,
- pitch jasno rozdziela dane publiczne od danych wymaganych od Taurona,
- repo zawiera instrukcje uruchomienia i zrodla danych.

## Najwieksze ryzyka

- Brak danych sieciowych nN/SN: rozwiazanie jako proxy + jasne zalozenia.
- Zbyt ambitny zakres: zaczac od PV-only.
- Zbyt duzo czasu na integracje API: dopuscic zapisane probki danych.
- Brak walidacji: pokazac baseline i metryki nawet na ograniczonym zbiorze.

## Kolejny krok

Po utworzeniu repo:

1. Wybrac finalny stack.
2. Dodac skrypt `fetch_weather.py`.
3. Dodac notebook `01_baseline_forecast.ipynb`.
4. Dodac prosty dashboard.
5. Zbudowac pierwsza probke danych dla 3-5 lokalizacji.

