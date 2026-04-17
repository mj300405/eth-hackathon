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
