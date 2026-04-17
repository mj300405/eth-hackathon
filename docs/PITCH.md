# Pitch

## One-liner

GridFlex OZE przewiduje, gdzie i kiedy lokalna produkcja z fotowoltaiki i wiatru moze przekroczyc bezpieczny margines pracy sieci dystrybucyjnej.

## Problem

Prosumentow i instalacji OZE przybywa szybciej niz mozna modernizowac cala siec. Operatorzy potrzebuja lepszej predykcji lokalnych nadwyzek, aby planowac przylaczenia, inwestycje i mechanizmy elastycznosci.

## Rozwiazanie

Budujemy model, ktory laczy:

- prognozy pogody,
- historyczna generacje OZE,
- publiczne dane o dostepnych mocach,
- proxy lokalnego popytu i gestosci OZE.

Wynikiem jest mapa ryzyka dla kolejnych godzin i rekomendacje dzialan.

## Demo

W demo pokazujemy:

1. Wybrane lokalizacje z obszaru Tauron.
2. Prognoze produkcji PV/wiatr na jutro.
3. Godziny najwiekszej generacji.
4. Mape ryzyka.
5. Rekomendacje: magazynowanie, przesuniecie zuzycia, inwestycja, monitoring.

## Dlaczego teraz

Rozwoj prosumeryzmu powoduje, ze siec dystrybucyjna musi byc zarzadzana bardziej predykcyjnie. Same dane historyczne nie wystarcza, bo najwieksze problemy pojawiaja sie lokalnie i godzinowo.

## Co mamy z danych publicznych

Mozemy zbudowac wiarygodny demonstrator:

- pogoda i promieniowanie,
- symulacje PV,
- generacja OZE na poziomie systemu,
- publiczne informacje o dostepnych mocach,
- dane o rozwoju mikroinstalacji.

## Co daje integracja z Tauronem

Po dolaczeniu danych OSD model moze dzialac na znacznie nizszym poziomie:

- stacje SN/nN,
- konkretne obwody,
- lokalne profile zuzycia,
- rzeczywiste pomiary napiec,
- historia ograniczen i awarii.

To zmienia MVP z mapy predykcyjnej w narzedzie wspierajace decyzje operacyjne i inwestycyjne.

## Wartosci biznesowe

- mniej lokalnych przeciazen,
- lepsze planowanie przylaczen,
- wiecej OZE w sieci bez chaotycznych inwestycji,
- wskazanie miejsc, gdzie magazyny energii lub elastycznosc maja najwiekszy sens,
- lepsza komunikacja z prosumentami i inwestorami.

## Uczciwe ograniczenie

Nie twierdzimy, ze z danych publicznych da sie sterowac siecia. Twierdzimy, ze z danych publicznych da sie pokazac dzialajaca warstwe predykcyjna, a dane Taurona odblokowuja jej wersje produkcyjna.

