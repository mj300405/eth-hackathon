# Pitch

## One-liner

GridFlex OZE pokazuje, jak Tauron Dystrybucja jako OSD moze predykcyjnie oceniac ryzyko lokalnych nadwyzek OZE na bazie rzeczywistych publicznych API i minimalnej, jawnie opisanej syntetyki tam, gdzie dane OSD sa chronione.

## Problem

Prosumentow i instalacji OZE przybywa szybciej niz mozna modernizowac cala siec. Operatorzy potrzebuja lepszej predykcji lokalnych nadwyzek, aby planowac przylaczenia, inwestycje i mechanizmy elastycznosci.

Projekt dotyczy dystrybucji energii, nie sprzedazy. Nie zakladamy wymiany danych pomiedzy spolka dystrybucyjna i spolkami sprzedazy.

## Rozwiazanie

Budujemy model, ktory laczy:

- zaufane dane pogodowe z IMGW-PIB albo zatwierdzonego dostawcy,
- publiczne przebiegi linii sredniego napiecia z BDOT10k/GUGiK albo OSM/Overpass jako proxy geometrii,
- publiczny profil PV z PVGIS/JRC jako ksztalt symulowanej generacji,
- opcjonalnie publiczne dane o dostepnych mocach jako pozniejszy kontekst sieciowy,
- minimalny syntetyczny popyt lokalny i limit feedera SN tam, gdzie nie ma dostepu do danych OSD,
- risk score wyliczony z generacji, popytu i limitu, a nie recznie wymyslone etykiety.

Wynikiem jest mapa ryzyka dla kolejnych godzin i rekomendacje dzialan.

## Demo

W demo pokazujemy:

1. Wybrane lokalizacje z obszaru Tauron.
2. Publiczna/proxy geometrie linii SN w wybranym obszarze.
3. Symulowana produkcje PV/wiatr na jutro dla feederow SN opartych o publiczna geometrie.
4. Godziny najwiekszej generacji.
5. Mape ryzyka dla syntetycznego scenariusza ograniczen.
6. Rekomendacje: magazynowanie, przesuniecie zuzycia, inwestycja, monitoring.

## Dlaczego teraz

Rozwoj prosumeryzmu powoduje, ze siec dystrybucyjna musi byc zarzadzana bardziej predykcyjnie. Same dane historyczne nie wystarcza, bo najwieksze problemy pojawiaja sie lokalnie i godzinowo.

## Co mamy z danych publicznych

W aktualnym POC realnie uzywamy trzech publicznych zrodel/API:

- IMGW-PIB public synop API jako oficjalne publiczne zrodlo meteo,
- PVGIS/JRC `seriescalc` API jako referencyjny profil produkcji PV,
- OSM/Overpass API jako publiczne proxy przebiegu linii sredniego napiecia.

Na tej podstawie mamy wiarygodny demonstrator API-first:

- obserwacja IMGW-PIB jako zaufany seed meteo,
- publiczne/proxy przebiegi linii sredniego napiecia dla Gliwic,
- profil PVGIS skalowany do feederow SN opartych o publiczna geometrie,
- minimalny syntetyczny popyt lokalny i limit przeplywu zwrotnego,
- risk score wyliczony jako wynik modelu, jasno oznaczony jako demo.

Publiczne dane Taurona o dostepnych mocach i uslugach elastycznosci oraz dane PSE/URE/GUS traktujemy jako kolejny krok integracji, nie jako element juz uzyty w pierwszej probce POC.

Nie uzywamy publicznej geometrii linii jako oficjalnej topologii Tauron Dystrybucja. W MVP przebieg linii daje realizm przestrzenny, a parametry pracy linii, obciazenia, generacja lokalna i przeciazenia sa symulowane.

## Zasada danych: API-first

Zakladamy, ze najpierw bierzemy wszystko, co mozemy bezpiecznie pozyskac z rzeczywistych publicznych API i zrodel: pogode z IMGW-PIB, profil PV z PVGIS/JRC i publiczna/proxy geometrie linii SN z OSM/Overpass albo BDOT10k. Dane syntetyczne generujemy tylko tam, gdzie realne dane sa chronione przez OSD i nie beda dostepne w MVP.

Minimalny syntetyczny zakres dla prezentacji to:

- przydzial mocy PV do publicznych/proxy feederow SN, jesli nie mamy lokalnego rozkladu instalacji,
- prosty lokalny profil popytu per feeder,
- syntetyczny limit przeplywu zwrotnego per feeder,
- wynikowe przeciazenie i risk score liczone ze wzoru, nie wpisywane recznie.

Sposob generowania syntetyki powinien byc deterministyczny i powiazany z danymi z API:

```text
pv_generation_kw = pvgis_kw_per_kwp * synthetic_pv_capacity_kwp
reverse_flow_kw = max(0, pv_generation_kw - synthetic_local_demand_kw)
overload_kw = max(0, reverse_flow_kw - synthetic_reverse_flow_limit_kw)
risk_score = f(overload_kw, czas_trwania, confidence)
```

Czyli generacja ma ksztalt z PVGIS, miejsce pochodzi z geometrii linii SN, a pogoda pochodzi z IMGW-PIB. Syntetyczny jest tylko brakujacy kontekst sieciowy: ile PV przypisujemy do feedera, ile wynosi lokalny popyt i jaki limit przeplywu zwrotnego zakladamy. Wszystkie losowe albo scenariuszowe parametry zapisujemy z seedem i zakresem, zeby wynik byl powtarzalny i audytowalny.

Te dane sa "Tauron-like" tylko na potrzeby demonstracji logiki produktu. Nie sa danymi Tauron Dystrybucja, nie reprezentuja rzeczywistej pracy sieci i nie powinny byc komunikowane jako walidacja operacyjna. Produkcyjna wersja wymagalaby formalnego dostepu do danych OSD albo uruchomienia modelu w bezpiecznym srodowisku Tauron Dystrybucja.

## Dane pogodowe: MVP vs produkcja

W MVP korzystamy z publicznych danych IMGW-PIB jako oficjalnego i zaufanego zrodla meteorologicznego. Nie nazywamy ich automatycznie produkcyjnie certyfikowanymi ani objetych SLA, ale sa wystarczajace, zeby pokazac metode, pipeline danych i zaleznosc produkcji PV/wiatr od pogody.

W wersji produkcyjnej dla OSD zakladamy formalny dostep do lepszego zrodla meteo: profesjonalnego API, Banku Danych IMGW-PIB, umowy z IMGW-PIB albo rownowaznego certyfikowanego dostawcy. Taki dostep powinien dawac mocniejsza audytowalnosc, komplet zmiennych potrzebnych do energetyki, stabilniejsze SLA i jasna odpowiedzialnosc za zrodlo danych.

Architektura pozostaje taka sama: zmienia sie adapter danych pogodowych, nie logika risk score.

## Klasyfikacja danych: MVP vs produkcja

| Obszar danych | MVP | Produkcja |
|---|---|---|
| Pogoda | publiczne IMGW-PIB jako oficjalne zaufane zrodlo | formalny produkt IMGW-PIB, Bank Danych, profesjonalne API albo certyfikowany dostawca z SLA |
| Geometria linii SN | BDOT10k/GUGiK albo OSM jako publiczne proxy przebiegu | oficjalna topologia OSD po formalnym dopuszczeniu |
| Generacja PV | symulacja PVGIS/model PV na danych pogodowych | pomiary/estymacje OSD, dane prosumenckie i model kalibrowany operacyjnie |
| Popyt lokalny | syntetyczny profil popytu | rzeczywiste profile zuzycia, agregaty AMI/SCADA zgodne z zasadami dostepu |
| Przeciazenia i limity | jawnie syntetyczne scenariusze demo | rzeczywiste limity, pomiary napiec, obciazenia i historia ograniczen z OSD |
| Dane sprzedazowe | nie uzywamy | nie uzywamy; projekt pozostaje po stronie dystrybucji |

## Co daje formalna integracja z OSD

Po formalnym dopuszczeniu danych OSD model moze dzialac na znacznie nizszym poziomie:

- stacje SN/nN,
- konkretne linie, obwody i konfiguracje pracy,
- lokalne profile zuzycia,
- rzeczywiste pomiary napiec,
- historia ograniczen i awarii.

To zmienia MVP z mapy predykcyjnej w narzedzie wspierajace decyzje operacyjne i inwestycyjne.

## Wartosci biznesowe

- mniej lokalnych przeciazen,
- lepsze planowanie przylaczen,
- wiecej OZE w sieci bez chaotycznych inwestycji,
- wskazanie miejsc, gdzie magazyny energii lub elastycznosc maja najwiekszy sens,
- lepsza komunikacja techniczna z prosumentami i inwestorami w zakresie przylaczen i elastycznosci.

## Uczciwe ograniczenie

Nie twierdzimy, ze z danych publicznych da sie sterowac siecia. Nie twierdzimy tez, ze mamy prawdziwe dane o przeciazeniach, limitach, obciazeniach albo topologii Tauron Dystrybucja. Pokazujemy metode na syntetycznych scenariuszach i zaufanych danych pogodowych, bez danych sprzedazowych i bez wymiany informacji pomiedzy dystrybucja a sprzedaza.
