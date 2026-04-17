"use client"

import { Lightbulb, Battery, Clock, Wrench, MonitorDot } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface RecommendationsProps {
  recommendations: string[]
  riskLevel: "NISKIE" | "SREDNIE" | "WYSOKIE"
}

function getIcon(recommendation: string) {
  if (recommendation.includes("magazynowanie")) return Battery
  if (recommendation.includes("Przesuń")) return Clock
  if (recommendation.includes("modernizacji")) return Wrench
  if (recommendation.includes("monitoring")) return MonitorDot
  return Lightbulb
}

function getSeverityColor(riskLevel: "NISKIE" | "SREDNIE" | "WYSOKIE", index: number): string {
  if (riskLevel === "WYSOKIE" && index === 0) return "bg-[#ef4444]"
  if (riskLevel === "SREDNIE" || (riskLevel === "WYSOKIE" && index === 1)) return "bg-[#f59e0b]"
  return "bg-[#22c55e]"
}

export function Recommendations({ recommendations, riskLevel }: RecommendationsProps) {
  if (recommendations.length === 0) {
    return (
      <Card>
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-[#e2007a]" />
            <CardTitle className="text-lg">Rekomendowane działania</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-6 text-muted-foreground">
            <p className="text-sm">Brak rekomendacji - niskie ryzyko przeciążenia</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-[#e2007a]" />
          <CardTitle className="text-lg">Rekomendowane działania</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <ul className="space-y-3">
          {recommendations.map((rec, index) => {
            const Icon = getIcon(rec)
            const severityColor = getSeverityColor(riskLevel, index)

            return (
              <li
                key={index}
                className="flex items-center gap-3 p-3 rounded-lg bg-muted/50 transition-all hover:bg-muted"
                style={{
                  animationDelay: `${index * 100}ms`,
                  animation: "fadeIn 0.3s ease-out forwards",
                }}
              >
                <div className={`w-2 h-2 rounded-full ${severityColor}`} />
                <Icon className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                <span className="text-sm text-foreground">{rec}</span>
              </li>
            )
          })}
        </ul>
      </CardContent>
    </Card>
  )
}
