'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { agentsAPI } from '@/lib/api'
import { format } from 'date-fns'

interface Agent {
  agent_id: string
  name: string
  email: string
  skills: string[]
  skill_levels: Record<string, string>
  is_active: boolean
  current_load: number
  max_concurrent_tickets: number
  utilization_percent: number
  total_assigned: number
  total_resolved: number
  channels: string[]
  created_at: string
  open_ticket_ids?: string[]
  open_count?: number
  resolved_count?: number
  last_assigned_at?: string
}

interface TeamStats {
  total_agents: number
  active_agents: number
  total_capacity: number
  total_load: number
  team_utilization_percent: number
  available_capacity: number
  agents: Agent[]
  top_performers: Agent[]
}

export default function AgentsPage() {
  const router = useRouter()
  const [teamStats, setTeamStats] = useState<TeamStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [showInactive, setShowInactive] = useState(false)

  useEffect(() => {
    loadTeamStats()
  }, [showInactive])

  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      loadTeamStats()
    }, 30000) // Refresh every 30 seconds

    return () => clearInterval(interval)
  }, [autoRefresh, showInactive])

  const loadTeamStats = async () => {
    try {
      const stats = await agentsAPI.getTeamStats()
      setTeamStats(stats)
    } catch (error) {
      console.error('Error loading team stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleAgentStatus = async (agentId: string, currentStatus: boolean) => {
    try {
      await agentsAPI.updateStatus(agentId, !currentStatus)
      await loadTeamStats()
    } catch (error) {
      console.error('Error toggling agent status:', error)
      alert('Failed to update agent status')
    }
  }

  const getSkillLevelColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'expert': return 'bg-green-100 text-green-800'
      case 'intermediate': return 'bg-blue-100 text-blue-800'
      case 'beginner': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getUtilizationColor = (percent: number) => {
    if (percent >= 90) return 'bg-red-500'
    if (percent >= 70) return 'bg-yellow-500'
    if (percent >= 50) return 'bg-blue-500'
    return 'bg-green-500'
  }

  const filteredAgents = teamStats?.agents.filter(agent => 
    showInactive ? true : agent.is_active
  ) || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Support Agents</h1>
          <p className="text-gray-600 mt-1">Team workload and performance monitoring</p>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={showInactive}
              onChange={(e) => setShowInactive(e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <span>Show Inactive</span>
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <span>Auto-refresh (30s)</span>
          </label>
          <button
            onClick={loadTeamStats}
            className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-gray-500">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4">Loading team data...</p>
        </div>
      ) : teamStats ? (
        <>
          {/* Team Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Agents</p>
                  <p className="text-3xl font-bold text-gray-900">{teamStats.total_agents}</p>
                  <p className="text-xs text-gray-500 mt-1">{teamStats.active_agents} active</p>
                </div>
                <div className="text-4xl">👥</div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Team Capacity</p>
                  <p className="text-3xl font-bold text-gray-900">{teamStats.total_capacity}</p>
                  <p className="text-xs text-gray-500 mt-1">{teamStats.available_capacity} available</p>
                </div>
                <div className="text-4xl">🎯</div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Current Load</p>
                  <p className="text-3xl font-bold text-gray-900">{teamStats.total_load}</p>
                  <p className="text-xs text-gray-500 mt-1">active tickets</p>
                </div>
                <div className="text-4xl">📊</div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Team Utilization</p>
                  <p className="text-3xl font-bold text-gray-900">{teamStats.team_utilization_percent.toFixed(1)}%</p>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div
                      className={`h-2 rounded-full ${getUtilizationColor(teamStats.team_utilization_percent)}`}
                      style={{ width: `${Math.min(teamStats.team_utilization_percent, 100)}%` }}
                    ></div>
                  </div>
                </div>
                <div className="text-4xl">⚡</div>
              </div>
            </div>
          </div>

          {/* Agent Cards Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredAgents.map((agent) => (
              <div
                key={agent.agent_id}
                className={`bg-white rounded-lg shadow-md p-6 ${!agent.is_active ? 'opacity-60' : ''}`}
              >
                {/* Agent Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => router.push(`/agents/${agent.agent_id}`)}
                        className="text-lg font-bold text-gray-900 hover:text-primary-600 transition-colors cursor-pointer"
                      >
                        {agent.name}
                      </button>
                      {agent.is_active ? (
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Active</span>
                      ) : (
                        <span className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">Offline</span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600">{agent.email}</p>
                    <p className="text-xs text-gray-500 mt-1">ID: {agent.agent_id}</p>
                  </div>
                  <button
                    onClick={() => toggleAgentStatus(agent.agent_id, agent.is_active)}
                    className={`px-3 py-1 rounded-md text-sm font-medium ${
                      agent.is_active
                        ? 'bg-red-100 text-red-700 hover:bg-red-200'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    }`}
                  >
                    {agent.is_active ? 'Deactivate' : 'Activate'}
                  </button>
                </div>

                {/* Skills */}
                <div className="mb-4">
                  <p className="text-xs font-semibold text-gray-500 uppercase mb-2">Skills</p>
                  <div className="flex flex-wrap gap-1">
                    {agent.skills.map((skill) => (
                      <span
                        key={skill}
                        className={`px-2 py-1 text-xs rounded-full ${getSkillLevelColor(agent.skill_levels?.[skill])}`}
                      >
                        {skill}
                        {agent.skill_levels?.[skill] && (
                          <span className="ml-1 opacity-75">({agent.skill_levels[skill][0].toUpperCase()})</span>
                        )}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Workload */}
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-1">
                    <p className="text-xs font-semibold text-gray-500 uppercase">Workload</p>
                    <p className="text-sm font-bold text-gray-900">
                      {agent.current_load}/{agent.max_concurrent_tickets}
                    </p>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${getUtilizationColor(agent.utilization_percent)}`}
                      style={{ width: `${agent.utilization_percent}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{agent.utilization_percent.toFixed(0)}% utilized</p>
                </div>

                {/* Performance Stats */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-xs text-gray-500">Total Assigned</p>
                    <p className="text-lg font-bold text-gray-900">{agent.total_assigned}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Total Resolved</p>
                    <p className="text-lg font-bold text-green-600">{agent.total_resolved}</p>
                  </div>
                </div>

                {/* Channels */}
                <div className="mb-4">
                  <p className="text-xs font-semibold text-gray-500 uppercase mb-2">Channels</p>
                  <div className="flex gap-2">
                    {agent.channels.map((channel) => (
                      <span key={channel} className="text-xl" title={channel}>
                        {channel === 'email' && '📧'}
                        {channel === 'sms' && '💬'}
                        {channel === 'whatsapp' && '📱'}
                        {channel === 'chat' && '💻'}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Last Activity */}
                {agent.last_assigned_at && (
                  <div className="text-xs text-gray-500 border-t pt-3">
                    Last assigned: {format(new Date(agent.last_assigned_at), 'MMM d, HH:mm')}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Top Performers */}
          {teamStats.top_performers && teamStats.top_performers.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">🏆 Top Performers</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
                {teamStats.top_performers.map((agent, index) => (
                  <div key={agent.agent_id} className="text-center">
                    <div className="text-3xl mb-2">
                      {index === 0 && '🥇'}
                      {index === 1 && '🥈'}
                      {index === 2 && '🥉'}
                      {index > 2 && '🏅'}
                    </div>
                    <p className="font-semibold text-gray-900">{agent.name}</p>
                    <p className="text-2xl font-bold text-green-600">{agent.total_resolved}</p>
                    <p className="text-xs text-gray-500">tickets resolved</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="p-12 text-center text-gray-500">
          <p className="text-lg">No agent data available</p>
          <p className="text-sm mt-2">Run setup_sample_agents.py to create sample agents</p>
        </div>
      )}
    </div>
  )
}

