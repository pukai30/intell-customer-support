'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import axios from 'axios'

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

export default function AgentDetailsPage() {
  const params = useParams()
  const agentId = params.agentId as string
  
  const [agent, setAgent] = useState<Agent | null>(null)
  const [holidays, setHolidays] = useState<AgentHoliday[]>([])
  const [loading, setLoading] = useState(true)
  const [showHolidayModal, setShowHolidayModal] = useState(false)
  const [selectedDate, setSelectedDate] = useState('')
  
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

  const loadAgentData = async () => {
    try {
      setLoading(true)
      const [agentRes, holidaysRes] = await Promise.all([
        axios.get(`${API_URL}/api/agents/${agentId}`),
        axios.get(`${API_URL}/api/agents/${agentId}/holidays`)
      ])
      setAgent(agentRes.data)
      setHolidays(holidaysRes.data.holidays || [])
    } catch (error) {
      console.error('Error loading agent data:', error)
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
              <h1 className="text-3xl font-bold text-gray-900">👤 Agent Details</h1>
              <p className="text-gray-600 mt-2">Manage agent information and holiday calendar</p>
            </div>
            <button
              onClick={() => setShowHolidayModal(true)}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              ➕ Add Holiday
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Agent Information */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Agent Information</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Basic Details</h3>
                  <div className="space-y-2 text-sm">
                    <p><span className="font-medium">Name:</span> {agent.name}</p>
                    <p><span className="font-medium">Email:</span> {agent.email}</p>
                    <p><span className="font-medium">Agent ID:</span> {agent.agent_id}</p>
                    <p><span className="font-medium">Domain:</span> {agent.domain}</p>
                    <p><span className="font-medium">Status:</span> 
                      <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${
                        agent.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {agent.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </p>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Work Details</h3>
                  <div className="space-y-2 text-sm">
                    <p><span className="font-medium">Tier:</span> 
                      <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getTierColor(agent.tier)}`}>
                        L{agent.tier}
                      </span>
                    </p>
                    <p><span className="font-medium">Current Load:</span> {agent.current_load}/{agent.max_concurrent_tickets}</p>
                    <p><span className="font-medium">Total Assigned:</span> {agent.total_assigned}</p>
                    <p><span className="font-medium">Total Resolved:</span> {agent.total_resolved}</p>
                    <p><span className="font-medium">Avg Resolution:</span> {agent.avg_resolution_time_minutes}min</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-6">
                <h3 className="font-medium text-gray-900 mb-2">Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {agent.skills.map((skill) => (
                    <span key={skill} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                      {skill} ({agent.skill_levels[skill] || 'beginner'})
                    </span>
                  ))}
                </div>
              </div>
              
              <div className="mt-6">
                <h3 className="font-medium text-gray-900 mb-2">Channels & Schedule</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p><span className="font-medium">Channels:</span> {agent.channels.join(', ')}</p>
                    <p><span className="font-medium">Shift:</span> {agent.shift_start} - {agent.shift_end}</p>
                  </div>
                  <div>
                    <p><span className="font-medium">Timezone:</span> {agent.timezone}</p>
                    <p><span className="font-medium">Handles Escalations:</span> {agent.handles_escalations ? 'Yes' : 'No'}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Holiday Calendar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">📅 Holiday Calendar</h2>
              
              {holidays.length === 0 ? (
                <p className="text-gray-500 text-sm">No holidays scheduled</p>
              ) : (
                <div className="space-y-3">
                  {holidays.map((holiday) => (
                    <div key={holiday.id} className="border border-gray-200 rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-medium text-gray-900 text-sm">{holiday.name}</h3>
                        <button
                          onClick={() => handleDeleteHoliday(holiday.id)}
                          className="text-red-600 hover:text-red-800 text-xs"
                        >
                          Delete
                        </button>
                      </div>
                      <div className="text-xs text-gray-600 space-y-1">
                        <p><span className="font-medium">Date:</span> {formatDate(holiday.date)}</p>
                        <p><span className="font-medium">Type:</span> 
                          <span className={`ml-1 px-2 py-0.5 rounded text-xs font-medium ${getLeaveTypeColor(holiday.leave_type)}`}>
                            {holiday.leave_type}
                          </span>
                        </p>
                        {holiday.start_time && holiday.end_time && (
                          <p><span className="font-medium">Time:</span> {holiday.start_time} - {holiday.end_time}</p>
                        )}
                        {holiday.reason && (
                          <p><span className="font-medium">Reason:</span> {holiday.reason}</p>
                        )}
                        {holiday.approved_by && (
                          <p><span className="font-medium">Approved by:</span> {holiday.approved_by}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

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
      </div>
    </div>
  )
}
