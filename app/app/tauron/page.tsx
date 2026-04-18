"use client"

import { useState, useCallback, useEffect } from "react"
import dynamic from "next/dynamic"
import { Header } from "@/components/dashboard/header"
import { LocationDetails } from "@/components/dashboard/location-details"
import { MVLineDetails } from "@/components/dashboard/mv-line-details"
import { Recommendations } from "@/components/dashboard/recommendations"
import { MVLinesTable } from "@/components/dashboard/mv-lines-table"
import { Footer } from "@/components/dashboard/footer"
import { GenerationOverview } from "@/components/dashboard/generation-overview"
import { fetchDashboardData, type DashboardData, type LocationData, type MVLineData } from "@/lib/api"
import { Card, CardContent } from "@/components/ui/card"
import { MapPin } from "lucide-react"
import { Button } from "@/components/ui/button"

const PolandMap = dynamic(
  () => import("@/components/dashboard/poland-map").then((mod) => mod.PolandMap),
  {
    ssr: false,
    loading: () => (
      <div className="h-full w-full flex items-center justify-center bg-muted rounded-lg">
        <div className="animate-pulse text-muted-foreground">Ładowanie mapy...</div>
      </div>
    ),
  }
)

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [selectedLocation, setSelectedLocation] = useState<LocationData | null>(null)
  const [selectedLine, setSelectedLine] = useState<MVLineData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadDashboardData = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await fetchDashboardData()
      setDashboardData(data)
      setSelectedLocation((current) => {
        if (!data.locations.length) return null
        if (!current) return data.locations[0]
        return data.locations.find((location) => location.location_id === current.location_id) ?? data.locations[0]
      })
      setSelectedLine((current) => {
        if (!current) return null
        return data.mv_lines.find((line) => line.mv_line_id === current.mv_line_id) ?? null
      })
    } catch (unknownError) {
      setError(unknownError instanceof Error ? unknownError.message : "Nie udało się pobrać danych z API.")
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    loadDashboardData()
  }, [loadDashboardData])

  const handleSelectLocation = useCallback((location: LocationData) => {
    setSelectedLocation(location)
    setSelectedLine(null)
  }, [])

  const handleSelectLine = useCallback(
    (line: MVLineData) => {
      setSelectedLine(line)
      setDashboardData((current) => {
        if (!current) return current
        const parent = current.locations.find((loc) => loc.location_id === line.location_id)
        if (parent) setSelectedLocation(parent)
        return current
      })
    },
    []
  )

  const locations = dashboardData?.locations ?? []
  const mvLines = dashboardData?.mv_lines ?? []

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header />

      <main className="flex-1 p-6">
        {isLoading ? (
          <Card>
            <CardContent className="py-12 text-center text-muted-foreground">
              Ładowanie danych z API...
            </CardContent>
          </Card>
        ) : error ? (
          <Card>
            <CardContent className="py-12 text-center text-muted-foreground">
              <p className="text-lg font-medium text-foreground">API nie zwróciło danych dashboardu</p>
              <p className="mt-2 text-sm">{error}</p>
              <button
                className="mt-4 rounded-md bg-[#e2007a] px-4 py-2 text-sm font-medium text-white hover:bg-[#c00066]"
                onClick={loadDashboardData}
              >
                Odśwież dane
              </button>
            </CardContent>
          </Card>
        ) : locations.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center text-muted-foreground">
              API nie zwróciło lokalizacji do wyświetlenia.
            </CardContent>
          </Card>
        ) : (
          <div className="flex gap-6 h-[calc(100vh-280px)] min-h-[600px]">
            <div className="w-3/5">
              <PolandMap
                locations={locations}
                mvLines={mvLines}
                selectedLocation={selectedLocation}
                selectedLineId={selectedLine?.mv_line_id ?? null}
                onSelectLocation={handleSelectLocation}
                onSelectLine={handleSelectLine}
              />
            </div>

            <div className="w-2/5 flex flex-col gap-4 overflow-y-auto">
              {selectedLine ? (
                <>
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-muted-foreground">Wybrana linia SN</p>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setSelectedLine(null)}
                      className="text-xs"
                    >
                      Wróć do oddziału
                    </Button>
                  </div>
                  <MVLineDetails line={selectedLine} />
                </>
              ) : selectedLocation ? (
                <>
                  <LocationDetails location={selectedLocation} />
                  <Recommendations
                    recommendations={selectedLocation.recommendations}
                    riskLevel={selectedLocation.risk_level}
                  />
                </>
              ) : (
                <Card className="flex-1">
                  <CardContent className="h-full flex flex-col items-center justify-center text-muted-foreground">
                    <MapPin className="w-12 h-12 mb-4 opacity-50" />
                    <p className="text-lg font-medium">Wybierz lokalizację</p>
                    <p className="text-sm">Kliknij marker na mapie, aby zobaczyć szczegóły</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}

        {dashboardData ? (
          <>
            <div className="mt-6">
              <GenerationOverview
                hourlyGenerationData={dashboardData.hourly_generation}
                mvLines={mvLines}
                selectedLine={selectedLine}
                onSelectLine={handleSelectLine}
              />
            </div>

            <div className="mt-6">
              <MVLinesTable
                lines={mvLines}
                selectedLineId={selectedLine?.mv_line_id ?? null}
                onSelectLine={handleSelectLine}
              />
            </div>
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  )
}
