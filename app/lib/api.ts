export type RiskLevel = "NISKIE" | "SREDNIE" | "WYSOKIE"

export interface HourlyGenerationData {
  hour: string
  solar: number
  wind: number
  total: number
}

export interface RiskyAreaData {
  location: string
  risk_score: number
  risk_level: RiskLevel
  peak_hour: string
  expected_overload: number
}

export interface LocationData {
  location_id: string
  name: string
  risk_score: number
  risk_level: RiskLevel
  peak_hour: string
  peak_generation_mw: number
  oze_density: number
  grid_constraint: number
  coordinates: [number, number]
  forecast: { hour: string; generation_mw: number }[]
  recommendations: string[]
  predicted_overload_feeder_count: number
  total_feeder_count: number
}

export interface MVLineForecastPoint {
  hour: string
  generation_mw: number
  probability: number
  reverse_flow_kw: number
  reverse_flow_limit_kw: number
}

export interface MVLineData {
  mv_line_id: string
  location_id: string
  feeder_id: string
  coordinates: [number, number][]
  voltage_v: number | null
  power: string | null
  operator_tag: string | null
  name: string | null
  is_official_tauron_topology: boolean
  risk_score: number
  risk_level: RiskLevel
  max_probability: number
  peak_hour: string
  reverse_flow_kw: number
  reverse_flow_limit_kw: number
  utilization: number
  overload_hours: number
  horizon_hours: number
  forecast: MVLineForecastPoint[]
}

export interface DashboardData {
  generated_at: string | null
  source: string
  horizon_hours: number
  locations: LocationData[]
  hourly_generation: HourlyGenerationData[]
  risky_areas: RiskyAreaData[]
  mv_lines: MVLineData[]
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

export async function fetchDashboardData(): Promise<DashboardData> {
  const response = await fetch(`${API_BASE_URL}/dashboard`, {
    method: "GET",
    cache: "no-store",
  })

  if (!response.ok) {
    throw new Error(`API returned ${response.status} for /dashboard`)
  }

  return response.json()
}
