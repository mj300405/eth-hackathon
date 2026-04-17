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
- liczy wskaznik ryzyka,
- pokazuje rekomendacje dzialan.

## In scope

- Prognoza produkcji PV dla wybranych lokalizacji.
- Opcjonalnie prognoza produkcji wiatrowej.
- Dane pogodowe z publicznych API.
- Dane historycznej generacji OZE jako punkt odniesienia.
- Publiczne dane Taurona o mapach elastycznosci i dostepnych mocach jako proxy ograniczen.
- Mapa i ranking obszarow wedlug ryzyka.
- Prosty model ML albo model hybrydowy: fizyczny + statystyczny.

## Out of scope

- Sterowanie praca sieci.
- Rzeczywiste przeliczanie rozpływow mocy.
- Dokladna analiza transformatorow SN/nN.
- Dane klientow indywidualnych.
- Dane z licznikow inteligentnych.
- Automatyczne wydawanie decyzji przylaczeniowych.

## Funkcje MVP

### 1. Prognoza OZE

Wejscie:

- lokalizacja,
- prognoza pogody,
- parametry instalacji PV/wiatr.

Wyjscie:

- godzinowa prognoza generacji,
- niepewnosc lub poziom ufności,
- godziny szczytu.

### 2. Wskaznik ryzyka

Wejscie:

- prognoza generacji,
- proxy lokalnej gestosci OZE,
- proxy ograniczen przylaczeniowych,
- opcjonalny profil popytu.

Wyjscie:

- risk score 0-100,
- etykieta: niski / sredni / wysoki,
- krotka rekomendacja.

### 3. Dashboard

Widoki:

- mapa obszarow,
- wykres godzinowy,
- lista lokalizacji z najwyzszym ryzykiem,
- panel "co zmieniaja dane Taurona".

## Przykladowe rekomendacje

- Wysoka prognoza PV i niski margines przylaczeniowy: rozważyć lokalne magazynowanie lub taryfy elastyczne.
- Wysoka produkcja w poludnie: przesunac zuzycie lokalne na godziny 10:00-15:00.
- Powtarzalne ryzyko w danym obszarze: kandydat do modernizacji sieci.
- Duza niepewnosc pogody: wymagany monitoring w czasie rzeczywistym.

## Dane potrzebne do wersji produkcyjnej

Od OSD potrzebne bylyby:

- topologia sieci,
- parametry linii i transformatorow,
- dane pomiarowe z GPZ/SN/nN,
- profile generacji prosumentow,
- profile zuzycia,
- dane napieciowe,
- statusy przylaczen,
- historia ograniczen i awarii.

## Metryki sukcesu

Techniczne:

- MAE/RMSE prognozy produkcji PV.
- Trafnosc wykrycia godzin szczytowej generacji.
- Stabilnosc risk score przy brakach danych.

Biznesowe:

- Czy system wskazuje obszary wymagajace uwagi?
- Czy rekomendacje sa zrozumiale dla operatora?
- Czy model pokazuje jasna wartosc po dolaczeniu danych Taurona?
