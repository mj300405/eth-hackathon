"use client"

import { Eye } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { LocationData } from "@/lib/data"

interface LocationsTableProps {
  locations: LocationData[]
  onSelectLocation: (location: LocationData) => void
}

function getRiskBadgeStyle(level: "NISKIE" | "SREDNIE" | "WYSOKIE") {
  switch (level) {
    case "NISKIE":
      return "bg-[#22c55e]/10 text-[#22c55e] border-[#22c55e]/20"
    case "SREDNIE":
      return "bg-[#f59e0b]/10 text-[#f59e0b] border-[#f59e0b]/20"
    case "WYSOKIE":
      return "bg-[#ef4444]/10 text-[#ef4444] border-[#ef4444]/20"
  }
}

function getRiskLabel(level: "NISKIE" | "SREDNIE" | "WYSOKIE") {
  switch (level) {
    case "NISKIE":
      return "Niskie"
    case "SREDNIE":
      return "Średnie"
    case "WYSOKIE":
      return "Wysokie"
  }
}

export function LocationsTable({ locations, onSelectLocation }: LocationsTableProps) {
  const sortedLocations = [...locations].sort((a, b) => b.risk_score - a.risk_score).slice(0, 5)

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">Top 5 lokalizacji - najwyższe ryzyko</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Lokalizacja
                </th>
                <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Risk Score
                </th>
                <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Szczyt generacji
                </th>
                <th className="text-left py-3 px-4 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Status
                </th>
                <th className="text-right py-3 px-4 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Akcje
                </th>
              </tr>
            </thead>
            <tbody>
              {sortedLocations.map((location) => (
                <tr
                  key={location.location_id}
                  className="border-b border-border/50 hover:bg-muted/50 transition-colors cursor-pointer"
                  onClick={() => onSelectLocation(location)}
                >
                  <td className="py-3 px-4">
                    <span className="font-medium text-foreground">{location.name}</span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 rounded-full bg-muted overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all"
                          style={{
                            width: `${location.risk_score}%`,
                            backgroundColor:
                              location.risk_score <= 33
                                ? "#22c55e"
                                : location.risk_score <= 66
                                ? "#f59e0b"
                                : "#ef4444",
                          }}
                        />
                      </div>
                      <span className="text-sm font-medium text-foreground">
                        {location.risk_score}
                      </span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-sm text-foreground">
                      {location.peak_hour} ({location.peak_generation_mw} MW)
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`inline-flex px-2.5 py-0.5 text-xs font-medium rounded-full border ${getRiskBadgeStyle(
                        location.risk_level
                      )}`}
                    >
                      {getRiskLabel(location.risk_level)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-[#e2007a] hover:text-[#c00066] hover:bg-[#e2007a]/10"
                      onClick={(e) => {
                        e.stopPropagation()
                        onSelectLocation(location)
                      }}
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      Szczegóły
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}
