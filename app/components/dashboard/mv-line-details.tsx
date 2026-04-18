"use client"

import { Zap, Clock, Gauge, AlertTriangle, Wrench, MapPin, TrendingUp } from "lucide-react"
import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { RiskGauge } from "./risk-gauge"
import type { MVLineData } from "@/lib/api"

interface MVLineDetailsProps {
  line: MVLineData
}

function formatFlow(value: number): string {
  return value >= 1000 ? `${(value / 1000).toFixed(2)} MW` : `${Math.round(value)} kW`
}

function formatVoltage(voltage: number | null): string {
  if (!voltage) return "b.d."
  return `${voltage / 1000} kV`
}

function cityLabel(locationId: string): string {
  return locationId.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
}

function recommendedAction(line: MVLineData): { title: string; body: string; tone: "danger" | "warn" | "ok" } {
  if (line.risk_level === "WYSOKIE") {
    return {
      title: "Zgłoś brygadę pomiarową",
      body: `Linia ${line.mv_line_id} przekracza limit przepływu zwrotnego w godzinach szczytu PV. Zaleca się pomiar napięcia na stronie SN, analizę nastaw zabezpieczeń i kandydaturę do modernizacji/magazynu energii.`,
      tone: "danger",
    }
  }
  if (line.risk_level === "SREDNIE") {
    return {
      title: "Monitoruj i przygotuj elastyczność",
      body: "Ryzyko okresowych przeciążeń. Przesuń elastyczne obciążenie do szczytu PV, zaplanuj monitoring 15-minutowy.",
      tone: "warn",
    }
  }
  return {
    title: "Normalny monitoring",
    body: "Linia mieści się w limitach przepływu zwrotnego. Brak rekomendowanych działań korekcyjnych.",
    tone: "ok",
  }
}

export function MVLineDetails({ line }: MVLineDetailsProps) {
  const action = recommendedAction(line)
  const utilizationPct = Math.round(line.utilization * 100)
  const overloadPct = Math.round((line.overload_hours / Math.max(1, line.horizon_hours)) * 100)

  return (
    <div className="flex flex-col gap-4">
      <Card>
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-[#e2007a]" />
            <CardTitle className="text-lg">{line.feeder_id}</CardTitle>
          </div>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <Badge variant="outline" className="text-xs font-mono">{line.mv_line_id}</Badge>
            <Badge variant="outline" className="text-xs">{formatVoltage(line.voltage_v)}</Badge>
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <MapPin className="w-3 h-3" /> {cityLabel(line.location_id)}
            </span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center">
            <RiskGauge score={line.risk_score} riskLevel={line.risk_level} />
          </div>
          <p className="text-center text-sm text-muted-foreground mt-2">
            Prawdopodobieństwo przeciążenia w szczycie: <span className="font-semibold text-foreground">{Math.round(line.max_probability * 100)}%</span>
          </p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-3 gap-3">
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="w-4 h-4 text-[#e2007a]" />
              <span className="text-xs font-medium text-muted-foreground">Szczyt</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{line.peak_hour}</p>
            <p className="text-sm text-muted-foreground">godzina ryzyka</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 mb-2">
              <Gauge className="w-4 h-4 text-[#e2007a]" />
              <span className="text-xs font-medium text-muted-foreground">Wykorzystanie</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{utilizationPct}%</p>
            <p className="text-sm text-muted-foreground">{formatFlow(line.reverse_flow_kw)} / {formatFlow(line.reverse_flow_limit_kw)}</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-[#e2007a]" />
              <span className="text-xs font-medium text-muted-foreground">Przeciążenie</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{line.overload_hours}/{line.horizon_hours}h</p>
            <p className="text-sm text-muted-foreground">{overloadPct}% horyzontu</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base flex items-center gap-2">
            <Wrench className={`w-4 h-4 ${
              action.tone === "danger" ? "text-[#ef4444]" : action.tone === "warn" ? "text-[#f59e0b]" : "text-[#22c55e]"
            }`} />
            {action.title}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground leading-relaxed">{action.body}</p>
        </CardContent>
      </Card>
    </div>
  )
}
