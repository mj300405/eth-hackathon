# GridFlex OZE

Projekt przygotowany na hackathon ETHSilesia 2026.

GridFlex OZE to demonstrator pokazujący, jak dane pogodowe, prognoza generacji OZE i prosty model ryzyka mogą wspierać decyzje wokół lokalnych nadwyżek energii. Repo łączy dashboard dla operatora, portal klienta, backend API i serwis modelu.

## O projekcie

W wersji hackathonowej projekt pokazuje dwa spojrzenia na ten sam problem:

- panel operatora z mapą lokalizacji, liniami SN, predykcją ryzyka i rekomendacjami,
- portal klienta z informacjami o taryfach, okresach potencjalnie taniej lub darmowej energii oraz chatbotem.

Celem nie jest sterowanie rzeczywistą siecią, tylko pokazanie kierunku produktu i sposobu prezentacji danych w czytelnym demo.

## Co zawiera demo

- frontend w Next.js z widokami `TAURON` i `Klient`,
- backend FastAPI wystawiający dane pod dashboard,
- osobny serwis modelu liczący predykcje przeciążeń,
- pipeline danych budujący próbki demo dla lokalizacji i feederów.

## Dane i założenia

Demo korzysta z połączenia danych publicznych i danych syntetycznych:

- pogoda: IMGW-PIB,
- profil produkcji PV: PVGIS/JRC,
- geometria linii SN: OSM/Overpass jako publiczny proxy,
- popyt lokalny i ograniczenia sieciowe: scenariusze syntetyczne do celów demonstracyjnych.

To oznacza, że projekt nie prezentuje rzeczywistych danych operacyjnych OSD i nie powinien być traktowany jako narzędzie produkcyjne. To hackathonowy proof of concept.

## Architektura

- `app/` - frontend Next.js,
- `api/` - publiczne API dla dashboardu,
- `model/` - trening, predykcja i serwis modelu,
- `data/` - skrypty pobierania i przygotowania danych,
- `docs/` - materiały do pitchu i opis architektury.

## Jak uruchomić demo

Najprostsza opcja:

```bash
docker compose up --build
```

Po starcie:

- frontend: `http://localhost:3000`
- API: `http://localhost:8000/docs`
- model service: `http://localhost:8001/docs`

## Najważniejsze scenariusze

- operator sprawdza, gdzie i kiedy może pojawić się podwyższone ryzyko lokalnej nadwyżki OZE,
- dashboard pokazuje lokalizacje, linie SN, poziomy ryzyka i rekomendacje działań,
- klient dostaje prostszy widok z taryfami, poradami i informacją o potencjalnych oknach korzystniejszego zużycia energii.

## Uczestnicy i zgłoszenie

### Uczestnicy

- Aleksandra Maksimowska
- Michał Jagoda
- Jakub Barylak

### Kategorie konkursowe

- AI Challenge powered by Tauron
- Katowicki.HUB: Innowacje

## Dokumentacja

- [docs/PITCH.md](docs/PITCH.md) - skrót prezentacji projektu,
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - opis architektury,
- [docs/DEMO_SCENARIO.md](docs/DEMO_SCENARIO.md) - scenariusz pokazu demo.

## Licencja

Projekt jest udostępniany na licencji GPLv3. Szczegóły są w pliku [LICENSE](LICENSE).
