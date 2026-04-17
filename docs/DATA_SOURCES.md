# Zrodla danych

Stan dokumentu: 2026-04-17

## Zasada

MVP powinno rozdzielac dwie kategorie danych:

- dane publiczne, ktore wystarcza do demonstratora,
- dane OSD, ktore sa potrzebne do wersji operacyjnej.

## Stan datasetow MVP

| Dataset | Status w repo | Docelowy plik | Zrodlo | Rola w MVP |
|---|---|---|---|---|
| `locations` | gotowy jako probka | `data/samples/locations.csv` | Tauron Dystrybucja - lista oddzialow | lista lokalizacji demo zgodna z obszarem Taurona |
| `pv_installation_assumptions` | gotowy jako probka | `data/samples/pv_installation_assumptions.csv` | zalozenia demo / PVGIS | parametry instalacji uzyte do symulacji PV |
| `weather_hourly` | brak | `data/processed/weather_hourly.csv` | Open-Meteo albo IMGW | wejscie do prognozy PV/wiatr |
| `generation_forecast` | brak | `data/processed/generation_forecast.csv` | PVGIS albo model z Open-Meteo | godzinowa prognoza produkcji OZE |
| `tauron_flexibility_constraints` | brak | `data/processed/tauron_flexibility_constraints.csv` | mapy elastycznosci Tauron Dystrybucja | najlepszy publiczny proxy ograniczen/przeciazen sieci |
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
| Pogoda bieżąca i historyczna | IMGW | https://dane.imgw.pl | temperatura, wiatr, zachmurzenie, opady |
| Prognozy i historia pogody | Open-Meteo | https://open-meteo.com | szybkie API pogodowe dla lokalizacji |
| Promieniowanie i meteorologia | NASA POWER | https://power.larc.nasa.gov | dane godzinowe solarne i pogodowe |
| Produkcja PV z lokalizacji | PVGIS | https://re.jrc.ec.europa.eu/pvg_tools/en/ | symulacja godzinowej produkcji PV |
| Generacja OZE w systemie | PSE raporty | https://raporty.pse.pl | walidacja trendow PV/wiatr na poziomie kraju |
| Dane systemowe | PSE | https://www.pse.pl/dane-systemowe | zapotrzebowanie, generacja, kontekst KSE |
| Dane europejskie | ENTSO-E Transparency Platform | https://transparency.entsoe.eu | generacja wedlug typu, alternatywne zrodlo |
| Zapotrzebowanie na uslugi elastycznosci | Tauron Dystrybucja | https://www.tauron-dystrybucja.pl/uslugi-dystrybucyjne/uslugi-elastycznosci/zwiekszenie-elastycznosci-sieci | GPZ/RS z czestotliwoscia ograniczen i zapotrzebowaniem MW |
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

## Jak obejsc braki danych w MVP

Zamiast udawac, ze mamy dane sieciowe, budujemy proxy.

### Proxy gestosci OZE

Mozliwe przyblizenia:

- liczba mikroinstalacji w regionie,
- moc mikroinstalacji per operator/wojewodztwo,
- gestosc zabudowy jednorodzinnej,
- liczba punktow poboru energii, jesli dostepna,
- publiczne dane o farmach PV/wiatrowych.

### Proxy ograniczen sieciowych

Mozliwe przyblizenia:

- dostepne moce przylaczeniowe z publikacji OSD,
- planowane odmowy/przylaczenia, jesli publiczne,
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

### `generation_forecast`

| Pole | Typ | Opis |
|---|---|---|
| `timestamp` | datetime | godzina prognozy |
| `location_id` | string | lokalizacja |
| `pv_kw` | float | prognoza PV |
| `wind_kw` | float | prognoza wiatru |
| `confidence` | float | pewnosc prognozy |

### `demand_proxy`

| Pole | Typ | Opis |
|---|---|---|
| `timestamp` | datetime | godzina albo reprezentatywna godzina profilu |
| `location_id` | string | lokalizacja |
| `demand_index` | float | popyt znormalizowany do 0-1 albo skali demo |
| `profile_type` | string | weekday/weekend/seasonal/demo |
| `source_url` | string | zrodlo danych lub opis zalozenia |

### `grid_proxy`

| Pole | Typ | Opis |
|---|---|---|
| `location_id` | string | lokalizacja |
| `nearest_network_node` | string | najblizszy GPZ/RS/grupa wezlow jesli znana |
| `constraint_index` | float | proxy ograniczen sieciowych 0-1 |
| `connection_capacity_index` | float | proxy dostepnej mocy |
| `oze_density_index` | float | proxy gestosci OZE |
| `demand_index` | float | proxy popytu |
| `flexibility_hours_per_year` | float | liczba godzin ograniczen z map elastycznosci jesli dostepna |
| `flexibility_mw` | float | zapotrzebowanie MW z map elastycznosci jesli dostepne |
| `proxy_confidence` | string | low/medium/high zalezne od jakosci mapowania |

### `tauron_flexibility_constraints`

| Pole | Typ | Opis |
|---|---|---|
| `constraint_id` | string | identyfikator wpisu |
| `branch` | string | oddzial Tauron Dystrybucja |
| `network_node` | string | nazwa GPZ/RS/linii z publikacji |
| `service_type` | string | typ uslugi elastycznosci |
| `period_start` | date | poczatek okresu swiadczenia |
| `period_end` | date | koniec okresu swiadczenia |
| `constraint_hours_per_year` | float | czestotliwosc ograniczen sieciowych w h/rok |
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
| `risk_score` | int | 0-100 |
| `risk_level` | string | low/medium/high |
| `recommendation` | string | rekomendacja |

## Plan pobierania danych

Na start:

1. Uzyj `data/samples/locations.csv` jako listy 11 oddzialow Tauron Dystrybucja.
2. Ustaw jawne zalozenia PV w `pv_installation_assumptions.csv`.
3. Pobierz pogode dla tych lokalizacji z Open-Meteo albo IMGW.
4. Uzyj PVGIS albo prostego modelu PV z promieniowania do wyznaczenia profilu PV.
5. Wprowadz recznie lub zeskrob publiczne dane Taurona o zapotrzebowaniu na uslugi elastycznosci.
6. Wprowadz recznie lub zeskrob dostepne moce przylaczeniowe Taurona.
7. Dodaj proxy gestosci OZE z URE/GUS albo ustaw wersje demonstracyjna.
8. Dodaj `demand_proxy.csv` jako prosty profil popytu.
9. Zapisz wszystko do `data/processed/`.

## Uwagi prawne i licencyjne

- Sprawdzic regulamin kazdego zrodla przed publicznym demo.
- W dashboardzie podac zrodla danych.
- Nie przetwarzac danych osobowych.
- Nie sugerowac, ze wyniki sa oficjalnymi danymi Taurona.
