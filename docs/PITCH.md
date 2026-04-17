# Pitch

## One-liner

GridFlex OZE pokazuje, jak Tauron Dystrybucja jako OSD moze predykcyjnie oceniac ryzyko lokalnych nadwyzek OZE na bazie zaufanych danych pogodowych i jawnie syntetycznych scenariuszy ograniczen sieci.

## Problem

Prosumentow i instalacji OZE przybywa szybciej niz mozna modernizowac cala siec. Operatorzy potrzebuja lepszej predykcji lokalnych nadwyzek, aby planowac przylaczenia, inwestycje i mechanizmy elastycznosci.

Projekt dotyczy dystrybucji energii, nie sprzedazy. Nie zakladamy wymiany danych pomiedzy spolka dystrybucyjna i spolkami sprzedazy.

## Rozwiazanie

Budujemy model, ktory laczy:

- zaufane prognozy pogody z IMGW-PIB albo zatwierdzonego dostawcy,
- publiczne przebiegi linii sredniego napiecia z BDOT10k/GUGiK albo OSM jako proxy geometrii,
- historyczna generacje OZE,
- publiczne dane o dostepnych mocach,
- syntetyczne scenariusze ograniczen sieciowych,
- proxy lokalnego popytu i gestosci OZE.

Wynikiem jest mapa ryzyka dla kolejnych godzin i rekomendacje dzialan.

## Demo

W demo pokazujemy:

1. Wybrane lokalizacje z obszaru Tauron.
2. Publiczna/proxy geometrie linii SN w wybranym obszarze.
3. Symulowana produkcje PV/wiatr na jutro dla syntetycznych feederow SN.
4. Godziny najwiekszej generacji.
5. Mape ryzyka dla syntetycznego scenariusza ograniczen.
6. Rekomendacje: magazynowanie, przesuniecie zuzycia, inwestycja, monitoring.

## Dlaczego teraz

Rozwoj prosumeryzmu powoduje, ze siec dystrybucyjna musi byc zarzadzana bardziej predykcyjnie. Same dane historyczne nie wystarcza, bo najwieksze problemy pojawiaja sie lokalnie i godzinowo.

## Co mamy z danych publicznych

Mozemy zbudowac wiarygodny demonstrator:

- zaufane dane pogodowe,
- publiczne/proxy przebiegi linii sredniego napiecia,
- symulacje PV,
- generacja OZE na poziomie systemu,
- publiczne informacje o dostepnych mocach,
- dane o rozwoju mikroinstalacji,
- syntetyczne scenariusze ograniczen, jasno oznaczone jako demo.

Nie uzywamy publicznej geometrii linii jako oficjalnej topologii Tauron Dystrybucja. W MVP przebieg linii daje realizm przestrzenny, a parametry pracy linii, obciazenia, generacja lokalna i przeciazenia sa symulowane.

## Dane pogodowe: MVP vs produkcja

W MVP korzystamy z publicznych danych IMGW-PIB jako oficjalnego i zaufanego zrodla meteorologicznego. To wystarcza, zeby pokazac metode, pipeline danych i zaleznosc produkcji PV/wiatr od pogody.

W wersji produkcyjnej dla OSD zakladamy formalny dostep do lepszego zrodla meteo: profesjonalnego API, Banku Danych IMGW-PIB, umowy z IMGW-PIB albo rownowaznego certyfikowanego dostawcy. Taki dostep powinien dawac mocniejsza audytowalnosc, komplet zmiennych potrzebnych do energetyki, stabilniejsze SLA i jasna odpowiedzialnosc za zrodlo danych.

Architektura pozostaje taka sama: zmienia sie adapter danych pogodowych, nie logika risk score.

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

Nie twierdzimy, ze z danych publicznych da sie sterowac siecia. Nie twierdzimy tez, ze mamy prawdziwe dane o przeciazeniach. Pokazujemy metode na syntetycznych scenariuszach i zaufanych danych pogodowych, bez danych sprzedazowych i bez wymiany informacji pomiedzy dystrybucja a sprzedaza.
