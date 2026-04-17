# Backlog

## Priorytet 0 - decyzje przed kodowaniem

- Wybrac finalny stack: Streamlit czy FastAPI + frontend.
- Wybrac zakres: PV-only czy PV + wiatr.
- Wybrac obszar demo: jeden oddzial Tauron + publiczne/proxy linie SN w tym obszarze.
- Potwierdzic, ze projekt jest wylacznie dla OSD/dystrybucji, bez danych sprzedazowych.
- Ustalic, czy dane pogodowe pobieramy z IMGW-PIB live, czy pracujemy na probkach od zaufanego dostawcy.

## Priorytet 1 - dane

- Przygotowac `locations.csv` na podstawie 11 oddzialow Tauron Dystrybucja.
- Przygotowac pobieranie publicznych/proxy geometrii linii SN z BDOT10k/GUGiK albo OSM.
- Przygotowac `mv_line_geometries.geojson` dla wybranego obszaru Taurona.
- Przygotowac `synthetic_mv_feeders.csv` na bazie geometrii linii SN.
- Przygotowac `pv_installation_assumptions.csv` z jawnymi zalozeniami instalacji demo.
- Dodac skrypt pobierania pogody z IMGW-PIB albo zatwierdzonego dostawcy.
- Dodac skrypt pobierania/symulacji PV z PVGIS.
- Przygotowac generator `synthetic_grid_constraints.csv` dla jawnie syntetycznych scenariuszy przeciazen.
- Przygotowac opcjonalny `tauron_flexibility_context.csv` z map zapotrzebowania na uslugi elastycznosci.
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
- Zdefiniowac `reverse_flow_kw`, `synthetic_reverse_flow_limit_kw` i `overload_kw`.
- Oznaczyc wszystkie ograniczenia/przeciazenia jako syntetyczne, jesli nie sa formalnie przekazanymi danymi OSD.
- Zdefiniowac `demand_modifier`.
- Obliczyc `risk_score` 0-100.
- Przypisac etykiety: low / medium / high.

## Priorytet 4 - demo

- Mapa lokalizacji i publicznych/proxy linii SN.
- Wykres godzinowy produkcji.
- Ranking lokalizacji wedlug ryzyka.
- Krotka rekomendacja dla kazdej lokalizacji.
- Widok porownujacy "demo syntetyczne" vs "formalna integracja z danymi OSD".

## Priorytet 5 - pitch

- Dopisac finalna nazwe projektu.
- Przygotowac 5-7 slajdow.
- Dodac screeny z dashboardu.
- Dopisac ograniczenia: infrastruktura krytyczna, unbundling, syntetyczne przeciazenia, zaufane meteo.

## Nice to have

- Forecast dla wiatru.
- Integracja z PSE API.
- Eksport raportu PDF.
- Tryb "co jesli": dodanie magazynu energii albo nowej farmy PV.
- Symulacja redukcji ryzyka po przesunieciu zuzycia.
