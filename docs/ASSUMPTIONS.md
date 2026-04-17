# Zalozenia regulacyjne i bezpieczenstwa

Stan dokumentu: 2026-04-17

## Kontekst

Energetyka jest infrastruktura krytyczna, dlatego projekt nie moze sugerowac dostepu do danych operacyjnych, nie moze uzywac niezweryfikowanych danych jako podstawy decyzji i nie moze mieszac perspektywy dystrybucji ze sprzedaza energii.

## 1. Zaufane dane pogodowe

Na potrzeby wersji dla Tauron Dystrybucja podstawowym zrodlem danych meteorologicznych powinien byc IMGW-PIB albo inny formalnie zaakceptowany dostawca danych pogodowych.

Zasady:

- `weather_hourly` w demo docelowym pochodzi z IMGW-PIB lub z certyfikowanego/zatwierdzonego dostawcy.
- Open-Meteo, NASA POWER i podobne serwisy moga byc uzyte tylko jako szybki fallback developerski, nie jako zrodlo dla prezentacji decyzyjnej dla OSD.
- Kazdy rekord pogodowy powinien miec `source`, `source_url`, `fetched_at` i informacje, czy jest to pomiar, prognoza, czy dane historyczne.
- Model ma pokazywac niepewnosc prognozy, bo pogoda jest krytycznym wejściem do predykcji PV/wiatr.

Uzasadnienie: dla infrastruktury krytycznej wazniejsza jest wiarygodnosc, audytowalnosc i odpowiedzialnosc za zrodlo danych niz wygoda integracji API.

## 2. Unbundling: tylko dystrybucja / OSD

Projekt jest kierowany do operatora systemu dystrybucyjnego, czyli do Tauron Dystrybucja. Nie pozycjonujemy go jednoczesnie jako narzedzia dla spolek sprzedazy/obrotu energia.

Zasady:

- Uzytkownikiem docelowym jest OSD: planowanie rozwoju sieci, przylaczenia, elastycznosc, utrzymanie i analityka sieciowa.
- Nie wykorzystujemy danych sprzedazowych, taryf handlowych, danych CRM, danych billingowych ani informacji o ofertach sprzedazy energii.
- Nie projektujemy przeplywu informacji od dystrybucji do sprzedazy ani od sprzedazy do dystrybucji.
- Komunikacja produktu powinna mowic o bezpieczenstwie pracy sieci, integracji OZE, planowaniu przylaczen i elastycznosci, a nie o optymalizacji sprzedazy energii.

Uzasadnienie: dystrybucja i sprzedaz energii funkcjonuja jako rozdzielone role. Projekt powinien byc bezpieczny regulacyjnie i nie tworzyc ryzyka wymiany informacji pomiedzy spolkami.

## 3. Dane o przeciazeniach sa syntetyczne

Nie zakladamy dostepu do rzeczywistych danych o przeciazeniach, awariach, napieciach, rozpływach mocy, obciazeniach transformatorow ani danych SCADA/AMI. W MVP dane o przeciazeniach i ograniczeniach operacyjnych sa symulowane.

Zasady:

- `synthetic_grid_constraints` jest jawnie oznaczony jako dataset symulacyjny.
- Publiczne dane Taurona o elastycznosci i dostepnych mocach moga sluzyc tylko jako kontekst lub proxy do kalibracji scenariusza, nie jako prawdziwa historia przeciazen.
- Dashboard musi oznaczac risk score jako wynik modelu demonstracyjnego, a nie oficjalny stan sieci Tauron Dystrybucja.
- Nie probujemy odtwarzac ani zgadywac chronionych stanow pracy sieci.

Uzasadnienie: realne dane operacyjne OSD sa wrazliwe i chronione. Demo ma pokazac metode, architekture i wartosc predykcji, a nie ujawniac ani rekonstruowac dane infrastruktury krytycznej.

## 4. Bezpieczna narracja MVP

Poprawna narracja:

> Pokazujemy demonstrator dla Tauron Dystrybucja jako OSD. Uzywamy zaufanych danych pogodowych, publicznych danych kontekstowych i syntetycznych scenariuszy ograniczen sieciowych. Projekt nie wykorzystuje danych sprzedazowych i nie zawiera rzeczywistych danych operacyjnych sieci.

Niepoprawna narracja:

> Mamy dane Taurona o przeciazeniach i mozemy na ich podstawie sterowac siecia albo wspierac sprzedaz energii.

