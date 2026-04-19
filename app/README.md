# App

Frontend projektu GridFlex OZE zbudowany w `Next.js` (`App Router`), `React 19`, `Tailwind CSS 4` i komponentach `Radix UI`.

Moduł odpowiada za webową warstwę demonstratora i udostępnia dwa główne scenariusze:

- `TAURON` (`/tauron`) - dashboard operatora z mapą, listą linii SN, podglądem ryzyka przeciążeń i prognozą generacji OZE,
- `Klient` (`/client`) - prostszy portal z informacjami o taryfach, przewidywanych oknach tańszej energii i chatbotem demo,
- `/` - landing page rozdzielający oba widoki.

## Charakter modułu

To warstwa prezentacji dla hackathonowego proof of concept. Frontend skupia się na czytelnym pokazaniu danych i scenariuszy produktu, a nie na pełnej logice biznesowej po stronie przeglądarki.

Najważniejsze elementy:

- dashboard operatora pobiera dane z API przez `app/lib/api.ts`, domyślnie z `http://localhost:8000/dashboard`,
- mapa i wizualizacje służą do eksploracji lokalizacji, linii SN i prognoz obciążenia,
- portal klienta jest w dużej mierze statycznym widokiem demonstracyjnym,
- chatbot `Karbusek` działa obecnie jako lokalny mock z gotowymi odpowiedziami, bez integracji z backendem lub modelem LLM.

## Uruchomienie lokalne

W katalogu `app/`:

```bash
npm install
npm run dev
```

Aplikacja uruchamia się domyślnie pod `http://localhost:3000`.

Jeśli API działa pod innym adresem, ustaw:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Struktura

- `app/` - routing i strony Next.js,
- `components/` - komponenty dashboardu, widoków i biblioteki UI,
- `lib/api.ts` - kontrakty typów i komunikacja z backendem,
- `public/` - statyczne assety,
- `styles/` i `app/globals.css` - style globalne.
