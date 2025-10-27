'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface SLAPolicy {
  policy_id: string
  name: string
  description: string
  domain: string
  categories: string[]
  priorities: string[]
  customer_tiers: string[]
  response_time_minutes: number
  resolution_time_minutes: number
  use_business_hours: boolean
  is_active: boolean
  is_default: boolean
  priority_order: number
  created_at: string
}

interface SLATemplate {
  template_id: string
  name: string
  description: string
  category: string
  policies_count: number
}

export default function SLAManagementPage() {
  const [policies, setPolicies] = useState<SLAPolicy[]>([])
  const [templates, setTemplates] = useState<SLATemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedPolicy, setSelectedPolicy] = useState<SLAPolicy | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    policy_id: '',
    name: '',
    description: '',
    domain: 'IT',
    categories: '',
    priorities: '',
    customer_tiers: 'standard',
    response_time_minutes: 60,
    resolution_time_minutes: 240,
    use_business_hours: true,
    auto_escalate: true,
    is_default: false,
    priority_order: 50
  })

  const loadData = async () => {
    try {
      setLoading(true)
      const [policiesRes, templatesRes] = await Promise.all([
        axios.get(`${API_URL}/api/sla/policies/list`),
        axios.get(`${API_URL}/api/sla/templates/list`)
      ])
      setPolicies(policiesRes.data.policies || [])
      setTemplates(templatesRes.data.templates || [])
    } catch (error) {
      console.error('Error loading SLA data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleCreatePolicy = async () => {
    try {
      await axios.post(`${API_URL}/api/sla/policies/create`, {
        ...formData,
        categories: formData.categories.split(',').map(c => c.trim()).filter(c => c),
        priorities: formData.priorities.split(',').map(p => p.trim()).filter(p => p),
        customer_tiers: [formData.customer_tiers]
      })
      alert('SLA Policy created successfully!')
      setShowCreateModal(false)
      loadData()
      // Reset form
      setFormData({
        policy_id: '',
        name: '',
        description: '',
        domain: 'IT',
        categories: '',
        priorities: '',
        customer_tiers: 'standard',
        response_time_minutes: 60,
        resolution_time_minutes: 240,
        use_business_hours: true,
        auto_escalate: true,
        is_default: false,
        priority_order: 50
      })
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleDeletePolicy = async (policyId: string) => {
    if (!confirm('Are you sure you want to deactivate this policy?')) return
    try {
      await axios.delete(`${API_URL}/api/sla/policies/${policyId}`)
      alert('Policy deactivated successfully!')
      loadData()
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || error.message}`)
    }
  }

  const formatTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading SLA Management...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">⚙️ SLA Management</h1>
            <p className="text-gray-600 mt-2">Configure and manage Service Level Agreement policies</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
          >
            ➕ Create New Policy
          </button>
        </div>

        {/* SLA Templates Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">📑 SLA Templates</h2>
          <p className="text-sm text-gray-600 mb-4">
            Quick-start with predefined SLA configurations
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {templates.map((template) => (
              <div key={template.template_id} className="border border-gray-200 rounded-lg p-4 hover:border-primary-500 transition-colors">
                <h3 className="font-bold text-gray-900">{template.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                <p className="text-xs text-gray-500 mt-2">{template.policies_count} policies</p>
                <button className="mt-3 w-full px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors text-sm font-medium">
                  Apply Template
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Active Policies */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold text-gray-900">Active SLA Policies ({policies.length})</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Policy Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Domain
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Categories
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Response Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Resolution Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Coverage
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {policies.map((policy) => (
                  <tr key={policy.policy_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{policy.name}</p>
                        <p className="text-xs text-gray-500">{policy.policy_id}</p>
                        {policy.is_default && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 mt-1">
                            DEFAULT
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {policy.domain}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-500">
                        {policy.categories.length > 0 ? (
                          <span>{policy.categories.slice(0, 2).join(', ')}{policy.categories.length > 2 && '...'}</span>
                        ) : (
                          <span className="text-gray-400">All</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-green-600">
                        {formatTime(policy.response_time_minutes)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-blue-600">
                        {formatTime(policy.resolution_time_minutes)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {policy.use_business_hours ? (
                        <span className="text-gray-600">Business Hours</span>
                      ) : (
                        <span className="text-purple-600 font-medium">24/7</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        policy.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {policy.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        onClick={() => setSelectedPolicy(policy)}
                        className="text-primary-600 hover:text-primary-900 mr-3"
                      >
                        View
                      </button>
                      <button
                        onClick={() => handleDeletePolicy(policy.policy_id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Create Policy Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b">
                <h2 className="text-2xl font-bold text-gray-900">Create New SLA Policy</h2>
              </div>
              <div className="p-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Policy ID *
                    </label>
                    <input
                      type="text"
                      value={formData.policy_id}
                      onChange={(e) => setFormData({...formData, policy_id: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="e.g., IT_CRITICAL_247"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Policy Name *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    placeholder="e.g., Critical Issues - 24/7"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    rows={2}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Categories (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={formData.categories}
                      onChange={(e) => setFormData({...formData, categories: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="e.g., outage, security"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Priorities (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={formData.priorities}
                      onChange={(e) => setFormData({...formData, priorities: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="e.g., urgent, high"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Response Time (minutes) *
                    </label>
                    <input
                      type="number"
                      value={formData.response_time_minutes}
                      onChange={(e) => setFormData({...formData, response_time_minutes: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Resolution Time (minutes) *
                    </label>
                    <input
                      type="number"
                      value={formData.resolution_time_minutes}
                      onChange={(e) => setFormData({...formData, resolution_time_minutes: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.use_business_hours}
                      onChange={(e) => setFormData({...formData, use_business_hours: e.target.checked})}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Use Business Hours (not 24/7)</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.auto_escalate}
                      onChange={(e) => setFormData({...formData, auto_escalate: e.target.checked})}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Auto-escalate on SLA breach</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_default}
                      onChange={(e) => setFormData({...formData, is_default: e.target.checked})}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Set as default policy</span>
                  </label>
                </div>
              </div>
              <div className="p-6 border-t flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreatePolicy}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Create Policy
                </button>
              </div>
            </div>
          </div>
        )}

        {/* View Policy Modal */}
        {selectedPolicy && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b">
                <h2 className="text-2xl font-bold text-gray-900">{selectedPolicy.name}</h2>
                <p className="text-sm text-gray-500 mt-1">{selectedPolicy.policy_id}</p>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Description</h3>
                  <p className="text-sm text-gray-600">{selectedPolicy.description}</p>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Response Time</h3>
                    <p className="text-2xl font-bold text-green-600">{formatTime(selectedPolicy.response_time_minutes)}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Resolution Time</h3>
                    <p className="text-2xl font-bold text-blue-600">{formatTime(selectedPolicy.resolution_time_minutes)}</p>
                  </div>
                </div>
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Applies To</h3>
                  <div className="space-y-1 text-sm">
                    <p><span className="font-medium">Categories:</span> {selectedPolicy.categories.join(', ') || 'All'}</p>
                    <p><span className="font-medium">Priorities:</span> {selectedPolicy.priorities.join(', ') || 'All'}</p>
                    <p><span className="font-medium">Customer Tiers:</span> {selectedPolicy.customer_tiers.join(', ')}</p>
                  </div>
                </div>
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Configuration</h3>
                  <div className="space-y-1 text-sm">
                    <p>Coverage: <span className="font-medium">{selectedPolicy.use_business_hours ? 'Business Hours' : '24/7'}</span></p>
                    <p>Priority Order: <span className="font-medium">{selectedPolicy.priority_order}</span></p>
                  </div>
                </div>
              </div>
              <div className="p-6 border-t flex justify-end">
                <button
                  onClick={() => setSelectedPolicy(null)}
                  className="px-6 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

