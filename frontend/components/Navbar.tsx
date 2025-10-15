'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navbar() {
  const pathname = usePathname()

  const isActive = (path: string) => {
    return pathname === path
      ? 'bg-primary-700 text-white'
      : 'text-gray-300 hover:bg-primary-600 hover:text-white'
  }

  return (
    <nav className="bg-primary-800 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-white text-xl font-bold">
              🤖 IT Support
            </Link>
          </div>
          
          <div className="flex space-x-4">
            <Link
              href="/knowledge-base"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/knowledge-base')}`}
            >
              📚 Knowledge Base
            </Link>
            <Link
              href="/tickets"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/tickets')}`}
            >
              🎫 Tickets
            </Link>
            <Link
              href="/agents"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/agents')}`}
            >
              👥 Agents
            </Link>
            <Link
              href="/sla-dashboard"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/sla-dashboard')}`}
            >
              📊 SLA
            </Link>
            <Link
              href="/sla-management"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/sla-management')}`}
            >
              ⚙️ SLA Config
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

{/* 
  AIRLINE SUPPORT FEATURES (COMMENTED OUT)
  
  To enable airline support, uncomment the code below and replace the navbar above:

  import { useState } from 'react'
  
  // Add to component:
  const [domain, setDomain] = useState<'IT' | 'AIRLINE'>('IT')
  const isDomainIT = domain === 'IT'
  const isDomainAirline = domain === 'AIRLINE'
  
  // Domain Switcher (add after brand):
  <div className="flex items-center space-x-2 ml-6">
    <button onClick={() => setDomain('IT')} className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${isDomainIT ? 'bg-white text-primary-800 shadow-md' : 'bg-primary-700 text-gray-300 hover:bg-primary-600'}`}>
      🖥️ IT
    </button>
    <button onClick={() => setDomain('AIRLINE')} className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${isDomainAirline ? 'bg-white text-blue-800 shadow-md' : 'bg-blue-700 text-gray-300 hover:bg-blue-600'}`}>
      ✈️ Airline
    </button>
  </div>
  
  // Airline Links (add before SLA Dashboard):
  {isDomainAirline && (
    <>
      <Link href="/bookings" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/bookings')}`}>
        📋 Bookings
      </Link>
      <Link href="/flights" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/flights')}`}>
        ✈️ Flights
      </Link>
    </>
  )}
*/}

