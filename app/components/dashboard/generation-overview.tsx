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
import { hourlyGenerationData, riskyAreasData } from "@/lib/data"

export function GenerationOverview() {
  const totalSolar = hourlyGenerationData.reduce((sum, d) => sum + d.solar, 0)
  const totalWind = hourlyGenerationData.reduce((sum, d) => sum + d.wind, 0)
  const peakHour = hourlyGenerationData.reduce((max, d) => (d.total > max.total ? d : max), hourlyGenerationData[0])

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Hourly Generation Chart */}
      <Card className="lg:col-span-2">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-semibold flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#e2007a]" />
              Prognoza generacji OZE (24h)
            </CardTitle>
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
              <BarChart data={hourlyGenerationData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
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
                <p className="text-xs text-muted-foreground">Fotowoltaika (suma)</p>
                <p className="text-lg font-semibold">{totalSolar.toFixed(0)} MWh</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Wind className="w-5 h-5 text-[#be185d]" />
              <div>
                <p className="text-xs text-muted-foreground">Wiatr (suma)</p>
                <p className="text-lg font-semibold">{totalWind.toFixed(0)} MWh</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#e2007a]" />
              <div>
                <p className="text-xs text-muted-foreground">Szczyt generacji</p>
                <p className="text-lg font-semibold">{peakHour.hour} ({peakHour.total.toFixed(1)} MW)</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Risky Areas List */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-[#e2007a]" />
            Obszary wysokiego ryzyka
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {riskyAreasData.map((area, index) => (
              <div
                key={area.location}
                className="flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white ${
                      area.risk_level === "WYSOKIE"
                        ? "bg-[#e2007a]"
                        : area.risk_level === "SREDNIE"
                        ? "bg-[#f472b6]"
                        : "bg-[#fbcfe8]"
                    }`}
                  >
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-medium text-sm">{area.location}</p>
                    <p className="text-xs text-muted-foreground">Szczyt: {area.peak_hour}</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge
                    variant="outline"
                    className={`text-xs ${
                      area.risk_level === "WYSOKIE"
                        ? "border-[#e2007a] text-[#e2007a] bg-pink-50"
                        : area.risk_level === "SREDNIE"
                        ? "border-[#f472b6] text-[#be185d] bg-pink-50"
                        : "border-[#fbcfe8] text-[#f472b6] bg-pink-50"
                    }`}
                  >
                    {area.risk_score}%
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">
                    +{area.expected_overload}% przeciążenie
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Łącznie obszarów wysokiego ryzyka:</span>
              <span className="font-semibold text-[#e2007a]">
                {riskyAreasData.filter((a) => a.risk_level === "WYSOKIE").length}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
