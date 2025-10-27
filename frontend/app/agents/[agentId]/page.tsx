'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import axios from 'axios'
import { 
  format, 
  startOfMonth, 
  endOfMonth, 
  startOfWeek, 
  endOfWeek, 
  eachDayOfInterval,
  isSameMonth,
  isToday,
  addMonths,
  subMonths
} from 'date-fns'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Agent {
  agent_id: string
  name: string
  email: string
  skills: string[]
  skill_levels: Record<string, string>
  tier: number
  is_active: boolean
  current_load: number
  max_concurrent_tickets: number
  total_assigned: number
  total_resolved: number
  avg_resolution_time_minutes: number
  channels: string[]
  shift_start: string
  shift_end: string
  timezone: string
  handles_escalations: boolean
  domain: string
  created_at: string
  last_assigned_at: string
}

interface AgentHoliday {
  id: string
  date: string
  name: string
  leave_type: string
  is_working_day: boolean
  start_time: string | null
  end_time: string | null
  reason: string | null
  approved_by: string | null
  created_at: string
}

interface OfficialHoliday {
  date: string
  name: string
  holiday_type: string
  region: string | null
  is_working_day: boolean
  is_recurring: boolean
}

interface AssignedTicket {
  ticket_id: string
  channel: string
  customer_identifier: string
  subject: string
  status: string
  priority: string
  created_at: string
  assigned_at: string
}

interface AvailableAgent {
  agent_id: string
  name: string
  email: string
  current_load: number
  max_concurrent_tickets: number
}

export default function AgentDetailsPage() {
  const params = useParams()
  const router = useRouter()
  const agentId = params.agentId as string
  
  const [agent, setAgent] = useState<Agent | null>(null)
  const [holidays, setHolidays] = useState<AgentHoliday[]>([])
  const [officialHolidays, setOfficialHolidays] = useState<OfficialHoliday[]>([])
  const [assignedTickets, setAssignedTickets] = useState<AssignedTicket[]>([])
  const [availableAgents, setAvailableAgents] = useState<AvailableAgent[]>([])
  const [loading, setLoading] = useState(true)
  const [showHolidayModal, setShowHolidayModal] = useState(false)
  const [showCalendar, setShowCalendar] = useState(false)
  const [showReassignModal, setShowReassignModal] = useState(false)
  const [selectedTicket, setSelectedTicket] = useState<AssignedTicket | null>(null)
  const [selectedDate, setSelectedDate] = useState('')
  const [currentMonth, setCurrentMonth] = useState(new Date())
  
  // Holiday form state
  const [holidayForm, setHolidayForm] = useState({
    date: '',
    name: '',
    leave_type: 'personal',
    is_working_day: false,
    start_time: '',
    end_time: '',
    reason: '',
    approved_by: ''
  })

  // Reassignment form state
  const [reassignForm, setReassignForm] = useState({
    new_agent_id: '',
    reason: ''
  })

  const loadAgentData = async () => {
    try {
      setLoading(true)
      const agentRes = await axios.get(`${API_URL}/api/agents/${agentId}`)
      setAgent(agentRes.data)
      
      console.log('Loading assigned tickets for agent:', agentRes.data.email)
      
      // Load other data after we have the agent
      const [holidaysRes, officialHolidaysRes, assignedTicketsRes, agentsRes] = await Promise.all([
        axios.get(`${API_URL}/api/agents/${agentId}/holidays`),
        axios.get(`${API_URL}/api/holidays/list`),
        axios.get(`${API_URL}/api/tickets/assigned/${encodeURIComponent(agentRes.data.email)}`),
        axios.get(`${API_URL}/api/agents/list`)
      ])
      
      console.log('Assigned tickets response:', assignedTicketsRes.data)
      
      setHolidays(holidaysRes.data.holidays || [])
      setOfficialHolidays(officialHolidaysRes.data.holidays || [])
      setAssignedTickets(assignedTicketsRes.data.tickets || [])
      setAvailableAgents(agentsRes.data.agents || [])
    } catch (error: any) {
      console.error('Error loading agent data:', error)
      console.error('Error details:', error.response?.data)
      alert(`Error loading data: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (agentId) {
      loadAgentData()
    }
  }, [agentId])

  const handleCreateHoliday = async () => {
    try {
      await axios.post(`${API_URL}/api/agents/${agentId}/holidays/create`, {
        ...holidayForm,
        agent_id: agentId
      })
      alert('Holiday created successfully!')
      setShowHolidayModal(false)
      loadAgentData()
      // Reset form
      setHolidayForm({
        date: '',
        name: '',
        leave_type: 'personal',
        is_working_day: false,
        start_time: '',
        end_time: '',
        reason: '',
        approved_by: ''
      })
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleDeleteHoliday = async (holidayId: string) => {
    if (!confirm('Are you sure you want to delete this holiday?')) return
    try {
      await axios.delete(`${API_URL}/api/agents/${agentId}/holidays/${holidayId}`)
      alert('Holiday deleted successfully!')
      loadAgentData()
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleReassignTicket = async () => {
    if (!selectedTicket || !reassignForm.new_agent_id) {
      alert('Please select a new agent')
      return
    }
    
    try {
      await axios.post(`${API_URL}/api/tickets/${selectedTicket.ticket_id}/reassign`, {
        ticket_id: selectedTicket.ticket_id,
        new_agent_id: reassignForm.new_agent_id,
        reason: reassignForm.reason
      })
      alert('Ticket reassigned successfully!')
      setShowReassignModal(false)
      setSelectedTicket(null)
      setReassignForm({ new_agent_id: '', reason: '' })
      loadAgentData()
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || error.message}`)
    }
  }

  const openReassignModal = (ticket: AssignedTicket) => {
    setSelectedTicket(ticket)
    setShowReassignModal(true)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getTierColor = (tier: number) => {
    switch (tier) {
      case 0: return 'bg-green-100 text-green-800'
      case 1: return 'bg-blue-100 text-blue-800'
      case 2: return 'bg-purple-100 text-purple-800'
      case 3: return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getLeaveTypeColor = (leaveType: string) => {
    switch (leaveType) {
      case 'personal': return 'bg-blue-100 text-blue-800'
      case 'sick': return 'bg-red-100 text-red-800'
      case 'vacation': return 'bg-green-100 text-green-800'
      case 'emergency': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open': return 'bg-yellow-100 text-yellow-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'resolved': return 'bg-green-100 text-green-800'
      case 'closed': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  // Calendar helper functions
  const isWeekend = (date: Date) => {
    const day = date.getDay()
    return day === 0 || day === 6 // Sunday or Saturday
  }

  const isNationalHoliday = (date: Date) => {
    const dateStr = format(date, 'yyyy-MM-dd')
    return officialHolidays.some(h => h.date === dateStr && h.holiday_type === 'national')
  }

  const isPersonalHoliday = (date: Date) => {
    const dateStr = format(date, 'yyyy-MM-dd')
    return holidays.some(h => h.date === dateStr)
  }

  const getDateCellClass = (date: Date) => {
    if (isToday(date)) {
      return 'bg-blue-500 text-white font-bold'
    }
    if (isWeekend(date) || isNationalHoliday(date)) {
      return 'bg-red-100 text-red-800 font-medium'
    }
    if (isPersonalHoliday(date)) {
      return 'bg-gray-300 text-gray-700'
    }
    return 'bg-white text-gray-900 hover:bg-gray-100'
  }

  const getCalendarDays = () => {
    const monthStart = startOfMonth(currentMonth)
    const monthEnd = endOfMonth(currentMonth)
    const calendarStart = startOfWeek(monthStart)
    const calendarEnd = endOfWeek(monthEnd)
    
    return eachDayOfInterval({ start: calendarStart, end: calendarEnd })
  }

  const handleCalendarNavigation = (direction: 'prev' | 'next') => {
    setCurrentMonth(direction === 'prev' ? subMonths(currentMonth, 1) : addMonths(currentMonth, 1))
  }

  const handleOpenCalendar = () => {
    setCurrentMonth(new Date()) // Set to today's month
    setShowCalendar(true)
  }

  // Tabular structure for agent information - only Name, Email, Current Load, Channels
  const agentDetails = agent ? [
    { label: 'Name', value: agent.name },
    { label: 'Email', value: agent.email },
    { label: 'Current Load', value: `${agent.current_load}/${agent.max_concurrent_tickets}` },
    { label: 'Channels', value: agent.channels.join(', ') }
  ] : []

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading agent details...</p>
        </div>
      </div>
    )
  }

  if (!agent) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="text-center py-12">
          <p className="text-gray-600">Agent not found</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <button 
                onClick={() => router.push('/agents')}
                className="text-primary-600 hover:text-primary-700 mb-2 text-sm font-medium"
              >
                ← Back to Agents
              </button>
              <h1 className="text-3xl font-bold text-gray-900">👤 Agent Details</h1>
              <p className="text-gray-600 mt-2">Comprehensive agent information and management</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleOpenCalendar}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center gap-2"
              >
                📅 View Calendar
              </button>
              <button
                onClick={() => setShowHolidayModal(true)}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium flex items-center gap-2"
              >
                ➕ Add Holiday
              </button>
            </div>
          </div>
        </div>

        {/* Agent Information Table */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Agent Information</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <tbody className="divide-y divide-gray-200">
                {agentDetails.map((detail, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-700 w-1/3">
                      {detail.label}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      <span>{detail.value}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Skills Section */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Skills</h2>
          </div>
          <div className="px-6 py-4">
            <div className="flex flex-wrap gap-2">
              {agent.skills.map((skill) => (
                <span key={skill} className="px-3 py-2 bg-blue-100 text-blue-800 rounded-lg text-sm font-medium">
                  {skill} <span className="text-xs opacity-75">({agent.skill_levels[skill] || 'beginner'})</span>
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Assigned Issues Table */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">📋 Assigned Issues</h2>
            <p className="text-sm text-gray-600 mt-1">Tickets currently assigned to this agent</p>
          </div>
          <div className="overflow-x-auto">
            {assignedTickets.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                <p className="text-lg">No assigned tickets</p>
                <p className="text-sm mt-2">This agent has no active ticket assignments</p>
              </div>
            ) : (
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ticket ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Channel</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assigned</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {assignedTickets.map((ticket) => (
                    <tr key={ticket.ticket_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {ticket.ticket_id}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate" title={ticket.subject}>
                        {ticket.subject}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {ticket.customer_identifier}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <span className="inline-flex px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full">
                          {ticket.channel}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(ticket.status)}`}>
                          {ticket.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(ticket.priority)}`}>
                          {ticket.priority}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(ticket.assigned_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => openReassignModal(ticket)}
                          className="text-primary-600 hover:text-primary-900 bg-primary-50 hover:bg-primary-100 px-3 py-1 rounded-md text-xs font-medium transition-colors"
                        >
                          Reassign
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Agent Holidays */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">📅 Personal Holidays & Leaves</h2>
            </div>
            <div className="p-6">
              {holidays.length === 0 ? (
                <p className="text-gray-500 text-sm text-center py-8">No personal holidays scheduled</p>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {holidays.map((holiday) => (
                    <div key={holiday.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-gray-900">{holiday.name}</h3>
                        <button
                          onClick={() => handleDeleteHoliday(holiday.id)}
                          className="text-red-600 hover:text-red-800 text-sm font-medium"
                        >
                          🗑️ Delete
                        </button>
                      </div>
                      <div className="space-y-1.5 text-sm">
                        <div className="flex items-center">
                          <span className="font-medium text-gray-600 w-24">Date:</span>
                          <span className="text-gray-900">{formatDate(holiday.date)}</span>
                        </div>
                        <div className="flex items-center">
                          <span className="font-medium text-gray-600 w-24">Type:</span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getLeaveTypeColor(holiday.leave_type)}`}>
                            {holiday.leave_type}
                          </span>
                        </div>
                        {holiday.start_time && holiday.end_time && (
                          <div className="flex items-center">
                            <span className="font-medium text-gray-600 w-24">Time:</span>
                            <span className="text-gray-900">{holiday.start_time} - {holiday.end_time}</span>
                          </div>
                        )}
                        {holiday.reason && (
                          <div className="flex items-start">
                            <span className="font-medium text-gray-600 w-24">Reason:</span>
                            <span className="text-gray-900 flex-1">{holiday.reason}</span>
                          </div>
                        )}
                        {holiday.approved_by && (
                          <div className="flex items-center">
                            <span className="font-medium text-gray-600 w-24">Approved by:</span>
                            <span className="text-gray-900">{holiday.approved_by}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">🏛️ Official Holidays</h2>
            </div>
            <div className="p-6">
              {officialHolidays.length === 0 ? (
                <p className="text-gray-500 text-sm text-center py-8">No official holidays loaded</p>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {officialHolidays.map((holiday, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-gray-900 text-sm">{holiday.name}</p>
                          <p className="text-xs text-gray-600">{holiday.date} • {holiday.holiday_type}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Calendar Modal */}
        {showCalendar && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
              <div className="px-6 py-4 border-b flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900">📅 Holiday Calendar</h2>
                <button
                  onClick={() => setShowCalendar(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
                >
                  ×
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-6">
                {/* Calendar Navigation */}
                <div className="flex items-center justify-between mb-6">
                  <button
                    onClick={() => handleCalendarNavigation('prev')}
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    ← Previous
                  </button>
                  <h3 className="text-xl font-bold text-gray-900">
                    {format(currentMonth, 'MMMM yyyy')}
                  </h3>
                  <button
                    onClick={() => handleCalendarNavigation('next')}
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Next →
                  </button>
                </div>

                {/* Calendar Grid */}
                <div className="grid grid-cols-7 gap-1 mb-4">
                  {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                    <div key={day} className="text-center font-semibold text-gray-700 py-2">
                      {day}
                    </div>
                  ))}
                  
                  {getCalendarDays().map((day, idx) => {
                    const dateStr = format(day, 'yyyy-MM-dd')
                    const dayHoliday = officialHolidays.find(h => h.date === dateStr)
                    const personalHoliday = holidays.find(h => h.date === dateStr)
                    
                    return (
                      <div
                        key={idx}
                        className={`aspect-square flex flex-col items-center justify-center text-sm rounded-lg transition-all ${
                          !isSameMonth(day, currentMonth) ? 'text-gray-400' : getDateCellClass(day)
                        }`}
                      >
                        <span>{format(day, 'd')}</span>
                        {(dayHoliday || personalHoliday) && (
                          <span className="text-xs mt-1 px-1 py-0.5 bg-white bg-opacity-50 rounded truncate w-full text-center">
                            {dayHoliday ? dayHoliday.name : personalHoliday?.name}
                          </span>
                        )}
                      </div>
                    )
                  })}
                </div>

                {/* Legend */}
                <div className="mt-6 border-t pt-4">
                  <h4 className="font-semibold text-gray-900 mb-3">Legend:</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 bg-blue-500 rounded"></div>
                      <span>Today</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 bg-red-100 rounded"></div>
                      <span>Weekend/Holiday</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 bg-gray-300 rounded"></div>
                      <span>Personal Leave</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 bg-white border rounded"></div>
                      <span>Work Day</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="px-6 py-4 border-t bg-gray-50 flex justify-end">
                <button
                  onClick={() => setShowCalendar(false)}
                  className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Add Holiday Modal */}
        {showHolidayModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b">
                <h2 className="text-2xl font-bold text-gray-900">Add Holiday/Leave</h2>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date *
                  </label>
                  <input
                    type="date"
                    value={holidayForm.date}
                    onChange={(e) => setHolidayForm({...holidayForm, date: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Holiday/Leave Name *
                  </label>
                  <input
                    type="text"
                    value={holidayForm.name}
                    onChange={(e) => setHolidayForm({...holidayForm, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    placeholder="e.g., Personal Leave, Sick Leave"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Leave Type
                  </label>
                  <select
                    value={holidayForm.leave_type}
                    onChange={(e) => setHolidayForm({...holidayForm, leave_type: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="personal">Personal</option>
                    <option value="sick">Sick Leave</option>
                    <option value="vacation">Vacation</option>
                    <option value="emergency">Emergency</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Start Time (Optional)
                    </label>
                    <input
                      type="time"
                      value={holidayForm.start_time}
                      onChange={(e) => setHolidayForm({...holidayForm, start_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      End Time (Optional)
                    </label>
                    <input
                      type="time"
                      value={holidayForm.end_time}
                      onChange={(e) => setHolidayForm({...holidayForm, end_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Reason (Optional)
                  </label>
                  <textarea
                    value={holidayForm.reason}
                    onChange={(e) => setHolidayForm({...holidayForm, reason: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    rows={2}
                    placeholder="Reason for leave..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Approved By (Optional)
                  </label>
                  <input
                    type="text"
                    value={holidayForm.approved_by}
                    onChange={(e) => setHolidayForm({...holidayForm, approved_by: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    placeholder="Manager name"
                  />
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={holidayForm.is_working_day}
                    onChange={(e) => setHolidayForm({...holidayForm, is_working_day: e.target.checked})}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Agent can work on this day (partial leave)</span>
                </div>
              </div>
              <div className="p-6 border-t flex justify-end space-x-3">
                <button
                  onClick={() => setShowHolidayModal(false)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateHoliday}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Add Holiday
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Reassignment Modal */}
        {showReassignModal && selectedTicket && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b">
                <h2 className="text-2xl font-bold text-gray-900">Reassign Ticket</h2>
                <p className="text-sm text-gray-600 mt-1">Ticket: {selectedTicket.ticket_id}</p>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Select New Agent *
                  </label>
                  <select
                    value={reassignForm.new_agent_id}
                    onChange={(e) => setReassignForm({...reassignForm, new_agent_id: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    required
                  >
                    <option value="">Choose an agent...</option>
                    {availableAgents
                      .filter(agent => agent.agent_id !== agentId) // Exclude current agent
                      .map((agent) => (
                        <option key={agent.agent_id} value={agent.agent_id}>
                          {agent.name} ({agent.email}) - Load: {agent.current_load}/{agent.max_concurrent_tickets}
                        </option>
                      ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Reason for Reassignment (Optional)
                  </label>
                  <textarea
                    value={reassignForm.reason}
                    onChange={(e) => setReassignForm({...reassignForm, reason: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    rows={3}
                    placeholder="Reason for reassignment..."
                  />
                </div>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-medium text-blue-900 mb-2">Ticket Details:</h3>
                  <div className="text-sm text-blue-800 space-y-1">
                    <p><span className="font-medium">Subject:</span> {selectedTicket.subject}</p>
                    <p><span className="font-medium">Customer:</span> {selectedTicket.customer_identifier}</p>
                    <p><span className="font-medium">Status:</span> 
                      <span className={`ml-1 px-2 py-0.5 rounded text-xs font-medium ${getStatusColor(selectedTicket.status)}`}>
                        {selectedTicket.status}
                      </span>
                    </p>
                    <p><span className="font-medium">Priority:</span> 
                      <span className={`ml-1 px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(selectedTicket.priority)}`}>
                        {selectedTicket.priority}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
              <div className="p-6 border-t flex justify-end space-x-3">
                <button
                  onClick={() => {
                    setShowReassignModal(false)
                    setSelectedTicket(null)
                    setReassignForm({ new_agent_id: '', reason: '' })
                  }}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleReassignTicket}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Reassign Ticket
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
