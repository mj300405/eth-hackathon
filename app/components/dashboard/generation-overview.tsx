"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Sun, Wind, AlertTriangle, TrendingUp } from "lucide-react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import type { HourlyGenerationData, MVLineData } from "@/lib/api"

interface GenerationOverviewProps {
  hourlyGenerationData: HourlyGenerationData[]
  mvLines: MVLineData[]
  selectedLine?: MVLineData | null
  onSelectLine?: (line: MVLineData) => void
}

export function GenerationOverview({ hourlyGenerationData, mvLines, selectedLine, onSelectLine }: GenerationOverviewProps) {
  const chartData = selectedLine
    ? selectedLine.forecast.map((point) => ({
        hour: point.hour,
        solar: point.generation_mw,
        wind: 0,
        total: point.generation_mw,
        probability: point.probability,
        reverse_flow_kw: point.reverse_flow_kw,
        reverse_flow_limit_kw: point.reverse_flow_limit_kw,
      }))
    : hourlyGenerationData.map((point) => ({
        hour: point.hour,
        solar: point.solar,
        wind: point.wind,
        total: point.total,
        probability: null as number | null,
        reverse_flow_kw: null as number | null,
        reverse_flow_limit_kw: null as number | null,
      }))

  if (chartData.length === 0) {
    return (
      <Card>
        <CardContent className="py-8 text-center text-muted-foreground">
          Brak danych generacji z API.
        </CardContent>
      </Card>
    )
  }

  const totalSolar = chartData.reduce((sum, d) => sum + d.solar, 0)
  const totalWind = chartData.reduce((sum, d) => sum + d.wind, 0)
  const peakHour = chartData.reduce((max, d) => (d.total > max.total ? d : max), chartData[0])
  const scopeLabel = selectedLine
    ? `${selectedLine.feeder_id} · ${selectedLine.mv_line_id}`
    : "Wszystkie linie SN (suma)"
  const totalLabel = selectedLine ? "MWh (linia)" : "MWh (suma)"

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Hourly Generation Chart */}
      <Card className="lg:col-span-2">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg font-semibold flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-[#e2007a]" />
                Prognoza generacji OZE (24h)
              </CardTitle>
              <p className="text-xs text-muted-foreground mt-1">{scopeLabel}</p>
            </div>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-sm bg-[#f472b6]" />
                <span className="text-muted-foreground">Fotowoltaika</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-sm bg-[#be185d]" />
                <span className="text-muted-foreground">Wiatr</span>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
                <XAxis
                  dataKey="hour"
                  tick={{ fontSize: 11, fill: "#6b7280" }}
                  tickLine={false}
                  axisLine={{ stroke: "#e5e7eb" }}
                  interval={1}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: "#6b7280" }}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(value) => `${value}`}
                  label={{ value: "MW", angle: -90, position: "insideLeft", fontSize: 11, fill: "#6b7280" }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "white",
                    border: "1px solid #e5e7eb",
                    borderRadius: "8px",
                    boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                  }}
                  formatter={(value: number, name: string) => [
                    `${value.toFixed(1)} MW`,
                    name === "solar" ? "Fotowoltaika" : "Wiatr",
                  ]}
                  labelFormatter={(label) => `Godzina: ${label}`}
                />
                <Bar dataKey="solar" stackId="a" fill="#f472b6" radius={[0, 0, 0, 0]} name="solar" />
                <Bar dataKey="wind" stackId="a" fill="#be185d" radius={[4, 4, 0, 0]} name="wind" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex items-center justify-center gap-8 mt-4 pt-4 border-t">
            <div className="flex items-center gap-2">
              <Sun className="w-5 h-5 text-[#f472b6]" />
              <div>
                <p className="text-xs text-muted-foreground">Fotowoltaika</p>
                <p className="text-lg font-semibold">{totalSolar.toFixed(1)} {totalLabel}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Wind className="w-5 h-5 text-[#be185d]" />
              <div>
                <p className="text-xs text-muted-foreground">Wiatr</p>
                <p className="text-lg font-semibold">{totalWind.toFixed(1)} {totalLabel}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#e2007a]" />
              <div>
                <p className="text-xs text-muted-foreground">Szczyt generacji</p>
                <p className="text-lg font-semibold">{peakHour.hour} ({peakHour.total.toFixed(2)} MW)</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Top risky MV lines */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-[#e2007a]" />
            Linie SN — pilne
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {[...mvLines].sort((a, b) => b.risk_score - a.risk_score).slice(0, 6).map((line, index) => (
              <button
                key={line.mv_line_id}
                type="button"
                onClick={() => onSelectLine?.(line)}
                className="w-full flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors text-left"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white shrink-0 ${
                      line.risk_level === "WYSOKIE"
                        ? "bg-[#ef4444]"
                        : line.risk_level === "SREDNIE"
                        ? "bg-[#f59e0b]"
                        : "bg-[#22c55e]"
                    }`}
                  >
                    {index + 1}
                  </div>
                  <div className="min-w-0">
                    <p className="font-medium text-sm truncate">{line.feeder_id}</p>
                    <p className="text-xs text-muted-foreground truncate">
                      {line.mv_line_id} · szczyt {line.peak_hour} · {line.overload_hours}h przeciąż.
                    </p>
                  </div>
                </div>
                <div className="text-right shrink-0 ml-2">
                  <Badge
                    variant="outline"
                    className={`text-xs ${
                      line.risk_level === "WYSOKIE"
                        ? "border-[#ef4444] text-[#ef4444] bg-red-50"
                        : line.risk_level === "SREDNIE"
                        ? "border-[#f59e0b] text-[#f59e0b] bg-amber-50"
                        : "border-[#22c55e] text-[#22c55e] bg-green-50"
                    }`}
                  >
                    {line.risk_score}
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">
                    {Math.round(line.max_probability * 100)}% P(ov)
                  </p>
                </div>
              </button>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Linie wysokiego ryzyka:</span>
              <span className="font-semibold text-[#ef4444]">
                {mvLines.filter((l) => l.risk_level === "WYSOKIE").length} / {mvLines.length}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
