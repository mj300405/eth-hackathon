"use client"

import { useEffect, useRef } from "react"
import type { LocationData } from "@/lib/data"

interface PolandMapProps {
  locations: LocationData[]
  selectedLocation: LocationData | null
  onSelectLocation: (location: LocationData) => void
}

function getRiskColor(score: number): string {
  if (score <= 33) return "#22c55e"
  if (score <= 66) return "#f59e0b"
  return "#ef4444"
}

function getMarkerSize(generation: number): number {
  const minSize = 12
  const maxSize = 28
  const maxGeneration = 50
  return Math.min(maxSize, minSize + (generation / maxGeneration) * (maxSize - minSize))
}

export function PolandMap({ locations, selectedLocation, onSelectLocation }: PolandMapProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)
  const markersRef = useRef<L.CircleMarker[]>([])

  useEffect(() => {
    if (typeof window === "undefined" || !mapRef.current) return

    const initMap = async () => {
      const L = (await import("leaflet")).default
      await import("leaflet/dist/leaflet.css")

      if (mapInstanceRef.current) return

      const map = L.map(mapRef.current!, {
        center: [51.0, 18.5],
        zoom: 7,
        zoomControl: true,
        scrollWheelZoom: true,
      })

      L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
      }).addTo(map)

      mapInstanceRef.current = map

      locations.forEach((location) => {
        const size = getMarkerSize(location.peak_generation_mw)
        const color = getRiskColor(location.risk_score)

        const marker = L.circleMarker([location.coordinates[0], location.coordinates[1]], {
          radius: size / 2,
          fillColor: color,
          color: "#ffffff",
          weight: 2,
          opacity: 1,
          fillOpacity: 0.85,
        }).addTo(map)

        marker.bindTooltip(
          `<div class="font-sans">
            <strong>${location.name}</strong><br/>
            Risk Score: ${location.risk_score}
          </div>`,
          { direction: "top", offset: [0, -size / 2] }
        )

        marker.on("click", () => {
          onSelectLocation(location)
        })

        markersRef.current.push(marker)
      })
    }

    initMap()

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
        markersRef.current = []
      }
    }
  }, [locations, onSelectLocation])

  useEffect(() => {
    if (!mapInstanceRef.current || !selectedLocation) return

    mapInstanceRef.current.setView(
      [selectedLocation.coordinates[0], selectedLocation.coordinates[1]],
      9,
      { animate: true }
    )
  }, [selectedLocation])

  return (
    <div className="relative h-full w-full rounded-lg overflow-hidden border border-border">
      <div ref={mapRef} className="h-full w-full" style={{ minHeight: "500px" }} />
      <div className="absolute bottom-4 left-4 bg-card/95 backdrop-blur-sm rounded-lg p-3 shadow-lg border border-border">
        <p className="text-xs font-medium mb-2 text-foreground">Poziom ryzyka</p>
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#22c55e]" />
            <span className="text-xs text-muted-foreground">Niskie (0-33)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#f59e0b]" />
            <span className="text-xs text-muted-foreground">Średnie (34-66)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#ef4444]" />
            <span className="text-xs text-muted-foreground">Wysokie (67-100)</span>
          </div>
        </div>
      </div>
    </div>
  )
}
