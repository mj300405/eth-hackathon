"use client"

import { Calendar, Zap, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import Link from "next/link"

const navItems = [
  { label: "Dashboard", active: true },
  { label: "Prognozy", active: false },
  { label: "Analityka", active: false },
  { label: "Ustawienia", active: false },
]

export function Header() {
  const [forecastHours, setForecastHours] = useState(24)

  return (
    <header className="border-b border-border bg-card">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-4">
          <Link href="/">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Powrót
            </Button>
          </Link>
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-[#e2007a]">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-[#e2007a]">GridFlex OZE</h1>
              <p className="text-sm text-muted-foreground">
                System predykcji przeciążeń sieci dystrybucyjnej
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-muted">
            <Calendar className="w-4 h-4 text-muted-foreground" />
            <span className="text-sm font-medium">Prognoza:</span>
            <div className="flex gap-1">
              <Button
                variant={forecastHours === 24 ? "default" : "ghost"}
                size="sm"
                onClick={() => setForecastHours(24)}
                className={forecastHours === 24 ? "bg-[#e2007a] hover:bg-[#c00066]" : ""}
              >
                24h
              </Button>
              <Button
                variant={forecastHours === 48 ? "default" : "ghost"}
                size="sm"
                onClick={() => setForecastHours(48)}
                className={forecastHours === 48 ? "bg-[#e2007a] hover:bg-[#c00066]" : ""}
              >
                48h
              </Button>
            </div>
          </div>

          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <Button
                key={item.label}
                variant={item.active ? "default" : "ghost"}
                size="sm"
                className={item.active ? "bg-[#e2007a] hover:bg-[#c00066]" : ""}
              >
                {item.label}
              </Button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}
