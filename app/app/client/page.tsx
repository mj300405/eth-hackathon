"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import {
  Zap,
  TrendingDown,
  Clock,
  Euro,
  ArrowLeft,
  Calendar,
  Info
} from "lucide-react"
import Link from "next/link"
import ChatbotWidget from "@/components/ChatbotWidget"

export default function ClientPage() {

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Powrót
                </Button>
              </Link>
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-[#e2007a] flex items-center justify-center">
                  <Zap className="text-white h-6 w-6" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-[#e2007a]">
                    Portal Klienta
                  </h1>
                  <p className="text-xs text-muted-foreground">Informacje o taryfach i oszczędzaniu energii</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-6">
        <Tabs defaultValue="tariffs" className="container max-w-7xl mx-auto">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="tariffs" className="gap-2">
              <Euro className="h-4 w-4" />
              Taryfy
            </TabsTrigger>
            <TabsTrigger value="predictions" className="gap-2">
              <TrendingDown className="h-4 w-4" />
              Predykcje
            </TabsTrigger>
          </TabsList>

          {/* Tariffs Tab */}
          <TabsContent value="tariffs">
            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="h-5 w-5 text-yellow-600" />
                    Taryfa G11
                  </CardTitle>
                  <CardDescription>Jednostrefowa - stała cena przez całą dobę</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
                    <span className="text-sm font-medium">Cena za kWh</span>
                    <span className="text-2xl font-bold text-yellow-600">0.85 zł</span>
                  </div>
                  <div className="space-y-2 text-sm">
                    <p className="flex items-start gap-2">
                      <Info className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                      <span>Stała cena niezależnie od pory dnia</span>
                    </p>
                    <p className="flex items-start gap-2">
                      <Info className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                      <span>Idealna dla gospodarstw z równomiernym zużyciem</span>
                    </p>
                    <p className="flex items-start gap-2">
                      <Info className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                      <span>Prostsza w zarządzaniu zużyciem</span>
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5 text-blue-600" />
                    Taryfa G12
                  </CardTitle>
                  <CardDescription>Dwustrefowa - niższa cena w nocy</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                      <div>
                        <span className="text-sm font-medium block">Taryfa dzienna</span>
                        <span className="text-xs text-muted-foreground">6:00 - 22:00</span>
                      </div>
                      <span className="text-2xl font-bold text-blue-600">0.95 zł</span>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-pink-50 rounded-lg">
                      <div>
                        <span className="text-sm font-medium block">Taryfa nocna</span>
                        <span className="text-xs text-muted-foreground">22:00 - 6:00</span>
                      </div>
                      <span className="text-2xl font-bold text-[#e2007a]">0.45 zł</span>
                    </div>
                  </div>
                  <div className="space-y-2 text-sm">
                    <p className="flex items-start gap-2">
                      <Info className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                      <span>Oszczędzaj do 50% używając urządzeń w nocy</span>
                    </p>
                    <p className="flex items-start gap-2">
                      <Info className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                      <span>Idealna dla posiadaczy pojazdów elektrycznych</span>
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Jak oszczędzać?</CardTitle>
                <CardDescription>Praktyczne wskazówki</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="p-4 bg-muted rounded-lg">
                    <h4 className="font-semibold mb-2 flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-[#e2007a]" />
                      Planuj pranie
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      Uruchamiaj pralkę i zmywarkę w nocy (22:00-6:00), aby korzystać z niższej taryfy
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <h4 className="font-semibold mb-2 flex items-center gap-2">
                      <Zap className="h-4 w-4 text-[#e2007a]" />
                      Ładuj pojazdy nocą
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      Samochody elektryczne i inne urządzenia ładuj w godzinach nocnych
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <h4 className="font-semibold mb-2 flex items-center gap-2">
                      <TrendingDown className="h-4 w-4 text-[#e2007a]" />
                      Monitoruj predykcje
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      Sprawdzaj przewidywania okresów darmowej energii i planuj zużycie
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Predictions Tab */}
          <TabsContent value="predictions">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingDown className="h-5 w-5 text-[#e2007a]" />
                    Predykcja darmowej energii
                  </CardTitle>
                  <CardDescription>
                    Okresy gdy energia może być dostępna za 0 zł dzięki wysokiej produkcji OZE i niskim obciążeniu sieci
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 bg-pink-50 border-2 border-pink-200 rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="font-semibold text-[#c00066]">Dziś, 13:00 - 15:00</h4>
                          <p className="text-sm text-[#e2007a]">Wysokie prawdopodobieństwo (85%)</p>
                        </div>
                        <Badge className="bg-[#e2007a]">Aktywne</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Wysoka produkcja energii słonecznej + niskie obciążenie sieci = darmowa energia
                      </p>
                    </div>

                    <div className="p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="font-semibold text-blue-800">Jutro, 11:00 - 14:00</h4>
                          <p className="text-sm text-blue-600">Średnie prawdopodobieństwo (65%)</p>
                        </div>
                        <Badge variant="outline" className="border-blue-600 text-blue-600">Przewidywane</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Słoneczny dzień + weekend = mniejsze obciążenie sieci
                      </p>
                    </div>

                    <div className="p-4 bg-yellow-50 border-2 border-yellow-200 rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="font-semibold text-yellow-800">Niedziela, 12:00 - 16:00</h4>
                          <p className="text-sm text-yellow-600">Niskie prawdopodobieństwo (35%)</p>
                        </div>
                        <Badge variant="outline" className="border-yellow-600 text-yellow-600">Możliwe</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Zmienne zachmurzenie może wpłynąć na produkcję energii słonecznej
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Jak to działa?</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm">
                    <p className="flex items-start gap-2">
                      <Zap className="h-5 w-5 text-[#e2007a] mt-0.5 flex-shrink-0" />
                      <span>
                        <strong>Wysoka produkcja OZE:</strong> Gdy farmy słoneczne i wiatrowe produkują więcej energii niż potrzeba
                      </span>
                    </p>
                    <p className="flex items-start gap-2">
                      <TrendingDown className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                      <span>
                        <strong>Niskie obciążenie sieci:</strong> W godzinach poza szczytem, gdy jest mniejsze zapotrzebowanie
                      </span>
                    </p>
                    <p className="flex items-start gap-2">
                      <Euro className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                      <span>
                        <strong>Cena 0 zł:</strong> Gdy te warunki się łączą, energia może być dostępna za darmo
                      </span>
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm mt-6">
        <div className="container mx-auto px-6 py-6">
          <p className="text-center text-sm text-muted-foreground">
            Made during ETHSilesia 2026 hackathon
          </p>
        </div>
      </footer>

      {/* Chatbot Widget */}
      <ChatbotWidget />
    </div>
  )
}
