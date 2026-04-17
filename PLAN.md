# Plan projektu

Stan dokumentu: 2026-04-17

## Cel

Zbudowac hackathonowy demonstrator systemu, ktory prognozuje produkcje energii z PV i wiatru oraz wyznacza lokalny wskaznik ryzyka problemow z integracja OZE w sieci dystrybucyjnej.

## Kontekst branżowy – wizja Taurona

Prezes Taurona, **Grzegorz Lot**, podczas Rady Programowej podkreślał kluczowe wyzwania i kierunki rozwoju:

> "Perspektywa klient, digitalizacja, kwestia jak rynku, regulacji oraz oczywiście zmian technologicznych to są takie wydarzenia, które ściągną tutaj wiele osób."

> "Każda kolejna rada programowa to duża dynamika i ścieranie się różnych poglądów. Rozliczamy dyskusję o przyszłości od tego, żeby podsumować co udało się zrealizować z naszych obietnic, deklaracji w poprzednich wydarzeniach."

*(powiedział po Radzie programowej EuroPower & OZE power 2026)*

W debacie „Transformacja energetyczna jako wzmacnianie polskiej gospodarki - między ambicją a realizmem" prezes Lot wskazał na kluczowe wyzwania operacyjne:

> "Zielona energia, tania energia i dostępna energia to są takie krytyczne czynniki sukcesu do tego, żeby gospodarka się rozwijała."

> "Sztuką jest to, żeby w maksymalnym stopniu powiązać ze sobą profil zużycia energii elektrycznej przez klienta z profilem produkcyjnym. Gdy będziemy potrafili te dwie rzeczy połączyć, cena energii elektrycznej będzie najniższa na świecie."

> "Musimy z pokorą podchodzić do tego, że nie wszystko udaje się zrobić od razu. Transformacja to nie wykonanie jednego, wielkiego skoku. To setki drobnych kroków, które przenoszą nas w świat nowej energii."

*(źródło: PAP MediaRoom, 42. edycja EuroPOWER & OZE POWER)*

Nasz projekt wpisuje się bezpośrednio w te priorytety: **digitalizacja** procesów OSD, wykorzystanie **zmian technologicznych** (AI, predykcja), odpowiedź na **wyzwania regulacyjne** związane z przyłączaniem OZE oraz **optymalizacja dopasowania profilu produkcji do zużycia** - dokładnie to, o czym mówi prezes Lot.

## Hipoteza

Jesli polaczymy zaufane prognozy meteorologiczne, historyczna generacje OZE, publiczne informacje o dostepnych mocach przylaczeniowych i syntetyczne scenariusze ograniczen, mozemy pokazac Tauron Dystrybucja uzyteczny model predykcyjny dla OSD. Po formalnym dolaczeniu bezpiecznych danych OSD ten sam model moze zostac rozszerzony do poziomu operacyjnego.

## Zakres MVP

MVP ma odpowiedziec na pytanie:

> Gdzie i w jakich godzinach jutro lokalna produkcja OZE moze najbardziej obciazyc siec?

Minimalny zakres:

- pobranie lub przygotowanie danych pogodowych dla wybranego obszaru,
- pobranie publicznej/proxy geometrii linii sredniego napiecia,
- oszacowanie produkcji PV i/lub wiatru na najblizsze 24-48 godzin,
- przygotowanie syntetycznego scenariusza ograniczen/przeciazen,
- zbudowanie prostego wskaznika ryzyka,
- pokazanie wynikow na mapie lub w dashboardzie,
- przygotowanie jasnej narracji: zaufane meteo, tylko OSD, brak danych sprzedazowych, syntetyczne ograniczenia teraz, formalne dane OSD w wersji produkcyjnej.

## Harmonogram 48h

### Godziny 0-3: doprecyzowanie problemu

- Wybrac obszar testowy, np. Slask / Malopolska / wybrane powiaty z obszaru Tauron.
- Wybrac poziom demo: publiczne/proxy linie SN jako geometria, syntetyczne parametry pracy jako dane scenariuszowe.
- Wybrac tryb MVP: PV-only albo PV + wiatr.
- Ustalic, czy robimy dashboard mapowy, czy notebook z wizualizacja.
- Zdefiniowac prosta metryke ryzyka.

Rezultat: zamkniety zakres, brak rozmywania projektu.

### Godziny 3-8: dane

- Pobranie danych pogodowych z IMGW-PIB albo zatwierdzonego dostawcy: temperatura, zachmurzenie/promieniowanie, predkosc wiatru.
- Pobranie publicznych/proxy przebiegow linii SN z BDOT10k/GUGiK albo OSM dla wybranego obszaru.
- Zbudowanie syntetycznych feederow SN na tej geometrii.
- Pobranie danych produkcji PV/wiatr lub przygotowanie syntetycznego targetu z PVGIS.
- Przygotowanie syntetycznych danych o ograniczeniach/przeciazeniach dla scenariusza demo.
- Zebranie publicznych informacji o mocach przylaczeniowych i planowanych przylaczeniach jako kontekstu.
- Przygotowanie jednego wspolnego formatu danych godzinowych.

Rezultat: dzialajacy dataset demo.

### Godziny 8-16: baseline modelu

- Baseline PV: regresja z promieniowania, godziny dnia, dnia roku i temperatury.
- Baseline wiatr: regresja z predkosci wiatru, kierunku i sezonowosci.
- Alternatywnie: bez ML, model fizyczno-statystyczny jako punkt odniesienia.
- Walidacja na historycznych dniach.

Rezultat: prognoza produkcji na wykresie.

### Godziny 16-24: wskaznik ryzyka

Przykladowy wzor dla syntetycznego feedera SN:

```text
reverse_flow_kw = max(0, pv_generation_kw - local_demand_kw)
overload_kw = max(0, reverse_flow_kw - synthetic_reverse_flow_limit_kw)
risk_score = f(overload_kw, duration, oze_density_index, confidence)
```

Gdzie:

- `pv_generation_kw` - symulowana produkcja OZE w danej godzinie,
- `local_demand_kw` - syntetyczny lub proxy popyt lokalny,
- `synthetic_reverse_flow_limit_kw` - syntetyczny limit przeplywu zwrotnego dla feedera SN,
- `overload_kw` - syntetyczne przekroczenie marginesu,
- `local_oze_density_index` - przyblizona gestosc mikroinstalacji/OZE,
- `connection_constraint_index` - syntetyczny/proxy indeks ograniczen na podstawie scenariusza demo, geometrii SN i publicznego kontekstu,
- `confidence` - jakosc wejsc i zalozen.

Rezultat: ryzyko niskie/srednie/wysokie dla kazdego syntetycznego feedera SN i godziny.

### Godziny 24-34: dashboard

- Mapa z publiczna/proxy geometria linii SN i syntetycznymi feederami.
- Timeline godzinowy.
- Wykres prognozy PV/wiatr.
- Panel rekomendacji.
- Widok "co daje formalne dolaczenie danych OSD".

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
- Slajd: czego potrzebujemy od OSD, aby przejsc do produkcji.

Rezultat: spojna historia, bez udawania dostepu do niepublicznych danych.

## Decyzje techniczne na start

Rekomendowany wariant na hackathon:

- Python + notebook do modelu.
- CSV/Parquet jako format posredni.
- Streamlit jako dashboard, jesli liczy sie szybkosc.
- FastAPI + React, jesli zespol ma frontendowca i chce pokazac bardziej produktowy UI.

## Podzial rol

- Data/ML: zaufane dane pogodowe, model PV/wiatr, walidacja.
- Backend/Data engineering: pipeline pobierania i normalizacji danych.
- Frontend/Data viz: mapa, wykresy, timeline.
- Product/Pitch: narracja, biznes, ograniczenia danych, prezentacja.

## Definition of Done

Projekt jest gotowy do pokazania, gdy:

- da sie uruchomic demo jednym poleceniem lub przez jeden notebook,
- jest jeden wybrany obszar testowy,
- dashboard pokazuje prognoze godzinowa,
- kazdy punkt/obszar ma risk score,
- pitch jasno rozdziela dane publiczne, syntetyczne scenariusze i dane wymagane od OSD,
- repo zawiera instrukcje uruchomienia i zrodla danych.

## Najwieksze ryzyka

- Brak danych sieciowych nN/SN: rozwiazanie jako syntetyczny scenariusz + proxy + jasne zalozenia.
- Zbyt ambitny zakres: zaczac od PV-only.
- Zbyt duzo czasu na integracje API: dopuscic zapisane probki danych.
- Brak walidacji: pokazac baseline i metryki nawet na ograniczonym zbiorze.

## Kolejny krok

Po utworzeniu repo:

1. Wybrac finalny stack.
2. Dodac skrypt `fetch_weather.py`.
3. Dodac notebook `01_baseline_forecast.ipynb`.
4. Dodac pobieranie publicznych/proxy linii SN.
5. Dodac generator `synthetic_mv_feeders.csv` i `synthetic_grid_constraints.csv`.
6. Dodac prosty dashboard.
7. Zbudowac pierwsza probke danych dla lokalizacji oddzialow Tauron Dystrybucja.
