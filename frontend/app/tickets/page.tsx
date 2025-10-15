'use client'

import { useState, useEffect } from 'react'
import { ticketsAPI } from '@/lib/api'
import { format } from 'date-fns'
import TicketDetailsModal from '@/components/TicketDetailsModal'

interface Message {
  role: string
  content: string
  timestamp: string
  metadata?: any
}

interface Ticket {
  ticket_id: string
  channel: string
  customer_identifier: string
  customer_name?: string
  subject?: string
  status: string
  priority: string
  conversation?: Message[]
  auto_resolved: boolean
  requires_human?: boolean
  assigned_to?: string
  assigned_at?: string
  created_at: string
  updated_at: string
  message_count?: number
}

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [filterStatus, setFilterStatus] = useState('')
  const [filterChannel, setFilterChannel] = useState('')
  const [unassignedCount, setUnassignedCount] = useState(0)
  const [showNotificationBanner, setShowNotificationBanner] = useState(true)

  useEffect(() => {
    loadTickets()
  }, [filterStatus, filterChannel])

  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      loadTickets()
    }, 10000) // Refresh every 10 seconds

    return () => clearInterval(interval)
  }, [autoRefresh, filterStatus, filterChannel])

  const loadTickets = async () => {
    try {
      const params: any = {}
      if (filterStatus) params.status = filterStatus
      if (filterChannel) params.channel = filterChannel
      
      const response = await ticketsAPI.list(params)
      setTickets(response.tickets || [])
      
      // Also load unassigned tickets count for notification
      try {
        const unassignedResponse = await ticketsAPI.getUnassigned(true)
        setUnassignedCount(unassignedResponse.count || 0)
      } catch (err) {
        console.error('Error loading unassigned count:', err)
      }
    } catch (error) {
      console.error('Error loading tickets:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (ticketId: string, newStatus: string) => {
    try {
      await ticketsAPI.updateStatus(ticketId, newStatus)
      alert(`Ticket status updated to ${newStatus}`)
      loadTickets()
    } catch (error) {
      console.error('Error updating status:', error)
      alert('Failed to update ticket status')
    }
  }

  const handleAssign = async (ticketId: string, assignedTo: string, notes?: string) => {
    try {
      await ticketsAPI.assign(ticketId, assignedTo, notes)
      alert(`Ticket assigned to ${assignedTo}`)
      loadTickets()
      // Reload the selected ticket to show updated assignment
      if (selectedTicket?.ticket_id === ticketId) {
        const updatedTicket = await ticketsAPI.get(ticketId)
        setSelectedTicket(updatedTicket)
      }
    } catch (error) {
      console.error('Error assigning ticket:', error)
      alert('Failed to assign ticket')
      throw error // Re-throw to let the modal handle it
    }
  }

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case 'email': return '📧'
      case 'sms': return '💬'
      case 'whatsapp': return '📱'
      case 'chat': return '💻'
      default: return '📨'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'resolved': return 'bg-blue-100 text-blue-800'
      case 'closed': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Email Ticket Monitoring</h1>
          <p className="text-gray-600 mt-1">Real-time ticket tracking and management</p>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <span>Auto-refresh (10s)</span>
          </label>
          <button
            onClick={loadTickets}
            className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Notification Banner for Unassigned Tickets */}
      {unassignedCount > 0 && showNotificationBanner && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-2xl">⚠️</span>
              <div>
                <h3 className="text-lg font-semibold text-yellow-800">
                  {unassignedCount} {unassignedCount === 1 ? 'Ticket Requires' : 'Tickets Require'} Human Attention
                </h3>
                <p className="text-sm text-yellow-700 mt-1">
                  Low confidence AI responses detected. These tickets need manual assignment and review.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  setFilterStatus('')
                  setFilterChannel('')
                  const unassignedTickets = tickets.filter(t => t.requires_human && !t.assigned_to)
                  if (unassignedTickets.length > 0) {
                    setSelectedTicket(unassignedTickets[0])
                  }
                }}
                className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
              >
                View & Assign
              </button>
              <button
                onClick={() => setShowNotificationBanner(false)}
                className="text-yellow-600 hover:text-yellow-800 font-bold text-xl px-2"
                title="Dismiss"
              >
                ×
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center gap-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mr-2">Status:</label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">All</option>
              <option value="open">Open</option>
              <option value="pending">Pending</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 mr-2">Channel:</label>
            <select
              value={filterChannel}
              onChange={(e) => setFilterChannel(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">All</option>
              <option value="email">Email</option>
              <option value="sms">SMS</option>
              <option value="whatsapp">WhatsApp</option>
              <option value="chat">Chat</option>
            </select>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Total Tickets</div>
          <div className="text-2xl font-bold text-gray-900">{tickets?.length || 0}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Open</div>
          <div className="text-2xl font-bold text-green-600">
            {tickets?.filter(t => t.status === 'open').length || 0}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Pending</div>
          <div className="text-2xl font-bold text-yellow-600">
            {tickets?.filter(t => t.status === 'pending').length || 0}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Auto-Resolved</div>
          <div className="text-2xl font-bold text-blue-600">
            {tickets?.filter(t => t.auto_resolved).length || 0}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-gray-500">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4">Loading tickets...</p>
          </div>
        ) : !tickets || tickets.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <p className="text-lg">No tickets found</p>
            <p className="text-sm mt-2">Tickets will appear here when customers contact support</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ticket ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Channel
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Subject / Preview
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Messages
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tickets.map((ticket) => (
                  <tr key={ticket.ticket_id} className={`hover:bg-gray-50 ${ticket.requires_human && !ticket.assigned_to ? 'bg-yellow-50' : ''}`}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      <div className="flex items-center gap-2">
                        {ticket.requires_human && !ticket.assigned_to && (
                          <span className="text-yellow-500" title="Requires Human Attention">⚠️</span>
                        )}
                        <span>{ticket.ticket_id}</span>
                      </div>
                      <div className="flex gap-1 mt-1">
                        {ticket.auto_resolved && (
                          <span className="text-xs text-blue-600 bg-blue-100 px-1 rounded">🤖 Auto</span>
                        )}
                        {ticket.assigned_to && (
                          <span className="text-xs text-green-600 bg-green-100 px-1 rounded" title={`Assigned to ${ticket.assigned_to}`}>
                            👤 {ticket.assigned_to.split('@')[0] || ticket.assigned_to}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="flex items-center gap-2">
                        <span className="text-xl">{getChannelIcon(ticket.channel)}</span>
                        <span className="text-sm text-gray-900 capitalize">{ticket.channel}</span>
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">{ticket.customer_name || 'Unknown'}</div>
                      <div className="text-sm text-gray-500">{ticket.customer_identifier}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900 font-medium">{ticket.subject || 'No Subject'}</div>
                      {ticket.conversation && ticket.conversation.length > 0 && (
                        <div className="text-sm text-gray-500 truncate max-w-md">
                          {ticket.conversation[0].content.substring(0, 100)}...
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {ticket.message_count || ticket.conversation?.length || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(ticket.status)}`}>
                        {ticket.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div>{format(new Date(ticket.created_at), 'MMM d, yyyy')}</div>
                      <div className="text-xs text-gray-400">{format(new Date(ticket.created_at), 'HH:mm')}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        onClick={() => setSelectedTicket(ticket)}
                        className="text-primary-600 hover:text-primary-900 font-medium"
                      >
                        👁️ View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Ticket Details Modal */}
      {selectedTicket && (
        <TicketDetailsModal
          ticket={selectedTicket}
          onClose={() => setSelectedTicket(null)}
          onStatusChange={handleStatusChange}
          onAssign={handleAssign}
        />
      )}
    </div>
  )
}

