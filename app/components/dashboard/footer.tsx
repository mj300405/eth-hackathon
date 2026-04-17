import { Info } from "lucide-react"

export function Footer() {
  return (
    <footer className="border-t border-border bg-card mt-auto">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <span>Dane pogodowe: IMGW-PIB</span>
            <span className="text-border">|</span>
            <span>Scenariusz: Syntetyczny</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#f59e0b]/10 border border-[#f59e0b]/20">
              <Info className="w-3.5 h-3.5 text-[#f59e0b]" />
              <span className="text-xs font-medium text-[#f59e0b]">
                Demo MVP - dane produkcyjne wymagają integracji z TAURON OSD
              </span>
            </div>

            <span className="text-xs text-muted-foreground">
              Made during ETHSilesia 2026 hackathon
            </span>
          </div>
        </div>
      </div>
    </footer>
  )
}
