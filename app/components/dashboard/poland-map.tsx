"use client"

import { useEffect, useRef } from "react"
import type { LocationData, MVLineData } from "@/lib/api"

interface PolandMapProps {
  locations: LocationData[]
  mvLines: MVLineData[]
  selectedLocation: LocationData | null
  selectedLineId: string | null
  onSelectLocation: (location: LocationData) => void
  onSelectLine: (line: MVLineData) => void
}

function getRiskColor(score: number): string {
  if (score <= 33) return "#22c55e"
  if (score <= 66) return "#f59e0b"
  return "#ef4444"
}

function getLineWeight(score: number, selected: boolean): number {
  const base = score >= 67 ? 5 : score >= 34 ? 4 : 3
  return selected ? base + 3 : base
}

function getMarkerSize(generation: number): number {
  const minSize = 12
  const maxSize = 28
  const maxGeneration = 50
  return Math.min(maxSize, minSize + (generation / maxGeneration) * (maxSize - minSize))
}

function formatProbability(probability: number): string {
  return `${Math.round(probability * 100)}%`
}

export function PolandMap({
  locations,
  mvLines,
  selectedLocation,
  selectedLineId,
  onSelectLocation,
  onSelectLine,
}: PolandMapProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)
  const polylineByIdRef = useRef<Map<string, L.Polyline>>(new Map())

  useEffect(() => {
    if (typeof window === "undefined" || !mapRef.current) return

    let cancelled = false

    const initMap = async () => {
      const L = (await import("leaflet")).default
      await import("leaflet/dist/leaflet.css")

      if (cancelled || !mapRef.current) return

      const map = L.map(mapRef.current, {
        center: [50.5, 18.8],
        zoom: 9,
        zoomControl: true,
        scrollWheelZoom: true,
        preferCanvas: true,
      })

      L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
      }).addTo(map)

      mapInstanceRef.current = map
      polylineByIdRef.current.clear()

      const allBounds: [number, number][] = []

      mvLines.forEach((line) => {
        const latlngs = line.coordinates.map(([lon, lat]) => [lat, lon] as [number, number])
        allBounds.push(...latlngs)

        const color = getRiskColor(line.risk_score)
        const polyline = L.polyline(latlngs, {
          color,
          weight: getLineWeight(line.risk_score, false),
          opacity: 0.9,
          lineCap: "round",
          lineJoin: "round",
        }).addTo(map)

        const voltage = line.voltage_v ? `${line.voltage_v / 1000} kV` : "b.d."
        const utilization = Math.round(line.utilization * 100)
        polyline.bindTooltip(
          `<div class="font-sans text-xs">
            <strong>${line.feeder_id}</strong> · ${line.mv_line_id}<br/>
            Napięcie: ${voltage}<br/>
            Ryzyko: ${line.risk_score} (${line.risk_level})<br/>
            P(przeciążenie): ${formatProbability(line.max_probability)}<br/>
            Szczyt: ${line.peak_hour}<br/>
            Przepływ zwrotny: ${line.reverse_flow_kw} / ${line.reverse_flow_limit_kw} kW (${utilization}%)<br/>
            Godziny przeciążenia: ${line.overload_hours}/${line.horizon_hours}
          </div>`,
          { sticky: true, direction: "top" }
        )

        polyline.on("click", () => onSelectLine(line))

        polylineByIdRef.current.set(line.mv_line_id, polyline)
      })

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

        marker.on("click", () => onSelectLocation(location))
      })

      if (allBounds.length >= 2) {
        map.fitBounds(allBounds, { padding: [40, 40], maxZoom: 12 })
      }
    }

    initMap()

    return () => {
      cancelled = true
      polylineByIdRef.current.clear()
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [locations, mvLines, onSelectLocation, onSelectLine])

  useEffect(() => {
    const map = mapInstanceRef.current
    if (!map) return

    polylineByIdRef.current.forEach((polyline, mvLineId) => {
      const line = mvLines.find((l) => l.mv_line_id === mvLineId)
      if (!line) return
      const isSelected = mvLineId === selectedLineId
      polyline.setStyle({
        color: isSelected ? "#e2007a" : getRiskColor(line.risk_score),
        weight: getLineWeight(line.risk_score, isSelected),
        opacity: isSelected ? 1 : 0.9,
      })
      if (isSelected) {
        polyline.bringToFront()
        const bounds = polyline.getBounds()
        if (bounds.isValid()) map.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 })
      }
    })
  }, [mvLines, selectedLineId])

  useEffect(() => {
    if (!mapInstanceRef.current || !selectedLocation || selectedLineId) return

    mapInstanceRef.current.setView(
      [selectedLocation.coordinates[0], selectedLocation.coordinates[1]],
      12,
      { animate: true }
    )
  }, [selectedLocation, selectedLineId])

  return (
    <div className="relative h-full w-full rounded-lg overflow-hidden border border-border">
      <div ref={mapRef} className="h-full w-full" style={{ minHeight: "500px" }} />
      <div className="absolute bottom-4 left-4 z-[500] bg-card/95 backdrop-blur-sm rounded-lg p-3 shadow-lg border border-border">
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
        <div className="mt-2 pt-2 border-t border-border space-y-1">
          <div className="flex items-center gap-2">
            <div className="h-1 w-6 bg-foreground rounded-sm" />
            <span className="text-xs text-muted-foreground">Linia SN (feeder)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-1.5 w-6 bg-[#e2007a] rounded-sm" />
            <span className="text-xs text-muted-foreground">Wybrana linia</span>
          </div>
        </div>
      </div>
    </div>
  )
}
