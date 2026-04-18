"use client"

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import type { LocationData } from "@/lib/api"

interface ForecastChartProps {
  forecast: LocationData["forecast"]
  peakHour: string
}

export function ForecastChart({ forecast, peakHour }: ForecastChartProps) {
  const dataWithPeak = forecast.map((item) => ({
    ...item,
    isPeak: item.hour.startsWith(peakHour.split(":")[0]),
  }))

  return (
    <div className="h-48 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={dataWithPeak} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="generationGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#e2007a" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#e2007a" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="hour"
            tick={{ fontSize: 10, fill: "#6b7280" }}
            tickLine={false}
            axisLine={{ stroke: "#e5e7eb" }}
          />
          <YAxis
            tick={{ fontSize: 10, fill: "#6b7280" }}
            tickLine={false}
            axisLine={{ stroke: "#e5e7eb" }}
            unit=" MW"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            }}
            labelStyle={{ fontWeight: 600, marginBottom: 4 }}
            formatter={(value: number) => [`${value.toFixed(1)} MW`, "Generacja"]}
          />
          <Area
            type="monotone"
            dataKey="generation_mw"
            stroke="#e2007a"
            strokeWidth={2}
            fill="url(#generationGradient)"
            animationDuration={1000}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
