"use client"

import { useState, useCallback } from "react"
import dynamic from "next/dynamic"
import { Header } from "@/components/dashboard/header"
import { LocationDetails } from "@/components/dashboard/location-details"
import { Recommendations } from "@/components/dashboard/recommendations"
import { LocationsTable } from "@/components/dashboard/locations-table"
import { Footer } from "@/components/dashboard/footer"
import { GenerationOverview } from "@/components/dashboard/generation-overview"
import { locationsData, type LocationData } from "@/lib/data"
import { Card, CardContent } from "@/components/ui/card"
import { MapPin } from "lucide-react"

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
  const [selectedLocation, setSelectedLocation] = useState<LocationData | null>(locationsData[0])

  const handleSelectLocation = useCallback((location: LocationData) => {
    setSelectedLocation(location)
  }, [])

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header />

      <main className="flex-1 p-6">
        <div className="flex gap-6 h-[calc(100vh-280px)] min-h-[600px]">
          {/* Left Column - Map */}
          <div className="w-3/5">
            <PolandMap
              locations={locationsData}
              selectedLocation={selectedLocation}
              onSelectLocation={handleSelectLocation}
            />
          </div>

          {/* Right Column - Details */}
          <div className="w-2/5 flex flex-col gap-4 overflow-y-auto">
            {selectedLocation ? (
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

        {/* Generation Overview Section */}
        <div className="mt-6">
          <GenerationOverview />
        </div>

        {/* Bottom Panel - Table */}
        <div className="mt-6">
          <LocationsTable locations={locationsData} onSelectLocation={handleSelectLocation} />
        </div>
      </main>

      <Footer />
    </div>
  )
}
