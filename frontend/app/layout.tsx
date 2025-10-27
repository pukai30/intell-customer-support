import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Intelligent Customer Support',
  description: 'AI-powered customer support system with knowledge base management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
          <Navbar />
          <main className="container mx-auto px-4 md:px-6 lg:px-8 py-8 max-w-7xl">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}

