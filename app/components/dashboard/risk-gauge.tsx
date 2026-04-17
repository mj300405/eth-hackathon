"use client"

import { useEffect, useState } from "react"

interface RiskGaugeProps {
  score: number
  riskLevel: "NISKIE" | "SREDNIE" | "WYSOKIE"
}

function getRiskColor(score: number): string {
  if (score <= 33) return "#22c55e"
  if (score <= 66) return "#f59e0b"
  return "#ef4444"
}

function getRiskLevelLabel(level: "NISKIE" | "SREDNIE" | "WYSOKIE"): string {
  switch (level) {
    case "NISKIE":
      return "NISKIE"
    case "SREDNIE":
      return "ŚREDNIE"
    case "WYSOKIE":
      return "WYSOKIE"
  }
}

export function RiskGauge({ score, riskLevel }: RiskGaugeProps) {
  const [animatedScore, setAnimatedScore] = useState(0)
  const color = getRiskColor(score)

  useEffect(() => {
    const duration = 1000
    const steps = 60
    const increment = score / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= score) {
        setAnimatedScore(score)
        clearInterval(timer)
      } else {
        setAnimatedScore(Math.round(current))
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [score])

  const circumference = 2 * Math.PI * 45
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative">
        <svg width="120" height="120" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="10"
          />
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            transform="rotate(-90 60 60)"
            style={{ transition: "stroke-dashoffset 0.5s ease-out" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold text-foreground">{animatedScore}</span>
          <span className="text-xs text-muted-foreground">/ 100</span>
        </div>
      </div>
      <span
        className="px-3 py-1 text-xs font-semibold rounded-full text-white"
        style={{ backgroundColor: color }}
      >
        {getRiskLevelLabel(riskLevel)}
      </span>
    </div>
  )
}
