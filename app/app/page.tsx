"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Building2, Users, ArrowRight } from "lucide-react"
import Link from "next/link"

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-pink-50 via-white to-green-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-[#e2007a] flex items-center justify-center">
                <span className="text-white font-bold text-xl">GF</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-[#e2007a]">
                  GridFlex OZE
                </h1>
                <p className="text-xs text-muted-foreground">Inteligentne zarządzanie energią</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center p-6">
        <div className="container max-w-6xl">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-[#e2007a] to-green-600 bg-clip-text text-transparent">
              Witaj w GridFlex OZE
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Platforma do zarządzania i predykcji obciążenia sieci energetycznej
            </p>
          </div>

          {/* Cards Section */}
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* TAURON Card */}
            <Card className="group hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-[#e2007a]">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto mb-4 h-20 w-20 rounded-full bg-gradient-to-br from-pink-100 to-pink-200 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Building2 className="h-10 w-10 text-[#e2007a]" />
                </div>
                <CardTitle className="text-2xl">TAURON</CardTitle>
                <CardDescription className="text-base">
                  Panel zarządzania dla operatora sieci
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2 text-sm text-muted-foreground mb-6">
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-[#e2007a]" />
                    Monitoring obciążenia sieci w czasie rzeczywistym
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-[#e2007a]" />
                    Predykcja przeciążeń lokalnych
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-[#e2007a]" />
                    Rekomendacje zarządzania energią
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-[#e2007a]" />
                    Analiza danych z instalacji OZE
                  </li>
                </ul>
                <Link href="/tauron" className="block">
                  <Button className="w-full bg-[#e2007a] hover:bg-[#c00066] group">
                    Przejdź do panelu
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* CLIENT Card */}
            <Card className="group hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-green-500">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto mb-4 h-20 w-20 rounded-full bg-gradient-to-br from-green-100 to-green-200 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Users className="h-10 w-10 text-green-600" />
                </div>
                <CardTitle className="text-2xl">Klient</CardTitle>
                <CardDescription className="text-base">
                  Informacje i wsparcie dla użytkowników
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2 text-sm text-muted-foreground mb-6">
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-green-600" />
                    Chatbot po śląsku do obsługi zapytań
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-green-600" />
                    Informacje o taryfach energetycznych
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-green-600" />
                    Predykcja okresów darmowej energii
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-green-600" />
                    Porady dotyczące oszczędzania energii
                  </li>
                </ul>
                <Link href="/client" className="block">
                  <Button className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 group">
                    Przejdź do portalu
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm mt-12">
        <div className="container mx-auto px-6 py-6">
          <p className="text-center text-sm text-muted-foreground">
            © 2024 GridFlex OZE. System predykcji przeciążeń sieci dystrybucyjnej.
          </p>
        </div>
      </footer>
    </div>
  )
}
