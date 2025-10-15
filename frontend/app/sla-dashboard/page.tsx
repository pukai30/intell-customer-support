'use client'

import { useState, useEffect } from 'react'
import { slaAPI } from '@/lib/api'

interface SLADashboard {
  total_tickets: number
  response_sla_breaches: number
  resolution_sla_breaches: number
  escalated_tickets: number
  response_compliance_rate: number
  resolution_compliance_rate: number
  avg_response_time_minutes: number
  tickets_by_escalation_level: {
    L0: number
    L1: number
    L2: number
    L3: number
  }
}

interface BreachedTicket {
  ticket_id: string
  customer_identifier: string
  subject: string
  created_at: string
  sla_response_deadline: string | null
  sla_resolution_deadline: string | null
  response_breached: boolean
  resolution_breached: boolean
  escalation_level: number
  assigned_to: string | null
}

export default function SLADashboardPage() {
  const [dashboard, setDashboard] = useState<SLADashboard | null>(null)
  const [breaches, setBreaches] = useState<BreachedTicket[]>([])
  const [loading, setLoading] = useState(true)

  const loadData = async () => {
    try {
      setLoading(true)
      const [dashboardData, breachesData] = await Promise.all([
        slaAPI.dashboard(),
        slaAPI.breaches()
      ])
      setDashboard(dashboardData)
      setBreaches(breachesData.breached_tickets || [])
    } catch (error) {
      console.error('Error loading SLA data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="container mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading SLA Dashboard...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">📊 SLA Dashboard</h1>
          <p className="text-gray-600 mt-2">Service Level Agreement Monitoring & Compliance</p>
        </div>

        {/* Metrics Grid */}
        {dashboard && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {/* Total Tickets */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Total Tickets</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{dashboard.total_tickets}</p>
                  </div>
                  <div className="bg-blue-100 rounded-full p-3">
                    <span className="text-2xl">🎫</span>
                  </div>
                </div>
              </div>

              {/* Response Compliance */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Response Compliance</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">
                      {dashboard.response_compliance_rate.toFixed(1)}%
                    </p>
                  </div>
                  <div className="bg-green-100 rounded-full p-3">
                    <span className="text-2xl">✅</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {dashboard.response_sla_breaches} breaches
                </p>
              </div>

              {/* Resolution Compliance */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Resolution Compliance</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">
                      {dashboard.resolution_compliance_rate.toFixed(1)}%
                    </p>
                  </div>
                  <div className="bg-green-100 rounded-full p-3">
                    <span className="text-2xl">🎯</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {dashboard.resolution_sla_breaches} breaches
                </p>
              </div>

              {/* Avg Response Time */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Avg Response Time</p>
                    <p className="text-3xl font-bold text-blue-600 mt-2">
                      {dashboard.avg_response_time_minutes.toFixed(0)}m
                    </p>
                  </div>
                  <div className="bg-blue-100 rounded-full p-3">
                    <span className="text-2xl">⏱️</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Escalation Levels */}
            <div className="bg-white rounded-lg shadow p-6 mb-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Tickets by Escalation Level</h2>
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <p className="text-sm text-gray-600">L0 (Initial)</p>
                  <p className="text-2xl font-bold text-green-600 mt-1">
                    {dashboard.tickets_by_escalation_level.L0}
                  </p>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <p className="text-sm text-gray-600">L1 (Escalated)</p>
                  <p className="text-2xl font-bold text-yellow-600 mt-1">
                    {dashboard.tickets_by_escalation_level.L1}
                  </p>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <p className="text-sm text-gray-600">L2 (Expert)</p>
                  <p className="text-2xl font-bold text-orange-600 mt-1">
                    {dashboard.tickets_by_escalation_level.L2}
                  </p>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <p className="text-sm text-gray-600">L3+ (Critical)</p>
                  <p className="text-2xl font-bold text-red-600 mt-1">
                    {dashboard.tickets_by_escalation_level.L3}
                  </p>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Breached Tickets */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold text-gray-900">⚠️ SLA Breached Tickets</h2>
            <p className="text-sm text-gray-600 mt-1">
              Tickets requiring immediate attention
            </p>
          </div>

          {breaches.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-500">✨ No SLA breaches - All tickets within SLA!</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ticket
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Customer
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Subject
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Breach Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Escalation
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Assigned To
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {breaches.map((ticket) => (
                    <tr key={ticket.ticket_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                        {ticket.ticket_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {ticket.customer_identifier}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                        {ticket.subject}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex flex-col space-y-1">
                          {ticket.response_breached && (
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                              Response
                            </span>
                          )}
                          {ticket.resolution_breached && (
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                              Resolution
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          ticket.escalation_level === 0 ? 'bg-green-100 text-green-800' :
                          ticket.escalation_level === 1 ? 'bg-yellow-100 text-yellow-800' :
                          ticket.escalation_level === 2 ? 'bg-orange-100 text-orange-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          L{ticket.escalation_level}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {ticket.assigned_to || 'Unassigned'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

