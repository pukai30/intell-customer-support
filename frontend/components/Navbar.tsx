'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navbar() {
  const pathname = usePathname()

  const isActive = (path: string) => {
    return pathname === path
      ? 'bg-white text-primary-600 shadow-md'
      : 'text-slate-700 hover:bg-white/50 hover:text-primary-600'
  }

  return (
    <nav className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 shadow-xl border-b-4 border-blue-500">
      <div className="container mx-auto px-4 md:px-6">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center space-x-3">
            <div className="bg-white rounded-lg p-2 shadow-lg">
              <span className="text-2xl">🤖</span>
            </div>
            <Link href="/" className="text-white text-2xl font-bold tracking-tight hover:text-blue-100 transition-colors">
              Intelligent Support
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-2">
            <Link
              href="/knowledge-base"
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${isActive('/knowledge-base')}`}
            >
              📚 Knowledge Base
            </Link>
            <Link
              href="/tickets"
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${isActive('/tickets')}`}
            >
              🎫 Tickets
            </Link>
            <Link
              href="/agents"
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${isActive('/agents')}`}
            >
              👥 Agents
            </Link>
            {/* SLA Dashboard - Commented out */}
            {/* <Link
              href="/sla-dashboard"
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${isActive('/sla-dashboard')}`}
            >
              📊 SLA Dashboard
            </Link> */}
            {/* SLA Management - Commented out */}
            {/* <Link
              href="/sla-management"
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${isActive('/sla-management')}`}
            >
              ⚙️ SLA Config
            </Link> */}
            <Link
              href="/settings"
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${isActive('/settings')}`}
            >
              ⚙️ Settings
            </Link>
          </div>

          {/* Mobile menu button */}
          <button className="md:hidden text-white hover:text-blue-100 p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  )
}

