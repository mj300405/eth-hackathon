# Zakres MVP

## Problem

Rosnaca liczba prosumentow i instalacji OZE powoduje lokalne skoki generacji, ktore moga prowadzic do problemow napieciowych, przeciazen i odmow lub ograniczen przylaczeniowych. Operator potrzebuje lepszej predykcji tego, kiedy i gdzie wystapia lokalne nadwyzki.

## Uzytkownik docelowy

Podstawowy uzytkownik MVP:

- analityk sieci dystrybucyjnej,
- zespol planowania rozwoju sieci,
- zespol przylaczen OZE,
- dyspozytor lub operator pracujacy na agregatach danych.

## Wersja hackathonowa

Wersja hackathonowa nie podejmuje decyzji operacyjnych. Daje warstwe predykcyjna:

- prognozuje generacje OZE,
- agreguje wynik do lokalizacji,
- liczy wskaznik ryzyka na syntetycznym scenariuszu ograniczen,
- pokazuje rekomendacje dzialan.

Projekt jest kierowany wylacznie do Tauron Dystrybucja jako OSD. Nie jest narzedziem dla sprzedazy energii i nie zaklada przeplywu danych pomiedzy dystrybucja a sprzedaza.

## In scope

- Prognoza produkcji PV dla wybranych lokalizacji.
- Opcjonalnie prognoza produkcji wiatrowej.
- Dane pogodowe z IMGW-PIB albo innego certyfikowanego/zatwierdzonego dostawcy.
- Publiczne geometrie linii sredniego napiecia z BDOT10k/GUGiK albo OSM jako proxy przebiegu linii.
- Publiczny profil PVGIS/JRC jako punkt odniesienia do symulowanej generacji PV.
- Syntetyczne dane o przeciazeniach/ograniczeniach jako scenariusz demo.
- Publiczne dane Taurona o mapach elastycznosci i dostepnych mocach jako opcjonalny kontekst, nie jako historia realnych przeciazen.
- Mapa i ranking obszarow wedlug ryzyka.
- Prosty model ML albo model hybrydowy: fizyczny + statystyczny.

## Out of scope

- Sterowanie praca sieci.
- Rzeczywiste przeliczanie rozpływow mocy.
- Oficjalna topologia Tauron Dystrybucja.
- Dokladna analiza transformatorow SN/nN.
- Rzeczywiste dane o przeciazeniach, napieciach, awariach, rozpływach mocy i SCADA/AMI.
- Dane klientow indywidualnych.
- Dane z licznikow inteligentnych.
- Dane sprzedazowe, taryfy handlowe, CRM, billing i jakakolwiek wymiana danych ze spolka sprzedazy.
- Automatyczne wydawanie decyzji przylaczeniowych.

## Funkcje MVP

### 1. Prognoza OZE

Wejscie:

- lokalizacja,
- syntetyczny feeder SN oparty o publiczna geometrie linii,
- prognoza pogody,
- parametry instalacji PV/wiatr.

Wyjscie:

- godzinowa prognoza generacji,
- niepewnosc lub poziom ufności,
- godziny szczytu.

### 2. Wskaznik ryzyka

Wejscie:

- prognoza generacji,
- publiczna/proxy geometria linii SN,
- proxy lokalnej gestosci OZE,
- syntetyczny scenariusz ograniczen/przeciazen,
- proxy ograniczen przylaczeniowych,
- opcjonalny profil popytu.

Wyjscie:

- risk score 0-100,
- etykieta: niski / sredni / wysoki,
- krotka rekomendacja.

### 3. Dashboard

Widoki:

- mapa obszarow,
- mapa publicznych/proxy linii SN i syntetycznych feederow,
- wykres godzinowy,
- lista lokalizacji z najwyzszym ryzykiem,
- panel "co zmienia formalnie dopuszczona integracja z danymi OSD".

## Przykladowe rekomendacje

- Wysoka prognoza PV i niski margines przylaczeniowy: rozważyć lokalne magazynowanie lub taryfy elastyczne.
- Wysoka produkcja w poludnie: przesunac zuzycie lokalne na godziny 10:00-15:00.
- Powtarzalne ryzyko w danym obszarze: kandydat do modernizacji sieci.
- Duza niepewnosc pogody: wymagany monitoring w czasie rzeczywistym.

## Dane potrzebne do wersji produkcyjnej

Od OSD, w formalnym i bezpiecznym trybie wspolpracy, potrzebne bylyby:

- topologia sieci,
- parametry linii i transformatorow,
- dane pomiarowe z GPZ/SN/nN,
- profile generacji prosumentow,
- profile zuzycia,
- dane napieciowe,
- statusy przylaczen,
- historia ograniczen i awarii.

Te dane nie sa zakladane w MVP i nie sa symulowane jako dane rzeczywiste. MVP uzywa jawnie syntetycznych scenariuszy.

## Metryki sukcesu

Techniczne:

- MAE/RMSE prognozy produkcji PV.
- Trafnosc wykrycia godzin szczytowej generacji.
- Stabilnosc risk score przy brakach danych.

Biznesowe:

- Czy system wskazuje obszary wymagajace uwagi w scenariuszu syntetycznym?
- Czy rekomendacje sa zrozumiale dla operatora?
- Czy model pokazuje jasna wartosc po formalnym dolaczeniu danych OSD?
