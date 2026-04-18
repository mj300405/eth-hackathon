import type { Metadata } from 'next'
import { Titillium_Web } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const titilliumWeb = Titillium_Web({
  subsets: ['latin', 'latin-ext'],
  weight: ['200', '300', '400', '600', '700', '900'],
  display: 'swap',
  variable: '--font-titillium-web',
})

export const metadata: Metadata = {
  title: 'GridFlex OZE - TAURON',
  description: 'System predykcji przeciążeń sieci dystrybucyjnej',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pl" className="bg-background">
      <body className={`${titilliumWeb.variable} font-sans antialiased`}>
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
