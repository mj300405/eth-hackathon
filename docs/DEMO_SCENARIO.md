# Scenariusz demo

## Cel demo

Pokazac, ze zespol potrafi przewidziec wysokie godziny generacji OZE i przelozyc je na praktyczna informacje dla operatora sieci, bez uzywania rzeczywistych danych operacyjnych OSD.

## Narracja 2-minutowa

1. Wybieramy kilka lokalizacji z obszaru Tauron.
2. System uzywa zaufanej prognozy pogody z IMGW-PIB albo zatwierdzonego dostawcy i estymuje produkcje PV/wiatr.
3. Dla kazdej lokalizacji liczymy risk score na syntetycznym scenariuszu ograniczen.
4. Dashboard pokazuje, gdzie jutro w godzinach poludniowych ryzyko jest najwyzsze.
5. Operator widzi rekomendacje: magazynowanie, przesuniecie zuzycia, monitoring albo inwestycja.

## Przykladowa historia

Jutro prognozowane jest wysokie naslonecznienie i niskie zachmurzenie. Model wskazuje, ze w godzinach 11:00-14:00 kilka lokalizacji bedzie miec wysoka produkcje PV. Tam, gdzie syntetyczny scenariusz zaklada niski margines sieciowy, system oznacza wysoki poziom ryzyka.

## Co klikamy w demo

- Start: mapa z lokalizacjami.
- Klikniecie lokalizacji: wykres produkcji na najblizsze godziny.
- Przelaczenie godziny: zmiana kolorow ryzyka na mapie.
- Panel rekomendacji: konkretne dzialanie dla operatora.
- Slajd koncowy: jak formalnie dopuszczone dane OSD poprawiaja dokladnosc i przejscie z demo do narzedzia operacyjnego.

## Najwazniejsze zdanie do jury

Pokazujemy demonstrator dla OSD: zaufane dane pogodowe, brak danych sprzedazowych, brak rzeczywistych danych o przeciazeniach, a risk score liczony na jawnie syntetycznym scenariuszu.
