# Zrodla danych

Stan dokumentu: 2026-04-17

## Zasada

MVP powinno rozdzielac dwie kategorie danych:

- zaufane dane publiczne lub formalnie zaakceptowane przez OSD, ktore wystarcza do demonstratora,
- syntetyczne dane scenariuszowe, ktore zastepuja chronione dane o przeciazeniach,
- dane OSD, ktore sa potrzebne do wersji operacyjnej, ale nie sa dostepne w MVP.

Ze wzgledu na infrastrukture krytyczna dane pogodowe dla wersji prezentowanej OSD powinny pochodzic z IMGW-PIB albo innego certyfikowanego/zatwierdzonego dostawcy. Open-Meteo, NASA POWER i podobne zrodla traktujemy tylko jako fallback developerski.

Ze wzgledu na unbundling projekt jest kierowany wylacznie do Tauron Dystrybucja jako OSD. Nie uzywamy danych sprzedazowych i nie projektujemy wymiany informacji ze spolkami sprzedazy energii.

## Klasyfikacja zaufania danych

| Obszar danych | MVP | Status zaufania w MVP | Produkcja | Jak komunikowac |
|---|---|---|---|---|
| Pogoda | publiczne dane IMGW-PIB z `dane.imgw.pl` | oficjalne i zaufane zrodlo publiczne, ale bez obiecywania SLA/certyfikacji produkcyjnej | formalny produkt IMGW-PIB, Bank Danych, profesjonalne API, umowa albo rownowazny certyfikowany dostawca | "oficjalne zrodlo IMGW-PIB w MVP; produkcyjnie formalny dostep/SLA" |
| Geometria linii SN | BDOT10k/GUGiK lub OSM/Overpass | publiczne proxy przestrzenne, nie oficjalna topologia Tauron Dystrybucja | oficjalna topologia OSD po formalnym dopuszczeniu | "publiczne/proxy przebiegi linii SN" |
| Oddzialy Tauron | strona Tauron Dystrybucja | oficjalne publiczne zrodlo organizacyjne | bez zmian albo dane referencyjne OSD | "oficjalna lista oddzialow Tauron Dystrybucja" |
| Generacja PV | PVGIS albo model PV na pogodzie | symulacja/estymacja do POC, nie pomiary prosumentow | dane pomiarowe/agregaty OSD i model kalibrowany operacyjnie | "symulowana generacja PV" |
| Orientacja PV | syntetyczny miks dachow/orientacji | zalozenie demo | dane z paszportyzacji instalacji, ankiet, teledetekcji albo agregatow OSD | "syntetyczne zalozenia orientacji" |
| Popyt lokalny | syntetyczny profil popytu | zalozenie demo | rzeczywiste profile zuzycia/agregaty AMI/SCADA zgodne z regulacjami | "syntetyczny/proxy profil popytu" |
| Limity linii i przeciazenia | syntetyczne scenariusze | jawnie symulowane, nie dane Taurona | rzeczywiste limity, pomiary i historia ograniczen OSD | "jawnie syntetyczne scenariusze ograniczen" |
| Dane sprzedazowe | brak | nie uzywamy | brak | "poza zakresem ze wzgledu na unbundling" |

## Stan datasetow MVP

| Dataset | Status w repo | Docelowy plik | Zrodlo | Rola w MVP |
|---|---|---|---|---|
| `locations` | gotowy jako probka | `data/samples/locations.csv` | Tauron Dystrybucja - lista oddzialow | lista lokalizacji demo zgodna z obszarem Taurona |
| `mv_line_geometries` | probka OSM dla Gliwic | `data/processed/mv_line_geometries.geojson` | BDOT10k/GUGiK albo OpenStreetMap | publiczny/proxy przebieg linii sredniego napiecia |
| `synthetic_mv_feeders` | brak | `data/processed/synthetic_mv_feeders.csv` | dataset wyliczany z geometrii SN | syntetyczne obszary feederow SN do POC |
| `pv_installation_assumptions` | gotowy jako probka | `data/samples/pv_installation_assumptions.csv` | zalozenia demo / PVGIS | parametry instalacji uzyte do symulacji PV |
| `weather_hourly` | probka IMGW dla Gliwic/Katowic | `data/processed/weather_hourly.csv` | IMGW-PIB albo zatwierdzony dostawca meteo | zaufane wejscie do prognozy PV/wiatr |
| `generation_forecast` | probka PVGIS dla Gliwic | `data/processed/generation_forecast.csv` | PVGIS albo model z meteo IMGW-PIB | symulowana godzinowa produkcja OZE dla POC |
| `synthetic_grid_constraints` | brak | `data/processed/synthetic_grid_constraints.csv` | symulacja demo | syntetyczne scenariusze przeciazen/ograniczen |
| `tauron_flexibility_context` | opcjonalny | `data/processed/tauron_flexibility_context.csv` | mapy elastycznosci Tauron Dystrybucja | publiczny kontekst, nie etykieta realnych przeciazen |
| `tauron_connection_capacity` | brak | `data/processed/tauron_connection_capacity.csv` | dostepne moce przylaczeniowe Tauron Dystrybucja | proxy marginesu przylaczeniowego |
| `oze_density` | brak | `data/processed/oze_density.csv` | URE / GUS / dane lokalne | proxy gestosci prosumentow i OZE |
| `demand_proxy` | brak | `data/processed/demand_proxy.csv` | GUS / profil dobowy / zalozenia demo | proxy lokalnego popytu |
| `grid_proxy` | brak | `data/processed/grid_proxy.csv` | dataset wyliczany | laczy constraint, capacity, OZE density i popyt |
| `risk_hourly` | brak | `data/processed/risk_hourly.csv` | dataset wyliczany | finalny wynik do mapy i dashboardu |
| `pse_oze_generation` | opcjonalny | `data/raw/pse_oze_generation.csv` | PSE raporty | walidacja trendow PV/wiatr na poziomie kraju |

## Dane publiczne

| Obszar | Zrodlo | Link | Uzycie w MVP |
|---|---|---|---|
| Obszar Taurona i oddzialy | Tauron Dystrybucja | https://www.tauron-dystrybucja.pl/kontakt/oddzialy | oficjalna lista lokalizacji startowych |
| Przebieg linii SN | BDOT10k / GUGiK | https://www.gugik.gov.pl/projekty/gbdot/produkty | preferowane publiczne zrodlo geometrii linii elektroenergetycznych SN |
| Przebieg linii SN fallback | OpenStreetMap / OpenInfrastructureMap | https://wiki.openstreetmap.org/wiki/Power_networks/Poland | alternatywne publiczne proxy linii 10-24 kV, gdy BDOT10k jest trudniejsze do pobrania |
| Pogoda biezaca, historyczna i prognozy | IMGW-PIB | https://dane.imgw.pl | podstawowe zaufane zrodlo meteo dla MVP OSD |
| Dane meteo developerskie | Open-Meteo | https://open-meteo.com | tylko fallback developerski, nie zrodlo decyzyjne dla OSD |
| Promieniowanie i meteorologia developerska | NASA POWER | https://power.larc.nasa.gov | tylko fallback/analityka porownawcza |
| Produkcja PV z lokalizacji | PVGIS | https://re.jrc.ec.europa.eu/pvg_tools/en/ | symulacja godzinowej produkcji PV |
| Generacja OZE w systemie | PSE raporty | https://raporty.pse.pl | walidacja trendow PV/wiatr na poziomie kraju |
| Dane systemowe | PSE | https://www.pse.pl/dane-systemowe | zapotrzebowanie, generacja, kontekst KSE |
| Dane europejskie | ENTSO-E Transparency Platform | https://transparency.entsoe.eu | generacja wedlug typu, alternatywne zrodlo |
| Zapotrzebowanie na uslugi elastycznosci | Tauron Dystrybucja | https://www.tauron-dystrybucja.pl/uslugi-dystrybucyjne/uslugi-elastycznosci/zwiekszenie-elastycznosci-sieci | publiczny kontekst do scenariuszy, nie rzeczywista historia przeciazen |
| Dostepne moce przylaczeniowe | Tauron Dystrybucja | https://www.tauron-dystrybucja.pl/przylaczenie-do-sieci/dostepne-moce | proxy ograniczen sieciowych |
| Postepowania na uslugi elastycznosci | Tauron Dystrybucja | https://www.tauron-dystrybucja.pl/przetargi/uslugi-elastycznosci | potwierdzenie konkretnych obszarow ograniczen |
| Planowane inwestycje/przylaczenia | Tauron media / mapy | https://media.tauron.pl | warstwa kontekstowa do mapy |
| Mikroinstalacje OZE | URE | https://www.ure.gov.pl | skala prosumeryzmu i dane po operatorach |
| Podzial administracyjny | GUS/TERYT | https://eteryt.stat.gov.pl | mapowanie lokalizacji do gmin/powiatow |

## Dane trudne albo niedostepne publicznie

Tych danych prawdopodobnie nie zdobedziemy bez wspolpracy z Tauronem:

- topologia sieci nN/SN,
- lokalne obciazenia transformatorow,
- profile generacji prosumentow,
- profile zuzycia odbiorcow,
- dane z licznikow inteligentnych,
- pomiary napiec,
- historia przeciazen i ograniczen,
- statusy lacznikow,
- dane SCADA/AMI.

W MVP nie probujemy ich pozyskac, odtwarzac ani zgadywac. Dane o przeciazeniach tworzymy jako syntetyczny scenariusz demo.

## Jak obejsc braki danych w MVP

Zamiast udawac, ze mamy dane sieciowe, budujemy proxy i syntetyczne scenariusze.

Najlepszy kompromis przestrzenny dla MVP to linia sredniego napiecia albo syntetyczny feeder SN. Geometrie linii mozemy wziac z publicznych danych BDOT10k albo OSM, ale nie traktujemy ich jako oficjalnej topologii Tauron Dystrybucja. Parametry pracy sieci, obciazenia, limity i historia przeciazen pozostaja syntetyczne.

### Proxy gestosci OZE

Mozliwe przyblizenia:

- liczba mikroinstalacji w regionie,
- moc mikroinstalacji per operator/wojewodztwo,
- gestosc zabudowy jednorodzinnej,
- liczba punktow poboru energii, jesli dostepna,
- publiczne dane o farmach PV/wiatrowych.

### Proxy ograniczen sieciowych

Mozliwe przyblizenia:

- syntetyczny scenariusz przeciazen dla oddzialow Tauron Dystrybucja,
- dostepne moce przylaczeniowe z publikacji OSD,
- publiczne mapy elastycznosci jako kontekst,
- planowane odmowy/przylaczenia, jesli publiczne i bezpieczne do uzycia,
- odleglosc od stacji lub obszarow inwestycyjnych,
- gestosc istniejacych instalacji OZE,
- historyczna czestotliwosc wysokiej generacji.

### Proxy lokalnego popytu

Mozliwe przyblizenia:

- profil dobowy zuzycia dla gospodarstw domowych,
- liczba mieszkancow,
- typ zabudowy,
- sezonowosc,
- dni robocze/weekendy.

## Minimalny model danych

### `locations`

| Pole | Typ | Opis |
|---|---|---|
| `location_id` | string | identyfikator lokalizacji |
| `name` | string | nazwa gminy/powiatu/punktu |
| `lat` | float | szerokosc geograficzna |
| `lon` | float | dlugosc geograficzna |
| `operator_area` | string | np. Tauron |
| `admin_level` | string | gmina/powiat/punkt |
| `tauron_branch` | string | nazwa oddzialu Tauron Dystrybucja |
| `voivodeship` | string | wojewodztwo |
| `source_url` | string | zrodlo potwierdzajace lokalizacje |
| `notes` | string | uwagi do lokalizacji |

### `weather_hourly`

| Pole | Typ | Opis |
|---|---|---|
| `timestamp` | datetime | godzina pomiaru/prognozy |
| `location_id` | string | lokalizacja |
| `temperature_c` | float | temperatura |
| `wind_speed_ms` | float | predkosc wiatru |
| `cloud_cover_pct` | float | zachmurzenie |
| `solar_radiation_wm2` | float | promieniowanie, jesli dostepne |
| `source` | string | IMGW-PIB albo zatwierdzony dostawca |
| `source_url` | string | link do zrodla |
| `fetched_at` | datetime | czas pobrania |
| `data_kind` | string | observation/forecast/history |

### `pv_installation_assumptions`

| Pole | Typ | Opis |
|---|---|---|
| `location_id` | string | lokalizacja |
| `pv_capacity_kwp` | float | moc instalacji przyjeta do symulacji |
| `tilt_deg` | float | kat nachylenia paneli |
| `azimuth_deg` | float | azymut paneli |
| `system_loss_pct` | float | zalozone straty systemowe |
| `assumption_type` | string | demo / pvgis / measured |
| `notes` | string | opis zalozenia |

### `mv_line_geometries`

Format preferowany: GeoJSON.

| Pole | Typ | Opis |
|---|---|---|
| `mv_line_id` | string | identyfikator linii/odcinka w naszym dataspecu |
| `source_feature_id` | string | identyfikator obiektu z BDOT10k/OSM jesli dostepny |
| `source` | string | bdot10k/osm/manual |
| `source_url` | string | link do zrodla |
| `voltage_v` | int | napiecie, np. 15000 albo 20000 jesli znane |
| `geometry` | linestring | geometria przebiegu linii |
| `length_km` | float | dlugosc odcinka |
| `operator_tag` | string | tag operatora jesli publicznie dostepny, bez zgadywania |
| `quality_flag` | string | high/medium/low zalezne od zrodla i kompletności |
| `is_official_tauron_topology` | bool | zawsze false w MVP |

### `synthetic_mv_feeders`

| Pole | Typ | Opis |
|---|---|---|
| `feeder_id` | string | syntetyczny identyfikator feedera SN |
| `branch_location_id` | string | oddzial/lokalizacja Tauron z `locations` |
| `mv_line_id` | string | publiczna geometria linii uzyta jako proxy |
| `feeder_name` | string | nazwa demo, bez uzycia nazw operacyjnych Taurona |
| `centroid_lat` | float | centroid obszaru feedera |
| `centroid_lon` | float | centroid obszaru feedera |
| `length_km` | float | dlugosc publicznej/proxy geometrii |
| `synthetic_capacity_kw` | float | syntetyczna przepustowosc do scenariusza |
| `synthetic_reverse_flow_limit_kw` | float | syntetyczny limit przeplywu zwrotnego |
| `synthetic_base_demand_kw` | float | syntetyczny bazowy popyt |
| `synthetic_pv_capacity_kwp` | float | syntetyczna moc PV przypisana do feedera |
| `area_type` | string | residential/industrial/mixed/rural |
| `is_synthetic` | bool | true |
| `source_note` | string | informacja, ze geometria jest publicznym proxy, a parametry sa syntetyczne |

### `generation_forecast`

| Pole | Typ | Opis |
|---|---|---|
| `timestamp` | datetime | godzina prognozy |
| `location_id` | string | lokalizacja albo oddzial nadrzedny |
| `feeder_id` | string | syntetyczny feeder SN, jesli prognoza jest na poziomie linii |
| `pv_kw` | float | prognoza PV |
| `wind_kw` | float | prognoza wiatru |
| `confidence` | float | pewnosc prognozy |
| `generation_basis` | string | pvgis/model/synthetic |

### `demand_proxy`

| Pole | Typ | Opis |
|---|---|---|
| `timestamp` | datetime | godzina albo reprezentatywna godzina profilu |
| `location_id` | string | lokalizacja |
| `feeder_id` | string | syntetyczny feeder SN, jesli profil jest na poziomie linii |
| `demand_index` | float | popyt znormalizowany do 0-1 albo skali demo |
| `demand_kw` | float | syntetyczny/proxy popyt lokalny |
| `profile_type` | string | weekday/weekend/seasonal/demo |
| `source_url` | string | zrodlo danych lub opis zalozenia |

### `grid_proxy`

| Pole | Typ | Opis |
|---|---|---|
| `location_id` | string | lokalizacja |
| `feeder_id` | string | syntetyczny feeder SN |
| `nearest_network_node` | string | najblizszy GPZ/RS/grupa wezlow jesli znana |
| `constraint_index` | float | proxy ograniczen sieciowych 0-1 |
| `connection_capacity_index` | float | proxy dostepnej mocy |
| `oze_density_index` | float | proxy gestosci OZE |
| `demand_index` | float | proxy popytu |
| `flexibility_hours_per_year` | float | liczba godzin ograniczen z map elastycznosci jesli dostepna |
| `flexibility_mw` | float | zapotrzebowanie MW z map elastycznosci jesli dostepne |
| `proxy_confidence` | string | low/medium/high zalezne od jakosci mapowania |

### `synthetic_grid_constraints`

| Pole | Typ | Opis |
|---|---|---|
| `scenario_id` | string | identyfikator scenariusza |
| `timestamp` | datetime | godzina scenariusza |
| `location_id` | string | lokalizacja |
| `feeder_id` | string | syntetyczny feeder SN |
| `synthetic_constraint_index` | float | symulowany poziom ograniczenia 0-1 |
| `synthetic_overload_flag` | bool | symulowana flaga przeciazenia |
| `synthetic_overload_mw` | float | symulowana wartosc przekroczenia/marginesu |
| `scenario_basis` | string | opis zalozen scenariusza |
| `is_synthetic` | bool | zawsze true |
| `source_note` | string | jasna informacja, ze to nie sa dane Taurona |

### `tauron_flexibility_context`

| Pole | Typ | Opis |
|---|---|---|
| `context_id` | string | identyfikator wpisu |
| `branch` | string | oddzial Tauron Dystrybucja |
| `network_node` | string | nazwa GPZ/RS/linii z publikacji |
| `service_type` | string | typ uslugi elastycznosci |
| `period_start` | date | poczatek okresu swiadczenia |
| `period_end` | date | koniec okresu swiadczenia |
| `constraint_hours_per_year` | float | publicznie podana czestotliwosc potrzeb elastycznosci w h/rok, nie historia przeciazen |
| `flexibility_mw` | float | zapotrzebowanie na moc w usludze elastycznosci |
| `source_url` | string | link do strony Taurona |
| `source_date` | date | data zebrania danych |

### `tauron_connection_capacity`

| Pole | Typ | Opis |
|---|---|---|
| `capacity_id` | string | identyfikator wpisu |
| `group_number` | string | numer grupy z publikacji Taurona |
| `group_name` | string | nazwa grupy wezlow |
| `nodes` | string | wezly/stacje w grupie |
| `year` | int | rok prognozy |
| `available_capacity_mw` | float | laczna dostepna moc przylaczeniowa |
| `source_url` | string | link do publikacji Taurona |
| `source_date` | date | data obowiazywania/pobrania |

### `risk_hourly`

| Pole | Typ | Opis |
|---|---|---|
| `timestamp` | datetime | godzina |
| `location_id` | string | lokalizacja |
| `feeder_id` | string | syntetyczny feeder SN |
| `risk_score` | int | 0-100 |
| `risk_level` | string | low/medium/high |
| `reverse_flow_kw` | float | syntetyczny przeplyw zwrotny |
| `overload_kw` | float | syntetyczne przekroczenie limitu |
| `recommendation` | string | rekomendacja |

## Plan pobierania danych

Na start:

1. Uzyj `data/samples/locations.csv` jako listy 11 oddzialow Tauron Dystrybucja.
2. Pobierz publiczne geometrie linii SN z BDOT10k/GUGiK albo OSM i zapisz jako `mv_line_geometries.geojson`.
3. Z geometrii linii utworz `synthetic_mv_feeders.csv`: publiczny przebieg + syntetyczne parametry pracy.
4. Ustaw jawne zalozenia PV w `pv_installation_assumptions.csv`.
5. Pobierz pogode dla tych lokalizacji z IMGW-PIB albo zatwierdzonego dostawcy meteo.
6. Uzyj PVGIS albo prostego modelu PV z promieniowania do wyznaczenia symulowanej produkcji PV dla feederow SN.
7. Wygeneruj `synthetic_grid_constraints.csv` jako jawny scenariusz przeciazen demo.
8. Opcjonalnie wprowadz publiczny kontekst Taurona o zapotrzebowaniu na uslugi elastycznosci.
9. Wprowadz recznie lub zeskrob dostepne moce przylaczeniowe Taurona.
10. Dodaj proxy gestosci OZE z URE/GUS albo ustaw wersje demonstracyjna.
11. Dodaj `demand_proxy.csv` jako prosty profil popytu.
12. Zapisz wszystko do `data/processed/`.

## Uwagi prawne i licencyjne

- Sprawdzic regulamin kazdego zrodla przed publicznym demo.
- W dashboardzie podac zrodla danych.
- Nie przetwarzac danych osobowych.
- Nie sugerowac, ze wyniki sa oficjalnymi danymi Taurona.
- Nie uzywac danych sprzedazowych ani nie projektowac wymiany informacji ze spolkami sprzedazy energii.
- Oznaczac wszystkie dane o przeciazeniach jako syntetyczne, jesli nie pochodza z formalnie przekazanego i dopuszczonego zbioru OSD.
- Oznaczac publiczne przebiegi linii SN jako proxy geometrii, nie oficjalna topologie Tauron Dystrybucja.
