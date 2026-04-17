"use client"

import { MapPin, Clock, Activity, Gauge } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RiskGauge } from "./risk-gauge"
import { ForecastChart } from "./forecast-chart"
import type { LocationData } from "@/lib/data"

interface LocationDetailsProps {
  location: LocationData
}

export function LocationDetails({ location }: LocationDetailsProps) {
  return (
    <div className="flex flex-col gap-4">
      <Card>
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-[#e2007a]" />
            <CardTitle className="text-lg">{location.name}</CardTitle>
          </div>
          <p className="text-sm text-muted-foreground">Oddział TAURON Dystrybucja</p>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <RiskGauge score={location.risk_score} riskLevel={location.risk_level} />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium mb-2 text-muted-foreground">
                Prognoza generacji OZE (24h)
              </p>
              <ForecastChart forecast={location.forecast} peakHour={location.peak_hour} />
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-3 gap-3">
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="w-4 h-4 text-[#e2007a]" />
              <span className="text-xs font-medium text-muted-foreground">Szczyt generacji</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{location.peak_hour}</p>
            <p className="text-sm text-muted-foreground">{location.peak_generation_mw} MW</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-[#e2007a]" />
              <span className="text-xs font-medium text-muted-foreground">Gęstość OZE</span>
            </div>
            <p className="text-2xl font-bold text-foreground">
              {(location.oze_density * 100).toFixed(0)}%
            </p>
            <p className="text-sm text-muted-foreground">nasycenia sieci</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 mb-2">
              <Gauge className="w-4 h-4 text-[#e2007a]" />
              <span className="text-xs font-medium text-muted-foreground">Obciążenie sieci</span>
            </div>
            <p className="text-2xl font-bold text-foreground">
              {(location.grid_constraint * 100).toFixed(0)}%
            </p>
            <p className="text-sm text-muted-foreground">wykorzystania</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
