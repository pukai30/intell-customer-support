'use client'

import { format } from 'date-fns'
import { useState } from 'react'

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
}

interface TicketDetailsModalProps {
  ticket: Ticket
  onClose: () => void
  onStatusChange: (ticketId: string, status: string) => void
  onAssign?: (ticketId: string, assignedTo: string, notes?: string) => void
}

export default function TicketDetailsModal({ ticket, onClose, onStatusChange, onAssign }: TicketDetailsModalProps) {
  const [showAssignForm, setShowAssignForm] = useState(false)
  const [assignTo, setAssignTo] = useState('')
  const [assignNotes, setAssignNotes] = useState('')
  const [isAssigning, setIsAssigning] = useState(false)

  const handleAssign = async () => {
    if (!assignTo.trim()) {
      alert('Please enter an agent email or name')
      return
    }

    setIsAssigning(true)
    try {
      if (onAssign) {
        await onAssign(ticket.ticket_id, assignTo, assignNotes || undefined)
      }
      setShowAssignForm(false)
      setAssignTo('')
      setAssignNotes('')
    } catch (error) {
      console.error('Error assigning ticket:', error)
      alert('Failed to assign ticket')
    } finally {
      setIsAssigning(false)
    }
  }
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{ticket.ticket_id}</h2>
            <p className="text-gray-600">{ticket.subject || 'No Subject'}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Ticket Info */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6 grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Channel</p>
            <p className="font-medium capitalize">{ticket.channel}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Status</p>
            <p className="font-medium capitalize">{ticket.status}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Customer</p>
            <p className="font-medium">{ticket.customer_name || ticket.customer_identifier}</p>
            <p className="text-sm text-gray-500">{ticket.customer_identifier}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Created</p>
            <p className="font-medium">{format(new Date(ticket.created_at), 'MMM d, yyyy HH:mm')}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Priority</p>
            <p className="font-medium capitalize">{ticket.priority}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Auto-Resolved</p>
            <p className="font-medium">{ticket.auto_resolved ? '✅ Yes' : '❌ No'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Requires Human</p>
            <p className="font-medium">{ticket.requires_human ? '⚠️ Yes' : '✅ No'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Assigned To</p>
            {ticket.assigned_to ? (
              <>
                <p className="font-medium">{ticket.assigned_to}</p>
                {ticket.assigned_at && (
                  <p className="text-xs text-gray-500">
                    {format(new Date(ticket.assigned_at), 'MMM d, HH:mm')}
                  </p>
                )}
              </>
            ) : (
              <p className="font-medium text-gray-400">Unassigned</p>
            )}
          </div>
        </div>

        {/* Conversation */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Full Email Trace / Conversation</h3>
          <div className="space-y-4">
            {ticket.conversation && ticket.conversation.length > 0 ? (
              ticket.conversation.map((message, idx) => (
                <div
                  key={idx}
                  className={`p-4 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-50 border-l-4 border-blue-500'
                      : message.role === 'assistant'
                      ? 'bg-green-50 border-l-4 border-green-500'
                      : 'bg-gray-50 border-l-4 border-gray-500'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <span className="font-semibold capitalize">
                        {message.role === 'user' ? '👤 Customer' : message.role === 'assistant' ? '🤖 AI Assistant' : '⚙️ System'}
                      </span>
                      {message.metadata && message.metadata.auto_generated && (
                        <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          Auto-Generated
                        </span>
                      )}
                      {message.metadata && message.metadata.confidence && (
                        <span className="ml-2 text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                          Confidence: {(message.metadata.confidence * 100).toFixed(0)}%
                        </span>
                      )}
                    </div>
                    <span className="text-sm text-gray-500">
                      {format(new Date(message.timestamp), 'MMM d, HH:mm:ss')}
                    </span>
                  </div>
                  <div className="text-gray-800 whitespace-pre-wrap">{message.content}</div>
                  {message.metadata && Object.keys(message.metadata).length > 0 && (
                    <details className="mt-2 text-sm">
                      <summary className="text-gray-500 cursor-pointer">Metadata</summary>
                      <pre className="mt-2 p-2 bg-white rounded text-xs overflow-x-auto">
                        {JSON.stringify(message.metadata, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-8">No conversation messages</p>
            )}
          </div>
        </div>

        {/* Assignment Section */}
        {!ticket.assigned_to && onAssign && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-lg font-semibold text-gray-900">
                {ticket.requires_human ? '⚠️ Requires Human Assignment' : 'Assign Ticket'}
              </h3>
              {!showAssignForm && (
                <button
                  onClick={() => setShowAssignForm(true)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Assign to Agent
                </button>
              )}
            </div>

            {showAssignForm && (
              <div className="mt-4 space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Agent Email/Name *
                  </label>
                  <input
                    type="text"
                    value={assignTo}
                    onChange={(e) => setAssignTo(e.target.value)}
                    placeholder="e.g., agent@company.com or John Smith"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Assignment Notes (Optional)
                  </label>
                  <textarea
                    value={assignNotes}
                    onChange={(e) => setAssignNotes(e.target.value)}
                    placeholder="Any special instructions or context..."
                    rows={3}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={handleAssign}
                    disabled={isAssigning}
                    className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400"
                  >
                    {isAssigning ? 'Assigning...' : 'Confirm Assignment'}
                  </button>
                  <button
                    onClick={() => {
                      setShowAssignForm(false)
                      setAssignTo('')
                      setAssignNotes('')
                    }}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-between items-center pt-6 border-t">
          <div className="flex gap-2">
            <select
              value={ticket.status}
              onChange={(e) => onStatusChange(ticket.ticket_id, e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="open">Open</option>
              <option value="pending">Pending</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

