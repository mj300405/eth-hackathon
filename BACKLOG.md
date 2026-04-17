# Backlog

## Priorytet 0 - decyzje przed kodowaniem

- Wybrac finalny stack: Streamlit czy FastAPI + frontend.
- Wybrac zakres: PV-only czy PV + wiatr.
- Wybrac obszar demo: 3-5 lokalizacji albo powiaty.
- Ustalic, czy dane pobieramy live z API, czy pracujemy na probkach.

## Priorytet 1 - dane

- Przygotowac `locations.csv` na podstawie 11 oddzialow Tauron Dystrybucja.
- Przygotowac `pv_installation_assumptions.csv` z jawnymi zalozeniami instalacji demo.
- Dodac skrypt pobierania pogody dla lokalizacji.
- Dodac skrypt pobierania/symulacji PV z PVGIS.
- Przygotowac `tauron_flexibility_constraints.csv` z map zapotrzebowania na uslugi elastycznosci.
- Przygotowac `tauron_connection_capacity.csv` z publikacji o dostepnych mocach.
- Przygotowac `demand_proxy.csv` z prostym profilem popytu.
- Ujednolicic format czasu.
- Zapisac dane do `data/processed/`.

## Priorytet 2 - model

- Zbudowac baseline PV.
- Obliczyc prognoze godzinowa na 24-48 godzin.
- Porownac wynik z prostym profilem dziennym.
- Dodac confidence albo etykiete jakosci prognozy.

## Priorytet 3 - risk score

- Zdefiniowac `oze_density_index`.
- Zdefiniowac `constraint_index`.
- Zdefiniowac `demand_modifier`.
- Obliczyc `risk_score` 0-100.
- Przypisac etykiety: low / medium / high.

## Priorytet 4 - demo

- Mapa lokalizacji.
- Wykres godzinowy produkcji.
- Ranking lokalizacji wedlug ryzyka.
- Krotka rekomendacja dla kazdej lokalizacji.
- Widok porownujacy "dane publiczne" vs "dane Taurona".

## Priorytet 5 - pitch

- Dopisac finalna nazwe projektu.
- Przygotowac 5-7 slajdow.
- Dodac screeny z dashboardu.
- Dopisac ograniczenia i dane potrzebne od Taurona.

## Nice to have

- Forecast dla wiatru.
- Integracja z PSE API.
- Eksport raportu PDF.
- Tryb "co jesli": dodanie magazynu energii albo nowej farmy PV.
- Symulacja redukcji ryzyka po przesunieciu zuzycia.
