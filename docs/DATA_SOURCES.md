# Zrodla danych

Stan dokumentu: 2026-04-17

## Zasada

MVP powinno rozdzielac dwie kategorie danych:

- zaufane dane publiczne lub formalnie zaakceptowane przez OSD, ktore wystarcza do demonstratora,
- syntetyczne dane scenariuszowe, ktore zastepuja chronione dane o przeciazeniach,
- dane OSD, ktore sa potrzebne do wersji operacyjnej, ale nie sa dostepne w MVP.

Ze wzgledu na infrastrukture krytyczna dane pogodowe dla wersji prezentowanej OSD powinny pochodzic z IMGW-PIB albo innego certyfikowanego/zatwierdzonego dostawcy. Open-Meteo, NASA POWER i podobne zrodla traktujemy tylko jako fallback developerski.

Ze wzgledu na unbundling projekt jest kierowany wylacznie do Tauron Dystrybucja jako OSD. Nie uzywamy danych sprzedazowych i nie projektujemy wymiany informacji ze spolkami sprzedazy energii.

## Stan datasetow MVP

| Dataset | Status w repo | Docelowy plik | Zrodlo | Rola w MVP |
|---|---|---|---|---|
| `locations` | gotowy jako probka | `data/samples/locations.csv` | Tauron Dystrybucja - lista oddzialow | lista lokalizacji demo zgodna z obszarem Taurona |
| `pv_installation_assumptions` | gotowy jako probka | `data/samples/pv_installation_assumptions.csv` | zalozenia demo / PVGIS | parametry instalacji uzyte do symulacji PV |
| `weather_hourly` | brak | `data/processed/weather_hourly.csv` | IMGW-PIB albo zatwierdzony dostawca meteo | zaufane wejscie do prognozy PV/wiatr |
| `generation_forecast` | brak | `data/processed/generation_forecast.csv` | PVGIS albo model z meteo IMGW-PIB | godzinowa prognoza produkcji OZE |
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

### `synthetic_grid_constraints`

| Pole | Typ | Opis |
|---|---|---|
| `scenario_id` | string | identyfikator scenariusza |
| `timestamp` | datetime | godzina scenariusza |
| `location_id` | string | lokalizacja |
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
| `risk_score` | int | 0-100 |
| `risk_level` | string | low/medium/high |
| `recommendation` | string | rekomendacja |

## Plan pobierania danych

Na start:

1. Uzyj `data/samples/locations.csv` jako listy 11 oddzialow Tauron Dystrybucja.
2. Ustaw jawne zalozenia PV w `pv_installation_assumptions.csv`.
3. Pobierz pogode dla tych lokalizacji z IMGW-PIB albo zatwierdzonego dostawcy meteo.
4. Uzyj PVGIS albo prostego modelu PV z promieniowania do wyznaczenia profilu PV.
5. Wygeneruj `synthetic_grid_constraints.csv` jako jawny scenariusz przeciazen demo.
6. Opcjonalnie wprowadz publiczny kontekst Taurona o zapotrzebowaniu na uslugi elastycznosci.
7. Wprowadz recznie lub zeskrob dostepne moce przylaczeniowe Taurona.
8. Dodaj proxy gestosci OZE z URE/GUS albo ustaw wersje demonstracyjna.
9. Dodaj `demand_proxy.csv` jako prosty profil popytu.
10. Zapisz wszystko do `data/processed/`.

## Uwagi prawne i licencyjne

- Sprawdzic regulamin kazdego zrodla przed publicznym demo.
- W dashboardzie podac zrodla danych.
- Nie przetwarzac danych osobowych.
- Nie sugerowac, ze wyniki sa oficjalnymi danymi Taurona.
- Nie uzywac danych sprzedazowych ani nie projektowac wymiany informacji ze spolkami sprzedazy energii.
- Oznaczac wszystkie dane o przeciazeniach jako syntetyczne, jesli nie pochodza z formalnie przekazanego i dopuszczonego zbioru OSD.
