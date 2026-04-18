"use client"

import { Eye, Wrench } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { MVLineData, RiskLevel } from "@/lib/api"

interface MVLinesTableProps {
  lines: MVLineData[]
  selectedLineId: string | null
  onSelectLine: (line: MVLineData) => void
  limit?: number
}

function getRiskBadgeStyle(level: RiskLevel) {
  switch (level) {
    case "NISKIE":
      return "bg-[#22c55e]/10 text-[#22c55e] border-[#22c55e]/20"
    case "SREDNIE":
      return "bg-[#f59e0b]/10 text-[#f59e0b] border-[#f59e0b]/20"
    case "WYSOKIE":
      return "bg-[#ef4444]/10 text-[#ef4444] border-[#ef4444]/20"
  }
}

function getRiskLabel(level: RiskLevel) {
  switch (level) {
    case "NISKIE":
      return "Niskie"
    case "SREDNIE":
      return "Średnie"
    case "WYSOKIE":
      return "Wysokie"
  }
}

function formatVoltage(voltage: number | null): string {
  if (!voltage) return "—"
  return `${voltage / 1000} kV`
}

function formatFlow(value: number): string {
  return value >= 1000 ? `${(value / 1000).toFixed(2)} MW` : `${Math.round(value)} kW`
}

function cityLabel(locationId: string): string {
  return locationId.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
}

export function MVLinesTable({ lines, selectedLineId, onSelectLine, limit = 20 }: MVLinesTableProps) {
  const sorted = [...lines].sort((a, b) => b.risk_score - a.risk_score).slice(0, limit)
  const highRiskCount = lines.filter((l) => l.risk_level === "WYSOKIE").length

  return (
    <Card>
      <CardHeader className="pb-2 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-lg">Linie SN — najwyższe ryzyko przeciążenia</CardTitle>
          <p className="text-xs text-muted-foreground mt-1">
            {lines.length} linii łącznie · {highRiskCount} wysokiego ryzyka · pokazane top {sorted.length}
          </p>
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">#</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Linia SN</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Napięcie</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Oddział</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Ryzyko</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Szczyt</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Przepływ zwrotny / limit</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Godz. przeciąż.</th>
                <th className="text-left py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
                <th className="text-right py-3 px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">Akcje</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((line, index) => {
                const isSelected = line.mv_line_id === selectedLineId
                return (
                  <tr
                    key={line.mv_line_id}
                    className={`border-b border-border/50 hover:bg-muted/50 transition-colors cursor-pointer ${
                      isSelected ? "bg-[#e2007a]/5" : ""
                    }`}
                    onClick={() => onSelectLine(line)}
                  >
                    <td className="py-3 px-3 text-sm text-muted-foreground">{index + 1}</td>
                    <td className="py-3 px-3">
                      <div className="flex flex-col">
                        <span className="font-medium text-foreground text-sm">{line.feeder_id}</span>
                        <span className="text-xs text-muted-foreground">{line.mv_line_id}</span>
                      </div>
                    </td>
                    <td className="py-3 px-3 text-sm">{formatVoltage(line.voltage_v)}</td>
                    <td className="py-3 px-3 text-sm">{cityLabel(line.location_id)}</td>
                    <td className="py-3 px-3">
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-2 rounded-full bg-muted overflow-hidden">
                          <div
                            className="h-full rounded-full transition-all"
                            style={{
                              width: `${line.risk_score}%`,
                              backgroundColor:
                                line.risk_score <= 33
                                  ? "#22c55e"
                                  : line.risk_score <= 66
                                  ? "#f59e0b"
                                  : "#ef4444",
                            }}
                          />
                        </div>
                        <span className="text-sm font-medium">{line.risk_score}</span>
                      </div>
                    </td>
                    <td className="py-3 px-3 text-sm">{line.peak_hour}</td>
                    <td className="py-3 px-3 text-sm">
                      <span className="font-medium">{formatFlow(line.reverse_flow_kw)}</span>
                      <span className="text-muted-foreground"> / {formatFlow(line.reverse_flow_limit_kw)}</span>
                    </td>
                    <td className="py-3 px-3 text-sm">
                      {line.overload_hours}/{line.horizon_hours}h
                    </td>
                    <td className="py-3 px-3">
                      <span className={`inline-flex px-2.5 py-0.5 text-xs font-medium rounded-full border ${getRiskBadgeStyle(line.risk_level)}`}>
                        {getRiskLabel(line.risk_level)}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-[#e2007a] hover:text-[#c00066] hover:bg-[#e2007a]/10"
                          onClick={(e) => {
                            e.stopPropagation()
                            onSelectLine(line)
                          }}
                        >
                          <Eye className="w-4 h-4 mr-1" />
                          Szczegóły
                        </Button>
                        {line.risk_level === "WYSOKIE" ? (
                          <span title="Kandydat do zgłoszenia brygady">
                            <Wrench className="w-4 h-4 text-[#ef4444]" />
                          </span>
                        ) : null}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}
